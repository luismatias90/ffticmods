"""
Identidade visual inspirada nos menus de Final Fantasy Tactics: The Ivalice
Chronicles: janelas azul-noite com moldura dupla dourada, texto creme, títulos
em ouro, detalhes em carmesim e a mão-cursor dos menus apontando o item
escolhido. Só estilo (QSS + fontes do Windows) e desenhos feitos em código;
nenhuma arte do jogo é usada.
"""

from __future__ import annotations

from PySide6.QtCore import QEvent, QObject, QPointF, QRectF, Qt
from PySide6.QtGui import (
    QBrush, QColor, QFont, QIcon, QLinearGradient, QPainter, QPainterPath, QPalette, QPen, QPixmap,
)
from PySide6.QtWidgets import QApplication, QListWidget, QStyle, QStyledItemDelegate

# Paleta
NIGHT = "#0a0d14"
NIGHT_LIGHT = "#141a28"
PANEL = "#1a2131"
PANEL_TOP = "#232c41"
PANEL_DEEP = "#0f131d"
ROW_ALT = "#151b29"
LINE = "#2b3348"
BRONZE = "#7a6238"
GOLD = "#d6b36a"
GOLD_LIGHT = "#f2dc9b"
GOLD_DIM = "#a68a52"
TEXT = "#ece4cf"
TEXT_MUTED = "#a69d87"
TEXT_DIM = "#6b675d"
CRIMSON = "#9e2b2b"
CRIMSON_LIGHT = "#c04242"
WINE = "#4f1313"
DANGER = "#e8836f"
JP_GREEN = "#9fd38a"

# Faixa de seleção (ouro se desfazendo para a direita, como nos menus do jogo).
_SELECTION = ("qlineargradient(x1:0, y1:0, x2:1, y2:0, "
              "stop:0 rgba(214,179,106,0.42), stop:0.6 rgba(214,179,106,0.14), stop:1 rgba(214,179,106,0.04))")
_HOVER = "rgba(214,179,106,0.09)"
_WINDOW = f"qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 {PANEL_TOP}, stop:0.12 {PANEL}, stop:1 #141a27)"

SERIF = "Palatino Linotype"
SERIF_FALLBACKS = ["Book Antiqua", "Georgia", "Times New Roman"]

# Espaço à esquerda dos itens de lista para a mão-cursor.
CURSOR_GUTTER = 30

QSS = f"""
* {{
    font-family: "{SERIF}", "Book Antiqua", Georgia, serif;
    font-size: 10.5pt;
}}
QMainWindow, QDialog, QMessageBox {{
    background: qradialgradient(cx:0.5, cy:0.0, radius:1.1, fx:0.5, fy:0.0,
        stop:0 {NIGHT_LIGHT}, stop:1 {NIGHT});
}}
QWidget {{ color: {TEXT}; }}
QLabel {{ color: {TEXT}; background: transparent; }}
QLabel#Muted {{ color: {TEXT_MUTED}; font-style: italic; }}
QToolTip {{
    color: {TEXT}; background: {PANEL}; border: 1px solid {GOLD}; padding: 5px 8px;
}}

/* ---- Cabeçalho ---- */
#Banner {{
    border: 3px double {GOLD_DIM};
    border-radius: 4px;
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 {NIGHT}, stop:0.35 #1b2238, stop:0.65 #1b2238, stop:1 {NIGHT});
}}
#BannerTitle {{
    color: {GOLD_LIGHT}; font-size: 21pt; font-weight: bold; letter-spacing: 4px;
}}
#BannerSubtitle {{ color: {TEXT_MUTED}; font-size: 10pt; font-style: italic; }}

/* ---- Janelas (painéis) ---- */
QGroupBox {{
    background: {_WINDOW};
    border: 3px double {GOLD_DIM};
    border-radius: 4px;
    margin-top: 14px;
    padding: 12px 10px 8px 10px;
}}
QGroupBox::title {{
    subcontrol-origin: margin; left: 14px; padding: 1px 12px;
    color: {GOLD_LIGHT}; background: {NIGHT};
    border: 1px solid {GOLD_DIM}; border-radius: 3px;
    font-weight: bold; letter-spacing: 1px;
}}

/* ---- Barra lateral (passos) ---- */
QFrame#Sidebar {{
    background: {_WINDOW};
    border: 3px double {GOLD_DIM}; border-radius: 4px;
}}
QLabel#SideCaption {{ color: {GOLD}; font-size: 8.5pt; font-weight: bold; letter-spacing: 3px; }}
QPushButton#Nav {{
    background: transparent; border: 1px solid transparent; border-left: 3px solid transparent;
    border-radius: 3px; padding: 0;
}}
QPushButton#Nav:hover:!checked {{ background: {_HOVER}; border-left: 3px solid {BRONZE}; }}
QPushButton#Nav:checked {{ background: {_SELECTION}; border: 1px solid {BRONZE}; border-left: 3px solid {GOLD}; }}
QLabel#NavTitle {{ color: {TEXT}; font-weight: bold; font-size: 11pt; }}
QLabel#NavTitle[current="true"] {{ color: {GOLD_LIGHT}; }}
QLabel#NavSubtitle {{ color: {TEXT_MUTED}; font-style: italic; font-size: 9.5pt; }}
QLabel#NavBadge {{
    color: {TEXT_MUTED}; background: {NIGHT}; border: 2px solid {BRONZE};
    border-radius: 14px; font-weight: bold;
}}
QLabel#NavBadge[active="true"] {{ color: {GOLD_LIGHT}; background: {CRIMSON}; border: 2px solid {GOLD}; }}
QFrame#InstalledCard {{ background: {PANEL_DEEP}; border: 1px solid {BRONZE}; border-radius: 3px; }}
QFrame#InstalledCard QLabel {{ color: {TEXT}; }}
QFrame#Sidebar QPushButton#Primary {{ padding: 10px 12px; }}

/* ---- Páginas ---- */
QFrame#Page {{ background: {_WINDOW}; border: 3px double {GOLD_DIM}; border-radius: 4px; }}
QLabel#PageTitle, QLabel#WizardTitle {{ color: {GOLD_LIGHT}; font-size: 16pt; font-weight: bold; letter-spacing: 1px; }}
QLabel#PageDesc {{ color: {TEXT_MUTED}; font-style: italic; }}
QLabel#ColumnTitle {{ color: {GOLD}; font-weight: bold; font-size: 11pt; letter-spacing: 1px; }}
QLabel#Note {{
    background: rgba(214,179,106,0.07); border: 1px solid {LINE}; border-left: 3px solid {GOLD};
    border-radius: 3px; padding: 6px 10px;
}}
QFrame#Rule {{
    border: none;
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 {GOLD}, stop:0.5 {GOLD_DIM}, stop:1 rgba(214,179,106,0));
}}
QCheckBox#SectionToggle {{
    background: {PANEL_DEEP}; border: 1px solid {BRONZE}; border-radius: 3px; padding: 6px 12px;
}}
QCheckBox#SectionToggle:hover {{ border: 1px solid {GOLD}; }}
QFrame#ActionBar {{ background: {PANEL_DEEP}; border: 1px solid {BRONZE}; border-radius: 3px; }}
QPushButton#Chip {{
    color: {TEXT}; background: {PANEL_DEEP};
    border: 1px solid {BRONZE}; border-radius: 12px; padding: 4px 14px;
}}
QPushButton#Chip:hover:!checked {{ color: {GOLD_LIGHT}; border: 1px solid {GOLD}; background: {PANEL}; }}
QPushButton#Chip:checked {{ color: {GOLD_LIGHT}; background: {CRIMSON}; border: 1px solid {GOLD}; font-weight: bold; }}
QPushButton#Chip:disabled {{ color: {TEXT_DIM}; }}
QPushButton#Accent {{
    color: {GOLD_LIGHT}; font-weight: bold; background: {NIGHT}; border: 1px solid {GOLD};
}}
QPushButton#Accent:hover {{ background: {PANEL_TOP}; }}
QPushButton#Accent:disabled {{ color: {TEXT_DIM}; border: 1px solid {BRONZE}; }}
QPushButton#Danger {{ color: {DANGER}; }}
QPushButton#Danger:disabled {{ color: {TEXT_DIM}; }}
QListWidget:disabled, QTableWidget:disabled, QTextBrowser:disabled, QLabel:disabled {{ color: {TEXT_DIM}; }}

/* ---- Abas ---- */
QTabWidget::pane {{
    background: {_WINDOW};
    border: 3px double {GOLD_DIM};
    border-radius: 4px;
    top: -3px;
}}
QTabBar::tab {{
    background: {PANEL_DEEP}; color: {TEXT_MUTED};
    border: 1px solid {BRONZE}; border-bottom: none;
    border-top-left-radius: 4px; border-top-right-radius: 4px;
    padding: 6px 18px; margin-right: 3px; font-weight: bold;
}}
QTabBar::tab:selected {{ background: {PANEL_TOP}; color: {GOLD_LIGHT}; border-color: {GOLD}; }}
QTabBar::tab:hover:!selected {{ color: {GOLD_LIGHT}; }}

/* ---- Botões ---- */
QPushButton {{
    color: {TEXT};
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #2a3349, stop:1 #191f2e);
    border: 1px solid {BRONZE}; border-radius: 3px;
    padding: 5px 14px;
}}
QPushButton:hover {{ color: {GOLD_LIGHT}; border: 1px solid {GOLD}; }}
QPushButton:pressed {{ background: {PANEL_DEEP}; }}
QPushButton:focus {{ border: 1px solid {GOLD}; }}
QPushButton:disabled {{ color: {TEXT_DIM}; border: 1px solid {LINE}; }}
QPushButton#Primary {{
    color: {GOLD_LIGHT}; font-weight: bold; font-size: 12pt; letter-spacing: 2px;
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 {CRIMSON_LIGHT}, stop:0.5 {CRIMSON}, stop:1 {WINE});
    border: 2px solid {GOLD}; padding: 8px 26px;
}}
QPushButton#Primary:hover {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #d65050, stop:0.5 {CRIMSON_LIGHT}, stop:1 {CRIMSON});
}}
QPushButton#Primary:disabled {{ color: {TEXT_DIM}; background: {PANEL_DEEP}; border: 2px solid {LINE}; }}
QPushButton#Secondary {{
    color: {TEXT}; background: {PANEL_DEEP}; border: 1px solid {BRONZE}; padding: 8px 18px;
}}
QPushButton#Secondary:hover {{ color: {GOLD_LIGHT}; border: 1px solid {GOLD}; }}

/* ---- Campos ---- */
QLineEdit, QSpinBox, QPlainTextEdit {{
    color: {TEXT}; background: {PANEL_DEEP};
    border: 1px solid {BRONZE}; border-radius: 3px; padding: 4px 6px;
    selection-background-color: {GOLD}; selection-color: {NIGHT};
}}
QLineEdit:focus, QSpinBox:focus, QPlainTextEdit:focus {{ border: 1px solid {GOLD}; }}
QLineEdit:disabled, QSpinBox:disabled {{ color: {TEXT_DIM}; border: 1px solid {LINE}; }}
QSpinBox {{ padding-right: 18px; }}
QSpinBox::up-button, QSpinBox::down-button {{
    subcontrol-origin: border; width: 18px;
    background: {PANEL_TOP}; border-left: 1px solid {BRONZE};
}}
QSpinBox::up-button {{ subcontrol-position: top right; border-top-right-radius: 3px; }}
QSpinBox::down-button {{ subcontrol-position: bottom right; border-bottom-right-radius: 3px; }}
QSpinBox::up-button:hover, QSpinBox::down-button:hover {{ background: {BRONZE}; }}
QSpinBox::up-arrow {{ image: url("@ARROW_UP@"); width: 9px; height: 6px; }}
QSpinBox::down-arrow {{ image: url("@ARROW_DOWN@"); width: 9px; height: 6px; }}

QCheckBox {{ color: {TEXT}; font-weight: bold; spacing: 8px; }}
QCheckBox:hover {{ color: {GOLD_LIGHT}; }}
QCheckBox::indicator {{
    width: 15px; height: 15px; border: 1px solid {GOLD_DIM}; border-radius: 2px; background: {PANEL_DEEP};
}}
QCheckBox::indicator:hover {{ border: 1px solid {GOLD}; }}
QCheckBox::indicator:checked {{ background: {CRIMSON}; border: 1px solid {GOLD}; image: url("@CHECK@"); }}

/* ---- Listas, tabela, prévia ---- */
QListWidget, QTableWidget, QTextBrowser {{
    color: {TEXT}; background: {PANEL_DEEP};
    border: 1px solid {BRONZE}; border-radius: 3px;
    alternate-background-color: {ROW_ALT};
    outline: none;
}}
QListWidget::item {{ padding: 5px 8px 5px {CURSOR_GUTTER}px; border-bottom: 1px solid {LINE}; }}
QListWidget::item:hover {{ background: {_HOVER}; }}
QListWidget::item:selected {{ color: {GOLD_LIGHT}; background: {_SELECTION}; }}
QTableWidget {{ gridline-color: {LINE}; }}
QTableWidget::item {{ padding: 2px 6px; }}
QTableWidget::item:selected {{ color: {GOLD_LIGHT}; background: {_SELECTION}; }}
QHeaderView::section {{
    color: {GOLD_LIGHT}; background: {NIGHT};
    border: none; border-bottom: 1px solid {GOLD_DIM}; border-right: 1px solid {LINE};
    padding: 5px; font-weight: bold; letter-spacing: 1px;
}}
QTableCornerButton::section {{ background: {NIGHT}; }}
QTableWidget QSpinBox {{ border: none; border-radius: 0; background: transparent; }}

/* ---- Registro e barra de status ---- */
QPlainTextEdit#Log {{
    color: {TEXT_MUTED}; background: {NIGHT};
    border: 1px solid {LINE}; border-radius: 3px;
    font-family: Consolas, monospace; font-size: 9pt;
}}
QStatusBar {{ background: {NIGHT}; border-top: 1px solid {LINE}; }}
QStatusBar::item {{ border: none; }}
QStatusBar QLabel {{ color: {TEXT_MUTED}; font-style: italic; padding-left: 4px; }}
QStatusBar QPushButton {{ padding: 1px 10px; font-size: 9.5pt; }}

/* ---- Rolagem e divisores ---- */
QScrollBar:vertical {{ background: {NIGHT}; width: 11px; margin: 0; border: none; }}
QScrollBar::handle:vertical {{ background: {BRONZE}; border-radius: 4px; min-height: 28px; margin: 2px; }}
QScrollBar::handle:vertical:hover {{ background: {GOLD}; }}
QScrollBar:horizontal {{ background: {NIGHT}; height: 11px; border: none; }}
QScrollBar::handle:horizontal {{ background: {BRONZE}; border-radius: 4px; min-width: 28px; margin: 2px; }}
QScrollBar::handle:horizontal:hover {{ background: {GOLD}; }}
QScrollBar::add-line, QScrollBar::sub-line {{ width: 0; height: 0; }}
QScrollBar::add-page, QScrollBar::sub-page {{ background: none; }}
QSplitter::handle {{ background: transparent; width: 8px; }}
QSplitter::handle:hover {{ background: rgba(214,179,106,0.15); }}

QComboBox {{
    color: {TEXT}; background: {PANEL_DEEP};
    border: 1px solid {BRONZE}; border-radius: 3px; padding: 3px 26px 3px 8px;
}}
QComboBox:hover, QComboBox:focus {{ border: 1px solid {GOLD}; }}
QComboBox::drop-down {{
    subcontrol-origin: padding; subcontrol-position: top right; width: 20px;
    border-left: 1px solid {BRONZE}; background: {PANEL_TOP};
}}
QComboBox::down-arrow {{ image: url("@ARROW_DOWN@"); width: 9px; height: 6px; }}
QComboBox QAbstractItemView {{
    color: {TEXT}; background: {PANEL}; border: 1px solid {GOLD_DIM}; outline: none;
    selection-background-color: {CRIMSON}; selection-color: {GOLD_LIGHT};
}}

/* ---- Assistente ---- */
QFrame#WizardSide {{ background: {_WINDOW}; border: 3px double {GOLD_DIM}; border-radius: 4px; }}
QFrame#WizardBody {{ background: {_WINDOW}; border: 3px double {GOLD_DIM}; border-radius: 4px; }}
QScrollArea {{ background: transparent; border: none; }}
QPushButton#Step {{
    text-align: left; color: {TEXT}; background: transparent;
    border: none; border-left: 3px solid transparent; border-radius: 0;
    padding: 7px 8px; font-weight: normal;
}}
QPushButton#Step:checked {{
    color: {GOLD_LIGHT}; background: {_SELECTION};
    border-left: 3px solid {GOLD}; font-weight: bold;
}}
QPushButton#Step:hover:!checked {{ color: {GOLD_LIGHT}; background: {_HOVER}; }}
QPushButton#Step:disabled {{ color: {TEXT_DIM}; }}
QPushButton#LangChoice {{
    font-size: 13pt; padding: 14px 18px; text-align: left;
}}
QPushButton#LangChoice:checked {{
    color: {GOLD_LIGHT}; font-weight: bold;
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 {CRIMSON_LIGHT}, stop:0.5 {CRIMSON}, stop:1 {WINE});
    border: 2px solid {GOLD};
}}

QMessageBox QLabel {{ color: {TEXT}; font-size: 11pt; }}
QMessageBox QPushButton {{ min-width: 80px; }}
"""

# CSS do painel de prévia (QTextBrowser usa um subconjunto de HTML/CSS).
PREVIEW_CSS = f"""
body {{ color: {TEXT}; font-family: "{SERIF}", Georgia, serif; font-size: 10.5pt; }}
h2 {{ color: {GOLD_LIGHT}; font-size: 18pt; margin-bottom: 2px; }}
h3 {{ color: {GOLD}; font-size: 11.5pt; margin-top: 14px; margin-bottom: 4px; letter-spacing: 1px; }}
b {{ color: {GOLD_LIGHT}; }}
.muted {{ color: {TEXT_MUTED}; }}
.warn {{ color: {DANGER}; }}
.jp {{ color: {JP_GREEN}; font-weight: bold; }}
.old {{ color: {TEXT_MUTED}; }}
th {{ color: {TEXT_MUTED}; text-align: right; font-weight: normal; }}
td {{ padding: 1px 8px 1px 0; }}
li {{ margin-bottom: 2px; }}
"""

STATUS_OK = JP_GREEN
STATUS_BAD = DANGER

# Linhas de título de seção nas listas (não selecionáveis).
SECTION_FG = GOLD
SECTION_BG = NIGHT
EMPTY_FG = TEXT_MUTED


def ornament(text: str) -> str:
    """Título com os losangos dourados dos menus de FFT."""
    return f"✦ {text} ✦"


def make_crest(size: int = 256) -> QPixmap:
    """Brasão: escudo carmesim com borda dourada e uma espada."""
    pix = QPixmap(size, size)
    pix.fill(Qt.transparent)
    p = QPainter(pix)
    p.setRenderHint(QPainter.Antialiasing)
    s = size / 100.0

    shield = QPainterPath()
    shield.moveTo(50 * s, 4 * s)
    shield.lineTo(90 * s, 16 * s)
    shield.cubicTo(90 * s, 58 * s, 76 * s, 82 * s, 50 * s, 96 * s)
    shield.cubicTo(24 * s, 82 * s, 10 * s, 58 * s, 10 * s, 16 * s)
    shield.closeSubpath()

    fill = QLinearGradient(QPointF(0, 0), QPointF(0, size))
    fill.setColorAt(0, QColor(CRIMSON_LIGHT))
    fill.setColorAt(1, QColor("#4a1111"))
    p.setBrush(QBrush(fill))
    p.setPen(QPen(QColor(GOLD), 6 * s))
    p.drawPath(shield)
    p.setPen(QPen(QColor(GOLD_DIM), 1.5 * s))
    p.setBrush(Qt.NoBrush)
    inner = QPainterPath(shield)
    p.save()
    p.translate(50 * s, 50 * s)
    p.scale(0.82, 0.82)
    p.translate(-50 * s, -50 * s)
    p.drawPath(inner)
    p.restore()

    blade = QLinearGradient(QPointF(45 * s, 0), QPointF(55 * s, 0))
    blade.setColorAt(0, QColor("#f4f1e8"))
    blade.setColorAt(1, QColor("#a9a59a"))
    p.setPen(QPen(QColor("#3a2716"), 1.2 * s))
    p.setBrush(QBrush(blade))
    sword = QPainterPath()
    sword.moveTo(50 * s, 18 * s)
    sword.lineTo(54 * s, 26 * s)
    sword.lineTo(54 * s, 66 * s)
    sword.lineTo(46 * s, 66 * s)
    sword.lineTo(46 * s, 26 * s)
    sword.closeSubpath()
    p.drawPath(sword)
    p.setBrush(QColor(GOLD))
    p.drawRoundedRect(QRectF(34 * s, 64 * s, 32 * s, 6 * s), 2 * s, 2 * s)
    p.setBrush(QColor("#5c3b1e"))
    p.drawRect(QRectF(47.5 * s, 70 * s, 5 * s, 12 * s))
    p.setBrush(QColor(GOLD))
    p.drawEllipse(QPointF(50 * s, 85 * s), 4 * s, 4 * s)
    p.end()
    return pix


_HAND: dict[float, QPixmap] = {}


def make_hand_cursor(ratio: float = 2.0) -> QPixmap:
    """Mão de luva branca apontando para a direita (22x16 lógicos), a seta clássica dos menus."""
    if ratio in _HAND:
        return _HAND[ratio]
    w, h = 22, 16
    pix = QPixmap(int(w * ratio), int(h * ratio))
    pix.setDevicePixelRatio(ratio)
    pix.fill(Qt.transparent)
    p = QPainter(pix)
    p.setRenderHint(QPainter.Antialiasing)

    finger = QPainterPath()
    finger.addRoundedRect(QRectF(9, 3.5, 12, 4.2), 2.1, 2.1)
    fist = QPainterPath()
    fist.addRoundedRect(QRectF(3, 3, 10, 10.5), 3, 3)
    hand = finger.united(fist)
    for top in (7.4, 9.6, 11.6):
        knuckle = QPainterPath()
        knuckle.addRoundedRect(QRectF(9.5, top, 4.6, 2.6), 1.3, 1.3)
        hand = hand.united(knuckle)

    glove = QLinearGradient(QPointF(0, 3), QPointF(0, 14))
    glove.setColorAt(0, QColor("#ffffff"))
    glove.setColorAt(1, QColor("#c9d0de"))
    outline = QPen(QColor("#141821"), 1.1)
    p.setPen(outline)
    p.setBrush(QBrush(glove))
    p.drawPath(hand)
    p.setPen(QPen(QColor("#5d6575"), 0.8))
    for y in (9.6, 11.6):
        p.drawLine(QPointF(10.2, y), QPointF(13.4, y))

    cuff = QLinearGradient(QPointF(0, 2), QPointF(0, 14))
    cuff.setColorAt(0, QColor(GOLD_LIGHT))
    cuff.setColorAt(1, QColor(GOLD_DIM))
    p.setPen(outline)
    p.setBrush(QBrush(cuff))
    p.drawRoundedRect(QRectF(0.6, 2.4, 3.6, 11.8), 1.2, 1.2)
    p.end()
    _HAND[ratio] = pix
    return pix


class HandCursorDelegate(QStyledItemDelegate):
    """Desenha a mão-cursor à esquerda do item selecionado (o QSS reserva o espaço)."""

    def paint(self, painter, option, index) -> None:
        super().paint(painter, option, index)
        if not (option.state & QStyle.State_Selected) or not (index.flags() & Qt.ItemIsSelectable):
            return
        ratio = painter.device().devicePixelRatioF() if painter.device() else 1.0
        hand = make_hand_cursor(max(2.0, ratio))
        size = hand.deviceIndependentSize()
        x = option.rect.left() + (CURSOR_GUTTER - size.width()) / 2 - 1
        y = option.rect.center().y() - size.height() / 2 + 1
        painter.drawPixmap(QPointF(x, y), hand)


class _CursorInstaller(QObject):
    """Coloca a mão-cursor em toda QListWidget do app, inclusive nas dos diálogos."""

    def eventFilter(self, obj, event) -> bool:
        if event.type() == QEvent.Polish and isinstance(obj, QListWidget) and not obj.property("handCursor"):
            obj.setProperty("handCursor", True)
            obj.setItemDelegate(HandCursorDelegate(obj))
        return False


def _icon_images() -> dict[str, str]:
    """Setas e marca de seleção (QSS não desenha formas), salvas no cache do app."""
    from . import paths

    folder = paths.cache_dir() / "theme"
    folder.mkdir(parents=True, exist_ok=True)
    result = {}
    shapes = {
        "ARROW_UP": ((18, 12), [(0, 12), (9, 0), (18, 12)], GOLD_LIGHT, True),
        "ARROW_DOWN": ((18, 12), [(0, 0), (9, 12), (18, 0)], GOLD_LIGHT, True),
        "CHECK": ((30, 30), [(6, 16), (12, 22), (24, 8)], GOLD_LIGHT, False),
    }
    for key, ((w, h), points, color, filled) in shapes.items():
        pix = QPixmap(w, h)
        pix.fill(Qt.transparent)
        p = QPainter(pix)
        p.setRenderHint(QPainter.Antialiasing)
        path = QPainterPath()
        path.moveTo(*points[0])
        for pt in points[1:]:
            path.lineTo(*pt)
        if filled:
            path.closeSubpath()
            p.setPen(Qt.NoPen)
            p.setBrush(QColor(color))
        else:
            p.setPen(QPen(QColor(color), 4, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            p.setBrush(Qt.NoBrush)
        p.drawPath(path)
        p.end()
        target = folder / f"{key.lower()}.png"
        pix.save(str(target))
        result[key] = target.as_posix()
    return result


def apply(app: QApplication) -> None:
    font = QFont(SERIF)
    font.setFamilies([SERIF, *SERIF_FALLBACKS])
    font.setPointSizeF(10.5)
    app.setFont(font)
    app.setStyle("Fusion")  # base neutra, para o QSS valer igual em todo Windows
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(NIGHT))
    palette.setColor(QPalette.WindowText, QColor(TEXT))
    palette.setColor(QPalette.Base, QColor(PANEL_DEEP))
    palette.setColor(QPalette.AlternateBase, QColor(ROW_ALT))
    palette.setColor(QPalette.Text, QColor(TEXT))
    palette.setColor(QPalette.PlaceholderText, QColor(TEXT_DIM))
    palette.setColor(QPalette.Button, QColor(PANEL))
    palette.setColor(QPalette.ButtonText, QColor(TEXT))
    palette.setColor(QPalette.Highlight, QColor(CRIMSON))
    palette.setColor(QPalette.HighlightedText, QColor(GOLD_LIGHT))
    palette.setColor(QPalette.ToolTipBase, QColor(PANEL))
    palette.setColor(QPalette.ToolTipText, QColor(TEXT))
    palette.setColor(QPalette.Link, QColor(GOLD))
    for role in (QPalette.WindowText, QPalette.Text, QPalette.ButtonText):
        palette.setColor(QPalette.Disabled, role, QColor(TEXT_DIM))
    app.setPalette(palette)
    qss = QSS
    for key, path in _icon_images().items():
        qss = qss.replace(f"@{key}@", path)
    app.setStyleSheet(qss)
    app.setWindowIcon(QIcon(make_crest()))
    installer = _CursorInstaller(app)
    app.installEventFilter(installer)
    app._hand_cursor_installer = installer  # mantém vivo enquanto o app existir
