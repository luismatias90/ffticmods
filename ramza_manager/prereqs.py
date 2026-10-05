"""Checagens de pré-requisitos compartilhadas pela janela principal e pelo assistente."""

from __future__ import annotations

import html
import subprocess
import sys
from pathlib import Path
from typing import Optional

from . import game_install, nxd_db, paths, reloaded, theme


def _hidden_run(args: list[str], timeout: float = 8) -> subprocess.CompletedProcess[str]:
    kwargs: dict = {"capture_output": True, "text": True, "timeout": timeout}
    if sys.platform == "win32":
        kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW
    return subprocess.run(args, **kwargs)


def dotnet9_installed() -> bool:
    for base in (Path(r"C:\Program Files\dotnet"), Path(r"C:\Program Files (x86)\dotnet")):
        shared = base / "shared" / "Microsoft.NETCore.App"
        try:
            if shared.is_dir() and any(p.name.startswith("9.") for p in shared.iterdir()):
                return True
        except OSError:
            continue
    try:
        out = _hidden_run(["dotnet", "--list-runtimes"]).stdout
    except (OSError, subprocess.TimeoutExpired):
        return False
    return any(line.startswith("Microsoft.NETCore.App 9.") for line in out.splitlines())


def _process_running(image: str) -> bool:
    try:
        out = _hidden_run(["tasklist", "/FI", f"IMAGENAME eq {image}", "/NH"]).stdout
    except (OSError, subprocess.TimeoutExpired):
        return False
    return image.lower() in out.lower()


def reloaded_running() -> bool:
    return _process_running("Reloaded-II.exe")


def game_running() -> bool:
    """O jogo grava o save ao fechar; editar com ele aberto perde a edição."""
    return _process_running("FFT_enhanced.exe")


def status_html(ok: bool, text: str) -> str:
    color = theme.STATUS_OK if ok else theme.STATUS_BAD
    mark = "✔" if ok else "✘"
    return f'<span style="color:{color}">{mark}</span> {html.escape(text)}'


def resolve_game(game_root: str) -> Optional[Path]:
    if not game_root:
        return None
    folder = Path(game_root)
    return folder if game_install.looks_like_game_root(folder) else None


def resolve_reloaded(reloaded_root: str) -> Optional[Path]:
    if not reloaded_root:
        return None
    folder = Path(reloaded_root)
    return folder if reloaded.looks_like_reloaded_install(folder) else None


def modloader_installed(reloaded_root: Optional[Path]) -> bool:
    return bool(reloaded_root and reloaded.is_mod_installed(reloaded_root, reloaded.MODLOADER_ID))


def game_added_to_reloaded(reloaded_root: Optional[Path]) -> bool:
    return bool(reloaded_root and reloaded.find_app_config(reloaded_root))


def data_ready() -> bool:
    return nxd_db.is_valid_db(paths.vanilla_sqlite())
