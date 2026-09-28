"""Janela principal do Solo Ramza Manager."""

from __future__ import annotations

import dataclasses
import html
import sys
import traceback
from pathlib import Path
from typing import Callable, Optional

from PySide6.QtCore import QObject, Qt, QThread, QTimer, QUrl, Signal
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import (
    QAbstractItemView, QApplication, QCheckBox, QComboBox, QDialog, QFileDialog, QFrame, QGridLayout, QGroupBox,
    QHBoxLayout, QHeaderView, QLabel, QLineEdit, QListWidget, QListWidgetItem, QMainWindow, QMessageBox,
    QPlainTextEdit, QPushButton, QSpinBox, QSplitter, QTableWidget, QTableWidgetItem, QTabWidget,
    QTextBrowser, QVBoxLayout, QWidget,
)

from . import (
    __version__, class_catalog, custom_class, game_install, i18n, mod_builder, nxd_db, paths, prereqs, reloaded,
    theme,
)
from .class_catalog import ClassOption
from .class_editor import CustomClassDialog
from .custom_class import CustomClass, CustomClassError
from .nxd_db import MAX_QUANTITY, BagItem
from .settings import Settings
from .tables import Job, ReferenceTables, load_reference_tables
from .wizard import SetupWizard

URL_RELOADED = "https://github.com/Reloaded-Project/Reloaded-II/releases/latest"
URL_MODLOADER = "https://github.com/Nenkai/fftivc.utility.modloader/releases/latest"
URL_DOTNET = "https://dotnet.microsoft.com/download/dotnet/9.0"

STAT_ROWS = [("HP", "HP"), ("MP", "MP"), ("Speed", "Speed"), ("PA", "PA"), ("MA", "MA")]


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
        if self.settings.language in i18n.LANGS:
            i18n.set_language(self.settings.language)
        self.tables: ReferenceTables = load_reference_tables(paths.data_dir())
        self.catalog: list[ClassOption] = []
        self.ability_names: dict[int, str] = {}
        self.command_names: dict[int, str] = {}
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
        self.main_tabs.addTab(self._build_class_tab(), "")
        self.main_tabs.addTab(self._build_bag_tab(), "")
        root.addWidget(self.main_tabs, 1)

        bottom = QHBoxLayout()
        self.lbl_active = QLabel()
        self.lbl_active.setWordWrap(True)
        bottom.addWidget(self.lbl_active, 1)
        self.btn_apply = QPushButton()
        self.btn_apply.setObjectName("Primary")
        self.btn_apply.clicked.connect(self.apply_mod)
        bottom.addWidget(self.btn_apply)
        self.btn_restore = QPushButton()
        self.btn_restore.setObjectName("Secondary")
        self.btn_restore.clicked.connect(self.restore)
        bottom.addWidget(self.btn_restore)
        root.addLayout(bottom)

        self.log_box = QPlainTextEdit()
        self.log_box.setReadOnly(True)
        self.log_box.setMaximumHeight(64)
        root.addWidget(self.log_box)
        self.setCentralWidget(central)
        self.retranslate_ui()

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
        self.banner_subtitle = QLabel()
        self.banner_subtitle.setObjectName("BannerSubtitle")
        texts.addWidget(title)
        texts.addWidget(self.banner_subtitle)
        layout.addLayout(texts, 1)
        self.lang_combo = QComboBox()
        self.lang_combo.addItem("PT-BR", i18n.LANG_PT)
        self.lang_combo.addItem("EN", i18n.LANG_EN)
        self.lang_combo.currentIndexChanged.connect(self._lang_combo_changed)
        layout.addWidget(self.lang_combo, 0, Qt.AlignBottom)
        version = QLabel(f"v{__version__}")
        version.setObjectName("BannerSubtitle")
        layout.addWidget(version, 0, Qt.AlignBottom)
        return banner

    @staticmethod
    def _page(body: str) -> str:
        return f"<html><head><style>{theme.PREVIEW_CSS}</style></head><body>{body}</body></html>"

    def _build_setup(self) -> QGroupBox:
        self.setup_group = QGroupBox()
        outer = QVBoxLayout(self.setup_group)
        outer.setContentsMargins(8, 4, 8, 4)
        header = QHBoxLayout()
        self.lbl_setup_summary = QLabel()
        header.addWidget(self.lbl_setup_summary, 1)
        self.btn_setup_toggle = QPushButton()
        self.btn_setup_toggle.clicked.connect(self._toggle_setup)
        header.addWidget(self.btn_setup_toggle)
        self.btn_wizard = QPushButton()
        self.btn_wizard.clicked.connect(self.open_wizard)
        header.addWidget(self.btn_wizard)
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
        self.lbl_row_game = QLabel()
        self.lbl_row_reloaded = QLabel()
        self.lbl_row_modloader = QLabel()
        self.lbl_row_dotnet = QLabel()
        self.lbl_row_data = QLabel()
        self.btn_browse_game = QPushButton()
        self.btn_browse_game.clicked.connect(self.browse_game)
        self.btn_browse_reloaded = QPushButton()
        self.btn_browse_reloaded.clicked.connect(self.browse_reloaded)
        self.btn_dl_reloaded = QPushButton()
        self.btn_dl_reloaded.clicked.connect(lambda: self._open(URL_RELOADED))
        self.btn_dl_modloader = QPushButton()
        self.btn_dl_modloader.clicked.connect(lambda: self._open(URL_MODLOADER))
        self.btn_dl_dotnet = QPushButton()
        self.btn_dl_dotnet.clicked.connect(lambda: self._open(URL_DOTNET))
        self.btn_extract = QPushButton()
        self.btn_extract.clicked.connect(self.extract_data)
        rows = [
            (self.lbl_row_game, self.lbl_game, [self.btn_browse_game]),
            (self.lbl_row_reloaded, self.lbl_reloaded, [self.btn_browse_reloaded, self.btn_dl_reloaded]),
            (self.lbl_row_modloader, self.lbl_modloader, [self.btn_dl_modloader]),
            (self.lbl_row_dotnet, self.lbl_dotnet, [self.btn_dl_dotnet]),
            (self.lbl_row_data, self.lbl_data, [self.btn_extract]),
        ]
        for r, (title, label, buttons) in enumerate(rows):
            grid.addWidget(title, r, 0)
            label.setTextInteractionFlags(Qt.TextSelectableByMouse)
            grid.addWidget(label, r, 1)
            box = QHBoxLayout()
            for btn in buttons:
                box.addWidget(btn)
            box.addStretch()
            grid.addLayout(box, r, 2)
        grid.setColumnStretch(1, 1)
        return self.setup_group

    def _toggle_setup(self) -> None:
        self._setup_expanded = not self.setup_details.isVisible()
        self._update_setup_visibility(all_ok=None)

    def _update_setup_visibility(self, all_ok: Optional[bool]) -> None:
        if all_ok is not None:
            self._setup_all_ok = all_ok
        expanded = self._setup_expanded if self._setup_expanded is not None else not self._setup_all_ok
        self.setup_details.setVisible(expanded)
        self.btn_setup_toggle.setText(i18n.t("btn_hide_details") if expanded else i18n.t("btn_show_details"))

    def retranslate_ui(self) -> None:
        t = i18n.t
        self.setWindowTitle(t("window_title", version=__version__))
        self.banner_subtitle.setText(t("banner_subtitle"))
        self.lang_combo.setToolTip(t("lang_tip"))
        self._sync_lang_combo()
        self.main_tabs.setTabText(0, t("tab_class"))
        self.main_tabs.setTabText(1, t("tab_bag"))
        self.btn_apply.setText(t("btn_apply"))
        self.btn_restore.setText(t("btn_restore"))
        self.setup_group.setTitle(theme.ornament(t("setup_title")))
        self.btn_wizard.setText(t("btn_wizard"))
        self.lbl_row_game.setText(f"<b>{t('row_game')}</b>")
        self.lbl_row_reloaded.setText(f"<b>{t('row_reloaded')}</b>")
        self.lbl_row_modloader.setText(f"<b>{t('row_modloader')}</b>")
        self.lbl_row_dotnet.setText(f"<b>{t('row_dotnet')}</b>")
        self.lbl_row_data.setText(f"<b>{t('row_data')}</b>")
        for btn in (self.btn_browse_game, self.btn_browse_reloaded):
            btn.setText(t("btn_browse"))
        for btn in (self.btn_dl_reloaded, self.btn_dl_modloader, self.btn_dl_dotnet):
            btn.setText(t("btn_download"))
        self.btn_extract.setText(t("btn_extract"))
        self.chk_class.setText(t("chk_class"))
        self.lbl_jp.setText(t("lbl_jp"))
        self.jp_spin.setToolTip(t("tip_jp"))
        self.search.setPlaceholderText(t("search_class"))
        for index, key in enumerate(self.lists):
            self.tabs.setTabText(index, class_catalog.category_labels()[key])
        self.tabs.setTabText(self._custom_tab_index(), t("cat_custom"))
        self.btn_cc_new.setText(t("cc_btn_new"))
        self.btn_cc_edit.setText(t("cc_btn_edit"))
        self.btn_cc_dup.setText(t("cc_btn_dup"))
        self.btn_cc_delete.setText(t("cc_btn_delete"))
        self.btn_cc_import.setText(t("cc_btn_import"))
        self.btn_cc_export.setText(t("cc_btn_export"))
        self.chk_bag.setText(t("chk_bag"))
        self.bag_help.setText(t("bag_help"))
        self.item_search.setPlaceholderText(t("search_item"))
        self.lbl_qty.setText(t("lbl_qty"))
        self.btn_add.setText(t("btn_add"))
        self.lbl_my_list.setText(t("lbl_my_list"))
        self.bag_table.setHorizontalHeaderLabels([t("col_item"), t("col_type"), t("col_qty")])
        self.btn_remove.setText(t("btn_remove"))
        self.btn_clear.setText(t("btn_clear"))
        self.btn_deluxe.setText(t("btn_deluxe"))
        if hasattr(self, "_setup_all_ok"):
            self._update_setup_visibility(None)

    def _sync_lang_combo(self) -> None:
        idx = self.lang_combo.findData(i18n.get_language())
        self.lang_combo.blockSignals(True)
        self.lang_combo.setCurrentIndex(idx if idx >= 0 else 0)
        self.lang_combo.blockSignals(False)

    def _lang_combo_changed(self, _index: int) -> None:
        lang = self.lang_combo.currentData()
        if lang and lang != i18n.get_language():
            self.apply_language(lang)

    def apply_language(self, lang: str) -> None:
        if lang not in i18n.LANGS:
            return
        i18n.set_language(lang)
        if self.settings.language != lang:
            self.settings.language = lang
            self.settings.save()
        self.retranslate_ui()
        self.refresh_all()

    def open_wizard(self) -> None:
        dlg = SetupWizard(self.settings, self)
        dlg.language_changed.connect(self.apply_language)
        if dlg.exec() == QDialog.Accepted:
            self.settings.wizard_done = True
            self.settings.save()
        self._autodetect()
        if self.settings.language in i18n.LANGS:
            self.apply_language(self.settings.language)
        else:
            self.refresh_all()

    def _build_class_tab(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)

        top = QHBoxLayout()
        self.chk_class = QCheckBox()
        self.chk_class.setChecked(self.settings.change_class)
        self.chk_class.toggled.connect(self._class_toggled)
        top.addWidget(self.chk_class)
        top.addStretch()
        self.lbl_jp = QLabel()
        top.addWidget(self.lbl_jp)
        self.jp_spin = QSpinBox()
        self.jp_spin.setRange(0, 9999)
        self.jp_spin.setValue(self.settings.jp_cost)
        self.jp_spin.valueChanged.connect(self._jp_changed)
        top.addWidget(self.jp_spin)
        layout.addLayout(top)

        self.class_body = QSplitter(Qt.Horizontal)
        left = QWidget()
        left_layout = QVBoxLayout(left)
        left_layout.setContentsMargins(0, 0, 0, 0)
        self.search = QLineEdit()
        self.search.setPlaceholderText("")
        self.search.textChanged.connect(self.fill_lists)
        left_layout.addWidget(self.search)
        self.tabs = QTabWidget()
        self.tabs.setObjectName("SubTabs")
        self.lists: dict[str, QListWidget] = {}
        for key, label in class_catalog.category_labels().items():
            lst = QListWidget()
            lst.currentItemChanged.connect(self.show_preview)
            self.lists[key] = lst
            self.tabs.addTab(lst, label)
        self.tabs.addTab(self._build_custom_page(), "")
        self.tabs.currentChanged.connect(lambda _i: self.show_preview())
        left_layout.addWidget(self.tabs)
        self.class_body.addWidget(left)
        self.preview = QTextBrowser()
        self.class_body.addWidget(self.preview)
        self.class_body.setSizes([420, 730])
        self.class_body.setEnabled(self.settings.change_class)
        layout.addWidget(self.class_body, 1)
        return page

    def _build_custom_page(self) -> QWidget:
        """Sub-aba 'Minhas classes': biblioteca de classes customizadas."""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        self.custom_list = QListWidget()
        self.custom_list.currentItemChanged.connect(self.show_preview)
        self.custom_list.itemDoubleClicked.connect(lambda _i: self.edit_custom())
        layout.addWidget(self.custom_list, 1)
        grid = QGridLayout()
        self.btn_cc_new = QPushButton()
        self.btn_cc_new.clicked.connect(self.new_custom)
        self.btn_cc_edit = QPushButton()
        self.btn_cc_edit.clicked.connect(self.edit_custom)
        self.btn_cc_dup = QPushButton()
        self.btn_cc_dup.clicked.connect(self.duplicate_custom)
        self.btn_cc_delete = QPushButton()
        self.btn_cc_delete.clicked.connect(self.delete_custom)
        self.btn_cc_import = QPushButton()
        self.btn_cc_import.clicked.connect(self.import_custom)
        self.btn_cc_export = QPushButton()
        self.btn_cc_export.clicked.connect(self.export_custom)
        buttons = [self.btn_cc_new, self.btn_cc_edit, self.btn_cc_dup,
                   self.btn_cc_import, self.btn_cc_export, self.btn_cc_delete]
        for index, btn in enumerate(buttons):
            grid.addWidget(btn, index // 3, index % 3)
        layout.addLayout(grid)
        return page

    def _build_bag_tab(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        self.chk_bag = QCheckBox()
        self.chk_bag.setChecked(self.settings.change_bag)
        self.chk_bag.toggled.connect(self._bag_toggled)
        layout.addWidget(self.chk_bag)
        self.bag_help = QLabel()
        self.bag_help.setWordWrap(True)
        self.bag_help.setTextFormat(Qt.RichText)
        layout.addWidget(self.bag_help)

        self.bag_body = QSplitter(Qt.Horizontal)

        left = QWidget()
        left_layout = QVBoxLayout(left)
        left_layout.setContentsMargins(0, 0, 0, 0)
        self.item_search = QLineEdit()
        self.item_search.setPlaceholderText("")
        self.item_search.textChanged.connect(self.fill_item_list)
        left_layout.addWidget(self.item_search)
        self.item_list = QListWidget()
        self.item_list.itemDoubleClicked.connect(lambda _i: self.add_bag_item())
        left_layout.addWidget(self.item_list, 1)
        add_row = QHBoxLayout()
        self.lbl_qty = QLabel()
        add_row.addWidget(self.lbl_qty)
        self.qty_spin = QSpinBox()
        self.qty_spin.setRange(1, MAX_QUANTITY)
        add_row.addWidget(self.qty_spin)
        self.btn_add = QPushButton()
        self.btn_add.clicked.connect(self.add_bag_item)
        add_row.addWidget(self.btn_add)
        add_row.addStretch()
        left_layout.addLayout(add_row)
        self.bag_body.addWidget(left)

        right = QWidget()
        right_layout = QVBoxLayout(right)
        right_layout.setContentsMargins(0, 0, 0, 0)
        self.lbl_my_list = QLabel()
        right_layout.addWidget(self.lbl_my_list)
        self.bag_table = QTableWidget(0, 3)
        self.bag_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.bag_table.verticalHeader().setVisible(False)
        self.bag_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.bag_table.setAlternatingRowColors(True)
        self.bag_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        right_layout.addWidget(self.bag_table, 1)
        buttons = QHBoxLayout()
        self.btn_remove = QPushButton()
        self.btn_remove.clicked.connect(self.remove_bag_item)
        self.btn_clear = QPushButton()
        self.btn_clear.clicked.connect(self.clear_bag)
        self.btn_deluxe = QPushButton()
        self.btn_deluxe.clicked.connect(self.reset_bag_to_deluxe)
        for btn in (self.btn_remove, self.btn_clear, self.btn_deluxe):
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
        self.lbl_game.setText(self._status(bool(game), str(game) if game else i18n.t("status_not_found")))
        rel = self.reloaded_root()
        self.lbl_reloaded.setText(self._status(
            bool(rel), str(rel) if rel else i18n.t("status_reloaded_missing")))
        loader = bool(rel and reloaded.is_mod_installed(rel, reloaded.MODLOADER_ID))
        self.lbl_modloader.setText(self._status(
            loader, i18n.t("status_installed") if loader else i18n.t("status_modloader_missing")))
        dotnet = prereqs.dotnet9_installed()
        self.lbl_dotnet.setText(self._status(
            dotnet, i18n.t("status_installed") if dotnet else i18n.t("status_dotnet_needed")))
        ready = self.data_ready()
        self.lbl_data.setText(self._status(
            ready, i18n.t("status_data_ready") if ready else i18n.t("status_data_missing")))
        checks = [bool(game), bool(rel), loader, dotnet, ready]
        all_ok = all(checks)
        if all_ok:
            summary = self._status(True, i18n.t("status_all_ok"))
        else:
            summary = self._status(False, i18n.t("status_missing", n=checks.count(False)))
        self.lbl_setup_summary.setText(summary)
        self._update_setup_visibility(all_ok)

        job_names = command_names = None
        if ready:
            db = paths.vanilla_sqlite()
            job_names = nxd_db.read_names(db, "Job")
            command_names = nxd_db.read_names(db, "JobCommand")
            self.command_names = command_names
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
            self.lbl_active.setText(i18n.t("mod_none"))
            return
        klass = installed.get("ClassName") or i18n.t("mod_original_class")
        bag = installed.get("BagItems") or []
        bag_text = i18n.t("mod_bag_count", n=len(bag)) if bag else i18n.t("mod_bag_original")
        self.lbl_active.setText(i18n.t("mod_active", klass=html.escape(klass), bag=html.escape(bag_text)))

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
                item.setToolTip(i18n.t("tip_job", job=option.job_id, cmd=option.job.job_command_id))
                lst.addItem(item)
        self.fill_custom_list()

    def fill_custom_list(self, select: Optional[Path] = None) -> None:
        needle = self.search.text().strip().lower()
        current = select or self._selected_custom_path()
        self.custom_list.blockSignals(True)
        self.custom_list.clear()
        entries = [(p, k, True) for p, k in custom_class.list_library(paths.presets_dir())]
        entries += [(p, k, False) for p, k in custom_class.list_library(paths.classes_dir())]
        for path, klass, builtin in entries:
            label = i18n.t("cc_label", name=klass.name, skillset=klass.skillset,
                           base=self.job_display_name(klass.base_job), n=len(klass.ability_ids))
            if builtin:
                label = f"★ {label}"
            if needle and needle not in label.lower():
                continue
            item = QListWidgetItem(label)
            item.setData(Qt.UserRole, (path, klass))
            item.setToolTip(i18n.t("cc_builtin_tip") if builtin else str(path))
            self.custom_list.addItem(item)
            if current and path == current:
                self.custom_list.setCurrentItem(item)
        self.custom_list.blockSignals(False)
        self.show_preview()

    @staticmethod
    def is_builtin(path: Path) -> bool:
        return path.parent == paths.presets_dir()

    def _saved_custom_path(self) -> Path:
        """Caminho salvo em settings (antigo: só o nome de um arquivo da biblioteca)."""
        saved = Path(self.settings.custom_class_file)
        return saved if saved.is_absolute() else paths.classes_dir() / saved

    def _custom_tab_index(self) -> int:
        return len(self.lists)

    def on_custom_tab(self) -> bool:
        return self.tabs.currentIndex() == self._custom_tab_index()

    def _selected_custom_path(self) -> Optional[Path]:
        item = self.custom_list.currentItem()
        return item.data(Qt.UserRole)[0] if item else None

    def selected_custom(self) -> Optional[tuple[Path, CustomClass]]:
        if not self.on_custom_tab():
            return None
        item = self.custom_list.currentItem()
        return item.data(Qt.UserRole) if item else None

    def job_display_name(self, job_id: int) -> str:
        for option in self.catalog:
            if option.job_id == job_id:
                return option.name
        job = self.tables.jobs.get(job_id)
        return job.name if job and job.name else f"Job {job_id}"

    def command_name(self, cmd_id: int) -> str:
        command = self.tables.commands.get(cmd_id)
        return (self.command_names.get(cmd_id) or "").strip() or (command.name if command else "") or f"#{cmd_id}"

    def _select_saved_class(self) -> None:
        if self.settings.custom_class_file:
            target = self._saved_custom_path()
            for row in range(self.custom_list.count()):
                if self.custom_list.item(row).data(Qt.UserRole)[0] == target:
                    self.tabs.setCurrentIndex(self._custom_tab_index())
                    self.custom_list.setCurrentRow(row)
                    return
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
        if self.on_custom_tab():
            return None
        key = list(self.lists)[self.tabs.currentIndex()]
        item = self.lists[key].currentItem()
        return item.data(Qt.UserRole) if item else None

    def show_preview(self, *_args) -> None:
        if self.on_custom_tab():
            selected = self.selected_custom()
            if selected is None:
                self.preview.setHtml(self._page(i18n.t("cc_preview_empty")))
            else:
                self._show_custom_preview(selected[1])
            return
        option = self.selected_option()
        if option is None:
            self.preview.setHtml(self._page(i18n.t("preview_empty")))
            return
        job = option.job
        command = self.tables.command_for(job)
        header = [f"<h2>{html.escape(option.name)}</h2>"]
        if option.experimental:
            header.append(i18n.t("warn_experimental"))
        self._render_preview(
            header, job, option.skillset_name or i18n.t("own_skillset"),
            command.action_ids if command else [], command.rsm_ids if command else [],
            mod_builder.plan_build(self.tables, job.id, option.name),
        )

    def _show_custom_preview(self, klass: CustomClass) -> None:
        esc = html.escape
        header = [f"<h2>{esc(klass.name)} <span class='muted'>✦</span></h2>"]
        if not custom_class.is_valid_base_job(self.tables, klass.base_job):
            header.append(f"<p class='warn'>{esc(i18n.t('cc_err_base', job=klass.base_job))}</p>")
            self.preview.setHtml(self._page("".join(header)))
            return
        header.append(i18n.t("cc_preview_meta", base=esc(self.job_display_name(klass.base_job)),
                             author=esc(klass.author or i18n.t("cc_no_author"))))
        if klass.description:
            header.append(f"<p><i>{esc(klass.description)}</i></p>")
        if class_catalog.category_for(klass.base_job) == class_catalog.CATEGORY_BOSS:
            header.append(i18n.t("warn_experimental"))
        special = custom_class.special_abilities(self.tables, klass)
        if special:
            names = esc(", ".join(self.ability_name(i) for i in special))
            header.append(f"<p class='warn'>{i18n.t('cc_special_warn', names=names)}</p>")
        changed = self._changed_fields(klass)
        if changed:
            header.append(i18n.t("cc_changed", names=esc(", ".join(changed))))
        self._render_preview(header, klass.effective_job(self.tables), klass.skillset, klass.actions, klass.rsm,
                             mod_builder.plan_build(self.tables, None, None, custom=klass))

    @staticmethod
    def _changed_fields(klass: CustomClass) -> list[str]:
        names = [f"{stat} ×" for stat in custom_class.STATS if stat in klass.multipliers]
        names += [f"{stat} growth" for stat in custom_class.STATS if stat in klass.growths]
        names += [label for label, value in (("Move", klass.move), ("Jump", klass.jump), ("C-Ev", klass.evasion))
                  if value is not None]
        if klass.innates is not None:
            names.append(i18n.t("cc_field_innates"))
        if klass.equip is not None:
            names.append(i18n.t("cc_field_equip"))
        return names

    def _render_preview(self, header: list[str], job: Job, skillset_name: str, action_ids: list[int],
                        rsm_ids: list[int], plan: mod_builder.BuildPlan) -> None:
        jp = self.jp_spin.value()
        esc = html.escape

        def ability_rows(ids: list[int]) -> str:
            if not ids:
                return f"<i>{i18n.t('none_f')}</i>"
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
        innate = ", ".join(esc(self.ability_name(i)) for i in job.innate_ability_ids) or i18n.t("none_f")
        parts = list(header)
        parts.append(i18n.t(
            "preview_skillset",
            name=esc(skillset_name),
            move=f.get("Move"), jump=f.get("Jump"), evade=f.get("CharacterEvasion"), job=job.id,
        ))
        parts.append(i18n.t("h_action") + ability_rows(action_ids))
        parts.append(i18n.t("h_rsm") + ability_rows(rsm_ids))
        parts.append(i18n.t("innate", names=innate))
        parts.append(i18n.t("equip", names=esc(", ".join(job.equippable) or i18n.t("none_m"))))
        parts.append(i18n.t("h_stats", rows=stats))
        extras = [s for s in (f.get("InnateStatus"), f.get("StartingStatus")) if s and s != "None"]
        if extras:
            parts.append(i18n.t("status_line", names=esc(" / ".join(extras))))
        if plan.spawn_changes:
            changes = "".join(
                f"<li>{slot}: {esc(self.item_name(old))} → {esc(self.item_name(new))}</li>"
                for slot, (old, new) in plan.spawn_changes.items()
            )
            parts.append(f"{i18n.t('h_gear')}<ul>{changes}</ul>")
        self.preview.setHtml(self._page("".join(parts)))

    # ------------------------------------------------------ custom classes

    def _editor(self, existing: Optional[CustomClass]) -> Optional[CustomClass]:
        dlg = CustomClassDialog(self.tables, self.catalog, self.ability_name, self.command_name, existing, self)
        if dlg.exec() != QDialog.Accepted:
            return None
        return dlg.result_class()

    def _after_library_change(self, path: Optional[Path]) -> None:
        self.tabs.setCurrentIndex(self._custom_tab_index())
        self.fill_custom_list(select=path)

    def new_custom(self) -> None:
        klass = self._editor(None)
        if klass:
            path = custom_class.save_file(klass, custom_class.free_path(paths.classes_dir(), klass.name))
            self._after_library_change(path)

    def edit_custom(self) -> None:
        selected = self.selected_custom()
        if selected is None:
            return
        path, klass = selected
        edited = self._editor(klass)
        if edited:
            if self.is_builtin(path):
                path = custom_class.free_path(paths.classes_dir(), edited.name)
                self.log(i18n.t("cc_builtin_copied", name=edited.name))
            custom_class.save_file(edited, path)
            self._after_library_change(path)

    def duplicate_custom(self) -> None:
        selected = self.selected_custom()
        if selected is None:
            return
        klass = selected[1]
        name = i18n.t("cc_copy_name", name=klass.name)[:custom_class.MAX_NAME]
        copy = dataclasses.replace(klass, name=name, actions=list(klass.actions), rsm=list(klass.rsm))
        path = custom_class.save_file(copy, custom_class.free_path(paths.classes_dir(), copy.name))
        self._after_library_change(path)

    def delete_custom(self) -> None:
        selected = self.selected_custom()
        if selected is None:
            return
        path, klass = selected
        if self.is_builtin(path):
            QMessageBox.information(self, i18n.t("cc_delete_title"), i18n.t("cc_builtin_no_delete"))
            return
        answer = QMessageBox.question(self, i18n.t("cc_delete_title"), i18n.t("cc_delete_body", name=klass.name))
        if answer != QMessageBox.Yes:
            return
        path.unlink(missing_ok=True)
        if self._saved_custom_path() == path:
            self.settings.custom_class_file = ""
            self.settings.save()
        self._after_library_change(None)

    def import_custom(self) -> None:
        files, _ = QFileDialog.getOpenFileNames(self, i18n.t("cc_import_title"), "", i18n.t("cc_file_filter"))
        if not files:
            return
        imported, messages, last = [], [], None
        for name in files:
            try:
                last, klass, warnings = custom_class.import_file(Path(name), paths.classes_dir(), self.tables)
            except CustomClassError as exc:
                messages.append(f"✘ {Path(name).name}: {exc}")
                continue
            imported.append(klass.name)
            messages += [f"⚠ {klass.name}: {w}" for w in warnings]
        self._after_library_change(last)
        if imported:
            messages.insert(0, i18n.t("cc_imported", names=", ".join(imported)))
        QMessageBox.information(self, i18n.t("cc_import_title"), "\n".join(messages))

    def export_custom(self) -> None:
        selected = self.selected_custom()
        if selected is None:
            QMessageBox.information(self, i18n.t("cc_export_title"), i18n.t("cc_pick_first"))
            return
        klass = selected[1]
        suggested = str(Path.home() / f"{custom_class.slug(klass.name)}{custom_class.FILE_SUFFIX}")
        target, _ = QFileDialog.getSaveFileName(self, i18n.t("cc_export_title"), suggested, i18n.t("cc_file_filter"))
        if not target:
            return
        path = Path(target)
        if not path.name.endswith(".json"):
            path = path.with_name(path.name + custom_class.FILE_SUFFIX)
        custom_class.save_file(klass, path)
        self.log(i18n.t("cc_exported", path=path))
        QMessageBox.information(self, i18n.t("cc_export_title"), i18n.t("cc_exported_body", path=path))

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
        folder = QFileDialog.getExistingDirectory(self, i18n.t("dlg_game_folder"))
        if folder:
            if not game_install.looks_like_game_root(Path(folder)):
                QMessageBox.warning(self, i18n.t("dlg_bad_folder"), i18n.t("dlg_no_exe"))
                return
            self.settings.game_root = folder
            self.settings.save()
            self.refresh_all()

    def browse_reloaded(self) -> None:
        folder = QFileDialog.getExistingDirectory(self, i18n.t("dlg_reloaded_folder"))
        if folder:
            if not reloaded.looks_like_reloaded_install(Path(folder)):
                QMessageBox.warning(self, i18n.t("dlg_bad_folder"), i18n.t("dlg_no_reloaded"))
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
        QMessageBox.critical(self, i18n.t("err_title"), message)

    def extract_data(self) -> None:
        game = self.game_root()
        if not game:
            QMessageBox.warning(self, i18n.t("dlg_no_game"), i18n.t("dlg_no_game_body"))
            return
        if not prereqs.dotnet9_installed():
            QMessageBox.warning(self, i18n.t("dlg_dotnet_title"), i18n.t("dlg_dotnet_body"))
            return

        def work(log):
            return nxd_db.extract_vanilla_db(game, paths.ff16tools_cli(), paths.cache_dir(), paths.vanilla_sqlite(), log)

        self._run(work, lambda _r: self.refresh_all(), i18n.t("log_extract"))

    def _require_ready(self) -> Optional[Path]:
        rel = self.reloaded_root()
        problems = []
        if not self.data_ready():
            problems.append(i18n.t("need_extract"))
        if not rel:
            problems.append(i18n.t("need_reloaded"))
        if problems:
            QMessageBox.warning(self, i18n.t("need_setup_title"), "\n".join(problems))
            return None
        if prereqs.reloaded_running():
            QMessageBox.warning(self, i18n.t("close_reloaded_title"), i18n.t("close_reloaded_body"))
            return None
        return rel

    def apply_mod(self) -> None:
        option = None
        custom: Optional[CustomClass] = None
        custom_path: Optional[Path] = None
        if self.chk_class.isChecked():
            selected_custom = self.selected_custom()
            if selected_custom is not None:
                custom_path = selected_custom[0]
                try:
                    custom, warnings = custom_class.sanitize(self.tables, selected_custom[1])
                except CustomClassError as exc:
                    QMessageBox.warning(self, i18n.t("cc_invalid_title"), str(exc))
                    return
                if not custom.ability_ids:
                    QMessageBox.warning(self, i18n.t("cc_invalid_title"), i18n.t("cc_need_skills"))
                    return
                for warning in warnings:
                    self.log(f"⚠ {custom.name}: {warning}")
            else:
                option = self.selected_option()
            if option is None and custom is None:
                QMessageBox.information(self, i18n.t("pick_class_title"), i18n.t("pick_class_body"))
                return
        bag = list(self.bag) if self.chk_bag.isChecked() else None
        if bag is not None and not bag:
            QMessageBox.information(self, i18n.t("empty_bag_title"), i18n.t("empty_bag_body"))
            return
        if option is None and custom is None and bag is None:
            QMessageBox.information(self, i18n.t("nothing_title"), i18n.t("nothing_body"))
            return
        rel = self._require_ready()
        if rel is None:
            return
        experimental = option.experimental if option else (
            custom is not None and class_catalog.category_for(custom.base_job) == class_catalog.CATEGORY_BOSS)
        class_name = option.name if option else custom.name if custom else None
        if experimental:
            answer = QMessageBox.question(
                self, i18n.t("experimental_title"),
                i18n.t("experimental_body", name=class_name))
            if answer != QMessageBox.Yes:
                return

        plan = mod_builder.plan_build(
            self.tables, option.job_id if option else None, class_name, bag, custom=custom)
        jp = self.jp_spin.value()
        db = paths.vanilla_sqlite()
        fallback_names = {i: self.item_name(i) for i in self.tables.items}
        if option:
            self.settings.class_job_id = option.job_id
            self.settings.custom_class_file = ""
            self.settings.save()
        elif custom_path:
            self.settings.custom_class_file = str(custom_path)
            self.settings.save()

        def nxd_builder(p, work_dir):
            class_edit = None
            if p.source_job is not None:
                class_edit = dict(ability_ids=p.ability_ids, jp_cost=jp, source_job_id=p.source_job.id,
                                  target_job_ids=class_catalog.RAMZA_JOB_IDS)
                if p.custom is not None:
                    class_edit.update(custom_name=p.custom.name, custom_description=p.custom.description,
                                      skillset_name=p.custom.skillset, target_command_ids=p.ramza_command_ids)
            return nxd_db.build_nxd_files(db, paths.ff16tools_cli(), work_dir, class_edit, p.bag, fallback_names)

        def work(log):
            log(i18n.t("log_building"))
            staged = mod_builder.build_mod(plan, paths.user_data_dir() / "build", nxd_builder)
            target = mod_builder.install_mod(staged, reloaded.mods_folder(rel))
            log(i18n.t("log_installed", path=target))
            return reloaded.set_mod_enabled(rel, mod_builder.MOD_ID, True)

        def done(enabled: bool) -> None:
            self.refresh_active()
            lines = []
            if class_name:
                lines.append(i18n.t("done_class", name=class_name))
            if plan.bag:
                lines.append(i18n.t("done_bag", n=len(plan.bag)))
            msg = i18n.t("done_intro") + "\n\n" + "\n".join(lines) + "\n\n"
            if enabled:
                msg += i18n.t("done_ok")
            else:
                msg += i18n.t("done_no_app", mod=mod_builder.MOD_NAME)
            QMessageBox.information(self, i18n.t("done_title"), msg)

        self._run(work, done, i18n.t("log_applying"))

    def restore(self) -> None:
        rel = self.reloaded_root()
        if rel is None:
            QMessageBox.warning(self, i18n.t("need_setup_title"), i18n.t("restore_need"))
            return
        if prereqs.reloaded_running():
            QMessageBox.warning(self, i18n.t("close_reloaded_title"), i18n.t("close_reloaded_restore"))
            return
        removed = mod_builder.uninstall_mod(reloaded.mods_folder(rel))
        reloaded.set_mod_enabled(rel, mod_builder.MOD_ID, False)
        self.refresh_active()
        self.log(i18n.t("log_removed") if removed else i18n.t("log_not_installed"))
        QMessageBox.information(self, i18n.t("restored_title"), i18n.t("restored_body"))


def main() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName("Solo Ramza Manager")
    theme.apply(app)
    window = MainWindow()
    window.show()
    if not window.settings.wizard_done:
        QTimer.singleShot(0, window.open_wizard)
    return app.exec()
