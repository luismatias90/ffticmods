"""Configurações do usuário (caminhos detectados, escolhas da run), em JSON."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from typing import Optional

from . import paths
from .mod_builder import DEFAULT_JP_COST


@dataclass
class Settings:
    game_root: str = ""
    reloaded_root: str = ""
    jp_cost: int = DEFAULT_JP_COST
    change_class: bool = True
    class_job_id: Optional[int] = None
    custom_class_file: str = ""  # caminho da classe customizada; vazio = classe do jogo
    change_bag: bool = False
    bag_items: list = field(default_factory=list)  # [[item_id, quantidade], ...]
    language: str = ""  # "pt" ou "en"; vazio até o assistente perguntar
    wizard_done: bool = False

    @classmethod
    def load(cls) -> "Settings":
        try:
            data = json.loads(paths.settings_file().read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return cls()
        known = {k: v for k, v in data.items() if k in cls.__dataclass_fields__}
        return cls(**known)

    def save(self) -> None:
        paths.settings_file().write_text(json.dumps(asdict(self), indent=2), encoding="utf-8")
