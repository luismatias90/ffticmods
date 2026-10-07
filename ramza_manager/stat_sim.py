"""
Simulação dos atributos do Ramza por nível, a partir do Multiplier e do Growth
da classe (fórmulas do FFT Battle Mechanics Guide).

O jogo guarda cada atributo como um valor "raw" (24 bits). A cada level up,
raw += raw // (Growth + nível_atual), usando o Growth da classe em que o nível
foi ganho. O valor exibido é raw * Multiplier // 1638400 (o Multiplier da
classe atual). A simulação supõe que todos os níveis foram ganhos nesta classe.

Valores raw de nível 1 de uma unidade masculina (o Ramza): HP e MP são
sorteados numa faixa, Speed/PA/MA são fixos.

relevel() leva um raw de um save para outro nível: subindo, aplica a mesma
conta do level up; descendo, desfaz a conta nível a nível.
"""

from __future__ import annotations

from typing import Mapping

MIN_LEVEL, MAX_LEVEL = 1, 99
DIVISOR = 1638400
RAW_MAX = 0xFFFFFF

# (mínimo, máximo) do raw de nível 1.
BASE_RAW: dict[str, tuple[int, int]] = {
    "HP": (491520, 524287),
    "MP": (229376, 245759),
    "Speed": (98304, 98304),
    "PA": (81920, 81920),
    "MA": (65536, 65536),
}
DISPLAY_CAP = {"HP": 999, "MP": 999, "Speed": 99, "PA": 99, "MA": 99}


def raw_at_level(raw: int, growth: int, level: int) -> int:
    """Raw no `level`, partindo do raw de nível 1."""
    for current in range(MIN_LEVEL, level):
        raw = min(RAW_MAX, raw + raw // (growth + current))
    return raw


def _level_down(raw: int, divisor: int) -> int:
    """O maior raw que, após um level up com `divisor` (Growth + nível), não passa de `raw`."""
    before = raw * divisor // (divisor + 1)
    while before + 1 + (before + 1) // divisor <= raw:
        before += 1
    while before > 0 and before + before // divisor > raw:
        before -= 1
    return before


def relevel(stat: str, raw: int, growth: int, old_level: int, new_level: int, from_scratch: bool = False) -> int:
    """
    Raw de `stat` no `new_level`. Normalmente parte do `raw` atual (no
    `old_level`), preservando o que a unidade já ganhou; com `from_scratch`,
    recalcula desde o nível 1 (meio da faixa de HP/MP) como se todos os
    níveis fossem ganhos nesta classe.
    """
    new_level = max(MIN_LEVEL, min(MAX_LEVEL, new_level))
    if from_scratch:
        low, high = BASE_RAW[stat]
        return raw_at_level((low + high) // 2, growth, new_level)
    old_level = max(MIN_LEVEL, min(MAX_LEVEL, old_level))
    for current in range(old_level, new_level):
        raw = min(RAW_MAX, raw + raw // (growth + current))
    for current in range(old_level - 1, new_level - 1, -1):
        raw = _level_down(raw, growth + current)
    return raw


def growths(fields: Mapping[str, str]) -> dict[str, int]:
    """Growth de cada atributo de um JobData; ignora valores ausentes ou inválidos."""
    out: dict[str, int] = {}
    for stat in BASE_RAW:
        try:
            growth = int(fields[f"{stat}Growth"])
        except (KeyError, TypeError, ValueError):
            continue
        if growth > 0:
            out[stat] = growth
    return out


def multipliers(fields: Mapping[str, str]) -> dict[str, int]:
    out: dict[str, int] = {}
    for stat in BASE_RAW:
        try:
            out[stat] = int(fields[f"{stat}Multiplier"])
        except (KeyError, TypeError, ValueError):
            continue
    return out


def displayed(stat: str, raw: int, multiplier: int) -> int:
    return min(DISPLAY_CAP[stat], raw * multiplier // DIVISOR)


def stat_range(stat: str, multiplier: int, growth: int, level: int) -> tuple[int, int]:
    """(mínimo, máximo) do atributo exibido no `level`."""
    level = max(MIN_LEVEL, min(MAX_LEVEL, level))
    low, high = BASE_RAW[stat]
    return (displayed(stat, raw_at_level(low, growth, level), multiplier),
            displayed(stat, raw_at_level(high, growth, level), multiplier))


def simulate(fields: Mapping[str, str], level: int) -> dict[str, tuple[int, int]]:
    """Atributos no `level` para os campos de um JobData; ignora atributos sem dados válidos."""
    mults = multipliers(fields)
    return {stat: stat_range(stat, mults[stat], growth, level)
            for stat, growth in growths(fields).items() if stat in mults}
