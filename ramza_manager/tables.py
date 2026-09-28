"""
Leitura das tabelas XML de referência (cópias originais do jogo, as mesmas que
o fftivc.utility.modloader usa como base): JobData, JobCommandData,
AbilityData, ItemData e SpawnData.

Os nomes em inglês vêm dos comentários `<Id>N</Id> <!-- Nome / 名前 / ... -->`
que acompanham cada entrada. Quando o banco nxd do jogo está disponível, a
interface prefere os nomes oficiais de lá (ver nxd_db.read_names).
"""

from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

EMPTY_ITEM = 255

_ID_COMMENT_RE = re.compile(r"<Id>(\d+)</Id>[ \t]*<!--\s*(.*?)\s*-->")


def _comment_names(xml_text: str) -> dict[int, str]:
    """Id -> primeiro nome do comentário (o inglês, antes de ' / ')."""
    names = {}
    for match in _ID_COMMENT_RE.finditer(xml_text):
        names[int(match.group(1))] = match.group(2).split(" / ")[0].strip()
    return names


def _entries(path: Path, tag: str) -> tuple[list[ET.Element], dict[int, str]]:
    text = path.read_text(encoding="utf-8-sig")
    root = ET.fromstring(text.encode("utf-8"))
    return root.findall(f"./Entries/{tag}"), _comment_names(text)


def _fields(element: ET.Element) -> dict[str, str]:
    return {child.tag: (child.text or "").strip() for child in element}


def split_flags(value: str) -> list[str]:
    """'Sword, Knife, Unarmed' -> ['Sword', 'Knife', 'Unarmed']; 'None'/'0' -> []."""
    parts = [p.strip() for p in (value or "").split(",")]
    return [p for p in parts if p and p not in ("None", "0")]


@dataclass
class Job:
    id: int
    name: str
    fields: dict[str, str] = field(default_factory=dict)  # na ordem do XML

    @property
    def job_command_id(self) -> int:
        return int(self.fields.get("JobCommandId", "0"))

    @property
    def equippable(self) -> list[str]:
        return split_flags(self.fields.get("EquippableItems", ""))

    @property
    def innate_ability_ids(self) -> list[int]:
        ids = [int(self.fields.get(f"InnateAbilityId{i}", "0")) for i in range(1, 5)]
        return [i for i in ids if i]


@dataclass
class JobCommand:
    id: int
    name: str
    action_ids: list[int]
    rsm_ids: list[int]  # reações / suportes / movimentos

    @property
    def all_ability_ids(self) -> list[int]:
        return self.action_ids + self.rsm_ids


@dataclass
class Ability:
    id: int
    name: str
    flags: list[str]
    ability_type: str


@dataclass
class Item:
    id: int
    name: str
    category: str
    price: int
    required_level: int


@dataclass
class ReferenceTables:
    jobs: dict[int, Job]
    commands: dict[int, JobCommand]
    abilities: dict[int, Ability]
    items: dict[int, Item]
    spawns: dict[int, dict[str, str]]

    def command_for(self, job: Job) -> Optional[JobCommand]:
        return self.commands.get(job.job_command_id)

    def ability_name(self, ability_id: int) -> str:
        ability = self.abilities.get(ability_id)
        return ability.name if ability and ability.name else f"Habilidade {ability_id}"

    def item_name(self, item_id: int) -> str:
        if item_id == EMPTY_ITEM:
            return "(vazio)"
        item = self.items.get(item_id)
        return item.name if item and item.name else f"Item {item_id}"


def load_reference_tables(data_dir: Path) -> ReferenceTables:
    jobs = {}
    elements, names = _entries(data_dir / "JobData.xml", "Job")
    for el in elements:
        fields = _fields(el)
        job_id = int(fields.pop("Id"))
        jobs[job_id] = Job(job_id, names.get(job_id, ""), fields)

    commands = {}
    elements, names = _entries(data_dir / "JobCommandData.xml", "JobCommand")
    for el in elements:
        fields = _fields(el)
        cmd_id = int(fields["Id"])
        # O XML de referência já traz os ids completos (0-511); os bits de
        # extensão são preenchidos pelo loader.
        actions = [int(fields.get(f"AbilityId{i}", "0")) for i in range(1, 17)]
        rsm = [int(fields.get(f"ReactionSupportMovementId{i}", "0")) for i in range(1, 7)]
        commands[cmd_id] = JobCommand(
            cmd_id, names.get(cmd_id, ""), [a for a in actions if a], [r for r in rsm if r]
        )

    abilities = {}
    elements, names = _entries(data_dir / "AbilityData.xml", "Ability")
    for el in elements:
        fields = _fields(el)
        ab_id = int(fields["Id"])
        abilities[ab_id] = Ability(
            ab_id, names.get(ab_id, ""), split_flags(fields.get("Flags", "")),
            fields.get("AbilityType", ""),
        )

    items = {}
    elements, names = _entries(data_dir / "ItemData.xml", "Item")
    for el in elements:
        fields = _fields(el)
        item_id = int(fields["Id"])
        items[item_id] = Item(
            item_id, names.get(item_id, ""), fields.get("ItemCategory", "None"),
            int(fields.get("Price", "0") or 0), int(fields.get("RequiredLevel", "0") or 0),
        )

    spawns = {}
    elements, _ = _entries(data_dir / "SpawnData.xml", "Spawn")
    for el in elements:
        fields = _fields(el)
        spawns[int(fields.pop("Id"))] = fields

    return ReferenceTables(jobs, commands, abilities, items, spawns)
