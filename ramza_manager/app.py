"""Janela principal do Solo Ramza Manager."""

from __future__ import annotations

import html
import subprocess
import sys
import traceback
from pathlib import Path
from typing import Callable, Optional

from PySide6.QtCore import QObject, Qt, QThread, QUrl, Signal
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import (
    QAbstractItemView, QApplication, QCheckBox, QFileDialog, QFrame, QGridLayout, QGroupBox, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QListWidget, QListWidgetItem, QMainWindow, QMessageBox,
    QPlainTextEdit, QPushButton, QSpinBox, QSplitter, QTableWidget, QTableWidgetItem, QTabWidget,
    QTextBrowser, QVBoxLayout, QWidget,
)

from . import __version__, class_catalog, game_install, mod_builder, nxd_db, paths, reloaded, theme
from .class_catalog import ClassOption
from .nxd_db import MAX_QUANTITY, BagItem
from .settings import Settings
from .tables import ReferenceTables, load_reference_tables

URL_RELOADED = "https://github.com/Reloaded-Project/Reloaded-II/releases/latest"
URL_MODLOADER = "https://github.com/Nenkai/fftivc.utility.modloader/releases/latest"
URL_DOTNET = "https://dotnet.microsoft.com/download/dotnet/9.0"

STAT_ROWS = [("HP", "HP"), ("MP", "MP"), ("Speed", "Speed"), ("PA", "PA"), ("MA", "MA")]

BAG_HELP = (
    "<b>Como funciona:</b> o jogo entrega os itens do <b>bônus da Deluxe Edition</b> no inventário. "
    "Este app troca o conteúdo desse bônus pela sua lista (as cores preta/vermelha do Ramza "
    "continuam). Funciona só com a Deluxe e, em geral, vale para <b>jogo novo</b>: um save que já "
    "recebeu o bônus não recebe de novo. <i>Experimental: teste primeiro com uma lista pequena.</i>"
)


def dotnet9_installed() -> bool:
    for base in (Path(r"C:\Program Files\dotnet"), Path(r"C:\Program Files (x86)\dotnet")):
        shared = base / "shared" / "Microsoft.NETCore.App"
        if shared.is_dir() and any(p.name.startswith("9.") for p in shared.iterdir()):
            return True
    return False


def reloaded_running() -> bool:
    try:
        out = subprocess.run(
            ["tasklist", "/FI", "IMAGENAME eq Reloaded-II.exe", "/NH"],
            capture_output=True, text=True, creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        ).stdout
    except OSError:
        return False
    return "reloaded-ii.exe" in out.lower()


class Worker(QObject):
    """Executa uma função numa thread separada, repassando mensagens de log."""

    log = Signal(str)
    done = Signal(object)
    failed = Signal(str)

    def __init__(self, fn: Callable[[Callable[[str], None]], object]):
        super().__init__()
        self.fn = fn

    def run(self) -> None:
        try:
            result = self.fn(self.log.emit)
        except Exception as exc:  # noqa: BLE001 - qualquer falha vira mensagem na tela
            self.log.emit(traceback.format_exc())
            self.failed.emit(str(exc))
            return
        self.done.emit(result)


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(f"Solo Ramza Manager {__version__} — FFT: The Ivalice Chronicles (Enhanced)")
        self.resize(1150, 800)

        self.settings = Settings.load()
        self.tables: ReferenceTables = load_reference_tables(paths.data_dir())
        self.catalog: list[ClassOption] = []
        self.ability_names: dict[int, str] = {}
        self.item_names: dict[int, str] = {}
        self.jp_costs: dict[int, int] = {}
        self.deluxe_default: list[BagItem] = []
        self.bag: list[BagItem] = [BagItem(int(i), int(q)) for i, q in self.settings.bag_items]
        self._thread: Optional[QThread] = None
        self._worker: Optional[Worker] = None
        self._on_done: Callable[[object], None] = lambda _r: None

        self._build_ui()
        self._autodetect()
        self.refresh_all()

    # ------------------------------------------------------------------ UI

    def _build_ui(self) -> None:
        central = QWidget()
        root = QVBoxLayout(central)
        root.addWidget(self._build_banner())
        root.addWidget(self._build_setup())

        self.main_tabs = QTabWidget()
        self.main_tabs.addTab(self._build_class_tab(), "Classe do Ramza")
        self.main_tabs.addTab(self._build_bag_tab(), "Itens iniciais (bolsa)")
        root.addWidget(self.main_tabs, 1)

        bottom = QHBoxLayout()
        self.lbl_active = QLabel()
        self.lbl_active.setWordWrap(True)
        bottom.addWidget(self.lbl_active, 1)
        self.btn_apply = QPushButton("Aplicar no jogo")
        self.btn_apply.setObjectName("Primary")
        self.btn_apply.clicked.connect(self.apply_mod)
        bottom.addWidget(self.btn_apply)
        self.btn_restore = QPushButton("Restaurar jogo original")
        self.btn_restore.setObjectName("Secondary")
        self.btn_restore.clicked.connect(self.restore)
        bottom.addWidget(self.btn_restore)
        root.addLayout(bottom)

        self.log_box = QPlainTextEdit()
        self.log_box.setReadOnly(True)
        self.log_box.setMaximumHeight(64)
        root.addWidget(self.log_box)
        self.setCentralWidget(central)

    def _build_banner(self) -> QFrame:
        banner = QFrame()
        banner.setObjectName("Banner")
        layout = QHBoxLayout(banner)
        layout.setContentsMargins(14, 8, 14, 8)
        crest = QLabel()
        crest.setPixmap(theme.make_crest(128).scaled(56, 56, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        layout.addWidget(crest)
        texts = QVBoxLayout()
        texts.setSpacing(0)
        title = QLabel("SOLO RAMZA MANAGER")
        title.setObjectName("BannerTitle")
        subtitle = QLabel("Final Fantasy Tactics · The Ivalice Chronicles — gerenciador de runs solo do Ramza")
        subtitle.setObjectName("BannerSubtitle")
        texts.addWidget(title)
        texts.addWidget(subtitle)
        layout.addLayout(texts, 1)
        version = QLabel(f"v{__version__}")
        version.setObjectName("BannerSubtitle")
        layout.addWidget(version, 0, Qt.AlignBottom)
        return banner

    @staticmethod
    def _page(body: str) -> str:
        return f"<html><head><style>{theme.PREVIEW_CSS}</style></head><body>{body}</body></html>"

    def _build_setup(self) -> QGroupBox:
        setup = QGroupBox(theme.ornament("Configuração"))
        outer = QVBoxLayout(setup)
        outer.setContentsMargins(8, 4, 8, 4)
        header = QHBoxLayout()
        self.lbl_setup_summary = QLabel()
        header.addWidget(self.lbl_setup_summary, 1)
        self.btn_setup_toggle = QPushButton()
        self.btn_setup_toggle.clicked.connect(self._toggle_setup)
        header.addWidget(self.btn_setup_toggle)
        outer.addLayout(header)
        self.setup_details = QWidget()
        outer.addWidget(self.setup_details)
        self._setup_expanded: Optional[bool] = None  # None = automático (abre só se falta algo)
        grid = QGridLayout(self.setup_details)
        grid.setContentsMargins(0, 4, 0, 0)
        self.lbl_game = QLabel()
        self.lbl_reloaded = QLabel()
        self.lbl_modloader = QLabel()
        self.lbl_dotnet = QLabel()
        self.lbl_data = QLabel()
        rows = [
            ("Jogo:", self.lbl_game, [("Procurar...", self.browse_game)]),
            ("Reloaded-II:", self.lbl_reloaded, [("Procurar...", self.browse_reloaded),
                                                 ("Baixar", lambda: self._open(URL_RELOADED))]),
            ("FFTIVC Mod Loader:", self.lbl_modloader, [("Baixar", lambda: self._open(URL_MODLOADER))]),
            (".NET 9 Runtime:", self.lbl_dotnet, [("Baixar", lambda: self._open(URL_DOTNET))]),
            ("Dados do jogo:", self.lbl_data, [("Extrair / atualizar", self.extract_data)]),
        ]
        for r, (title, label, buttons) in enumerate(rows):
            grid.addWidget(QLabel(f"<b>{title}</b>"), r, 0)
            label.setTextInteractionFlags(Qt.TextSelectableByMouse)
            grid.addWidget(label, r, 1)
            box = QHBoxLayout()
            for text, slot in buttons:
                btn = QPushButton(text)
                btn.clicked.connect(slot)
                box.addWidget(btn)
            box.addStretch()
            grid.addLayout(box, r, 2)
        grid.setColumnStretch(1, 1)
        return setup

    def _toggle_setup(self) -> None:
        self._setup_expanded = not self.setup_details.isVisible()
        self._update_setup_visibility(all_ok=None)

    def _update_setup_visibility(self, all_ok: Optional[bool]) -> None:
        if all_ok is not None:
            self._setup_all_ok = all_ok
        expanded = self._setup_expanded if self._setup_expanded is not None else not self._setup_all_ok
        self.setup_details.setVisible(expanded)
        self.btn_setup_toggle.setText("Ocultar detalhes ▴" if expanded else "Detalhes ▾")

    def _build_class_tab(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)

        top = QHBoxLayout()
        self.chk_class = QCheckBox("Trocar a classe do Ramza")
        self.chk_class.setChecked(self.settings.change_class)
        self.chk_class.toggled.connect(self._class_toggled)
        top.addWidget(self.chk_class)
        top.addStretch()
        top.addWidget(QLabel("Custo de JP das skills:"))
        self.jp_spin = QSpinBox()
        self.jp_spin.setRange(0, 9999)
        self.jp_spin.setValue(self.settings.jp_cost)
        self.jp_spin.setToolTip("0 = grátis. Se o jogo não deixar aprender com 0, use 1.")
        self.jp_spin.valueChanged.connect(self._jp_changed)
        top.addWidget(self.jp_spin)
        layout.addLayout(top)

        self.class_body = QSplitter(Qt.Horizontal)
        left = QWidget()
        left_layout = QVBoxLayout(left)
        left_layout.setContentsMargins(0, 0, 0, 0)
        self.search = QLineEdit()
        self.search.setPlaceholderText("Buscar classe ou skillset...")
        self.search.textChanged.connect(self.fill_lists)
        left_layout.addWidget(self.search)
        self.tabs = QTabWidget()
        self.tabs.setObjectName("SubTabs")
        self.lists: dict[str, QListWidget] = {}
        for key, label in class_catalog.CATEGORY_LABELS.items():
            lst = QListWidget()
            lst.currentItemChanged.connect(self.show_preview)
            self.lists[key] = lst
            self.tabs.addTab(lst, label)
        self.tabs.currentChanged.connect(lambda _i: self.show_preview())
        left_layout.addWidget(self.tabs)
        self.class_body.addWidget(left)
        self.preview = QTextBrowser()
        self.class_body.addWidget(self.preview)
        self.class_body.setSizes([420, 730])
        self.class_body.setEnabled(self.settings.change_class)
        layout.addWidget(self.class_body, 1)
        return page

    def _build_bag_tab(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        self.chk_bag = QCheckBox("Trocar os itens do bônus da Deluxe Edition pela minha lista")
        self.chk_bag.setChecked(self.settings.change_bag)
        self.chk_bag.toggled.connect(self._bag_toggled)
        layout.addWidget(self.chk_bag)
        help_label = QLabel(BAG_HELP)
        help_label.setWordWrap(True)
        layout.addWidget(help_label)

        self.bag_body = QSplitter(Qt.Horizontal)

        left = QWidget()
        left_layout = QVBoxLayout(left)
        left_layout.setContentsMargins(0, 0, 0, 0)
        self.item_search = QLineEdit()
        self.item_search.setPlaceholderText("Buscar item ou tipo (ex.: Elixir, Sword, Ring)...")
        self.item_search.textChanged.connect(self.fill_item_list)
        left_layout.addWidget(self.item_search)
        self.item_list = QListWidget()
        self.item_list.itemDoubleClicked.connect(lambda _i: self.add_bag_item())
        left_layout.addWidget(self.item_list, 1)
        add_row = QHBoxLayout()
        add_row.addWidget(QLabel("Quantidade:"))
        self.qty_spin = QSpinBox()
        self.qty_spin.setRange(1, MAX_QUANTITY)
        add_row.addWidget(self.qty_spin)
        btn_add = QPushButton("Adicionar →")
        btn_add.clicked.connect(self.add_bag_item)
        add_row.addWidget(btn_add)
        add_row.addStretch()
        left_layout.addLayout(add_row)
        self.bag_body.addWidget(left)

        right = QWidget()
        right_layout = QVBoxLayout(right)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.addWidget(QLabel("<b>Minha lista</b>"))
        self.bag_table = QTableWidget(0, 3)
        self.bag_table.setHorizontalHeaderLabels(["Item", "Tipo", "Qtd"])
        self.bag_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.bag_table.verticalHeader().setVisible(False)
        self.bag_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.bag_table.setAlternatingRowColors(True)
        self.bag_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        right_layout.addWidget(self.bag_table, 1)
        buttons = QHBoxLayout()
        for text, slot in (
            ("Remover selecionado", self.remove_bag_item),
            ("Limpar", self.clear_bag),
            ("Padrão da Deluxe", self.reset_bag_to_deluxe),
        ):
            btn = QPushButton(text)
            btn.clicked.connect(slot)
            buttons.addWidget(btn)
        buttons.addStretch()
        right_layout.addLayout(buttons)
        self.bag_body.addWidget(right)
        self.bag_body.setSizes([520, 630])
        self.bag_body.setEnabled(self.settings.change_bag)
        layout.addWidget(self.bag_body, 1)
        return page

    # -------------------------------------------------------------- helpers

    def _open(self, url: str) -> None:
        QDesktopServices.openUrl(QUrl(url))

    def log(self, text: str) -> None:
        self.log_box.appendPlainText(text)

    def _jp_changed(self, value: int) -> None:
        self.settings.jp_cost = value
        self.settings.save()
        self.show_preview()

    def _class_toggled(self, checked: bool) -> None:
        self.settings.change_class = checked
        self.settings.save()
        self.class_body.setEnabled(checked)

    def _bag_toggled(self, checked: bool) -> None:
        self.settings.change_bag = checked
        self.settings.save()
        self.bag_body.setEnabled(checked)

    def game_root(self) -> Optional[Path]:
        p = Path(self.settings.game_root) if self.settings.game_root else None
        return p if p and game_install.looks_like_game_root(p) else None

    def reloaded_root(self) -> Optional[Path]:
        p = Path(self.settings.reloaded_root) if self.settings.reloaded_root else None
        return p if p and reloaded.looks_like_reloaded_install(p) else None

    def data_ready(self) -> bool:
        return nxd_db.is_valid_db(paths.vanilla_sqlite())

    def _autodetect(self) -> None:
        if not self.game_root():
            found = game_install.find_game_root()
            if found:
                self.settings.game_root = str(found)
        if not self.reloaded_root():
            found = reloaded.find_installed_reloaded()
            if found:
                self.settings.reloaded_root = str(found)
        self.settings.save()

    @staticmethod
    def _status(ok: bool, text: str) -> str:
        color = theme.STATUS_OK if ok else theme.STATUS_BAD
        mark = "✔" if ok else "✘"
        return f'<span style="color:{color}">{mark}</span> {html.escape(text)}'

    def ability_name(self, ability_id: int) -> str:
        return self.ability_names.get(ability_id) or self.tables.ability_name(ability_id)

    def item_name(self, item_id: int) -> str:
        return self.item_names.get(item_id) or self.tables.item_name(item_id)

    # ------------------------------------------------------------- refresh

    def refresh_all(self) -> None:
        game = self.game_root()
        self.lbl_game.setText(self._status(bool(game), str(game) if game else "não encontrado"))
        rel = self.reloaded_root()
        self.lbl_reloaded.setText(self._status(bool(rel), str(rel) if rel else "não encontrado — instale e aponte a pasta"))
        loader = bool(rel and reloaded.is_mod_installed(rel, reloaded.MODLOADER_ID))
        self.lbl_modloader.setText(self._status(loader, "instalado" if loader else "não encontrado na pasta Mods do Reloaded-II"))
        dotnet = dotnet9_installed()
        self.lbl_dotnet.setText(self._status(dotnet, "instalado" if dotnet else "necessário para ler os dados do jogo"))
        ready = self.data_ready()
        self.lbl_data.setText(self._status(ready, "prontos" if ready else "clique em 'Extrair / atualizar' (uns 10 segundos)"))
        checks = [bool(game), bool(rel), loader, dotnet, ready]
        all_ok = all(checks)
        if all_ok:
            summary = self._status(True, "Tudo pronto: jogo, Reloaded-II, Mod Loader, .NET 9 e dados do jogo")
        else:
            summary = self._status(False, f"Falta configurar {checks.count(False)} item(ns) — veja abaixo")
        self.lbl_setup_summary.setText(summary)
        self._update_setup_visibility(all_ok)

        job_names = command_names = None
        if ready:
            db = paths.vanilla_sqlite()
            job_names = nxd_db.read_names(db, "Job")
            command_names = nxd_db.read_names(db, "JobCommand")
            self.ability_names = nxd_db.read_names(db, "Ability")
            self.item_names = nxd_db.read_names(db, "Item")
            self.jp_costs = nxd_db.read_jp_costs(db)
            self.deluxe_default = nxd_db.read_bonus_items(db)
        self.catalog = class_catalog.build_catalog(self.tables, job_names, command_names)
        self.fill_lists()
        self._select_saved_class()
        self.fill_item_list()
        self.fill_bag_table()
        self.refresh_active()

    def refresh_active(self) -> None:
        rel = self.reloaded_root()
        installed = mod_builder.read_installed(reloaded.mods_folder(rel)) if rel else None
        if not installed:
            self.lbl_active.setText("Mod atual: <b>nenhum</b> (jogo original)")
            return
        klass = installed.get("ClassName") or "original (Squire)"
        bag = installed.get("BagItems") or []
        bag_text = f"{len(bag)} item(ns) no bônus" if bag else "bônus original"
        self.lbl_active.setText(f"Mod atual: Ramza = <b>{html.escape(klass)}</b> · Bolsa: <b>{bag_text}</b>")

    # --------------------------------------------------------- class tab

    def _ability_count(self, option: ClassOption) -> int:
        command = self.tables.command_for(option.job)
        return len(command.all_ability_ids) if command else 0

    def fill_lists(self) -> None:
        needle = self.search.text().strip().lower()
        for key, lst in self.lists.items():
            lst.clear()
            for option in self.catalog:
                if option.category != key:
                    continue
                label = option.label(self._ability_count(option))
                if needle and needle not in label.lower():
                    continue
                item = QListWidgetItem(label)
                item.setData(Qt.UserRole, option)
                item.setToolTip(f"Job {option.job_id} · skillset {option.job.job_command_id}")
                lst.addItem(item)
        self.show_preview()

    def _select_saved_class(self) -> None:
        job_id = self.settings.class_job_id
        if job_id is None:
            return
        for tab_index, lst in enumerate(self.lists.values()):
            for row in range(lst.count()):
                if lst.item(row).data(Qt.UserRole).job_id == job_id:
                    self.tabs.setCurrentIndex(tab_index)
                    lst.setCurrentRow(row)
                    return

    def selected_option(self) -> Optional[ClassOption]:
        key = list(self.lists)[self.tabs.currentIndex()]
        item = self.lists[key].currentItem()
        return item.data(Qt.UserRole) if item else None

    def show_preview(self, *_args) -> None:
        option = self.selected_option()
        if option is None:
            self.preview.setHtml(self._page(
                "<h2>Escolha uma classe</h2>"
                "<p>Selecione uma classe na lista para ver skills, equipamentos e atributos.</p>"
                "<p>Ao aplicar, as três classes próprias do Ramza (Cap. 1, Cap. 2–3 e Cap. 4) viram a "
                "classe escolhida. Ele continua começando no nível 1 e evolui normalmente. "
                "O resto do jogo não muda.</p>"
            ))
            return
        job = option.job
        plan = mod_builder.plan_build(self.tables, job.id, option.name)
        command = self.tables.command_for(job)
        jp = self.jp_spin.value()
        esc = html.escape

        def ability_rows(ids: list[int]) -> str:
            if not ids:
                return "<i>nenhuma</i>"
            rows = []
            for ab_id in ids:
                old = self.jp_costs.get(ab_id)
                before = f"<span class='old'>{old} →</span> " if old is not None else ""
                rows.append(f"<tr><td>{esc(self.ability_name(ab_id))}</td>"
                            f"<td align='right'>{before}<span class='jp'>{jp} JP</span></td></tr>")
            return "<table cellspacing=4>" + "".join(rows) + "</table>"

        f = job.fields
        stats = "".join(
            f"<tr><td>{label}</td><td align='right'>{f.get(key + 'Multiplier', '?')}</td>"
            f"<td align='right'>{f.get(key + 'Growth', '?')}</td></tr>"
            for key, label in STAT_ROWS
        )
        innate = ", ".join(esc(self.ability_name(i)) for i in job.innate_ability_ids) or "nenhuma"
        parts = [f"<h2>{esc(option.name)}</h2>"]
        if option.experimental:
            parts.append(
                "<p class='warn'><b>⚠ Experimental:</b> classe de chefe/inimigo. Pode ter "
                "animações faltando ou travar o jogo com o sprite do Ramza. Salve antes de testar.</p>"
            )
        parts.append(
            f"<p><b>Skillset:</b> {esc(option.skillset_name or 'próprio')} · "
            f"<b>Move</b> {f.get('Move')} · <b>Jump</b> {f.get('Jump')} · "
            f"<b>Evasão</b> {f.get('CharacterEvasion')}% · <span class='muted'>Job {job.id}</span></p>"
        )
        parts.append("<h3>Habilidades de ação</h3>" + ability_rows(command.action_ids if command else []))
        parts.append("<h3>Reação / Suporte / Movimento</h3>" + ability_rows(command.rsm_ids if command else []))
        parts.append(f"<p><b>Habilidades inatas:</b> {innate}</p>")
        parts.append(f"<p><b>Equipamentos:</b> {esc(', '.join(job.equippable) or 'nenhum')}</p>")
        parts.append(
            "<h3>Atributos</h3><table cellspacing=4><tr><th></th><th>Multiplicador</th>"
            f"<th>Crescimento*</th></tr>{stats}</table>"
            "<p class='muted'>* crescimento: quanto menor, mais o atributo sobe por nível.</p>"
        )
        extras = [s for s in (f.get("InnateStatus"), f.get("StartingStatus")) if s and s != "None"]
        if extras:
            parts.append(f"<p><b>Status inato/inicial:</b> {esc(' / '.join(extras))}</p>")
        if plan.spawn_changes:
            changes = "".join(
                f"<li>{slot}: {esc(self.item_name(old))} → {esc(self.item_name(new))}</li>"
                for slot, (old, new) in plan.spawn_changes.items()
            )
            parts.append(f"<h3>Equipamento inicial ajustado</h3><ul>{changes}</ul>")
        self.preview.setHtml(self._page("".join(parts)))

    # ----------------------------------------------------------- bag tab

    def fill_item_list(self) -> None:
        needle = self.item_search.text().strip().lower()
        self.item_list.clear()
        for item in sorted(self.tables.items.values(), key=lambda i: i.id):
            if item.id == 0 or item.category == "None":
                continue
            name = self.item_name(item.id)
            label = f"{name}  ·  {item.category}"
            if needle and needle not in label.lower():
                continue
            entry = QListWidgetItem(label)
            entry.setData(Qt.UserRole, item.id)
            entry.setToolTip(f"Item {item.id}")
            self.item_list.addItem(entry)

    def fill_bag_table(self) -> None:
        self.bag_table.setRowCount(0)  # descarta os spinboxes antigos
        self.bag_table.setRowCount(len(self.bag))
        for row, entry in enumerate(self.bag):
            item = self.tables.items.get(entry.item_id)
            self.bag_table.setItem(row, 0, QTableWidgetItem(self.item_name(entry.item_id)))
            self.bag_table.setItem(row, 1, QTableWidgetItem(item.category if item else ""))
            spin = QSpinBox()
            spin.setRange(1, MAX_QUANTITY)
            spin.setValue(entry.quantity)
            spin.valueChanged.connect(lambda value, r=row: self._set_quantity(r, value))
            self.bag_table.setCellWidget(row, 2, spin)

    def _save_bag(self) -> None:
        self.settings.bag_items = [[b.item_id, b.quantity] for b in self.bag]
        self.settings.save()

    def _set_quantity(self, row: int, value: int) -> None:
        if 0 <= row < len(self.bag):
            self.bag[row].quantity = value
            self._save_bag()

    def add_bag_item(self) -> None:
        current = self.item_list.currentItem()
        if current is None:
            return
        item_id = current.data(Qt.UserRole)
        qty = self.qty_spin.value()
        for entry in self.bag:
            if entry.item_id == item_id:
                entry.quantity = min(MAX_QUANTITY, entry.quantity + qty)
                break
        else:
            self.bag.append(BagItem(item_id, qty))
        self._save_bag()
        self.fill_bag_table()

    def remove_bag_item(self) -> None:
        rows = sorted({i.row() for i in self.bag_table.selectedIndexes()}, reverse=True)
        for row in rows:
            del self.bag[row]
        self._save_bag()
        self.fill_bag_table()

    def clear_bag(self) -> None:
        self.bag = []
        self._save_bag()
        self.fill_bag_table()

    def reset_bag_to_deluxe(self) -> None:
        self.bag = [BagItem(b.item_id, b.quantity) for b in self.deluxe_default]
        self._save_bag()
        self.fill_bag_table()

    # ------------------------------------------------------------- actions

    def browse_game(self) -> None:
        folder = QFileDialog.getExistingDirectory(self, "Pasta do jogo (onde fica FFT_enhanced.exe)")
        if folder:
            if not game_install.looks_like_game_root(Path(folder)):
                QMessageBox.warning(self, "Pasta inválida", "Não encontrei FFT_enhanced.exe nessa pasta.")
                return
            self.settings.game_root = folder
            self.settings.save()
            self.refresh_all()

    def browse_reloaded(self) -> None:
        folder = QFileDialog.getExistingDirectory(self, "Pasta do Reloaded-II (onde fica Reloaded-II.exe)")
        if folder:
            if not reloaded.looks_like_reloaded_install(Path(folder)):
                QMessageBox.warning(self, "Pasta inválida", "Não encontrei Reloaded-II.exe nessa pasta.")
                return
            self.settings.reloaded_root = folder
            self.settings.save()
            self.refresh_all()

    def _run(self, fn, on_done, busy_text: str) -> None:
        if self._thread is not None:
            return
        self.log(busy_text)
        self.setEnabled(False)
        thread = QThread(self)
        worker = Worker(fn)
        worker.moveToThread(thread)
        # Conectados a métodos deste QObject (e não a funções soltas) para o
        # Qt entregar os sinais na thread da interface.
        worker.log.connect(self.log)
        worker.done.connect(self._worker_done)
        worker.failed.connect(self._worker_failed)
        thread.started.connect(worker.run)
        self._thread, self._worker, self._on_done = thread, worker, on_done
        thread.start()

    def _finish_worker(self) -> None:
        if self._thread is not None:
            self._thread.quit()
            self._thread.wait()
        self._thread = None
        self._worker = None
        self.setEnabled(True)

    def _worker_done(self, result) -> None:
        self._finish_worker()
        self._on_done(result)

    def _worker_failed(self, message: str) -> None:
        self._finish_worker()
        QMessageBox.critical(self, "Erro", message)

    def extract_data(self) -> None:
        game = self.game_root()
        if not game:
            QMessageBox.warning(self, "Jogo não encontrado", "Aponte a pasta do jogo primeiro.")
            return
        if not dotnet9_installed():
            QMessageBox.warning(self, ".NET 9", "Instale o .NET 9 Runtime (botão 'Baixar') e tente de novo.")
            return

        def work(log):
            return nxd_db.extract_vanilla_db(game, paths.ff16tools_cli(), paths.cache_dir(), paths.vanilla_sqlite(), log)

        self._run(work, lambda _r: self.refresh_all(), "Extraindo tabelas do jogo (só leitura)...")

    def _require_ready(self) -> Optional[Path]:
        rel = self.reloaded_root()
        problems = []
        if not self.data_ready():
            problems.append("• Extraia os dados do jogo (botão 'Extrair / atualizar').")
        if not rel:
            problems.append("• Instale o Reloaded-II e aponte a pasta dele.")
        if problems:
            QMessageBox.warning(self, "Falta configurar", "\n".join(problems))
            return None
        if reloaded_running():
            QMessageBox.warning(self, "Feche o Reloaded-II",
                                "Feche o Reloaded-II antes de continuar, senão ele desfaz a ativação do mod.")
            return None
        return rel

    def apply_mod(self) -> None:
        option = None
        if self.chk_class.isChecked():
            option = self.selected_option()
            if option is None:
                QMessageBox.information(self, "Escolha uma classe",
                                        "Selecione uma classe na aba 'Classe do Ramza', ou desmarque "
                                        "'Trocar a classe do Ramza'.")
                return
        bag = list(self.bag) if self.chk_bag.isChecked() else None
        if bag is not None and not bag:
            QMessageBox.information(self, "Lista vazia",
                                    "Adicione itens na aba 'Itens iniciais', ou desmarque a troca do bônus.")
            return
        if option is None and bag is None:
            QMessageBox.information(self, "Nada para aplicar",
                                    "Marque a troca de classe e/ou a troca dos itens. Para voltar ao jogo "
                                    "original, use 'Restaurar jogo original'.")
            return
        rel = self._require_ready()
        if rel is None:
            return
        if option and option.experimental:
            answer = QMessageBox.question(
                self, "Classe experimental",
                f"{option.name} é uma classe de chefe/inimigo e pode travar o jogo.\nAplicar mesmo assim?")
            if answer != QMessageBox.Yes:
                return

        plan = mod_builder.plan_build(
            self.tables, option.job_id if option else None, option.name if option else None, bag)
        jp = self.jp_spin.value()
        db = paths.vanilla_sqlite()
        fallback_names = {i: self.item_name(i) for i in self.tables.items}
        if option:
            self.settings.class_job_id = option.job_id
            self.settings.save()

        def nxd_builder(p, work_dir):
            class_edit = None
            if p.source_job is not None:
                class_edit = dict(ability_ids=p.ability_ids, jp_cost=jp, source_job_id=p.source_job.id,
                                  target_job_ids=class_catalog.RAMZA_JOB_IDS)
            return nxd_db.build_nxd_files(db, paths.ff16tools_cli(), work_dir, class_edit, p.bag, fallback_names)

        def work(log):
            log("Gerando mod...")
            staged = mod_builder.build_mod(plan, paths.user_data_dir() / "build", nxd_builder)
            target = mod_builder.install_mod(staged, reloaded.mods_folder(rel))
            log(f"Mod instalado em {target}")
            return reloaded.set_mod_enabled(rel, mod_builder.MOD_ID, True)

        def done(enabled: bool) -> None:
            self.refresh_active()
            lines = []
            if option:
                lines.append(f"• Ramza agora é {option.name}.")
            if plan.bag:
                lines.append(f"• Bônus da Deluxe trocado por {len(plan.bag)} item(ns). Comece um jogo novo para recebê-los.")
            msg = "Pronto!\n\n" + "\n".join(lines) + "\n\n"
            if enabled:
                msg += "O mod já está ativado no Reloaded-II. Abra o jogo pelo Reloaded-II."
            else:
                msg += ("Não achei o FFT_enhanced.exe no Reloaded-II. Adicione o jogo lá e ative os mods "
                        f"'{mod_builder.MOD_NAME}' e 'FFTIVC Mod Loader'.")
            QMessageBox.information(self, "Mod aplicado", msg)

        self._run(work, done, "Aplicando...")

    def restore(self) -> None:
        rel = self.reloaded_root()
        if rel is None:
            QMessageBox.warning(self, "Falta configurar", "Aponte a pasta do Reloaded-II primeiro.")
            return
        if reloaded_running():
            QMessageBox.warning(self, "Feche o Reloaded-II", "Feche o Reloaded-II antes de restaurar.")
            return
        removed = mod_builder.uninstall_mod(reloaded.mods_folder(rel))
        reloaded.set_mod_enabled(rel, mod_builder.MOD_ID, False)
        self.refresh_active()
        self.log("Mod removido. Jogo original." if removed else "O mod não estava instalado.")
        QMessageBox.information(self, "Restaurado", "O mod foi removido: Ramza e bônus voltaram ao original.")


def main() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName("Solo Ramza Manager")
    theme.apply(app)
    window = MainWindow()
    window.show()
    return app.exec()
