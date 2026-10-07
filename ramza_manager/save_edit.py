"""
Edição dos saves manuais da versão Enhanced: nível (com os atributos), JP,
Bravura e Fé do Ramza e itens somados ao inventário.

O save do Steam é um PNG (`enhanced.png`) com um chunk próprio `ffTo` que
guarda os dados criptografados. O FF16Tools.CLI (`unpack-save`/`pack-save`)
abre e fecha esse chunk; o resto do PNG (a miniatura) fica como está, porque
o `pack-save` gera uma imagem em branco no lugar.

Formato do `fftsave.bin` (mapeado comparando saves; mesmo layout de unidade
do PSX, com itens e habilidades em 16 bits):

  0x00  u32 tamanho do cabeçalho (0x10)
  0x04  u32 CRC32 de tudo a partir de 0x10
  0x10  50 slots de SLOT_SIZE bytes; slot usado começa com b"SC"
        slot+0x04  título em Shift-JIS largo ("FFT FILE01 00:17:23")
        slot+0x44  u32 data/hora (Unix)
        slot+0x518 54 unidades, UNIT_SIZE bytes cada (Ramza é a 1ª)
          +0x00 conjunto de sprite (Ramza: 1, 2 ou 3)  +0x01 id (Ramza: 0)
          +0x02 job  +0x1C EXP  +0x1D nível  +0x1E Bravura  +0x1F Fé
          +0x20 HP, +0x23 MP, +0x26 Speed, +0x29 PA, +0x2C MA: valores "raw"
                de 24 bits (ver stat_sim; o exibido sai do Multiplier da classe)
          +0x80 JP atual de cada job (u16); o índice 0 é a classe própria da
                unidade, que no Ramza são os Jobs 1-3 trocados pelo mod.
        slot+0x83A8 inventário: 1 byte (quantidade) por id de item, 0-260.
                    Conferido comprando 3 Potion (240) e 2 Clothing (186).
"""

from __future__ import annotations

import ctypes
import datetime
import os
import shutil
import struct
import unicodedata
import zlib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Mapping, Optional

from . import ff16tools, i18n, stat_sim

SAVE_FOLDER = Path("My Games") / "FINAL FANTASY TACTICS - The Ivalice Chronicles" / "Steam"
SAVE_FILE = "enhanced.png"
SAVE_BIN = "fftsave.bin"
SAVE_CHUNK = b"ffTo"

HEADER_SIZE = 0x10
SLOT_SIZE = 0x9CE4
SLOT_MAGIC = b"SC"
SLOT_TITLE = slice(0x04, 0x40)
SLOT_TIME = 0x44
UNIT_START = 0x518
UNIT_SIZE = 0x258
UNIT_COUNT = 54
INVENTORY = UNIT_START + UNIT_COUNT * UNIT_SIZE  # 0x83A8
ITEM_COUNT = 261
MAX_QUANTITY = 99
RAMZA_SPRITES = (1, 2, 3)
RAMZA_UNIT_ID = 0

EXP, LEVEL, BRAVE, FAITH, JP = 0x1C, 0x1D, 0x1E, 0x1F, 0x80
RAW_STATS = {"HP": 0x20, "MP": 0x23, "Speed": 0x26, "PA": 0x29, "MA": 0x2C}
RAW_SIZE = 3
MAX_JP = 9999
MAX_STAT = 100

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


class SaveError(RuntimeError):
    pass


@dataclass
class BagItem:
    item_id: int
    quantity: int


@dataclass
class RamzaStats:
    level: int
    brave: int
    faith: int
    jp: int
    job: int = 0
    raw: dict[str, int] = field(default_factory=dict)  # atributo -> valor raw


@dataclass
class SlotInfo:
    index: int  # 0-based
    title: str
    saved_at: Optional[datetime.datetime]
    ramza: Optional[RamzaStats]  # None = não achou o Ramza no slot
    inventory: bytes = b""  # quantidade por id de item


# ---------------------------------------------------------------------------
# Onde ficam os saves
# ---------------------------------------------------------------------------

def _documents_dir() -> Path:
    """Pasta Documentos de verdade (pode ter sido movida, ex.: OneDrive)."""
    try:
        buf = ctypes.create_unicode_buffer(260)
        if ctypes.windll.shell32.SHGetFolderPathW(None, 5, None, 0, buf) == 0 and buf.value:  # CSIDL_PERSONAL
            return Path(buf.value)
    except (AttributeError, OSError):
        pass
    return Path(os.environ.get("USERPROFILE") or Path.home()) / "Documents"


def find_save_files() -> list[Path]:
    """Os `enhanced.png` de cada conta Steam, o mais recente primeiro."""
    root = _documents_dir() / SAVE_FOLDER
    try:
        found = [p for p in root.glob(f"*/{SAVE_FILE}") if p.is_file()]
    except OSError:
        return []
    return sorted(found, key=lambda p: p.stat().st_mtime, reverse=True)


# ---------------------------------------------------------------------------
# fftsave.bin
# ---------------------------------------------------------------------------

def slot_count(data: bytes) -> int:
    return max(0, (len(data) - HEADER_SIZE) // SLOT_SIZE)


def _slot_base(index: int) -> int:
    return HEADER_SIZE + index * SLOT_SIZE


def _ramza_offset(data: bytes, index: int) -> Optional[int]:
    base = _slot_base(index) + UNIT_START
    for offset in range(base, base + UNIT_COUNT * UNIT_SIZE, UNIT_SIZE):
        if data[offset + 1] == RAMZA_UNIT_ID and data[offset] in RAMZA_SPRITES:
            return offset
    return None


def _read_raw(data: bytes, pos: int) -> int:
    return int.from_bytes(data[pos:pos + RAW_SIZE], "little")


def parse_slots(data: bytes) -> list[SlotInfo]:
    """Slots usados do `fftsave.bin`."""
    slots = []
    for index in range(slot_count(data)):
        base = _slot_base(index)
        slot = data[base:base + SLOT_SIZE]
        if not slot.startswith(SLOT_MAGIC):
            continue
        raw = slot[SLOT_TITLE].split(b"\0")[0]
        title = unicodedata.normalize("NFKC", raw.decode("cp932", errors="replace")).strip()
        stamp = struct.unpack_from("<I", slot, SLOT_TIME)[0]
        try:
            saved_at = datetime.datetime.fromtimestamp(stamp) if stamp else None
        except (OverflowError, OSError, ValueError):
            saved_at = None
        ramza = None
        offset = _ramza_offset(data, index)
        if offset is not None:
            ramza = RamzaStats(
                level=data[offset + LEVEL], brave=data[offset + BRAVE], faith=data[offset + FAITH],
                jp=struct.unpack_from("<H", data, offset + JP)[0], job=data[offset + 2],
                raw={stat: _read_raw(data, offset + pos) for stat, pos in RAW_STATS.items()},
            )
        inventory = slot[INVENTORY:INVENTORY + ITEM_COUNT]
        slots.append(SlotInfo(index, title, saved_at, ramza, inventory))
    return slots


def update_checksum(data: bytearray) -> None:
    struct.pack_into("<I", data, 4, zlib.crc32(data[HEADER_SIZE:]))


def merge_items(items: Iterable[BagItem], valid_ids: Optional[Iterable[int]] = None) -> list[BagItem]:
    """Junta ids repetidos e descarta ids inválidos e quantidades <= 0."""
    valid = set(valid_ids) if valid_ids is not None else set(range(ITEM_COUNT))
    merged: dict[int, int] = {}
    for entry in items:
        if 0 <= entry.item_id < ITEM_COUNT and entry.item_id in valid and entry.quantity > 0:
            merged[entry.item_id] = merged.get(entry.item_id, 0) + entry.quantity
    return [BagItem(i, q) for i, q in merged.items()]


def edit_slot(
    data: bytes, index: int, jp: int, brave: int, faith: int, items: Iterable[BagItem] = (),
    level: Optional[int] = None, growths: Mapping[str, int] = {}, from_scratch: bool = False,
) -> bytes:
    """
    Novo `fftsave.bin` com JP/Bravura/Fé do Ramza trocados no slot `index` e
    `items` somados ao inventário (até MAX_QUANTITY por item).

    Com `level`, o Ramza vai para esse nível (EXP zerado) e cada atributo de
    `growths` acompanha o Growth da classe (ver stat_sim.relevel);
    `from_scratch` recalcula os atributos desde o nível 1.
    """
    base = _slot_base(index)
    if not 0 <= index < slot_count(data) or data[base:base + len(SLOT_MAGIC)] != SLOT_MAGIC:
        raise SaveError(i18n.t("save_err_slot", n=index + 1))
    offset = _ramza_offset(data, index)
    if offset is None:
        raise SaveError(i18n.t("save_err_no_ramza", n=index + 1))
    out = bytearray(data)
    out[offset + BRAVE] = max(0, min(MAX_STAT, brave))
    out[offset + FAITH] = max(0, min(MAX_STAT, faith))
    struct.pack_into("<H", out, offset + JP, max(0, min(MAX_JP, jp)))
    if level is not None:
        old_level = out[offset + LEVEL]
        new_level = max(stat_sim.MIN_LEVEL, min(stat_sim.MAX_LEVEL, level))
        if new_level != old_level or from_scratch:
            for stat, growth in growths.items():
                pos = offset + RAW_STATS[stat]
                raw = stat_sim.relevel(stat, _read_raw(out, pos), growth, old_level, new_level, from_scratch)
                out[pos:pos + RAW_SIZE] = raw.to_bytes(RAW_SIZE, "little")
            out[offset + LEVEL] = new_level
            out[offset + EXP] = 0
    for entry in merge_items(items):
        pos = base + INVENTORY + entry.item_id
        out[pos] = max(out[pos], min(MAX_QUANTITY, out[pos] + entry.quantity))
    update_checksum(out)
    return bytes(out)


# ---------------------------------------------------------------------------
# PNG
# ---------------------------------------------------------------------------

def _chunks(png: bytes) -> list[tuple[bytes, bytes]]:
    if not png.startswith(PNG_SIGNATURE):
        raise SaveError(i18n.t("save_err_png"))
    chunks, pos = [], len(PNG_SIGNATURE)
    while pos + 12 <= len(png):
        length, kind = struct.unpack_from(">I4s", png, pos)
        chunks.append((kind, png[pos + 8:pos + 8 + length]))
        pos += 12 + length
        if kind == b"IEND":
            break
    return chunks


def _chunk_bytes(kind: bytes, body: bytes) -> bytes:
    return struct.pack(">I", len(body)) + kind + body + struct.pack(">I", zlib.crc32(kind + body))


def replace_save_chunk(original_png: bytes, packed_png: bytes) -> bytes:
    """O PNG original (com a miniatura) levando o chunk de dados de `packed_png`."""
    new_body = next((body for kind, body in _chunks(packed_png) if kind == SAVE_CHUNK), None)
    if new_body is None:
        raise SaveError(i18n.t("save_err_png"))
    out, replaced = [PNG_SIGNATURE], False
    for kind, body in _chunks(original_png):
        if kind == SAVE_CHUNK:
            body, replaced = new_body, True
        out.append(_chunk_bytes(kind, body))
    if not replaced:
        raise SaveError(i18n.t("save_err_png"))
    return b"".join(out)


# ---------------------------------------------------------------------------
# Ler e gravar o save
# ---------------------------------------------------------------------------

def _unpack(cli: Path, png: Path, out_dir: Path) -> bytes:
    shutil.rmtree(out_dir, ignore_errors=True)
    out_dir.mkdir(parents=True)
    if ff16tools.unpack_save(cli, png, out_dir) != 0 or not (out_dir / SAVE_BIN).exists():
        raise SaveError(i18n.t("save_err_unpack", name=png.name))
    return (out_dir / SAVE_BIN).read_bytes()


def read_save(cli: Path, png: Path, work_dir: Path) -> list[SlotInfo]:
    return parse_slots(_unpack(cli, png, work_dir / "read"))


def write_slot(
    cli: Path, png: Path, work_dir: Path, backup_dir: Path,
    index: int, jp: int, brave: int, faith: int, items: Iterable[BagItem] = (),
    level: Optional[int] = None, growths: Mapping[str, int] = {}, from_scratch: bool = False,
) -> Path:
    """
    Grava a edição (ver edit_slot) no slot `index` de `png` e devolve o backup
    do arquivo original. O resultado é aberto de novo e conferido byte a byte
    antes de substituir o save.
    """
    shutil.rmtree(work_dir, ignore_errors=True)
    edited = edit_slot(_unpack(cli, png, work_dir / "in"), index, jp, brave, faith, items,
                       level, growths, from_scratch)

    stage = work_dir / "stage"
    stage.mkdir(parents=True)
    (stage / SAVE_BIN).write_bytes(edited)
    packed = work_dir / "packed.png"
    if ff16tools.pack_save(cli, stage, packed) != 0 or not packed.exists():
        raise SaveError(i18n.t("save_err_pack"))

    original = png.read_bytes()
    result = work_dir / SAVE_FILE
    result.write_bytes(replace_save_chunk(original, packed.read_bytes()))
    if _unpack(cli, result, work_dir / "check") != edited:
        raise SaveError(i18n.t("save_err_verify"))

    backup_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = backup_dir / f"{png.parent.name}_{png.stem}_{stamp}.png"
    shutil.copy2(png, backup)
    tmp = png.with_name(png.name + ".tmp")
    shutil.copy(result, tmp)
    os.replace(tmp, png)
    shutil.rmtree(work_dir, ignore_errors=True)
    return backup
