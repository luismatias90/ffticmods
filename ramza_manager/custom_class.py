"""
Classes customizadas: uma classe base (atributos, equipamentos, Move/Jump,
inatas) mais um skillset montado à mão com habilidades de qualquer skillset
do jogo. Qualquer campo da classe base pode ser sobrescrito (bloco "job").

O skillset vai nos skillsets próprios do Ramza (JobCommand 25, 26 e 27), que
nenhuma outra unidade usa. Assim o skillset misto não vaza para inimigos.

Cada classe é um arquivo JSON pequeno (`*.ramzaclass.json`) que dá para
exportar, mandar para outras pessoas e importar:

  {
    "format": "soloramza-class", "version": 1,
    "name": "Spellblade", "skillset": "Runeblade",
    "author": "...", "description": "...",
    "base_job": 76,
    "actions": [138, 139, 10, 11],
    "rsm": [447, 454],
    "job": {                                  (opcional, versão 2)
      "equip": ["Sword", "Rod", "Shield", "Armor", "Ring"],
      "innates": [472],
      "multipliers": {"PA": 130}, "growths": {"MA": 40},
      "move": 4, "jump": 3, "evasion": 15
    }
  }

Os ids são os do jogo (Job e Ability), iguais em todos os idiomas. O que não
aparece em "job" vem da classe base. Não existe esquiva mágica por classe no
JobData: ela vem só de escudos, capas e acessórios.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field, replace
from pathlib import Path
from typing import Optional

from . import __version__, i18n
from .class_catalog import RAMZA_JOB_IDS, category_for
from .tables import Job, ReferenceTables

FORMAT = "soloramza-class"
FORMAT_VERSION = 2  # 2: bloco "job" (equipamentos, inatas, atributos, Move/Jump/esquiva)
FILE_SUFFIX = ".ramzaclass.json"

# Tamanho fixo das listas no JobCommandData do jogo.
MAX_ACTIONS = 16
MAX_RSM = 6
MAX_NAME = 24
MAX_DESCRIPTION = 300
MAX_AUTHOR = 40

# Skillsets de onde as habilidades podem vir: tabela principal (0-175) e os
# três de War of the Lions (224-226). 176-223 são de monstro.
_COMMAND_IDS = set(range(0, 176)) | {224, 225, 226}

# Tipos de habilidade com mecânica própria (usam o inventário, alcance de
# Jump, cálculo de Arithmeticks...). Funcionam em testes da comunidade, mas
# fora do skillset original merecem um aviso.
SPECIAL_TYPES = {"Item", "Throwing", "Jumping", "Math"}

# Atributos do JobData: <X>Multiplier e <X>Growth.
STATS = ("HP", "MP", "Speed", "PA", "MA")
MAX_INNATES = 4
# Faixas aceitas (os campos são 1 byte no jogo).
MULTIPLIER_RANGE = (1, 255)
GROWTH_RANGE = (1, 255)
MOVE_RANGE = (1, 10)
JUMP_RANGE = (1, 10)
EVASION_RANGE = (0, 100)

# Flags de EquippableItems, agrupadas para o editor.
EQUIP_GROUPS: dict[str, tuple[str, ...]] = {
    "weapon": ("Unarmed", "Knife", "NinjaBlade", "Sword", "KnightSword", "Katana", "Axe", "Rod", "Staff",
               "Flail", "Gun", "Crossbow", "Bow", "Instrument", "Book", "Polearm", "Pole", "Bag", "Cloth",
               "FellSword"),
    "shield": ("Shield",),
    "head": ("Hat", "Helmet", "HairAdornment"),
    "body": ("Clothing", "Armor", "Robe"),
    "accessory": ("Shoes", "Armguard", "Ring", "Armlet", "Cloak", "Perfume", "LipRouge"),
}
EQUIP_FLAGS = tuple(flag for group in EQUIP_GROUPS.values() for flag in group)


class CustomClassError(ValueError):
    """Arquivo de classe inválido (mensagem já traduzida)."""


@dataclass
class CustomClass:
    name: str
    skillset: str
    base_job: int
    actions: list[int] = field(default_factory=list)
    rsm: list[int] = field(default_factory=list)
    author: str = ""
    description: str = ""
    # Sobrescritas da classe base (None / ausente = valor da base).
    equip: Optional[list[str]] = None
    innates: Optional[list[int]] = None
    multipliers: dict[str, int] = field(default_factory=dict)
    growths: dict[str, int] = field(default_factory=dict)
    move: Optional[int] = None
    jump: Optional[int] = None
    evasion: Optional[int] = None

    @property
    def ability_ids(self) -> list[int]:
        return self.actions + self.rsm

    def job_overrides(self) -> dict[str, str]:
        """Campos do JobData que a classe troca em relação à base."""
        out: dict[str, str] = {}
        if self.innates is not None:
            ids = list(self.innates[:MAX_INNATES]) + [0] * (MAX_INNATES - len(self.innates[:MAX_INNATES]))
            for i, ab_id in enumerate(ids, 1):
                out[f"InnateAbilityId{i}"] = str(ab_id)
        if self.equip is not None:
            out["EquippableItems"] = ", ".join(f for f in EQUIP_FLAGS if f in self.equip) or "None"
        for stat, value in self.growths.items():
            out[f"{stat}Growth"] = str(value)
        for stat, value in self.multipliers.items():
            out[f"{stat}Multiplier"] = str(value)
        for key, value in (("Move", self.move), ("Jump", self.jump), ("CharacterEvasion", self.evasion)):
            if value is not None:
                out[key] = str(value)
        return out

    def effective_job(self, tables: ReferenceTables) -> Job:
        """A classe base com as sobrescritas aplicadas (mesma ordem de campos)."""
        base = tables.jobs[self.base_job]
        fields = dict(base.fields)
        fields.update(self.job_overrides())
        return Job(base.id, base.name, fields)

    def _job_dict(self) -> dict:
        job: dict = {}
        if self.equip is not None:
            job["equip"] = [f for f in EQUIP_FLAGS if f in self.equip]
        if self.innates is not None:
            job["innates"] = list(self.innates)
        if self.multipliers:
            job["multipliers"] = {k: self.multipliers[k] for k in STATS if k in self.multipliers}
        if self.growths:
            job["growths"] = {k: self.growths[k] for k in STATS if k in self.growths}
        for key in ("move", "jump", "evasion"):
            if getattr(self, key) is not None:
                job[key] = getattr(self, key)
        return job

    def to_dict(self) -> dict:
        return {
            "format": FORMAT,
            "version": FORMAT_VERSION,
            "app_version": __version__,
            "name": self.name,
            "skillset": self.skillset,
            "author": self.author,
            "description": self.description,
            "base_job": self.base_job,
            "actions": list(self.actions),
            "rsm": list(self.rsm),
            "job": self._job_dict(),
        }

    @classmethod
    def from_dict(cls, data: object) -> "CustomClass":
        """Lê o JSON sem consultar o jogo. Erros de estrutura viram CustomClassError."""
        if not isinstance(data, dict) or data.get("format") != FORMAT:
            raise CustomClassError(i18n.t("cc_err_format"))
        version = data.get("version")
        if not isinstance(version, int) or version > FORMAT_VERSION:
            raise CustomClassError(i18n.t("cc_err_version", version=version))

        def text(key: str, limit: int, required: bool = False) -> str:
            value = data.get(key, "")
            if not isinstance(value, str):
                raise CustomClassError(i18n.t("cc_err_field", field=key))
            value = " ".join(value.split()) if key != "description" else value.strip()
            if required and not value:
                raise CustomClassError(i18n.t("cc_err_field", field=key))
            return value[:limit]

        def ids(key: str) -> list[int]:
            value = data.get(key, [])
            if not isinstance(value, list) or not all(isinstance(i, int) and not isinstance(i, bool) for i in value):
                raise CustomClassError(i18n.t("cc_err_field", field=key))
            return list(value)

        base_job = data.get("base_job")
        if not _is_int(base_job):
            raise CustomClassError(i18n.t("cc_err_field", field="base_job"))
        name = text("name", MAX_NAME, required=True)
        klass = cls(
            name=name,
            skillset=text("skillset", MAX_NAME) or name,
            base_job=base_job,
            actions=ids("actions"),
            rsm=ids("rsm"),
            author=text("author", MAX_AUTHOR),
            description=text("description", MAX_DESCRIPTION),
        )
        job = data.get("job", {})
        if job is None:
            job = {}
        if not isinstance(job, dict):
            raise CustomClassError(i18n.t("cc_err_field", field="job"))
        if "equip" in job:
            equip = job["equip"]
            if not isinstance(equip, list) or not all(isinstance(f, str) for f in equip):
                raise CustomClassError(i18n.t("cc_err_field", field="job.equip"))
            klass.equip = list(equip)
        if "innates" in job:
            innates = job["innates"]
            if not isinstance(innates, list) or not all(_is_int(i) for i in innates):
                raise CustomClassError(i18n.t("cc_err_field", field="job.innates"))
            klass.innates = list(innates)
        for key in ("multipliers", "growths"):
            values = job.get(key, {})
            if not isinstance(values, dict) or not all(k in STATS and _is_int(v) for k, v in values.items()):
                raise CustomClassError(i18n.t("cc_err_field", field=f"job.{key}"))
            setattr(klass, key, dict(values))
        for key in ("move", "jump", "evasion"):
            if key in job and job[key] is not None:
                if not _is_int(job[key]):
                    raise CustomClassError(i18n.t("cc_err_field", field=f"job.{key}"))
                setattr(klass, key, job[key])
        return klass


def _is_int(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


# ---------------------------------------------------------------------------
# Habilidades disponíveis
# ---------------------------------------------------------------------------

def _pool(tables: ReferenceTables, attr: str) -> dict[int, int]:
    """Habilidade -> primeiro skillset (menor id) em que ela aparece."""
    pool: dict[int, int] = {}
    for cmd_id in sorted(tables.commands):
        if cmd_id not in _COMMAND_IDS:
            continue
        for ab_id in getattr(tables.commands[cmd_id], attr):
            if ab_id and ab_id in tables.abilities:
                pool.setdefault(ab_id, cmd_id)
    return pool


def action_pool(tables: ReferenceTables) -> dict[int, int]:
    return _pool(tables, "action_ids")


def rsm_pool(tables: ReferenceTables) -> dict[int, int]:
    return _pool(tables, "rsm_ids")


def innate_pool(tables: ReferenceTables) -> list[int]:
    """Reações/suportes/movimentos dos skillsets + as inatas que as classes do jogo já usam."""
    ids = set(rsm_pool(tables))
    for job in tables.jobs.values():
        ids.update(i for i in job.innate_ability_ids if i in tables.abilities)
    return sorted(ids)


def is_valid_base_job(tables: ReferenceTables, job_id: int) -> bool:
    return job_id in tables.jobs and job_id not in RAMZA_JOB_IDS and category_for(job_id) is not None


def special_abilities(tables: ReferenceTables, klass: CustomClass) -> list[int]:
    return [i for i in klass.actions if i in tables.abilities and tables.abilities[i].ability_type in SPECIAL_TYPES]


def sanitize(tables: ReferenceTables, klass: CustomClass) -> tuple[CustomClass, list[str]]:
    """
    Confere a classe contra as tabelas do jogo. Habilidades desconhecidas,
    repetidas, no tipo de slot errado ou além do limite saem, com um aviso
    para cada caso. Classe base inválida é erro.
    """
    if not is_valid_base_job(tables, klass.base_job):
        raise CustomClassError(i18n.t("cc_err_base", job=klass.base_job))
    warnings: list[str] = []

    def clean(ids: list[int], pool: dict[int, int], limit: int, slot: str) -> list[int]:
        out: list[int] = []
        for ab_id in ids:
            if ab_id in out:
                continue
            if ab_id not in pool:
                warnings.append(i18n.t("cc_warn_dropped", id=ab_id, slot=slot))
                continue
            out.append(ab_id)
        if len(out) > limit:
            warnings.append(i18n.t("cc_warn_limit", slot=slot, n=limit))
            out = out[:limit]
        return out

    actions = clean(klass.actions, action_pool(tables), MAX_ACTIONS, i18n.t("cc_slot_action"))
    rsm = clean(klass.rsm, rsm_pool(tables), MAX_RSM, i18n.t("cc_slot_rsm"))
    innates = None
    if klass.innates is not None:
        pool = {i: 0 for i in innate_pool(tables)}
        innates = clean([i for i in klass.innates if i], pool, MAX_INNATES, i18n.t("cc_slot_innate"))
    equip = None
    if klass.equip is not None:
        equip = [f for f in EQUIP_FLAGS if f in klass.equip]
        for flag in klass.equip:
            if flag not in EQUIP_FLAGS:
                warnings.append(i18n.t("cc_warn_equip", flag=flag))

    def clamp(label: str, value: int, bounds: tuple[int, int]) -> int:
        low, high = bounds
        if not low <= value <= high:
            warnings.append(i18n.t("cc_warn_range", field=label, low=low, high=high))
        return max(low, min(high, value))

    multipliers = {k: clamp(f"{k} mult.", v, MULTIPLIER_RANGE) for k, v in klass.multipliers.items()}
    growths = {k: clamp(f"{k} growth", v, GROWTH_RANGE) for k, v in klass.growths.items()}
    move = clamp("Move", klass.move, MOVE_RANGE) if klass.move is not None else None
    jump = clamp("Jump", klass.jump, JUMP_RANGE) if klass.jump is not None else None
    evasion = clamp("C-Ev", klass.evasion, EVASION_RANGE) if klass.evasion is not None else None
    clean_class = replace(klass, actions=actions, rsm=rsm, innates=innates, equip=equip, multipliers=multipliers,
                          growths=growths, move=move, jump=jump, evasion=evasion)
    return clean_class, warnings


# ---------------------------------------------------------------------------
# Arquivos
# ---------------------------------------------------------------------------

def load_file(path: Path) -> CustomClass:
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, UnicodeDecodeError, ValueError) as exc:
        raise CustomClassError(i18n.t("cc_err_read", name=path.name, error=exc)) from exc
    return CustomClass.from_dict(data)


def save_file(klass: CustomClass, path: Path) -> Path:
    path.write_text(json.dumps(klass.to_dict(), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return path


def slug(name: str) -> str:
    text = re.sub(r"[^\w\- ]+", "", name, flags=re.UNICODE).strip().replace(" ", "_")
    return text[:40] or "classe"


def free_path(folder: Path, name: str) -> Path:
    """Caminho livre na biblioteca para uma classe com esse nome."""
    base = slug(name)
    path = folder / f"{base}{FILE_SUFFIX}"
    n = 2
    while path.exists():
        path = folder / f"{base}-{n}{FILE_SUFFIX}"
        n += 1
    return path


def list_library(folder: Path) -> list[tuple[Path, CustomClass]]:
    """Classes salvas na biblioteca, por nome. Arquivos quebrados são ignorados."""
    found = []
    for path in sorted(folder.glob(f"*{FILE_SUFFIX}")):
        try:
            found.append((path, load_file(path)))
        except CustomClassError:
            continue
    found.sort(key=lambda pair: pair[1].name.lower())
    return found


def import_file(source: Path, folder: Path, tables: ReferenceTables) -> tuple[Path, CustomClass, list[str]]:
    """Valida um arquivo recebido e grava uma cópia limpa na biblioteca."""
    klass, warnings = sanitize(tables, load_file(source))
    return save_file(klass, free_path(folder, klass.name)), klass, warnings


def find_in_library(folder: Path, filename: str) -> Optional[tuple[Path, CustomClass]]:
    for path, klass in list_library(folder):
        if path.name == filename:
            return path, klass
    return None
