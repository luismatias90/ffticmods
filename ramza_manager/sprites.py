"""
Sprites de batalha que podem substituir o do Ramza.

O Ramza não usa o sprite da classe: o jogo desenha as folhas próprias dele
(capítulo 1, capítulos 2–3 e capítulo 4). Trocar o sprite é copiar a folha de
outro personagem humano por cima dessas três. Retrato do menu e algumas cenas
de evento usam outros arquivos e continuam com o Ramza original.

Nomes de arquivo são os do fftpack do jogo (battle_<stem>_spr.bin). Só entram
folhas humanas: monstro tem outra grade de animação e trava com os movimentos
do Ramza. Duplicatas idênticas (o mesmo desenho em dois arquivos) ficam de fora.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
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

_STEM = re.compile(r"^[a-z0-9_]+$")

# (arquivo, categoria, nome em português, nome em inglês)
_ROWS: tuple[tuple[str, str, str, str], ...] = (
    ("aguri", CATEGORY_UNIQUE, "Agrias", "Agrias"),
    ("ajora", CATEGORY_UNIQUE, "Santo Ajora", "St. Ajora"),
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
    ("h82", CATEGORY_UNIQUE, "Alma (cemitério)", "Alma (graveyard)"),
    ("h83", CATEGORY_UNIQUE, "Celia", "Celia"),
    ("hime", CATEGORY_UNIQUE, "Ovelia", "Ovelia"),
    ("ledy", CATEGORY_UNIQUE, "Lettie", "Lettie"),
    ("mara", CATEGORY_UNIQUE, "Marach (outro traje)", "Marach (other outfit)"),
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


def extract_sprite(game_root, cli, stem: str) -> bytes:
    """Lê a folha de sprite escolhida do 0002.pac do jogo (fftpack)."""
    pack = game_install.enhanced_pack_dir(Path(game_root)) / "0002.pac"
    if not pack.is_file():
        raise RuntimeError(i18n.t("sprite_no_pack"))
    relative = game_path(stem)
    out = paths.cache_dir() / "sprite_unpack"
    code = ff16tools.unpack_pack(cli, pack, out, relative, None)
    extracted = out / Path(relative)
    if code != 0 or not extracted.is_file():
        raise RuntimeError(i18n.t("sprite_extract_fail", name=get(stem).name(), code=code))
    data = extracted.read_bytes()
    if not data:
        raise RuntimeError(i18n.t("sprite_extract_fail", name=get(stem).name(), code=code))
    return data
