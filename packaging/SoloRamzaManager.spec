# -*- mode: python ; coding: utf-8 -*-
r"""
Build (a partir da RAIZ do projeto):

    .venv\Scripts\pyinstaller packaging\SoloRamzaManager.spec --noconfirm

Saída: dist\SoloRamzaManager\SoloRamzaManager.exe. Distribua a pasta inteira.

Onedir, não onefile: o FF16Tools.CLI.exe precisa existir como arquivo real no
disco para ser executado. O cache do jogo e as configurações ficam em
%LOCALAPPDATA%\SoloRamzaManager, nunca dentro da pasta do app.
"""

from pathlib import Path

ROOT = Path(SPECPATH).parent

a = Analysis(
    [str(ROOT / "SoloRamzaManager.pyw")],
    pathex=[str(ROOT)],
    datas=[
        (str(ROOT / "data"), "data"),
        (str(ROOT / "tools"), "tools"),
    ],
    excludes=["tkinter", "pytest"],
    noarchive=False,
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
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    upx=False,
    name="SoloRamzaManager",
)
