"""
Encontrar a instalação Steam de FINAL FANTASY TACTICS - The Ivalice Chronicles
e os pacotes .pac originais da versão Enhanced.

Adaptado de mod_studio/game_install.py (The Ivalice Chronicles Mod Studio, GPL-3).
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Optional

GAME_FOLDER_NAME = "FINAL FANTASY TACTICS - The Ivalice Chronicles"
ENHANCED_EXE = "FFT_enhanced.exe"

# Pacotes gerados pelo mod loader ficam na mesma pasta dos originais. Nunca
# extrair deles, senão a "referência original" vira uma mistura com mods.
_MOD_PACK_MARKERS = ("modded", ".diff.")


def _windows_steam_roots() -> list[Path]:
    roots: list[Path] = []
    try:
        import winreg
    except ImportError:
        return roots
    for hive, subkey, value_name in (
        (winreg.HKEY_CURRENT_USER, r"Software\Valve\Steam", "SteamPath"),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Valve\Steam", "InstallPath"),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Valve\Steam", "InstallPath"),
    ):
        try:
            with winreg.OpenKey(hive, subkey) as key:
                raw, _ = winreg.QueryValueEx(key, value_name)
            if raw:
                roots.append(Path(str(raw)))
        except OSError:
            continue
    return roots


def _common_steam_roots() -> list[Path]:
    candidates: list[Path] = []
    for drive in "CDEFGHIJ":
        base = Path(f"{drive}:/")
        candidates += [
            base / "Program Files (x86)" / "Steam",
            base / "Program Files" / "Steam",
            base / "Steam",
            base / "SteamLibrary",
            base / "Games" / "Steam",
            base / "Games" / "SteamLibrary",
        ]
    return candidates


def _library_roots_from_vdf(steam_root: Path) -> list[Path]:
    vdf = steam_root / "steamapps" / "libraryfolders.vdf"
    try:
        text = vdf.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return []
    return [Path(m.replace("\\\\", "\\")) for m in re.findall(r'"path"\s+"([^"]+)"', text)]


def steam_library_roots() -> list[Path]:
    seen: set[Path] = set()
    ordered: list[Path] = []

    def add(path: Path) -> None:
        try:
            resolved = path.resolve()
        except OSError:
            return
        if resolved in seen or not resolved.is_dir():
            return
        seen.add(resolved)
        ordered.append(resolved)

    for root in _windows_steam_roots() + _common_steam_roots():
        add(root)
    for root in list(ordered):
        for extra in _library_roots_from_vdf(root):
            add(extra)
    return ordered


def looks_like_game_root(folder: Path) -> bool:
    try:
        return folder.is_dir() and (folder / ENHANCED_EXE).exists()
    except OSError:
        return False


def find_game_root() -> Optional[Path]:
    for library in steam_library_roots():
        candidate = library / "steamapps" / "common" / GAME_FOLDER_NAME
        if looks_like_game_root(candidate):
            return candidate
    return None


def enhanced_pack_dir(game_root: Path) -> Path:
    return game_root / "data" / "enhanced"


def looks_like_mod_pack(name: str) -> bool:
    lowered = name.lower()
    return any(marker in lowered for marker in _MOD_PACK_MARKERS)


def vanilla_pack_files(pack_dir: Path) -> list[Path]:
    """
    Os .pac originais, com os 0004* primeiro: é neles que ficam as tabelas
    nxd (0004.pac + um 0004.<idioma>.pac por idioma, conferido no jogo real).
    """
    try:
        packs = [
            p for p in pack_dir.iterdir()
            if p.is_file() and p.suffix.lower() == ".pac" and not looks_like_mod_pack(p.name)
        ]
    except OSError:
        return []
    packs.sort(key=lambda p: (not p.name.startswith("0004"), p.name.lower()))
    return packs
