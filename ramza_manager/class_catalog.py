"""
Quais classes podem ser escolhidas para o Ramza, e em que categoria cada uma
aparece.

Faixas de Job Id conferidas na tabela nex `Job` do jogo (versão Enhanced):
  1-3     classes do próprio Ramza (Cap. 1, Cap. 2-3, Cap. 4) - são o alvo
  4-59    personagens únicos (Holy Knight, Sword Saint, Dragonkin, ...)
  60-73   Lucavi e versões de história de classes genéricas (ocultas)
  74-93   classes genéricas (Squire ... Mime)
  94-141  monstros (fora: o Ramza ficaria sem menu/equipamento)
  144-154 chefes finais/inimigos especiais (Byblos, Automaton, Ultima Demon...)
  155-168 vazias nesta versão
  169-173 monstros duplicados
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from . import i18n
from .tables import Job, ReferenceTables

RAMZA_JOB_IDS = (1, 2, 3)

CATEGORY_GENERIC = "generic"
CATEGORY_UNIQUE = "unique"
CATEGORY_BOSS = "boss"

def category_labels() -> dict[str, str]:
    return {
        CATEGORY_GENERIC: i18n.t("cat_generic"),
        CATEGORY_UNIQUE: i18n.t("cat_unique"),
        CATEGORY_BOSS: i18n.t("cat_boss"),
    }

_GENERIC_IDS = range(74, 94)
_UNIQUE_IDS = range(4, 60)
_BOSS_IDS = list(range(60, 74)) + list(range(142, 155))


@dataclass
class ClassOption:
    job: Job
    name: str
    skillset_name: str
    category: str

    @property
    def job_id(self) -> int:
        return self.job.id

    @property
    def experimental(self) -> bool:
        return self.category == CATEGORY_BOSS

    def label(self, ability_count: int) -> str:
        skillset = self.skillset_name or i18n.t("own_skillset")
        return i18n.t("class_label", name=self.name, skillset=skillset, n=ability_count)


def category_for(job_id: int) -> Optional[str]:
    if job_id in _GENERIC_IDS:
        return CATEGORY_GENERIC
    if job_id in _UNIQUE_IDS:
        return CATEGORY_UNIQUE
    if job_id in _BOSS_IDS:
        return CATEGORY_BOSS
    return None


def build_catalog(
    tables: ReferenceTables,
    job_names: Optional[dict[int, str]] = None,
    command_names: Optional[dict[int, str]] = None,
) -> list[ClassOption]:
    """
    Lista de classes selecionáveis. `job_names`/`command_names` vêm do nxd do
    jogo (nomes oficiais); sem eles, usa os comentários do XML de referência.

    Classes sem nome são entradas vazias/internas e ficam de fora. Duplicatas
    exatas (mesmo nome + mesmo skillset, ex.: Cleric 20/44) aparecem uma vez.
    """
    job_names = job_names or {}
    command_names = command_names or {}
    options: list[ClassOption] = []
    seen: set[tuple[str, int]] = set()

    for job_id in sorted(tables.jobs):
        category = category_for(job_id)
        if category is None:
            continue
        job = tables.jobs[job_id]
        name = (job_names.get(job_id) or "").strip() if job_names else job.name
        if not name:
            continue
        cmd_id = job.job_command_id
        if cmd_id >= 176 and cmd_id < 224:  # skillset de monstro
            continue
        key = (name, cmd_id)
        if key in seen:
            continue
        seen.add(key)
        command = tables.commands.get(cmd_id)
        skillset = (command_names.get(cmd_id) or "").strip() or (command.name if command else "")
        options.append(ClassOption(job, name, skillset, category))
    return options
