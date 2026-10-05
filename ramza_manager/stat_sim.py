"""
Simulação dos atributos do Ramza por nível, a partir do Multiplier e do Growth
da classe (fórmulas do FFT Battle Mechanics Guide).

O jogo guarda cada atributo como um valor "raw" (24 bits). A cada level up,
raw += raw // (Growth + nível_atual), usando o Growth da classe em que o nível
foi ganho. O valor exibido é raw * Multiplier // 1638400 (o Multiplier da
classe atual). A simulação supõe que todos os níveis foram ganhos nesta classe.

Valores raw de nível 1 de uma unidade masculina (o Ramza): HP e MP são
sorteados numa faixa, Speed/PA/MA são fixos.
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
    out: dict[str, tuple[int, int]] = {}
    for stat in BASE_RAW:
        try:
            multiplier = int(fields[f"{stat}Multiplier"])
            growth = int(fields[f"{stat}Growth"])
        except (KeyError, TypeError, ValueError):
            continue
        if growth > 0:
            out[stat] = stat_range(stat, multiplier, growth, level)
    return out
