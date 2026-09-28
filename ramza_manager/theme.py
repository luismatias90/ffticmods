"""
Identidade visual inspirada nos menus de Final Fantasy Tactics: moldura de
madeira escura, painéis de pergaminho com texto em tinta, detalhes em ouro e
carmesim. Só estilo (QSS + fontes do Windows) e um brasão desenhado em
código; nenhuma arte do jogo é usada.
"""

from __future__ import annotations

from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import (
    QBrush, QColor, QFont, QIcon, QLinearGradient, QPainter, QPainterPath, QPalette, QPen, QPixmap,
)
from PySide6.QtWidgets import QApplication

# Paleta
WOOD_DARK = "#17110b"
WOOD = "#241a11"
WOOD_LIGHT = "#3a2a1a"
PARCHMENT = "#efe3c4"
PARCHMENT_ALT = "#e5d4ad"
PARCHMENT_DARK = "#d6c192"
INK = "#3a2716"
INK_MUTED = "#76593a"
GOLD = "#d4af5a"
GOLD_DARK = "#a3802f"
GOLD_LIGHT = "#f0d68e"
CRIMSON = "#8e2626"
CRIMSON_LIGHT = "#ad3434"
MOSS = "#4d7a2a"
TEXT_ON_WOOD = "#eadcb8"

SERIF = "Palatino Linotype"
SERIF_FALLBACKS = ["Book Antiqua", "Georgia", "Times New Roman"]

QSS = f"""
* {{
    font-family: "{SERIF}", "Book Antiqua", Georgia, serif;
    font-size: 10.5pt;
}}
QMainWindow, QDialog, QMessageBox {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 {WOOD}, stop:1 {WOOD_DARK});
}}
QLabel {{ color: {TEXT_ON_WOOD}; background: transparent; }}
QToolTip {{
    color: {INK}; background: {PARCHMENT}; border: 1px solid {GOLD_DARK}; padding: 4px;
}}

/* ---- Cabeçalho ---- */
#Banner {{
    border: 2px solid {GOLD_DARK};
    border-radius: 6px;
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #2b0f0f, stop:0.5 {CRIMSON}, stop:1 #2b0f0f);
}}
#BannerTitle {{
    color: {GOLD_LIGHT}; font-size: 22pt; font-weight: bold; letter-spacing: 3px;
}}
#BannerSubtitle {{ color: {PARCHMENT}; font-size: 10pt; font-style: italic; }}

/* ---- Grupos (painéis de pergaminho) ---- */
QGroupBox {{
    background: {PARCHMENT};
    border: 2px solid {GOLD_DARK};
    border-radius: 6px;
    margin-top: 14px;
    padding: 12px 10px 8px 10px;
}}
QGroupBox::title {{
    subcontrol-origin: margin; left: 14px; padding: 1px 10px;
    color: {GOLD_LIGHT}; background: {WOOD_LIGHT};
    border: 1px solid {GOLD_DARK}; border-radius: 4px;
    font-weight: bold; letter-spacing: 1px;
}}
QGroupBox QLabel {{ color: {INK}; }}

/* ---- Abas ---- */
QTabWidget::pane {{
    background: {PARCHMENT};
    border: 2px solid {GOLD_DARK};
    border-radius: 6px;
    top: -2px;
}}
QTabWidget QLabel {{ color: {INK}; }}
QTabBar::tab {{
    background: {WOOD_LIGHT}; color: {PARCHMENT_DARK};
    border: 1px solid {GOLD_DARK}; border-bottom: none;
    border-top-left-radius: 6px; border-top-right-radius: 6px;
    padding: 6px 16px; margin-right: 3px; font-weight: bold;
}}
QTabBar::tab:selected {{ background: {PARCHMENT}; color: {CRIMSON}; }}
QTabBar::tab:hover:!selected {{ background: #4a3622; color: {GOLD_LIGHT}; }}
QTabWidget#SubTabs::pane {{ background: {PARCHMENT_ALT}; border: 1px solid {GOLD_DARK}; }}
QTabWidget#SubTabs QTabBar::tab {{ padding: 4px 12px; font-weight: normal; }}
QTabWidget#SubTabs QTabBar::tab:selected {{ background: {PARCHMENT_ALT}; }}

/* ---- Botões ---- */
QPushButton {{
    color: {INK};
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #f6ecd2, stop:1 {PARCHMENT_DARK});
    border: 1px solid {GOLD_DARK}; border-radius: 5px;
    padding: 5px 14px;
}}
QPushButton:hover {{ border: 1px solid {GOLD}; background: #fbf3de; }}
QPushButton:pressed {{ background: {PARCHMENT_DARK}; }}
QPushButton:disabled {{ color: #9c8a6a; }}
QPushButton#Primary {{
    color: {GOLD_LIGHT}; font-weight: bold; font-size: 12pt; letter-spacing: 1px;
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 {CRIMSON_LIGHT}, stop:1 #5e1616);
    border: 2px solid {GOLD}; padding: 8px 26px;
}}
QPushButton#Primary:hover {{ background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #c24040, stop:1 {CRIMSON}); }}
QPushButton#Secondary {{
    color: {PARCHMENT}; background: {WOOD_LIGHT}; border: 1px solid {GOLD_DARK}; padding: 8px 18px;
}}
QPushButton#Secondary:hover {{ background: #4a3622; color: {GOLD_LIGHT}; }}

/* ---- Campos ---- */
QLineEdit, QSpinBox {{
    color: {INK}; background: #fbf5e4;
    border: 1px solid {GOLD_DARK}; border-radius: 4px; padding: 4px 6px;
    selection-background-color: {GOLD}; selection-color: {INK};
}}
QLineEdit:focus, QSpinBox:focus {{ border: 1px solid {CRIMSON}; }}
QSpinBox {{ padding-right: 18px; }}
QSpinBox::up-button, QSpinBox::down-button {{
    subcontrol-origin: border; width: 18px;
    background: {PARCHMENT_DARK}; border-left: 1px solid {GOLD_DARK};
}}
QSpinBox::up-button {{ subcontrol-position: top right; border-top-right-radius: 4px; }}
QSpinBox::down-button {{ subcontrol-position: bottom right; border-bottom-right-radius: 4px; }}
QSpinBox::up-button:hover, QSpinBox::down-button:hover {{ background: {GOLD}; }}
QSpinBox::up-arrow {{ image: url("@ARROW_UP@"); width: 9px; height: 6px; }}
QSpinBox::down-arrow {{ image: url("@ARROW_DOWN@"); width: 9px; height: 6px; }}

QCheckBox {{ color: {INK}; font-weight: bold; spacing: 8px; }}
QCheckBox::indicator {{
    width: 16px; height: 16px; border: 2px solid {GOLD_DARK}; border-radius: 3px; background: #fbf5e4;
}}
QCheckBox::indicator:checked {{ background: {CRIMSON}; border: 2px solid {GOLD}; }}

/* ---- Listas, tabela, prévia ---- */
QListWidget, QTableWidget, QTextBrowser {{
    color: {INK}; background: #f7eed6;
    border: 1px solid {GOLD_DARK}; border-radius: 4px;
    alternate-background-color: {PARCHMENT_ALT};
    outline: none;
}}
QListWidget::item {{ padding: 5px 8px; border-bottom: 1px solid #e2d2ab; }}
QListWidget::item:hover {{ background: #efe0b8; }}
QListWidget::item:selected {{
    color: {PARCHMENT}; background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {CRIMSON}, stop:1 #6d1c1c);
    border-left: 4px solid {GOLD};
}}
QTableWidget {{ gridline-color: #dcc9a0; }}
QTableWidget::item:selected {{ color: {PARCHMENT}; background: {CRIMSON}; }}
QHeaderView::section {{
    color: {GOLD_LIGHT}; background: {WOOD_LIGHT};
    border: none; border-right: 1px solid {GOLD_DARK}; padding: 5px; font-weight: bold;
}}
QTableCornerButton::section {{ background: {WOOD_LIGHT}; }}

/* ---- Log ---- */
QPlainTextEdit {{
    color: {PARCHMENT_DARK}; background: #120d08;
    border: 1px solid {GOLD_DARK}; border-radius: 4px;
    font-family: Consolas, monospace; font-size: 9pt;
}}

/* ---- Rolagem e divisores ---- */
QScrollBar:vertical {{ background: {PARCHMENT_ALT}; width: 12px; margin: 0; border: none; }}
QScrollBar::handle:vertical {{ background: {GOLD_DARK}; border-radius: 5px; min-height: 28px; margin: 2px; }}
QScrollBar::handle:vertical:hover {{ background: {GOLD}; }}
QScrollBar:horizontal {{ background: {PARCHMENT_ALT}; height: 12px; border: none; }}
QScrollBar::handle:horizontal {{ background: {GOLD_DARK}; border-radius: 5px; min-width: 28px; margin: 2px; }}
QScrollBar::add-line, QScrollBar::sub-line {{ width: 0; height: 0; }}
QScrollBar::add-page, QScrollBar::sub-page {{ background: none; }}
QSplitter::handle {{ background: transparent; width: 8px; }}

QComboBox {{
    color: {INK}; background: #fbf5e4;
    border: 1px solid {GOLD_DARK}; border-radius: 4px; padding: 3px 8px;
}}
QComboBox:hover {{ border: 1px solid {GOLD}; }}
QComboBox QAbstractItemView {{
    color: {INK}; background: {PARCHMENT};
    selection-background-color: {CRIMSON}; selection-color: {PARCHMENT};
}}

QFrame#WizardBody {{
    background: {PARCHMENT};
    border: 2px solid {GOLD_DARK};
    border-radius: 6px;
}}
QFrame#WizardBody QLabel {{ color: {INK}; }}
QScrollArea {{ background: transparent; border: none; }}

QPushButton#Step {{
    text-align: left; color: {PARCHMENT}; background: transparent;
    border: none; border-left: 3px solid transparent;
    padding: 7px 8px; font-weight: normal;
}}
QPushButton#Step:checked {{
    color: {GOLD_LIGHT}; background: {WOOD_LIGHT};
    border-left: 3px solid {GOLD}; font-weight: bold;
}}
QPushButton#Step:hover:!checked {{ color: {GOLD_LIGHT}; }}
QPushButton#Step:disabled {{ color: #6d5a40; }}
QPushButton#LangChoice {{
    font-size: 13pt; padding: 14px 18px; text-align: left;
}}
QPushButton#LangChoice:checked {{
    color: {GOLD_LIGHT}; font-weight: bold;
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 {CRIMSON_LIGHT}, stop:1 #5e1616);
    border: 2px solid {GOLD};
}}

QMessageBox QLabel {{ color: {TEXT_ON_WOOD}; font-size: 11pt; }}
QMessageBox QPushButton {{ min-width: 80px; }}
"""

# CSS do painel de prévia (QTextBrowser usa um subconjunto de HTML/CSS).
PREVIEW_CSS = f"""
body {{ color: {INK}; font-family: "{SERIF}", Georgia, serif; font-size: 10.5pt; }}
h2 {{ color: {CRIMSON}; font-size: 18pt; margin-bottom: 2px; }}
h3 {{ color: {INK}; font-size: 12pt; margin-top: 14px; margin-bottom: 4px;
      border-bottom: 1px solid {GOLD_DARK}; }}
.muted {{ color: {INK_MUTED}; }}
.warn {{ color: {CRIMSON}; }}
.jp {{ color: {MOSS}; font-weight: bold; }}
.old {{ color: {INK_MUTED}; }}
th {{ color: {INK_MUTED}; text-align: right; font-weight: normal; }}
td {{ padding: 1px 8px 1px 0; }}
"""

STATUS_OK = MOSS
STATUS_BAD = CRIMSON


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
    p.setPen(QPen(QColor(GOLD_DARK), 1.5 * s))
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


def _arrow_images() -> tuple[str, str]:
    """Setas dos campos numéricos (QSS não desenha triângulos), salvas no cache do app."""
    from . import paths

    folder = paths.cache_dir() / "theme"
    folder.mkdir(parents=True, exist_ok=True)
    result = []
    for name, points in (
        ("arrow_up.png", [(0, 12), (9, 0), (18, 12)]),
        ("arrow_down.png", [(0, 0), (9, 12), (18, 0)]),
    ):
        pix = QPixmap(18, 12)
        pix.fill(Qt.transparent)
        p = QPainter(pix)
        p.setRenderHint(QPainter.Antialiasing)
        p.setPen(Qt.NoPen)
        p.setBrush(QColor(INK))
        path = QPainterPath()
        path.moveTo(*points[0])
        for pt in points[1:]:
            path.lineTo(*pt)
        path.closeSubpath()
        p.drawPath(path)
        p.end()
        target = folder / name
        pix.save(str(target))
        result.append(target.as_posix())
    return result[0], result[1]


def apply(app: QApplication) -> None:
    font = QFont(SERIF)
    font.setFamilies([SERIF, *SERIF_FALLBACKS])
    font.setPointSizeF(10.5)
    app.setFont(font)
    app.setStyle("Fusion")  # base neutra, para o QSS valer igual em todo Windows
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(WOOD))
    palette.setColor(QPalette.WindowText, QColor(TEXT_ON_WOOD))
    palette.setColor(QPalette.Base, QColor("#f7eed6"))
    palette.setColor(QPalette.AlternateBase, QColor(PARCHMENT_ALT))
    palette.setColor(QPalette.Text, QColor(INK))
    palette.setColor(QPalette.Button, QColor(PARCHMENT))
    palette.setColor(QPalette.ButtonText, QColor(INK))
    palette.setColor(QPalette.Highlight, QColor(CRIMSON))
    palette.setColor(QPalette.HighlightedText, QColor(PARCHMENT))
    palette.setColor(QPalette.ToolTipBase, QColor(PARCHMENT))
    palette.setColor(QPalette.ToolTipText, QColor(INK))
    app.setPalette(palette)
    up, down = _arrow_images()
    app.setStyleSheet(QSS.replace("@ARROW_UP@", up).replace("@ARROW_DOWN@", down))
    app.setWindowIcon(QIcon(make_crest()))
