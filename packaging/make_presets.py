"""Gera data/classes/*.ramzaclass.json (classes de fábrica). Rodar da raiz: .venv\Scripts\python packaging\make_presets.py"""
import os
import sys
from pathlib import Path

sys.path.insert(0, os.getcwd())
from ramza_manager import custom_class, paths
from ramza_manager.custom_class import CustomClass
from ramza_manager.tables import load_reference_tables

t = load_reference_tables(paths.data_dir())
AUTHOR = "Solo Ramza Manager"
LIGHT_ACC = ["Shoes", "Armguard", "Ring", "Armlet", "Cloak", "Perfume"]

PRESETS = [
    dict(
        file="red_mage", name="Red Mage", skillset="Red Magicks", base_job=80,
        description="A swordsman who dabbles in both white and black magicks. Jack of all trades, master of none.",
        actions=[1, 2, 5, 8, 9, 11, 14, 16, 17, 20, 21, 24, 25, 32, 34, 39],
        rsm=[435, 467, 482, 468, 486],
        equip=["Unarmed", "Knife", "Sword", "Rod", "Hat", "Clothing", "Robe", "Shield"] + LIGHT_ACC,
        multipliers={"HP": 100, "MP": 110, "PA": 100, "MA": 115},
    ),
    dict(
        file="mystic_knight", name="Mystic Knight", skillset="Spellblade", base_job=76,
        description="A knight who channels magick through the blade, afflicting foes with every strike.",
        actions=[234, 235, 236, 237, 240, 241, 243, 244, 245, 246, 247, 16, 20, 24, 142, 145],
        rsm=[447, 435, 467, 482, 486],
        multipliers={"MP": 100, "MA": 105},
    ),
    dict(
        file="paladin", name="Paladin", skillset="Holy Arts", base_job=76,
        description="A holy knight sworn to protect. Wields sacred sword arts and healing prayers.",
        actions=[155, 156, 157, 158, 159, 1, 2, 5, 9, 11, 14],
        rsm=[447, 428, 475, 468, 486],
        multipliers={"MP": 100, "MA": 100},
    ),
    dict(
        file="dark_knight", name="Dark Knight", skillset="Darkness", base_job=76,
        description="A knight who trades light for power, sapping the strength and life of all who oppose him.",
        actions=[164, 165, 196, 197, 198, 199, 235, 236, 241, 28, 30],
        rsm=[442, 438, 465, 476, 486],
        equip=["Unarmed", "Sword", "KnightSword", "FellSword", "Katana", "Axe", "Helmet", "Armor", "Robe"]
        + LIGHT_ACC,
        multipliers={"HP": 130, "PA": 130, "MA": 90},
        evasion=5,
    ),
    dict(
        file="sage", name="Sage", skillset="Sage Magicks", base_job=79,
        description="A scholar who has mastered both white and black magicks, at the cost of a frail body.",
        actions=[1, 2, 3, 5, 6, 9, 11, 14, 15, 17, 18, 21, 22, 25, 26, 31],
        rsm=[428, 435, 467, 482, 494, 486],
        equip=["Unarmed", "Rod", "Staff", "Book", "Hat", "Clothing", "Robe"] + LIGHT_ACC,
        multipliers={"MA": 130},
    ),
    dict(
        file="ranger", name="Ranger", skillset="Marksmanship", base_job=77,
        description="A hunter who picks targets apart from afar with bow, crossbow and gun.",
        actions=[406, 407, 408, 410, 412, 213, 214, 215],
        rsm=[424, 452, 469, 471, 487],
        equip=["Unarmed", "Knife", "Bow", "Crossbow", "Gun", "Hat", "HairAdornment", "Clothing"] + LIGHT_ACC,
        multipliers={"Speed": 105},
        move=4,
    ),
    dict(
        file="battle_monk", name="Battle Monk", skillset="Fist Arts", base_job=78,
        description="A monk who fights on the front line, rallying himself with war cries between blows.",
        actions=[100, 101, 102, 103, 104, 105, 106, 107, 146, 150, 151, 153],
        rsm=[442, 431, 465, 493, 486],
        move=4,
    ),
]

out_dir = paths.data_dir() / "classes"
out_dir.mkdir(exist_ok=True)
for spec in PRESETS:
    spec = dict(spec)
    filename = spec.pop("file")
    klass = CustomClass(author=AUTHOR, **spec)
    clean, warnings = custom_class.sanitize(t, klass)
    assert not warnings, (klass.name, warnings)
    assert (clean.actions, clean.rsm) == (klass.actions, klass.rsm), klass.name
    path = custom_class.save_file(clean, out_dir / f"{filename}{custom_class.FILE_SUFFIX}")
    print(path.name, len(clean.actions), len(clean.rsm), clean.job_overrides())
