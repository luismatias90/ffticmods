"""
Sprites de batalha que podem substituir o do Ramza.

O Ramza não usa o sprite da classe: o jogo desenha as folhas próprias dele
(capítulo 1, capítulos 2–3 e capítulo 4). Retrato do menu e algumas cenas de
evento usam outros arquivos e continuam com o Ramza original.

Cada folha existe duas vezes no jogo:
- clássica, no fftpack (battle_<stem>_spr.bin): paleta de cores + pixels de 256 px;
- HD, no system/ffto/g2d.dat: o desenho que o modo Enhanced mostra em batalha,
  em duas texturas seguidas (metade de cima e metade de baixo da folha).
O mod troca as duas, senão o Enhanced continua desenhando o Ramza.

Só entram folhas humanas com as duas metades HD: monstro tem outra grade de
animação e trava com os movimentos do Ramza. Duplicatas idênticas ficam de fora.
"""

from __future__ import annotations

import json
import re
import shutil
import sqlite3
import struct
import zlib
from dataclasses import dataclass, field
from pathlib import Path

from . import ff16tools, game_install, i18n, paths

CATEGORY_UNIQUE = "unique"
CATEGORY_GENERIC = "generic"

# As três folhas que o jogo pede quando o Ramza entra em cena.
RAMZA_SPRITE_FILES = (
    "fftpack/unit/battle_ramuza_spr.bin",
    "fftpack/unit/battle_ramuza2_spr.bin",
    "fftpack/unit/battle_ramuza3_spr.bin",
)

G2D_PACK = "0007.pac"
G2D_PATH = "system/ffto/g2d.dat"
# Índice (na tabela do g2d.dat) da metade de cima de cada folha; a de baixo é o seguinte.
RAMZA_G2D_TOPS = (830, 832, 834)
G2D_TOP_SIZE = 131072  # 512 x 512 px, 4 bits por pixel
G2D_BOTTOM_SIZE = 118784  # 512 x 464 px

# No Enhanced as cores do Ramza não vêm da folha clássica: vêm da tabela nex
# CharCLUT (Key 1/2/3 = capítulos; Key2 0–3 = as quatro cores de roupa).
CHARCLUT_PACK = "0004.pac"
CHARCLUT_FILE = "charclut.nxd"
CHARCLUT_TABLE = "CharCLUT"
RAMZA_CLUT_KEYS = (1, 2, 3)

# Retratos do menu: wldface_<id>_<variante>; o id é o spriteset do jogo
# original (Ramza 1–3) e as variantes 08–11 acompanham as cores de roupa.
FACE_PACK = "0008.pac"
RAMZA_FACES = (1, 2, 3)
FACE_VARIANTS = (8, 9, 10, 11)
# Achados comparando o retrato de batalha de cada folha HD com os retratos do
# menu. Quem não tem um retrato que bata (Lettie e a maioria dos aldeões)
# fica sem entrada e mantém o retrato do Ramza.
_FACE: dict[str, int] = {
    "aguri": 52, "aru": 7, "aruma": 48, "bariten": 29, "baru": 33, "baruna": 23, "beio": 31,
    "cloud": 50, "daisu": 9, "dily": 4, "dily2": 5, "dily3": 6, "dora": 24, "eru": 27,
    "furaia": 28, "gando": 26, "goru": 11, "h75": 37, "h76": 38, "h77": 39, "h78": 195,
    "h80": 47, "h81": 43, "h83": 131, "hime": 12, "musu": 34, "oran": 21, "oru": 13,
    "rafa": 25, "ragu": 10, "reze": 15, "rudo": 35, "simon": 19, "voru": 36, "wigu": 32,
    "zaru": 8, "zaru2": 175, "zarumou": 16,
    "mina_m": 96, "mina_w": 97, "item_m": 98, "item_w": 99, "knight_m": 100, "knight_w": 101,
    "yumi_m": 102, "yumi_w": 103, "monk_m": 104, "monk_w": 105, "siro_m": 106, "siro_w": 107,
    "kuro_m": 108, "kuro_w": 109, "toki_m": 110, "toki_w": 111, "syou_m": 112, "syou_w": 113,
    "thief_m": 114, "thief_w": 115, "waju_m": 116, "waju_w": 117, "onmyo_m": 118, "onmyo_w": 119,
    "fusui_m": 120, "fusui_w": 121, "ryu_m": 122, "ryu_w": 123, "samu_m": 124, "samu_w": 125,
    "ninja_m": 126, "ninja_w": 127, "san_m": 128, "san_w": 129, "gin_m": 130, "odori_w": 131,
    "mono_m": 132, "mono_w": 133, "60m": 82,
}


def has_portrait(stem: str) -> bool:
    return stem in _FACE

# Achados comparando pixel a pixel cada folha clássica com as texturas do g2d.dat.
_HD_TOP: dict[str, int] = {
    "aguri": 914, "aru": 842, "aruma": 907, "bariten": 878, "baru": 886, "baruna": 866,
    "beio": 882, "cloud": 910, "daisu": 846, "dily": 836, "dily2": 838, "dily3": 840,
    "dora": 868, "eru": 874, "furaia": 876, "gando": 872, "goru": 850, "h75": 894,
    "h76": 896, "h77": 898, "h78": 900, "h80": 905, "h81": 902, "h83": 926, "hime": 852,
    "ledy": 928, "musu": 888, "oran": 864, "oru": 854, "rafa": 870, "ragu": 848,
    "reze": 858, "rudo": 890, "simon": 862, "voru": 892, "wigu": 884, "zaru": 844,
    "zaru2": 912, "zarumou": 860,
    "mina_m": 992, "mina_w": 994, "item_m": 996, "item_w": 998, "knight_m": 1000,
    "knight_w": 1002, "yumi_m": 1004, "yumi_w": 1006, "monk_m": 1008, "monk_w": 1010,
    "siro_m": 1012, "siro_w": 1014, "kuro_m": 1016, "kuro_w": 1018, "toki_m": 1020,
    "toki_w": 1022, "syou_m": 1024, "syou_w": 1026, "thief_m": 1028, "thief_w": 1030,
    "waju_m": 1032, "waju_w": 1034, "onmyo_m": 1036, "onmyo_w": 1038, "fusui_m": 1040,
    "fusui_w": 1042, "ryu_m": 1044, "ryu_w": 1046, "samu_m": 1048, "samu_w": 1050,
    "ninja_m": 1052, "ninja_w": 1054, "san_m": 1056, "san_w": 1058, "gin_m": 1060,
    "odori_w": 1062, "mono_m": 1064, "mono_w": 1066,
    "10m": 954, "10w": 956, "20m": 958, "20w": 960, "40m": 962, "40w": 964,
    "60m": 966, "60w": 968,
}

_STEM = re.compile(r"^[a-z0-9_]+$")

# (arquivo, categoria, nome em português, nome em inglês)
_ROWS: tuple[tuple[str, str, str, str], ...] = (
    ("aguri", CATEGORY_UNIQUE, "Agrias", "Agrias"),
    ("aru", CATEGORY_UNIQUE, "Argath", "Argath"),
    ("aruma", CATEGORY_UNIQUE, "Alma", "Alma"),
    ("bariten", CATEGORY_UNIQUE, "Barrington", "Barrington"),
    ("baru", CATEGORY_UNIQUE, "Meliadoul", "Meliadoul"),
    ("baruna", CATEGORY_UNIQUE, "Gaffgarion", "Gaffgarion"),
    ("beio", CATEGORY_UNIQUE, "Beowulf", "Beowulf"),
    ("cloud", CATEGORY_UNIQUE, "Cloud", "Cloud"),
    ("daisu", CATEGORY_UNIQUE, "Dycedarg", "Dycedarg"),
    ("dily", CATEGORY_UNIQUE, "Delita (cap. 1)", "Delita (ch. 1)"),
    ("dily2", CATEGORY_UNIQUE, "Delita (cap. 2–4)", "Delita (ch. 2–4)"),
    ("dily3", CATEGORY_UNIQUE, "Delita rei", "King Delita"),
    ("dora", CATEGORY_UNIQUE, "Delacroix", "Delacroix"),
    ("eru", CATEGORY_UNIQUE, "Elmdore", "Elmdore"),
    ("furaia", CATEGORY_UNIQUE, "Tietra", "Tietra"),
    ("gando", CATEGORY_UNIQUE, "Marach", "Marach"),
    ("goru", CATEGORY_UNIQUE, "Goltanna", "Goltanna"),
    ("h75", CATEGORY_UNIQUE, "Loffrey", "Loffrey"),
    ("h76", CATEGORY_UNIQUE, "Isilud", "Isilud"),
    ("h77", CATEGORY_UNIQUE, "Cletienne", "Cletienne"),
    ("h78", CATEGORY_UNIQUE, "Wiegraf (Templários)", "Wiegraf (Templars)"),
    ("h80", CATEGORY_UNIQUE, "Meliadoul (outro traje)", "Meliadoul (other outfit)"),
    ("h81", CATEGORY_UNIQUE, "Balk", "Balk"),
    ("h83", CATEGORY_UNIQUE, "Celia", "Celia"),
    ("hime", CATEGORY_UNIQUE, "Ovelia", "Ovelia"),
    ("ledy", CATEGORY_UNIQUE, "Lettie", "Lettie"),
    ("musu", CATEGORY_UNIQUE, "Mustadio", "Mustadio"),
    ("oran", CATEGORY_UNIQUE, "Orran", "Orran"),
    ("oru", CATEGORY_UNIQUE, "Orlandeau", "Orlandeau"),
    ("rafa", CATEGORY_UNIQUE, "Rapha", "Rapha"),
    ("ragu", CATEGORY_UNIQUE, "Larg", "Larg"),
    ("reze", CATEGORY_UNIQUE, "Reis", "Reis"),
    ("rudo", CATEGORY_UNIQUE, "Ludovich", "Ludovich"),
    ("simon", CATEGORY_UNIQUE, "Simon", "Simon"),
    ("voru", CATEGORY_UNIQUE, "Folmarv", "Folmarv"),
    ("wigu", CATEGORY_UNIQUE, "Wiegraf (Death Corps)", "Wiegraf (Death Corps)"),
    ("zaru", CATEGORY_UNIQUE, "Zalbaag", "Zalbaag"),
    ("zaru2", CATEGORY_UNIQUE, "Zalbaag (morto-vivo)", "Zalbaag (undead)"),
    ("zarumou", CATEGORY_UNIQUE, "Zalmour", "Zalmour"),
    ("mina_m", CATEGORY_GENERIC, "Escudeiro (homem)", "Squire (male)"),
    ("mina_w", CATEGORY_GENERIC, "Escudeiro (mulher)", "Squire (female)"),
    ("knight_m", CATEGORY_GENERIC, "Cavaleiro (homem)", "Knight (male)"),
    ("knight_w", CATEGORY_GENERIC, "Cavaleira", "Knight (female)"),
    ("yumi_m", CATEGORY_GENERIC, "Arqueiro", "Archer (male)"),
    ("yumi_w", CATEGORY_GENERIC, "Arqueira", "Archer (female)"),
    ("monk_m", CATEGORY_GENERIC, "Monge (homem)", "Monk (male)"),
    ("monk_w", CATEGORY_GENERIC, "Monge (mulher)", "Monk (female)"),
    ("siro_m", CATEGORY_GENERIC, "Mago branco", "White Mage (male)"),
    ("siro_w", CATEGORY_GENERIC, "Maga branca", "White Mage (female)"),
    ("kuro_m", CATEGORY_GENERIC, "Mago negro", "Black Mage (male)"),
    ("kuro_w", CATEGORY_GENERIC, "Maga negra", "Black Mage (female)"),
    ("toki_m", CATEGORY_GENERIC, "Mago do tempo", "Time Mage (male)"),
    ("toki_w", CATEGORY_GENERIC, "Maga do tempo", "Time Mage (female)"),
    ("syou_m", CATEGORY_GENERIC, "Invocador", "Summoner (male)"),
    ("syou_w", CATEGORY_GENERIC, "Invocadora", "Summoner (female)"),
    ("thief_m", CATEGORY_GENERIC, "Ladrão", "Thief (male)"),
    ("thief_w", CATEGORY_GENERIC, "Ladra", "Thief (female)"),
    ("waju_m", CATEGORY_GENERIC, "Orador", "Orator (male)"),
    ("waju_w", CATEGORY_GENERIC, "Oradora", "Orator (female)"),
    ("fusui_m", CATEGORY_GENERIC, "Geomante (homem)", "Geomancer (male)"),
    ("fusui_w", CATEGORY_GENERIC, "Geomante (mulher)", "Geomancer (female)"),
    ("ryu_m", CATEGORY_GENERIC, "Lanceiro", "Dragoon (male)"),
    ("ryu_w", CATEGORY_GENERIC, "Lanceira", "Dragoon (female)"),
    ("ninja_m", CATEGORY_GENERIC, "Ninja (homem)", "Ninja (male)"),
    ("ninja_w", CATEGORY_GENERIC, "Ninja (mulher)", "Ninja (female)"),
    ("samu_m", CATEGORY_GENERIC, "Samurai (homem)", "Samurai (male)"),
    ("samu_w", CATEGORY_GENERIC, "Samurai (mulher)", "Samurai (female)"),
    ("san_m", CATEGORY_GENERIC, "Aritmético", "Arithmetician (male)"),
    ("san_w", CATEGORY_GENERIC, "Aritmética", "Arithmetician (female)"),
    ("onmyo_m", CATEGORY_GENERIC, "Místico", "Mystic (male)"),
    ("onmyo_w", CATEGORY_GENERIC, "Mística", "Mystic (female)"),
    ("item_m", CATEGORY_GENERIC, "Químico", "Chemist (male)"),
    ("item_w", CATEGORY_GENERIC, "Química", "Chemist (female)"),
    ("mono_m", CATEGORY_GENERIC, "Mimo (homem)", "Mime (male)"),
    ("mono_w", CATEGORY_GENERIC, "Mimo (mulher)", "Mime (female)"),
    ("gin_m", CATEGORY_GENERIC, "Bardo", "Bard"),
    ("odori_w", CATEGORY_GENERIC, "Dançarina", "Dancer"),
    ("10m", CATEGORY_GENERIC, "Garoto", "Boy"),
    ("10w", CATEGORY_GENERIC, "Garota", "Girl"),
    ("20m", CATEGORY_GENERIC, "Homem jovem", "Young man"),
    ("20w", CATEGORY_GENERIC, "Mulher jovem", "Young woman"),
    ("40m", CATEGORY_GENERIC, "Homem", "Man"),
    ("40w", CATEGORY_GENERIC, "Mulher", "Woman"),
    ("60m", CATEGORY_GENERIC, "Homem idoso", "Old man"),
    ("60w", CATEGORY_GENERIC, "Mulher idosa", "Old woman"),
)


@dataclass(frozen=True)
class SpriteOption:
    stem: str
    category: str
    name_pt: str
    name_en: str

    def name(self) -> str:
        return self.name_pt if i18n.get_language() == i18n.LANG_PT else self.name_en


CATALOG: tuple[SpriteOption, ...] = tuple(SpriteOption(*row) for row in _ROWS)
_BY_STEM = {option.stem: option for option in CATALOG}


def category_labels() -> dict[str, str]:
    return {
        CATEGORY_UNIQUE: i18n.t("sprite_cat_unique"),
        CATEGORY_GENERIC: i18n.t("sprite_cat_generic"),
    }


def get(stem: str) -> SpriteOption | None:
    return _BY_STEM.get(stem)


def game_path(stem: str) -> str:
    """Caminho interno no .pac. Recusa qualquer coisa que não seja um sprite da lista."""
    if get(stem) is None or not _STEM.match(stem):
        raise ValueError(stem)
    return f"fftpack/unit/battle_{stem}_spr.bin"


@dataclass(frozen=True)
class SpriteAssets:
    classic: bytes  # battle_<stem>_spr.bin
    hd_top: bytes  # textura do g2d.dat, já descomprimida
    hd_bottom: bytes
    charclut_nxd: bytes = b""  # tabela CharCLUT com as cores do personagem nas linhas do Ramza
    portrait: dict[str, bytes] = field(default_factory=dict)  # caminho no .pac -> conteúdo


def ramza_portrait_files(texture: bytes, parts: bytes) -> dict[str, bytes]:
    files = {}
    for face in RAMZA_FACES:
        for variant in FACE_VARIANTS:
            files[_face_path("texture", face, variant, "tex")] = texture
            files[_face_path("textureparts", face, variant, "utexpt")] = parts
    return files


def _face_path(kind: str, face: int, variant: int, ext: str) -> str:
    return f"ui/ffto/common/face/{kind}/wldface_{face:03d}_{variant:02d}_uitx.{ext}"


def classic_clut(classic: bytes) -> list[int]:
    """Primeira paleta da folha clássica (16 cores RGB555) no formato do CLUTData (R, G, B de 0 a 248)."""
    values = []
    for i in range(16):
        color = struct.unpack_from("<H", classic, i * 2)[0]
        values += [(color & 31) * 8, ((color >> 5) & 31) * 8, ((color >> 10) & 31) * 8]
    return values


def apply_ramza_clut(con: sqlite3.Connection, clut: list[int]) -> None:
    data = json.dumps(clut, separators=(",", ":"))
    con.execute(f'UPDATE "{CHARCLUT_TABLE}" SET CLUTData = ? WHERE Key IN ({",".join("?" * len(RAMZA_CLUT_KEYS))})',
                (data, *RAMZA_CLUT_KEYS))


def _build_charclut(game_root, cli, classic: bytes, stem: str) -> bytes:
    work = paths.cache_dir() / "sprite_clut"
    shutil.rmtree(work, ignore_errors=True)
    nxd_dir = work / "nxd"
    nxd_dir.mkdir(parents=True)
    (nxd_dir / CHARCLUT_FILE).write_bytes(_unpack(game_root, cli, CHARCLUT_PACK, f"nxd/{CHARCLUT_FILE}", stem))
    db = work / "charclut.sqlite"
    if ff16tools.nxd_to_sqlite(cli, nxd_dir, db, None) != 0 or not db.is_file():
        raise RuntimeError(i18n.t("sprite_extract_fail", name=get(stem).name(), code="CharCLUT"))
    con = sqlite3.connect(str(db))
    try:
        apply_ramza_clut(con, classic_clut(classic))
        con.commit()
    finally:
        con.close()
    out = work / "out"
    out.mkdir()
    produced = out / CHARCLUT_FILE
    if ff16tools.sqlite_to_nxd(cli, db, out, [CHARCLUT_TABLE], None) != 0 or not produced.is_file():
        raise RuntimeError(i18n.t("sprite_extract_fail", name=get(stem).name(), code="CharCLUT"))
    return produced.read_bytes()


def _portrait(game_root, cli, stem: str) -> dict[str, bytes]:
    face = _FACE.get(stem)
    if face is None:
        return {}
    texture = _unpack(game_root, cli, FACE_PACK, _face_path("texture", face, 8, "tex"), stem)
    parts = _unpack(game_root, cli, FACE_PACK, _face_path("textureparts", face, 8, "utexpt"), stem)
    return ramza_portrait_files(texture, parts)


def hd_top_index(stem: str) -> int:
    if get(stem) is None or stem not in _HD_TOP:
        raise ValueError(stem)
    return _HD_TOP[stem]


def _unpack(game_root, cli, pack_name: str, relative: str, stem: str) -> bytes:
    pack = game_install.enhanced_pack_dir(Path(game_root)) / pack_name
    if not pack.is_file():
        raise RuntimeError(i18n.t("sprite_no_pack", pack=pack_name))
    out = paths.cache_dir() / "sprite_unpack"
    code = ff16tools.unpack_pack(cli, pack, out, relative, None)
    extracted = out / Path(relative)
    if code != 0 or not extracted.is_file() or extracted.stat().st_size == 0:
        raise RuntimeError(i18n.t("sprite_extract_fail", name=get(stem).name(), code=code))
    return extracted.read_bytes()


def g2d_texture(archive: bytes, index: int) -> bytes:
    """Descomprime a textura `index` de um g2d.dat (cabeçalho YOX + tabela no fim)."""
    if archive[:4] != b"YOX\0":
        raise ValueError("g2d.dat")
    toc_offset, count = struct.unpack_from("<II", archive, 8)
    if not 0 <= index < count:
        raise ValueError(index)
    offset, packed = struct.unpack_from("<II", archive, toc_offset + index * 16)
    if archive[offset:offset + 4] != b"YOX\0":
        raise ValueError(index)
    version, size = struct.unpack_from("<II", archive, offset + 4)
    payload = archive[offset + 16:offset + packed]
    data = payload[:size] if version == 0 else zlib.decompressobj().decompress(payload, size)
    if len(data) != size:
        raise ValueError(index)
    return data


def extract_sprite(game_root, cli, stem: str) -> SpriteAssets:
    """Lê a folha clássica (0002.pac) e as duas texturas HD (0007.pac) do personagem escolhido."""
    top_index = hd_top_index(stem)
    classic = _unpack(game_root, cli, "0002.pac", game_path(stem), stem)
    archive = _unpack(game_root, cli, G2D_PACK, G2D_PATH, stem)
    try:
        top = g2d_texture(archive, top_index)
        bottom = g2d_texture(archive, top_index + 1)
    except (ValueError, struct.error, zlib.error):
        top = bottom = b""
    if len(top) != G2D_TOP_SIZE or len(bottom) != G2D_BOTTOM_SIZE:
        raise RuntimeError(i18n.t("sprite_extract_fail", name=get(stem).name(), code="g2d"))
    charclut = _build_charclut(game_root, cli, classic, stem)
    return SpriteAssets(classic, top, bottom, charclut, _portrait(game_root, cli, stem))
