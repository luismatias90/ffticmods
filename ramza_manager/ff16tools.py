"""
Wrapper do FF16Tools.CLI (Nenkai, MIT): extrair .nxd dos .pac e converter
.nxd <-> SQLite, abrir/fechar saves (.png).

Comandos adaptados de mod_studio/ff16tools.py (The Ivalice Chronicles Mod Studio, GPL-3).
"""

from __future__ import annotations

from pathlib import Path
from typing import Callable, Optional

from .proc_util import run_streaming

LineCb = Optional[Callable[[str], None]]


def unpack_pack(cli: Path, pack_file: Path, output_dir: Path, filter_text: str, line_cb: LineCb = None) -> int:
    """`unpack-all` de um único .pac, só os arquivos cujo caminho contém filter_text."""
    return run_streaming(
        [str(cli), "unpack-all", "-i", str(pack_file), "-o", str(output_dir), "-g", "fft",
         "--filter", filter_text],
        line_cb,
    )


def nxd_to_sqlite(cli: Path, nxd_dir: Path, sqlite_path: Path, line_cb: LineCb = None) -> int:
    return run_streaming(
        [str(cli), "nxd-to-sqlite", "-i", str(nxd_dir), "-o", str(sqlite_path), "-g", "fft"],
        line_cb,
    )


def sqlite_to_nxd(cli: Path, sqlite_path: Path, output_dir: Path, tables: list[str], line_cb: LineCb = None) -> int:
    command = [str(cli), "sqlite-to-nxd", "-i", str(sqlite_path), "-o", str(output_dir), "-g", "fft"]
    if tables:
        command += ["-t", *tables]
    return run_streaming(command, line_cb)


def unpack_save(cli: Path, save_png: Path, output_dir: Path, line_cb: LineCb = None) -> int:
    return run_streaming([str(cli), "unpack-save", "-i", str(save_png), "-o", str(output_dir)], line_cb)


def pack_save(cli: Path, input_dir: Path, save_png: Path, line_cb: LineCb = None) -> int:
    return run_streaming(
        [str(cli), "pack-save", "-i", str(input_dir), "-o", str(save_png), "-g", "fft", "-s"],
        line_cb,
    )
