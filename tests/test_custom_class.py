import json
import sqlite3
import xml.etree.ElementTree as ET

import pytest

from ramza_manager import custom_class, mod_builder, nxd_db, paths
from ramza_manager.custom_class import CustomClass, CustomClassError
from ramza_manager.tables import load_reference_tables


@pytest.fixture(scope="module")
def tables():
    return load_reference_tables(paths.data_dir())


def _spellblade(tables):
    knight, black_mage = tables.commands[7], tables.commands[tables.jobs[80].job_command_id]
    return CustomClass(
        name="Spellblade", skillset="Runeblade", base_job=76,
        actions=knight.action_ids[:3] + black_mage.action_ids[:3],
        rsm=knight.rsm_ids[:2], author="tester", description="Espada e magia.",
    )


def _entries(xml_text, tag):
    root = ET.fromstring(xml_text.encode("utf-8"))
    return {int(e.findtext("Id")): {c.tag: c.text for c in e} for e in root.findall(f"./Entries/{tag}")}


def test_roundtrip_file(tables, tmp_path):
    klass = _spellblade(tables)
    path = custom_class.save_file(klass, tmp_path / "x.ramzaclass.json")
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["format"] == custom_class.FORMAT and data["version"] == custom_class.FORMAT_VERSION
    assert custom_class.load_file(path) == klass


@pytest.mark.parametrize("data", [
    [], {"format": "other"}, {"format": "soloramza-class", "version": 99, "name": "X", "base_job": 76},
    {"format": "soloramza-class", "version": 1, "name": "", "base_job": 76},
    {"format": "soloramza-class", "version": 1, "name": "X", "base_job": "76"},
    {"format": "soloramza-class", "version": 1, "name": "X", "base_job": 76, "actions": ["1"]},
])
def test_bad_files_are_rejected(data):
    with pytest.raises(CustomClassError):
        CustomClass.from_dict(data)


def test_skillset_defaults_to_name_and_text_is_trimmed():
    klass = CustomClass.from_dict({"format": "soloramza-class", "version": 1,
                                   "name": "  Very   Long Name " + "x" * 40, "base_job": 76})
    assert klass.name.startswith("Very Long Name") and len(klass.name) == custom_class.MAX_NAME
    assert klass.skillset == klass.name


def test_sanitize_drops_bad_abilities(tables):
    klass = _spellblade(tables)
    rsm_id = klass.rsm[0]
    dirty = CustomClass(klass.name, klass.skillset, klass.base_job,
                        actions=klass.actions + [klass.actions[0], rsm_id, 9999], rsm=klass.rsm + [klass.actions[0]])
    clean, warnings = custom_class.sanitize(tables, dirty)
    assert clean.actions == klass.actions  # repetida fora, R/S/M e inexistente fora
    assert clean.rsm == klass.rsm
    assert len(warnings) == 3


def test_sanitize_limits_and_base(tables):
    pool = list(custom_class.action_pool(tables))
    clean, warnings = custom_class.sanitize(tables, CustomClass("X", "X", 76, actions=pool[:20]))
    assert len(clean.actions) == custom_class.MAX_ACTIONS and warnings
    for bad_base in (1, 2, 3, 100, 9999):  # Ramza, monstro, inexistente
        with pytest.raises(CustomClassError):
            custom_class.sanitize(tables, CustomClass("X", "X", bad_base, actions=pool[:1]))


def test_pools_exclude_monster_skillsets(tables):
    actions = custom_class.action_pool(tables)
    assert all(cmd in custom_class._COMMAND_IDS for cmd in actions.values())
    assert not set(actions) & set(custom_class.rsm_pool(tables))


def test_plan_uses_ramza_skillsets(tables):
    klass = _spellblade(tables)
    plan = mod_builder.plan_build(tables, None, None, custom=klass)
    assert plan.class_name == "Spellblade" and plan.source_job.id == 76
    jobs = _entries(plan.job_xml, "Job")
    assert {j: e["JobCommandId"] for j, e in jobs.items()} == {1: "25", 2: "26", 3: "27"}
    assert jobs[1]["EquippableItems"] == tables.jobs[76].fields["EquippableItems"]
    commands = _entries(plan.command_xml, "JobCommand")
    assert sorted(commands) == [25, 26, 27] == plan.ramza_command_ids
    for entry in commands.values():
        actions = [int(entry[f"AbilityId{i}"]) for i in range(1, 17)]
        rsm = [int(entry[f"ReactionSupportMovementId{i}"]) for i in range(1, 7)]
        assert actions == klass.actions + [0] * (16 - len(klass.actions))  # slots antigos zerados
        assert rsm == klass.rsm + [0] * (6 - len(klass.rsm))
    assert plan.ability_ids == klass.actions + klass.rsm


def test_regular_plan_has_no_command_table(tables):
    plan = mod_builder.plan_build(tables, 80, "Black Mage")
    assert plan.command_xml is None and plan.ramza_command_ids == []


def test_mod_folder_with_custom_class(tables, tmp_path):
    klass = _spellblade(tables)
    root = mod_builder.build_mod(mod_builder.plan_build(tables, None, None, custom=klass), tmp_path / "stage")
    assert (root / "FFTIVC/tables/enhanced/JobCommandData.xml").exists()
    config = json.loads((root / "ModConfig.json").read_text(encoding="utf-8"))
    plugin = config["PluginData"]["SoloRamzaManager"]
    assert plugin["ClassName"] == "Spellblade" and plugin["SourceJobId"] == 76
    assert CustomClass.from_dict(plugin["CustomClass"]) == klass


def _fake_db(path):
    con = sqlite3.connect(str(path))
    for lang in ("en", "ja"):
        con.execute(f'CREATE TABLE "Ability-{lang}" (Key INTEGER, Name TEXT, JpCost1 INTEGER, JpCost2 INTEGER)')
        con.executemany(f'INSERT INTO "Ability-{lang}" VALUES (?,?,?,?)', [(138, "Rend", 100, 0), (1, "Cure", 50, 0)])
        con.execute(f'CREATE TABLE "Job-{lang}" (Key INTEGER, Name TEXT, Unknown4 TEXT, Description TEXT, '
                    f'Unknown6 TEXT, "jobcommand+Id" INTEGER)')
        con.executemany(f'INSERT INTO "Job-{lang}" VALUES (?,?,?,?,?,?)',
                        [(1, "Squire", "", "d", "", 25), (2, "Squire", "", "d", "", 26),
                         (3, "Gallant Knight", "", "d", "", 27), (76, "Knight", "", "kd", "", 7)])
        con.execute(f'CREATE TABLE "JobCommand-{lang}" (Key INTEGER, Name TEXT)')
        con.executemany(f'INSERT INTO "JobCommand-{lang}" VALUES (?,?)',
                        [(7, "Arts of War"), (25, "Mettle"), (26, "Mettle"), (27, "Mettle")])
    con.commit()
    con.close()


def test_nxd_custom_edits(tmp_path):
    db = tmp_path / "t.sqlite"
    _fake_db(db)
    con = sqlite3.connect(str(db))
    changed = nxd_db.apply_class_edits(con, [138], 0, 76, (1, 2, 3), custom_name="Spellblade",
                                       custom_description="Espada e magia.", skillset_name="Runeblade",
                                       target_command_ids=(25, 26, 27))
    con.commit()
    assert "JobCommand-en" in changed and "JobCommand-ja" in changed
    for lang in ("en", "ja"):
        rows = con.execute(f'SELECT Key, Name, Unknown4, Description, "jobcommand+Id" FROM "Job-{lang}" '
                           'WHERE Key <= 3 ORDER BY Key').fetchall()
        assert rows == [(k, "Spellblade", "Spellblade", "Espada e magia.", 24 + k) for k in (1, 2, 3)]
        names = dict(con.execute(f'SELECT Key, Name FROM "JobCommand-{lang}"').fetchall())
        assert names == {7: "Arts of War", 25: "Runeblade", 26: "Runeblade", 27: "Runeblade"}
    con.close()
    assert nxd_db.read_jp_costs(db) == {138: 0, 1: 50}


def test_import_writes_clean_copy(tables, tmp_path):
    source = tmp_path / "shared.json"
    data = _spellblade(tables).to_dict()
    data["actions"] = data["actions"] + [9999]
    source.write_text(json.dumps(data), encoding="utf-8")
    library = tmp_path / "lib"
    library.mkdir()
    path, klass, warnings = custom_class.import_file(source, library, tables)
    assert path.name == "Spellblade.ramzaclass.json" and warnings
    path2, _, _ = custom_class.import_file(source, library, tables)
    assert path2.name == "Spellblade-2.ramzaclass.json"  # não sobrescreve
    (library / "broken.ramzaclass.json").write_text("{", encoding="utf-8")
    assert [k.name for _p, k in custom_class.list_library(library)] == ["Spellblade", "Spellblade"]
    assert 9999 not in custom_class.load_file(path).actions


def _tweaked(tables):
    klass = _spellblade(tables)
    klass.equip = ["Sword", "Rod", "Shield", "Robe", "Ring", "Bogus"]
    klass.innates = [472, 0]
    klass.multipliers = {"PA": 130, "MA": 300}
    klass.growths = {"MA": 40}
    klass.move, klass.jump, klass.evasion = 5, 3, 15
    return klass


def test_overrides_roundtrip_and_old_files(tables, tmp_path):
    klass, _ = custom_class.sanitize(tables, _tweaked(tables))
    path = custom_class.save_file(klass, tmp_path / "x.ramzaclass.json")
    assert custom_class.load_file(path) == klass
    v1 = {"format": "soloramza-class", "version": 1, "name": "Old", "base_job": 76, "actions": [138]}
    old = CustomClass.from_dict(v1)
    assert old.equip is None and old.innates is None and not old.multipliers and old.move is None
    assert old.job_overrides() == {}


def test_bad_job_block_is_rejected():
    base = {"format": "soloramza-class", "version": 2, "name": "X", "base_job": 76}
    for job in ([], {"equip": "Sword"}, {"innates": ["a"]}, {"multipliers": {"Luck": 5}}, {"move": "4"}):
        with pytest.raises(CustomClassError):
            CustomClass.from_dict({**base, "job": job})


def test_sanitize_overrides(tables):
    clean, warnings = custom_class.sanitize(tables, _tweaked(tables))
    assert clean.equip == ["Sword", "Rod", "Shield", "Robe", "Ring"]
    assert clean.innates == [472]
    assert clean.multipliers == {"PA": 130, "MA": 255}
    assert len(warnings) == 2  # 'Bogus' e MA 300


def test_plan_applies_overrides(tables):
    clean, _ = custom_class.sanitize(tables, _tweaked(tables))
    plan = mod_builder.plan_build(tables, None, None, custom=clean)
    job = _entries(plan.job_xml, "Job")[1]
    knight = tables.jobs[76].fields
    assert job["EquippableItems"] == "Sword, Rod, Shield, Robe, Ring"
    assert [job[f"InnateAbilityId{i}"] for i in range(1, 5)] == ["472", "0", "0", "0"]
    assert job["PAMultiplier"] == "130" and job["MAGrowth"] == "40"
    assert job["HPMultiplier"] == knight["HPMultiplier"]  # o resto vem da base
    assert (job["Move"], job["Jump"], job["CharacterEvasion"]) == ("5", "3", "15")
    assert job["JobCommandId"] == "25"
    # equipamento inicial segue o equipamento da classe customizada, não o da base
    assert "RightWeapon" not in plan.spawn_changes  # Broadsword é Sword, permitido
    assert "Armor" in plan.spawn_changes or "Helmet" in plan.spawn_changes  # sem Clothing/Hat


def test_innate_pool_has_existing_innates(tables):
    pool = set(custom_class.innate_pool(tables))
    for job in tables.jobs.values():
        assert set(job.innate_ability_ids) <= pool | {i for i in job.innate_ability_ids if i not in tables.abilities}
