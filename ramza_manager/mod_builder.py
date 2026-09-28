"""
Gera o mod Reloaded-II do Solo Ramza Manager. Duas partes independentes:

1. Classe: transforma as classes do Ramza (Jobs 1, 2 e 3) na classe escolhida,
   ou numa classe customizada (classe base + skillset montado à mão).
2. Bolsa: troca o conteúdo do pacote de bônus da Deluxe Edition pelos itens
   escolhidos (o jogo entrega esse pacote no inventário).

Estrutura gerada (mesmo formato usado pelo Mod Studio / fftivc.utility.modloader):

  <ModId>/ModConfig.json
  <ModId>/FFTIVC/tables/enhanced/JobData.xml      Jobs 1-3 = classe escolhida
  <ModId>/FFTIVC/tables/enhanced/JobCommandData.xml   skillsets 25-27 (classe customizada)
  <ModId>/FFTIVC/tables/enhanced/AbilityData.xml  tira DontLearnWithJP (se houver)
  <ModId>/FFTIVC/tables/enhanced/SpawnData.xml    equipamento inicial (se preciso)
  <ModId>/FFTIVC/data/enhanced/nxd/ability.*.nxd  JP das skills da classe
  <ModId>/FFTIVC/data/enhanced/nxd/job.*.nxd      nome + skillset nos Jobs 1-3
  <ModId>/FFTIVC/data/enhanced/nxd/jobcommand.*.nxd   nome do skillset customizado
  <ModId>/FFTIVC/data/enhanced/nxd/systembonus*.nxd   conteúdo do pacote de bônus

Nada de nível, EXP, atributos base ou história é tocado.
"""

from __future__ import annotations

import json
import shutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Optional
from xml.sax.saxutils import escape

from . import __version__
from .class_catalog import RAMZA_JOB_IDS
from .custom_class import MAX_ACTIONS, MAX_RSM, CustomClass
from .nxd_db import MAX_QUANTITY, BagItem
from .tables import EMPTY_ITEM, Job, ReferenceTables

MOD_ID = "fftivc.soloramza.classmanager"
MOD_NAME = "Solo Ramza Manager"
MODLOADER_ID = "fftivc.utility.modloader"
GAME_MODE = "enhanced"
RAMZA_SPAWN_ID = 2
# Skillset próprio de cada Job do Ramza (Mettle). Só esses Jobs os usam.
RAMZA_COMMAND_IDS = {1: 25, 2: 26, 3: 27}
DEFAULT_JP_COST = 0

# Campos que continuam sendo os do Ramza:
# - ImmuneStatus: o Ramza é imune a Traitor; mantido para não arriscar cenas.
# - Monster*: só fazem sentido para monstros.
KEEP_RAMZA_FIELDS = {"ImmuneStatus", "MonsterPortrait", "MonsterPalette", "MonsterGraphic"}

WEAPON_CATEGORIES = [
    "Sword", "Knife", "KnightSword", "Katana", "NinjaBlade", "Axe", "Rod", "Staff", "Flail",
    "Gun", "Crossbow", "Bow", "Instrument", "Book", "Polearm", "Pole", "Bag", "Cloth", "FellSword",
]
SLOT_CATEGORIES = {
    "Helmet": ["Hat", "Helmet", "HairAdornment"],
    "Armor": ["Clothing", "Armor", "Robe"],
    "Accessory": ["Shoes", "Armguard", "Ring", "Armlet", "Cloak", "Perfume", "LipRouge"],
    "RightWeapon": WEAPON_CATEGORIES,
    "RightShield": ["Shield"],
    "LeftWeapon": [],   # nunca preenchemos a mão esquerda
    "LeftShield": [],
}


@dataclass
class BuildPlan:
    source_job: Optional[Job]           # None = não troca a classe
    class_name: Optional[str]
    job_xml: Optional[str]
    ability_xml: Optional[str]
    spawn_xml: Optional[str]
    ability_ids: list[int]
    spawn_changes: dict[str, tuple[int, int]] = field(default_factory=dict)  # slot -> (antes, depois)
    bag: Optional[list[BagItem]] = None  # None = não mexe no pacote de bônus
    custom: Optional[CustomClass] = None  # classe customizada (skillset nos 25-27)
    command_xml: Optional[str] = None

    @property
    def ramza_command_ids(self) -> list[int]:
        """Skillsets próprios do Ramza reescritos pela classe customizada."""
        return sorted(RAMZA_COMMAND_IDS.values()) if self.custom else []

    @property
    def is_empty(self) -> bool:
        return self.source_job is None and not self.bag


# ---------------------------------------------------------------------------
# XML
# ---------------------------------------------------------------------------

def _table_xml(root: str, tag: str, entries: list[dict[str, str]], note: str) -> str:
    lines = [
        '<?xml version="1.0" encoding="utf-8"?>',
        f"<!-- {escape(note)} -->",
        f"<{root}>",
        "  <Version>1</Version>",
        "  <Entries>",
    ]
    for entry in entries:
        lines.append(f"    <{tag}>")
        for name, value in entry.items():
            lines.append(f"      <{name}>{escape(str(value))}</{name}>")
        lines.append(f"    </{tag}>")
    lines += ["  </Entries>", f"</{root}>", ""]
    return "\n".join(lines)


def _job_entries(source: Job, keep_ramza_command: bool = False) -> list[dict[str, str]]:
    entries = []
    for job_id in RAMZA_JOB_IDS:
        entry = {"Id": str(job_id)}
        entry.update({k: v for k, v in source.fields.items() if k not in KEEP_RAMZA_FIELDS})
        if keep_ramza_command:
            entry["JobCommandId"] = str(RAMZA_COMMAND_IDS[job_id])
        entries.append(entry)
    return entries


def _command_entries(custom: CustomClass) -> list[dict[str, str]]:
    """Os três skillsets do Ramza com a lista da classe customizada (slots vazios = 0)."""
    entries = []
    for cmd_id in sorted(RAMZA_COMMAND_IDS.values()):
        entry = {"Id": str(cmd_id)}
        for i in range(MAX_ACTIONS):
            entry[f"AbilityId{i + 1}"] = str(custom.actions[i] if i < len(custom.actions) else 0)
        for i in range(MAX_RSM):
            entry[f"ReactionSupportMovementId{i + 1}"] = str(custom.rsm[i] if i < len(custom.rsm) else 0)
        entries.append(entry)
    return entries


def _pick_item(tables: ReferenceTables, categories: list[str]) -> int:
    """O item mais básico (menor nível exigido, depois menor preço) nas categorias dadas."""
    candidates = [
        item for item in tables.items.values()
        if item.id < EMPTY_ITEM and item.category in categories and item.price > 0
    ]
    if not candidates:
        return EMPTY_ITEM
    return min(candidates, key=lambda i: (i.required_level, i.price, i.id)).id


def starting_gear_changes(tables: ReferenceTables, source: Job) -> dict[str, tuple[int, int]]:
    """
    Equipamento inicial do Ramza que a nova classe não pode usar, e o que
    entra no lugar. O SpawnData exige que o equipamento seja equipável pela
    classe da unidade.
    """
    equippable = set(source.equippable)
    spawn = tables.spawns.get(RAMZA_SPAWN_ID, {})
    changes = {}
    for slot, slot_categories in SLOT_CATEGORIES.items():
        current = int(spawn.get(slot, EMPTY_ITEM))
        if current == EMPTY_ITEM:
            continue
        item = tables.items.get(current)
        if item and item.category in equippable:
            continue
        allowed = [c for c in slot_categories if c in equippable]
        replacement = _pick_item(tables, allowed) if allowed else EMPTY_ITEM
        if replacement != current:
            changes[slot] = (current, replacement)
    return changes


def validate_bag(tables: ReferenceTables, bag: list[BagItem]) -> list[BagItem]:
    """Remove itens inexistentes/duplicados e limita a quantidade a 1-99."""
    merged: dict[int, int] = {}
    for entry in bag:
        if entry.item_id <= 0 or entry.item_id not in tables.items:
            continue
        merged[entry.item_id] = merged.get(entry.item_id, 0) + entry.quantity
    return [BagItem(i, max(1, min(MAX_QUANTITY, q))) for i, q in merged.items()]


def plan_build(
    tables: ReferenceTables,
    source_job_id: Optional[int],
    class_name: Optional[str],
    bag: Optional[list[BagItem]] = None,
    custom: Optional[CustomClass] = None,
) -> BuildPlan:
    """
    Calcula tudo que vai no mod (função pura, sem tocar em disco). Com
    `custom`, a classe base e o nome vêm dela e `source_job_id`/`class_name`
    são ignorados.
    """
    bag = validate_bag(tables, bag) if bag else None
    if custom is not None:
        source_job_id, class_name = custom.base_job, custom.name
    if source_job_id is None:
        return BuildPlan(None, None, None, None, None, [], {}, bag)
    if source_job_id in RAMZA_JOB_IDS:
        raise ValueError("Escolha uma classe diferente das classes originais do Ramza.")
    source = tables.jobs[source_job_id]
    if custom is not None:
        source = custom.effective_job(tables)  # base + equipamentos/inatas/atributos da classe
        ability_ids = custom.ability_ids
    else:
        command = tables.command_for(source)
        ability_ids = command.all_ability_ids if command else []

    note = f"Gerado pelo Solo Ramza Manager {__version__}: Ramza = {class_name} (Job {source_job_id})"
    job_xml = _table_xml("JobTable", "Job", _job_entries(source, custom is not None), note)
    command_xml = None
    if custom is not None:
        command_xml = _table_xml("JobCommandTable", "JobCommand", _command_entries(custom), note)

    ability_entries = []
    for ab_id in ability_ids:
        ability = tables.abilities.get(ab_id)
        if ability and "DontLearnWithJP" in ability.flags:
            flags = [f for f in ability.flags if f != "DontLearnWithJP"]
            ability_entries.append({"Id": str(ab_id), "Flags": ", ".join(flags) or "0"})
    ability_xml = _table_xml("AbilityTable", "Ability", ability_entries, note) if ability_entries else None

    changes = starting_gear_changes(tables, source)
    spawn_xml = None
    if changes:
        entry = {"Id": str(RAMZA_SPAWN_ID)}
        entry.update({slot: str(new) for slot, (_old, new) in changes.items()})
        spawn_xml = _table_xml("SpawnTable", "Spawn", [entry], note)

    return BuildPlan(source, class_name, job_xml, ability_xml, spawn_xml, ability_ids, changes, bag,
                     custom, command_xml)


# ---------------------------------------------------------------------------
# Pasta do mod
# ---------------------------------------------------------------------------

def mod_config(plan: BuildPlan) -> dict:
    parts = []
    if plan.custom is not None:
        parts.append(f"Ramza joga como {plan.class_name}, classe customizada (base: Job {plan.source_job.id}), "
                     f"skillset {plan.custom.skillset} com {len(plan.ability_ids)} skills.")
    elif plan.source_job is not None:
        parts.append(f"Ramza joga como {plan.class_name} (Job {plan.source_job.id}), todas as skills da classe liberadas.")
    if plan.bag:
        parts.append(f"Bônus da Deluxe Edition trocado por {len(plan.bag)} item(ns) escolhido(s).")
    plugin = {
        "ClassName": plan.class_name,
        "SourceJobId": plan.source_job.id if plan.source_job else None,
        "BagItems": [[b.item_id, b.quantity] for b in plan.bag] if plan.bag else [],
        "CustomClass": plan.custom.to_dict() if plan.custom else None,
    }
    return {
        "ModId": MOD_ID,
        "ModName": MOD_NAME,
        "ModAuthor": "Solo Ramza Manager",
        "ModVersion": __version__,
        "ModDescription": " ".join(parts),
        "ModDll": "",
        "ModIcon": "",
        "ModR2RManagedDll32": "",
        "ModR2RManagedDll64": "",
        "ModNativeDll32": "",
        "ModNativeDll64": "",
        "Tags": [],
        "CanUnload": None,
        "HasExports": None,
        "IsLibrary": False,
        "PluginData": {"SoloRamzaManager": plugin},
        "IsUniversalMod": False,
        "ModDependencies": [MODLOADER_ID],
        "OptionalDependencies": [],
        "SupportedAppId": ["fft_enhanced.exe"],
        "ProjectUrl": "",
    }


def write_mod_folder(plan: BuildPlan, mod_root: Path, nxd_files: list[Path]) -> None:
    tables_dir = mod_root / "FFTIVC" / "tables" / GAME_MODE
    for filename, text in (
        ("JobData.xml", plan.job_xml),
        ("JobCommandData.xml", plan.command_xml),
        ("AbilityData.xml", plan.ability_xml),
        ("SpawnData.xml", plan.spawn_xml),
    ):
        if text:
            tables_dir.mkdir(parents=True, exist_ok=True)
            (tables_dir / filename).write_text(text, encoding="utf-8")

    if nxd_files:
        nxd_dir = mod_root / "FFTIVC" / "data" / GAME_MODE / "nxd"
        nxd_dir.mkdir(parents=True, exist_ok=True)
        for path in nxd_files:
            shutil.copy(path, nxd_dir / path.name)

    config = mod_config(plan)
    (mod_root / "ModConfig.json").write_text(json.dumps(config, indent=2, ensure_ascii=False), encoding="utf-8")


def install_mod(staged_root: Path, mods_folder: Path) -> Path:
    """Substitui a versão anterior do mod na pasta Mods do Reloaded-II."""
    target = mods_folder / MOD_ID
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(staged_root, target)
    return target


def uninstall_mod(mods_folder: Path) -> bool:
    target = mods_folder / MOD_ID
    if target.exists():
        shutil.rmtree(target)
        return True
    return False


def read_installed(mods_folder: Path) -> Optional[dict]:
    """O que o mod instalado aplica ({ClassName, SourceJobId, BagItems}), ou None se não há mod."""
    config = mods_folder / MOD_ID / "ModConfig.json"
    try:
        data = json.loads(config.read_text(encoding="utf-8-sig"))
    except (OSError, ValueError):
        return None
    return (data.get("PluginData") or {}).get("SoloRamzaManager", {})


def read_installed_class(mods_folder: Path) -> Optional[str]:
    installed = read_installed(mods_folder)
    return installed.get("ClassName") if installed else None


def build_mod(
    plan: BuildPlan,
    staging_root: Path,
    nxd_builder: Optional[Callable[[BuildPlan, Path], list[Path]]] = None,
) -> Path:
    """Monta o mod completo em `staging_root/<ModId>` e devolve esse caminho."""
    shutil.rmtree(staging_root, ignore_errors=True)
    mod_root = staging_root / MOD_ID
    mod_root.mkdir(parents=True)
    nxd_files = nxd_builder(plan, staging_root / "_nxd_work") if nxd_builder else []
    write_mod_folder(plan, mod_root, nxd_files)
    return mod_root
