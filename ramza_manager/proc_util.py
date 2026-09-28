"""
Executar ferramentas de linha de comando (FF16Tools.CLI) sem abrir janela de
console e repassando a saída linha a linha.

Adaptado de mod_studio/proc_util.py (The Ivalice Chronicles Mod Studio, GPL-3).
"""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Callable, Optional


def _no_window_flags() -> dict:
    flags = getattr(subprocess, "CREATE_NO_WINDOW", 0x08000000)
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    return {"creationflags": flags, "startupinfo": startupinfo}


def run_streaming(
    command: list[str],
    line_cb: Optional[Callable[[str], None]] = None,
    cwd: Optional[Path] = None,
) -> int:
    # stdin fechado: ferramentas .NET que pedem "press any key" falham em vez
    # de travar para sempre.
    process = subprocess.Popen(
        command,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
        bufsize=1,
        cwd=str(cwd) if cwd else None,
        **_no_window_flags(),
    )
    assert process.stdout is not None
    for line in process.stdout:
        if line_cb:
            line_cb(line.rstrip("\n"))
    process.wait()
    return process.returncode
