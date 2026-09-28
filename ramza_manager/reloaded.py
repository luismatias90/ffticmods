"""
Detectar o Reloaded-II, achar a pasta Mods e ativar/desativar o mod no perfil
do FFT_enhanced.exe.

Detecção adaptada de mod_studio/reloaded.py (The Ivalice Chronicles Mod Studio, GPL-3).
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Optional

MODLOADER_ID = "fftivc.utility.modloader"
ENHANCED_APP_ID = "fft_enhanced.exe"

_INSTALL_MARKERS = ["Reloaded-II.exe", "Reloaded-II32.exe", "Loader"]


def looks_like_reloaded_install(folder: Path) -> bool:
    if not folder.is_dir():
        return False
    return any((folder / marker).exists() for marker in _INSTALL_MARKERS)


def _launcher_config_path() -> Optional[Path]:
    appdata = os.environ.get("APPDATA")
    if not appdata:
        return None
    candidate = Path(appdata) / "Reloaded-Mod-Loader-II" / "ReloadedII.json"
    return candidate if candidate.is_file() else None


def _read_launcher_config() -> Optional[dict]:
    path = _launcher_config_path()
    if path is None:
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8-sig", errors="replace"))
    except (OSError, ValueError):
        return None


def find_installed_reloaded() -> Optional[Path]:
    config = _read_launcher_config()
    if config and config.get("LauncherPath"):
        root = Path(str(config["LauncherPath"])).parent
        if looks_like_reloaded_install(root):
            return root
    home = Path.home()
    common = [
        home / "Desktop" / "Reloaded-II",
        home / "Reloaded-II",
        home / "Downloads" / "Reloaded-II",
        home / "Documents" / "Reloaded-II",
    ]
    for drive in "CDEFGH":
        common += [Path(f"{drive}:/Reloaded-II"), Path(f"{drive}:/Games/Reloaded-II")]
    for candidate in common:
        if looks_like_reloaded_install(candidate):
            return candidate
    return None


def _configured_dir(key: str, portable_subdir: str) -> Optional[Path]:
    config = _read_launcher_config()
    if not config:
        return None
    if config.get("UsePortableMode"):
        launcher = config.get("LauncherPath")
        return Path(str(launcher)).parent / portable_subdir if launcher else None
    configured = config.get(key)
    return Path(str(configured)) if configured else None


def mods_folder(reloaded_root: Path) -> Path:
    """Onde o Reloaded-II realmente carrega os mods (respeita ModConfigDirectory)."""
    folder = _configured_dir("ModConfigDirectory", "Mods") or reloaded_root / "Mods"
    folder.mkdir(parents=True, exist_ok=True)
    return folder


def apps_folder(reloaded_root: Path) -> Path:
    return _configured_dir("ApplicationConfigDirectory", "Apps") or reloaded_root / "Apps"


def is_mod_installed(reloaded_root: Path, mod_id: str) -> bool:
    folder = mods_folder(reloaded_root)
    try:
        children = list(folder.iterdir())
    except OSError:
        return False
    for child in children:
        config = child / "ModConfig.json"
        try:
            data = json.loads(config.read_text(encoding="utf-8-sig"))
        except (OSError, ValueError):
            continue
        if str(data.get("ModId", "")).lower() == mod_id.lower():
            return True
    return False


def find_app_config(reloaded_root: Path, app_id: str = ENHANCED_APP_ID) -> Optional[Path]:
    """O AppConfig.json do jogo no Reloaded-II (existe depois que você adiciona o jogo lá)."""
    folder = apps_folder(reloaded_root)
    try:
        children = list(folder.iterdir())
    except OSError:
        return None
    for child in children:
        config = child / "AppConfig.json"
        try:
            data = json.loads(config.read_text(encoding="utf-8-sig"))
        except (OSError, ValueError):
            continue
        if str(data.get("AppId", "")).lower() == app_id:
            return config
    return None


def set_mod_enabled(reloaded_root: Path, mod_id: str, enabled: bool) -> bool:
    """
    Liga/desliga o mod (e o modloader, quando ligando) no perfil do jogo.
    Retorna False se o jogo ainda não foi adicionado ao Reloaded-II.
    O Reloaded-II deve estar fechado, senão ele sobrescreve a mudança.
    """
    config_path = find_app_config(reloaded_root)
    if config_path is None:
        return False
    data = json.loads(config_path.read_text(encoding="utf-8-sig"))
    mods = [m for m in (data.get("EnabledMods") or []) if str(m).lower() != mod_id.lower()]
    if enabled:
        if not any(str(m).lower() == MODLOADER_ID for m in mods):
            mods.insert(0, MODLOADER_ID)
        mods.append(mod_id)
    data["EnabledMods"] = mods
    config_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return True
