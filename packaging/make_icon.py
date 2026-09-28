"""Gera data/app.ico (o brasão do tema) para o .exe. Rodar da raiz do projeto."""

import sys
from pathlib import Path

from PySide6.QtGui import QGuiApplication

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from ramza_manager.theme import make_crest  # noqa: E402

app = QGuiApplication(sys.argv)
target = ROOT / "data" / "app.ico"
if not make_crest(256).save(str(target), "ICO"):
    raise SystemExit("Falha ao gerar o ícone")
print(target)
