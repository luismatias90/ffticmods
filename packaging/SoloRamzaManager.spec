# -*- mode: python ; coding: utf-8 -*-
r"""
Build (a partir da RAIZ do projeto):

    .venv\Scripts\pyinstaller packaging\SoloRamzaManager.spec --noconfirm

Saída: dist\SoloRamzaManager\SoloRamzaManager.exe. Distribua a pasta inteira.

Onedir, não onefile: o FF16Tools.CLI.exe precisa existir como arquivo real no
disco para ser executado. O cache do jogo e as configurações ficam em
%LOCALAPPDATA%\SoloRamzaManager, nunca dentro da pasta do app.
"""

import re
from pathlib import Path

from PyInstaller.utils.win32.versioninfo import (
    FixedFileInfo, StringFileInfo, StringStruct, StringTable, VarFileInfo,
    VarStruct, VSVersionInfo,
)

ROOT = Path(SPECPATH).parent

# Metadados de versão no .exe (Propriedades > Detalhes). Um executável sem eles
# pesa contra nas heurísticas de antivírus e na checagem do Nexus Mods.
VERSION = re.search(
    r'__version__\s*=\s*"([^"]+)"',
    (ROOT / "ramza_manager" / "__init__.py").read_text(encoding="utf-8"),
).group(1)
_parts = tuple(int(p) for p in VERSION.split("."))
_vtuple = (_parts + (0, 0, 0, 0))[:4]

version_info = VSVersionInfo(
    ffi=FixedFileInfo(filevers=_vtuple, prodvers=_vtuple),
    kids=[
        StringFileInfo([StringTable("040904B0", [
            StringStruct("CompanyName", "Luis Matias"),
            StringStruct("FileDescription", "Solo Ramza Manager"),
            StringStruct("FileVersion", VERSION),
            StringStruct("InternalName", "SoloRamzaManager"),
            StringStruct("LegalCopyright", "GPL-3.0 - github.com/luismatias90/ffticmods"),
            StringStruct("OriginalFilename", "SoloRamzaManager.exe"),
            StringStruct("ProductName", "Solo Ramza Manager"),
            StringStruct("ProductVersion", VERSION),
        ])]),
        VarFileInfo([VarStruct("Translation", [0x0409, 1200])]),
    ],
)

a = Analysis(
    [str(ROOT / "SoloRamzaManager.pyw")],
    pathex=[str(ROOT)],
    datas=[
        (str(ROOT / "data"), "data"),
        (str(ROOT / "tools"), "tools"),
    ],
    excludes=["tkinter", "pytest"],
    # Módulos como .pyc soltos em _internal, sem base_library.zip: o Nexus Mods
    # põe em quarentena qualquer upload com um arquivo compactado dentro.
    noarchive=True,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="SoloRamzaManager",
    console=False,
    upx=False,
    icon=str(ROOT / "data" / "app.ico"),  # gerado por packaging/make_icon.py
    version=version_info,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    upx=False,
    name="SoloRamzaManager",
)
