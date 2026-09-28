"""
Onde ficam os arquivos do app.

Dois lugares diferentes, de propósito:
- bundled_root(): arquivos que vêm junto com o app (data/, tools/). Em build
  PyInstaller é sys._MEIPASS; rodando do código-fonte é a raiz do projeto.
- user_data_dir(): cache do jogo extraído e configurações do usuário, em
  %LOCALAPPDATA%/SoloRamzaManager. Nunca dentro da pasta do app, para que
  atualizar/apagar o app não perca nada e o build não carregue dados de uma
  máquina específica.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

APP_NAME = "SoloRamzaManager"


def bundled_root() -> Path:
    meipass = getattr(sys, "_MEIPASS", None)
    if meipass:
        return Path(meipass)
    return Path(__file__).resolve().parent.parent


def data_dir() -> Path:
    return bundled_root() / "data"


def ff16tools_cli() -> Path:
    return bundled_root() / "tools" / "FF16Tools" / "win-x64" / "FF16Tools.CLI.exe"


def user_data_dir() -> Path:
    base = os.environ.get("LOCALAPPDATA")
    root = Path(base) if base else Path.home() / "AppData" / "Local"
    d = root / APP_NAME
    d.mkdir(parents=True, exist_ok=True)
    return d


def cache_dir() -> Path:
    d = user_data_dir() / "cache"
    d.mkdir(parents=True, exist_ok=True)
    return d


def vanilla_sqlite() -> Path:
    """Banco SQLite com as tabelas nxd originais do jogo (nunca é editado)."""
    return cache_dir() / "vanilla.sqlite"


def settings_file() -> Path:
    return user_data_dir() / "settings.json"


def classes_dir() -> Path:
    """Biblioteca de classes customizadas (*.ramzaclass.json)."""
    d = user_data_dir() / "classes"
    d.mkdir(parents=True, exist_ok=True)
    return d
