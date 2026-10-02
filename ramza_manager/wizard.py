"""Assistente do que instalar e de como configurar o Solo Ramza Manager."""

from __future__ import annotations

import traceback
from pathlib import Path
from typing import Callable, Optional

from PySide6.QtCore import QObject, QThread, QUrl, Qt, Signal
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import (
    QButtonGroup, QDialog, QFileDialog, QFrame, QHBoxLayout, QLabel, QMessageBox,
    QPlainTextEdit, QPushButton, QScrollArea, QStackedWidget, QVBoxLayout, QWidget,
)

from . import game_install, i18n, nxd_db, paths, prereqs, reloaded, theme
from .settings import Settings

URL_RELOADED = "https://github.com/Reloaded-Project/Reloaded-II/releases/latest"
URL_MODLOADER = "https://github.com/Nenkai/fftivc.utility.modloader/releases/latest"
URL_DOTNET = "https://dotnet.microsoft.com/download/dotnet/9.0"

_STEP_KEYS = (
    "wiz_step_lang",
    "wiz_step_overview",
    "wiz_step_dotnet",
    "wiz_step_reloaded",
    "wiz_step_loader",
    "wiz_step_game",
    "wiz_step_extract",
    "wiz_step_use",
)


class _Worker(QObject):
    log = Signal(str)
    done = Signal(object)
    failed = Signal(str)

    def __init__(self, fn: Callable[[Callable[[str], None]], object]):
        super().__init__()
        self.fn = fn

    def run(self) -> None:
        try:
            result = self.fn(self.log.emit)
        except Exception as exc:  # noqa: BLE001
            self.log.emit(traceback.format_exc())
            self.failed.emit(str(exc))
            return
        self.done.emit(result)


def _rich(text: str) -> QLabel:
    label = QLabel(text)
    label.setWordWrap(True)
    label.setTextFormat(Qt.RichText)
    label.setTextInteractionFlags(Qt.TextSelectableByMouse)
    return label


class SetupWizard(QDialog):
    """Passo a passo de instalação e configuração. O idioma vale para o app inteiro."""

    language_changed = Signal(str)

    def __init__(self, settings: Settings, parent=None):
        super().__init__(parent)
        self.settings = settings
        self.resize(880, 640)
        self.setMinimumSize(760, 560)
        self._thread: Optional[QThread] = None
        self._worker: Optional[_Worker] = None

        if not self.settings.game_root:
            found = game_install.find_game_root()
            if found:
                self.settings.game_root = str(found)
        if not self.settings.reloaded_root:
            found = reloaded.find_installed_reloaded()
            if found:
                self.settings.reloaded_root = str(found)
        if self.settings.game_root or self.settings.reloaded_root:
            self.settings.save()

        root = QVBoxLayout(self)
        root.setContentsMargins(14, 14, 14, 14)

        body = QHBoxLayout()
        self.side = QFrame()
        self.side.setObjectName("WizardSide")
        self.side.setFixedWidth(210)
        side_layout = QVBoxLayout(self.side)
        side_layout.setContentsMargins(8, 8, 8, 8)
        self.step_buttons: list[QPushButton] = []
        for index, key in enumerate(_STEP_KEYS):
            btn = QPushButton(i18n.t(key))
            btn.setObjectName("Step")
            btn.setCheckable(True)
            btn.clicked.connect(lambda _checked=False, i=index: self._go(i))
            self.step_buttons.append(btn)
            side_layout.addWidget(btn)
        side_layout.addStretch()
        body.addWidget(self.side)

        self.stack = QStackedWidget()
        self.stack.addWidget(self._build_language())
        self.stack.addWidget(self._build_text_page("overview"))
        self.stack.addWidget(self._build_dotnet())
        self.stack.addWidget(self._build_reloaded())
        self.stack.addWidget(self._build_loader())
        self.stack.addWidget(self._build_game())
        self.stack.addWidget(self._build_extract())
        self.stack.addWidget(self._build_use())
        body.addWidget(self.stack, 1)
        root.addLayout(body, 1)

        nav = QHBoxLayout()
        self.btn_skip = QPushButton()
        self.btn_skip.setObjectName("Secondary")
        self.btn_skip.clicked.connect(self._skip)
        nav.addWidget(self.btn_skip)
        nav.addStretch()
        self.btn_back = QPushButton()
        self.btn_back.clicked.connect(lambda: self._go(self.stack.currentIndex() - 1))
        nav.addWidget(self.btn_back)
        self.btn_next = QPushButton()
        self.btn_next.setObjectName("Primary")
        self.btn_next.clicked.connect(self._next)
        nav.addWidget(self.btn_next)
        root.addLayout(nav)

        chosen = self.settings.language if self.settings.language in i18n.LANGS else ""
        if chosen:
            i18n.set_language(chosen)
            self._select_lang_button(chosen)
        self.retranslate()
        self._go(1 if chosen else 0)

    # ---------------------------------------------------------------- pages

    def _build_language(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        self.lbl_lang_title = QLabel()
        self._title(self.lbl_lang_title)
        layout.addWidget(self.lbl_lang_title)
        self.lbl_lang_body = _rich("")
        layout.addWidget(self.lbl_lang_body)
        self.lang_group = QButtonGroup(self)
        self.lang_group.setExclusive(True)
        self.btn_pt = QPushButton("Português (Brasil)")
        self.btn_en = QPushButton("English")
        for btn, lang in ((self.btn_pt, i18n.LANG_PT), (self.btn_en, i18n.LANG_EN)):
            btn.setObjectName("LangChoice")
            btn.setCheckable(True)
            btn.clicked.connect(lambda _c=False, code=lang: self._pick_language(code))
            self.lang_group.addButton(btn)
            layout.addWidget(btn)
        layout.addStretch()
        return self._wrap(page)

    def _build_text_page(self, key: str) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        title = QLabel()
        self._title(title)
        body = _rich("")
        layout.addWidget(title)
        layout.addWidget(body)
        layout.addStretch()
        setattr(self, f"lbl_{key}_title", title)
        setattr(self, f"lbl_{key}_body", body)
        return self._wrap(page)

    def _build_dotnet(self) -> QWidget:
        page, self.lbl_dotnet_title, self.lbl_dotnet_body, self.lbl_dotnet_status = self._check_page()
        row = QHBoxLayout()
        self.btn_dl_dotnet = QPushButton()
        self.btn_dl_dotnet.clicked.connect(lambda: self._open(URL_DOTNET))
        self.btn_check_dotnet = QPushButton()
        self.btn_check_dotnet.clicked.connect(self._refresh_status)
        row.addWidget(self.btn_dl_dotnet)
        row.addWidget(self.btn_check_dotnet)
        row.addStretch()
        page.layout().addLayout(row)
        return self._wrap(page)

    def _build_reloaded(self) -> QWidget:
        page, self.lbl_rel_title, self.lbl_rel_body, self.lbl_rel_status = self._check_page()
        row = QHBoxLayout()
        self.btn_dl_rel = QPushButton()
        self.btn_dl_rel.clicked.connect(lambda: self._open(URL_RELOADED))
        self.btn_browse_rel = QPushButton()
        self.btn_browse_rel.clicked.connect(self._browse_reloaded)
        self.btn_check_rel = QPushButton()
        self.btn_check_rel.clicked.connect(self._refresh_status)
        row.addWidget(self.btn_dl_rel)
        row.addWidget(self.btn_browse_rel)
        row.addWidget(self.btn_check_rel)
        row.addStretch()
        page.layout().addLayout(row)
        return self._wrap(page)

    def _build_loader(self) -> QWidget:
        page, self.lbl_loader_title, self.lbl_loader_body, self.lbl_loader_status = self._check_page()
        self.lbl_app_status = _rich("")
        page.layout().insertWidget(2, self.lbl_app_status)
        row = QHBoxLayout()
        self.btn_dl_loader = QPushButton()
        self.btn_dl_loader.clicked.connect(lambda: self._open(URL_MODLOADER))
        self.btn_check_loader = QPushButton()
        self.btn_check_loader.clicked.connect(self._refresh_status)
        row.addWidget(self.btn_dl_loader)
        row.addWidget(self.btn_check_loader)
        row.addStretch()
        page.layout().addLayout(row)
        return self._wrap(page)

    def _build_game(self) -> QWidget:
        page, self.lbl_game_title, self.lbl_game_body, self.lbl_game_status = self._check_page()
        row = QHBoxLayout()
        self.btn_browse_game = QPushButton()
        self.btn_browse_game.clicked.connect(self._browse_game)
        self.btn_check_game = QPushButton()
        self.btn_check_game.clicked.connect(self._refresh_status)
        row.addWidget(self.btn_browse_game)
        row.addWidget(self.btn_check_game)
        row.addStretch()
        page.layout().addLayout(row)
        return self._wrap(page)

    def _build_extract(self) -> QWidget:
        page, self.lbl_extract_title, self.lbl_extract_body, self.lbl_extract_status = self._check_page()
        row = QHBoxLayout()
        self.btn_extract = QPushButton()
        self.btn_extract.setObjectName("Primary")
        self.btn_extract.clicked.connect(self._extract)
        self.btn_check_extract = QPushButton()
        self.btn_check_extract.clicked.connect(self._refresh_status)
        row.addWidget(self.btn_extract)
        row.addWidget(self.btn_check_extract)
        row.addStretch()
        page.layout().addLayout(row)
        self.extract_log = QPlainTextEdit()
        self.extract_log.setObjectName("Log")
        self.extract_log.setReadOnly(True)
        self.extract_log.setMaximumHeight(120)
        page.layout().addWidget(self.extract_log)
        return self._wrap(page)

    def _build_use(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        self.lbl_use_title = QLabel()
        self._title(self.lbl_use_title)
        self.lbl_use_body = _rich("")
        self.lbl_use_check_title = QLabel()
        self.lbl_use_check_title.setStyleSheet("font-weight: bold;")
        self.lbl_use_checks = _rich("")
        layout.addWidget(self.lbl_use_title)
        layout.addWidget(self.lbl_use_body)
        layout.addWidget(self.lbl_use_check_title)
        layout.addWidget(self.lbl_use_checks)
        layout.addStretch()
        return self._wrap(page)

    def _check_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        title = QLabel()
        self._title(title)
        body = _rich("")
        status = _rich("")
        layout.addWidget(title)
        layout.addWidget(body)
        layout.addWidget(status)
        layout.addStretch()
        return page, title, body, status

    @staticmethod
    def _title(label: QLabel) -> None:
        label.setObjectName("WizardTitle")

    def _wrap(self, inner: QWidget) -> QScrollArea:
        frame = QFrame()
        frame.setObjectName("WizardBody")
        outer = QVBoxLayout(frame)
        outer.setContentsMargins(16, 14, 16, 14)
        outer.addWidget(inner)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setWidget(frame)
        return scroll

    # -------------------------------------------------------------- language

    def _select_lang_button(self, lang: str) -> None:
        btn = self.btn_pt if lang == i18n.LANG_PT else self.btn_en
        btn.setChecked(True)

    def _pick_language(self, lang: str) -> None:
        i18n.set_language(lang)
        self.settings.language = lang
        self.settings.save()
        self.language_changed.emit(lang)
        self.retranslate()
        self._update_nav()

    # ----------------------------------------------------------------- nav

    def _language_chosen(self) -> bool:
        return self.settings.language in i18n.LANGS

    def _go(self, index: int) -> None:
        index = max(0, min(index, self.stack.count() - 1))
        if index != 0 and not self._language_chosen():
            index = 0
        self.stack.setCurrentIndex(index)
        for i, btn in enumerate(self.step_buttons):
            btn.setChecked(i == index)
            btn.setEnabled(i == 0 or self._language_chosen())
        self._refresh_status()
        self._update_nav()

    def _next(self) -> None:
        if self.stack.currentIndex() == 0 and not self._language_chosen():
            return
        if self.stack.currentIndex() >= self.stack.count() - 1:
            self.accept()
            return
        self._go(self.stack.currentIndex() + 1)

    def _skip(self) -> None:
        self.accept()

    def _update_nav(self) -> None:
        index = self.stack.currentIndex()
        last = index >= self.stack.count() - 1
        self.btn_back.setEnabled(index > 0)
        self.btn_next.setEnabled(index > 0 or self._language_chosen())
        self.btn_next.setText(i18n.t("wiz_finish") if last else i18n.t("wiz_next"))
        self.btn_skip.setVisible(index > 0)
        self.setWindowTitle(i18n.t("wiz_title"))

    def retranslate(self) -> None:
        t = i18n.t
        for btn, key in zip(self.step_buttons, _STEP_KEYS):
            btn.setText(t(key))
        self.lbl_lang_title.setText(t("wiz_lang_title"))
        self.lbl_lang_body.setText(t("wiz_lang_body"))
        self.lbl_overview_title.setText(t("wiz_overview_title"))
        self.lbl_overview_body.setText(t("wiz_overview_body"))
        self.lbl_dotnet_title.setText(t("wiz_dotnet_title"))
        self.lbl_dotnet_body.setText(t("wiz_dotnet_body"))
        self.lbl_rel_title.setText(t("wiz_reloaded_title"))
        self.lbl_rel_body.setText(t("wiz_reloaded_body"))
        self.lbl_loader_title.setText(t("wiz_loader_title"))
        self.lbl_loader_body.setText(t("wiz_loader_body"))
        self.lbl_game_title.setText(t("wiz_game_title"))
        self.lbl_game_body.setText(t("wiz_game_body"))
        self.lbl_extract_title.setText(t("wiz_extract_title"))
        self.lbl_extract_body.setText(t("wiz_extract_body"))
        self.lbl_use_title.setText(t("wiz_use_title"))
        self.lbl_use_body.setText(t("wiz_use_body"))
        self.lbl_use_check_title.setText(t("wiz_checklist_title"))
        for btn in (
            self.btn_dl_dotnet, self.btn_dl_rel, self.btn_dl_loader,
        ):
            btn.setText(t("btn_download"))
        for btn in (
            self.btn_check_dotnet, self.btn_check_rel, self.btn_check_loader,
            self.btn_check_game, self.btn_check_extract,
        ):
            btn.setText(t("wiz_check"))
        self.btn_browse_rel.setText(t("btn_browse"))
        self.btn_browse_game.setText(t("btn_browse"))
        self.btn_extract.setText(t("wiz_extract"))
        self.btn_back.setText(t("wiz_back"))
        self.btn_skip.setText(t("wiz_skip"))
        self._refresh_status()
        self._update_nav()

    # --------------------------------------------------------------- status

    def _refresh_status(self) -> None:
        t = i18n.t
        dotnet = prereqs.dotnet9_installed()
        game = prereqs.resolve_game(self.settings.game_root)
        rel = prereqs.resolve_reloaded(self.settings.reloaded_root)
        loader = prereqs.modloader_installed(rel)
        added = prereqs.game_added_to_reloaded(rel)
        ready = prereqs.data_ready()
        self.lbl_dotnet_status.setText(prereqs.status_html(dotnet, t("wiz_dotnet_ok") if dotnet else t("wiz_dotnet_bad")))
        rel_text = str(rel) if rel else t("wiz_reloaded_bad")
        self.lbl_rel_status.setText(prereqs.status_html(bool(rel), t("wiz_reloaded_ok") + f"  {rel_text}" if rel else rel_text))
        self.lbl_app_status.setText(prereqs.status_html(added, t("wiz_app_ok") if added else t("wiz_app_bad")))
        self.lbl_loader_status.setText(prereqs.status_html(loader, t("wiz_loader_ok") if loader else t("wiz_loader_bad")))
        game_text = str(game) if game else t("wiz_game_bad")
        self.lbl_game_status.setText(prereqs.status_html(bool(game), t("wiz_game_ok") + f"  {game_text}" if game else game_text))
        if self._thread is not None:
            self.lbl_extract_status.setText(prereqs.status_html(True, t("wiz_extract_running")))
        else:
            self.lbl_extract_status.setText(prereqs.status_html(ready, t("wiz_extract_ok") if ready else t("wiz_extract_bad")))
        lines = [
            prereqs.status_html(dotnet, ".NET 9 Runtime"),
            prereqs.status_html(bool(rel), "Reloaded-II"),
            prereqs.status_html(added, "Reloaded-II: FFT_enhanced.exe"),
            prereqs.status_html(loader, "FFTIVC Mod Loader"),
            prereqs.status_html(bool(game), t("row_game").rstrip(":")),
            prereqs.status_html(ready, t("row_data").rstrip(":")),
        ]
        self.lbl_use_checks.setText("<br>".join(lines))

    # -------------------------------------------------------------- actions

    def _open(self, url: str) -> None:
        QDesktopServices.openUrl(QUrl(url))

    def _browse_game(self) -> None:
        folder = QFileDialog.getExistingDirectory(self, i18n.t("dlg_game_folder"))
        if not folder:
            return
        if not game_install.looks_like_game_root(Path(folder)):
            QMessageBox.warning(self, i18n.t("dlg_bad_folder"), i18n.t("dlg_no_exe"))
            return
        self.settings.game_root = folder
        self.settings.save()
        self._refresh_status()

    def _browse_reloaded(self) -> None:
        folder = QFileDialog.getExistingDirectory(self, i18n.t("dlg_reloaded_folder"))
        if not folder:
            return
        if not reloaded.looks_like_reloaded_install(Path(folder)):
            QMessageBox.warning(self, i18n.t("dlg_bad_folder"), i18n.t("dlg_no_reloaded"))
            return
        self.settings.reloaded_root = folder
        self.settings.save()
        self._refresh_status()

    def _extract(self) -> None:
        if self._thread is not None:
            return
        game = prereqs.resolve_game(self.settings.game_root)
        if not game:
            QMessageBox.warning(self, i18n.t("dlg_no_game"), i18n.t("dlg_no_game_body"))
            return
        if not prereqs.dotnet9_installed():
            QMessageBox.warning(self, i18n.t("dlg_dotnet_title"), i18n.t("dlg_dotnet_body"))
            return
        self.extract_log.clear()
        self.lbl_extract_status.setText(prereqs.status_html(True, i18n.t("wiz_extract_running")))
        self.btn_extract.setEnabled(False)
        self.btn_next.setEnabled(False)
        self.btn_back.setEnabled(False)
        self.btn_skip.setEnabled(False)

        def work(log):
            return nxd_db.extract_vanilla_db(
                game, paths.ff16tools_cli(), paths.cache_dir(), paths.vanilla_sqlite(), log)

        thread = QThread(self)
        worker = _Worker(work)
        worker.moveToThread(thread)
        worker.log.connect(self.extract_log.appendPlainText)
        worker.done.connect(self._extract_done)
        worker.failed.connect(self._extract_failed)
        thread.started.connect(worker.run)
        self._thread, self._worker = thread, worker
        thread.start()

    def _finish_extract(self) -> None:
        if self._thread is not None:
            self._thread.quit()
            self._thread.wait()
        self._thread = None
        self._worker = None
        self.btn_extract.setEnabled(True)
        self.btn_skip.setEnabled(True)
        self._update_nav()
        self._refresh_status()

    def _extract_done(self, _result) -> None:
        self._finish_extract()

    def _extract_failed(self, message: str) -> None:
        self._finish_extract()
        QMessageBox.critical(self, i18n.t("err_title"), message)

    def closeEvent(self, event) -> None:  # noqa: N802
        if self._thread is not None:
            event.ignore()
            return
        super().closeEvent(event)
