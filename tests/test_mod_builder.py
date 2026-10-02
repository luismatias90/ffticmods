import json
import sqlite3
import struct
import xml.etree.ElementTree as ET
import zlib

import pytest

from ramza_manager import class_catalog, mod_builder, nxd_db, paths, sprites
from ramza_manager.tables import load_reference_tables


@pytest.fixture(scope="module")
def tables():
    return load_reference_tables(paths.data_dir())


def _jobs_in(xml_text):
    root = ET.fromstring(xml_text.encode("utf-8"))
    return {int(j.findtext("Id")): {c.tag: c.text for c in j} for j in root.findall("./Entries/Job")}


def test_reference_tables_know_ramza(tables):
    assert tables.jobs[1].job_command_id == 25
    assert tables.jobs[30].job_command_id == 40
    assert tables.spawns[2]["RightWeapon"] == "19"


def test_holy_knight_rewrites_only_ramza_jobs(tables):
    plan = mod_builder.plan_build(tables, 30, "Holy Knight")
    jobs = _jobs_in(plan.job_xml)
    assert sorted(jobs) == [1, 2, 3]
    for entry in jobs.values():
        assert entry["JobCommandId"] == "40"
        assert "KnightSword" in entry["EquippableItems"]
        assert "ImmuneStatus" not in entry  # mantém a imunidade original do Ramza
        assert "MonsterGraphic" not in entry
    assert plan.ability_ids == tables.commands[40].all_ability_ids


def test_ramza_own_job_is_rejected(tables):
    with pytest.raises(ValueError):
        mod_builder.plan_build(tables, 2, "Squire")


def test_starting_gear_follows_class(tables):
    # Mago Negro não usa espada: a Broadsword vira o item básico de uma arma permitida.
    changes = mod_builder.starting_gear_changes(tables, tables.jobs[80])
    old, new = changes["RightWeapon"]
    assert old == 19
    assert tables.items[new].category in tables.jobs[80].equippable
    # Sword Saint usa tudo o que o Ramza começa equipado.
    assert mod_builder.starting_gear_changes(tables, tables.jobs[13]) == {}


def test_dont_learn_with_jp_is_cleared(tables):
    blocked = [a.id for a in tables.abilities.values() if "DontLearnWithJP" in a.flags]
    if not blocked:
        pytest.skip("nenhuma habilidade com DontLearnWithJP")
    target = next(
        (cmd for cmd in tables.commands.values() if set(cmd.all_ability_ids) & set(blocked)), None
    )
    job = next((j for j in tables.jobs.values() if target and j.job_command_id == target.id and j.id not in (1, 2, 3)), None)
    if job is None:
        pytest.skip("nenhuma classe usa essas habilidades")
    plan = mod_builder.plan_build(tables, job.id, "X")
    assert plan.ability_xml and "DontLearnWithJP" not in plan.ability_xml


def test_catalog_categories(tables):
    catalog = class_catalog.build_catalog(tables)
    ids = {o.job_id for o in catalog}
    assert not ids & set(class_catalog.RAMZA_JOB_IDS)
    assert 80 in ids and 30 in ids
    assert not any(94 <= i <= 141 for i in ids)  # sem monstros


def _fake_db(path):
    con = sqlite3.connect(str(path))
    for lang in ("en", "ja"):
        con.execute(f'CREATE TABLE "Ability-{lang}" (Key INTEGER, Name TEXT, JpCost1 INTEGER, JpCost2 INTEGER)')
        con.executemany(f'INSERT INTO "Ability-{lang}" VALUES (?,?,?,?)',
                        [(155, "Judgment Blade", 100, 0), (156, "Cleansing", 144, 1), (1, "Cure", 50, 0)])
        con.execute(
            f'CREATE TABLE "Job-{lang}" (Key INTEGER, Name TEXT, Unknown4 TEXT, Description TEXT, '
            f'Unknown6 TEXT, "jobcommand+Id" INTEGER, TexturePartsIndex INTEGER)'
        )
        con.executemany(f'INSERT INTO "Job-{lang}" VALUES (?,?,?,?,?,?,?)',
                        [(1, "Squire", "", "d", "", 25, 21), (2, "Squire", "", "d", "", 26, 21),
                         (3, "Gallant Knight", "", "d", "", 27, 21),
                         (30, "Holy Knight" if lang == "en" else None, "", "hk", "", 40, 9)])
    con.commit()
    con.close()


def test_apply_edits_touches_only_selected_rows(tmp_path):
    db = tmp_path / "t.sqlite"
    _fake_db(db)
    con = sqlite3.connect(str(db))
    changed = nxd_db.apply_class_edits(con, [155, 156], 0, 30, (1, 2, 3))
    con.commit()
    con.close()
    assert set(changed) == {"Ability-en", "Job-en", "Ability-ja", "Job-ja"}
    costs = nxd_db.read_jp_costs(db)
    assert costs == {155: 0, 156: 0, 1: 50}
    con = sqlite3.connect(str(db))
    rows = con.execute('SELECT Key, Name, "jobcommand+Id", TexturePartsIndex FROM "Job-en" ORDER BY Key').fetchall()
    assert rows[:3] == [(1, "Holy Knight", 40, 21), (2, "Holy Knight", 40, 21), (3, "Holy Knight", 40, 21)]
    # Idioma sem nome para a classe: mantém o texto do Ramza, troca só o skillset.
    rows = con.execute('SELECT Key, Name, "jobcommand+Id" FROM "Job-ja" WHERE Key <= 3').fetchall()
    assert rows == [(1, "Squire", 40), (2, "Squire", 40), (3, "Gallant Knight", 40)]
    con.close()


def test_jp_cost_split_into_two_bytes(tmp_path):
    db = tmp_path / "t.sqlite"
    _fake_db(db)
    con = sqlite3.connect(str(db))
    nxd_db.apply_class_edits(con, [155], 300, 30, (1,))
    con.commit()
    con.close()
    assert nxd_db.read_jp_costs(db)[155] == 300


def test_mod_folder_layout(tables, tmp_path):
    plan = mod_builder.plan_build(tables, 80, "Black Mage")
    root = mod_builder.build_mod(plan, tmp_path / "stage")
    config = json.loads((root / "ModConfig.json").read_text(encoding="utf-8"))
    assert config["ModId"] == mod_builder.MOD_ID
    assert config["ModDependencies"] == ["fftivc.utility.modloader"]
    assert config["SupportedAppId"] == ["fft_enhanced.exe"]
    assert (root / "FFTIVC/tables/enhanced/JobData.xml").exists()
    assert (root / "FFTIVC/tables/enhanced/SpawnData.xml").exists()

    mods = tmp_path / "Mods"
    mods.mkdir()
    mod_builder.install_mod(root, mods)
    assert mod_builder.read_installed_class(mods) == "Black Mage"
    assert mod_builder.uninstall_mod(mods)
    assert mod_builder.read_installed_class(mods) is None


def _fake_bonus_db(path):
    con = sqlite3.connect(str(path))
    con.execute('CREATE TABLE "SystemBonusItemContents" (Key INTEGER, Key2 INTEGER, DLCFlags INTEGER, UnionId TEXT)')
    con.executemany('INSERT INTO "SystemBonusItemContents" VALUES (?,?,?,?)', [
        (1, 0, 0, "Item:2"), (1, 1, 0, "SystemBonusSpecialItem:5"),
        (2, 0, 0, "Item:257"), (2, 1, 0, "SystemBonusSpecialItem:3"),
        (2, 2, 0, "SystemBonusSpecialItem:2"), (2, 3, 0, "SystemBonusSpecialItem:1"),
    ])
    for lang in ("en", "ja"):
        con.execute(f'CREATE TABLE "SystemBonusSpecialItem-{lang}" (Key INTEGER, DLCFlags INTEGER, Comment TEXT, '
                    'UnionId TEXT, Quantity INTEGER, Caption TEXT)')
        con.executemany(f'INSERT INTO "SystemBonusSpecialItem-{lang}" VALUES (?,?,?,?,?,?)', [
            (1, 0, None, "120:25", 1, "Red Equipment for Ramza"),
            (2, 0, None, "120:26", 1, "Black Equipment for Ramza"),
            (3, 0, None, "Item:253", 10, "10 Tufts of Phoenix Down"),
            (5, 0, None, "Item:241", 10, "10 High Potions"),
        ])
        con.execute(f'CREATE TABLE "SystemBonusItem-{lang}" (Key INTEGER, DLCFlags INTEGER, Title TEXT, '
                    'Description TEXT, UnionId TEXT, Comment TEXT)')
        con.execute(f'INSERT INTO "SystemBonusItem-{lang}" VALUES (2, 0, "Deluxe", "old", "SystemBonusEntitlement:2", NULL)')
        con.execute(f'CREATE TABLE "Item-{lang}" (Key INTEGER, Name TEXT, NameSingular TEXT)')
        con.executemany(f'INSERT INTO "Item-{lang}" VALUES (?,?,?)',
                        [(240, "Elixir" if lang == "en" else None, None if lang == "en" else "エリクサー"),
                         (19, "Broadsword", "Broadsword")])
    con.commit()
    con.close()


def test_read_bonus_items(tmp_path):
    db = tmp_path / "b.sqlite"
    _fake_bonus_db(db)
    items = nxd_db.read_bonus_items(db)
    assert [(b.item_id, b.quantity) for b in items] == [(257, 1), (253, 10)]


def test_bag_replaces_deluxe_contents_and_keeps_colors(tmp_path):
    db = tmp_path / "b.sqlite"
    _fake_bonus_db(db)
    con = sqlite3.connect(str(db))
    bag = [nxd_db.BagItem(240, 20), nxd_db.BagItem(19, 1), nxd_db.BagItem(241, 5)]
    changed = nxd_db.apply_bag_edits(con, bag, {241: "X-Potion"})
    con.commit()
    assert "SystemBonusItemContents" in changed and "SystemBonusSpecialItem-ja" in changed
    rows = con.execute('SELECT Key, Key2, UnionId FROM "SystemBonusItemContents" ORDER BY rowid').fetchall()
    assert rows == [
        (1, 0, "Item:2"), (1, 1, "SystemBonusSpecialItem:5"),  # pré-venda intocado
        (2, 0, "SystemBonusSpecialItem:3"),  # 1ª quantidade reaproveita a linha original
        (2, 1, "Item:19"),                   # avulso entra direto, como os itens da Deluxe
        (2, 2, "SystemBonusSpecialItem:6"),  # quantidade extra: próxima chave em sequência
        (2, 3, "SystemBonusSpecialItem:2"), (2, 4, "SystemBonusSpecialItem:1"),  # cores mantidas
    ]
    special = con.execute('SELECT Key, UnionId, Quantity, Caption FROM "SystemBonusSpecialItem-en" ORDER BY rowid').fetchall()
    assert special == [
        (1, "120:25", 1, "Red Equipment for Ramza"), (2, "120:26", 1, "Black Equipment for Ramza"),
        (3, "Item:240", 20, "Elixir × 20"), (5, "Item:241", 10, "10 High Potions"),
        (6, "Item:241", 5, "X-Potion × 5"),
    ]
    ja = con.execute('SELECT Caption FROM "SystemBonusSpecialItem-ja" WHERE Key = 3').fetchone()[0]
    assert ja == "エリクサー × 20"  # nome do idioma, via NameSingular
    desc = con.execute('SELECT Description FROM "SystemBonusItem-en" WHERE Key = 2').fetchone()[0]
    assert desc.splitlines() == ["- Elixir × 20", "- Broadsword", "- X-Potion × 5",
                                 "- Black Equipment for Ramza", "- Red Equipment for Ramza"]
    con.close()
    assert [(b.item_id, b.quantity) for b in nxd_db.read_bonus_items(db)] == [(240, 20), (19, 1), (241, 5)]


def test_single_items_need_no_new_special_rows(tmp_path):
    db = tmp_path / "b.sqlite"
    _fake_bonus_db(db)
    con = sqlite3.connect(str(db))
    changed = nxd_db.apply_bag_edits(con, [nxd_db.BagItem(19, 1)], {})
    con.commit()
    assert not any(t.startswith("SystemBonusSpecialItem") for t in changed)
    keys = [k for (k,) in con.execute('SELECT Key FROM "SystemBonusSpecialItem-en"')]
    assert keys == [1, 2, 3, 5]
    con.close()


def test_sprite_catalog_is_human_sheets_only():
    stems = [option.stem for option in sprites.CATALOG]
    assert len(stems) == len(set(stems))
    assert sprites.get("aguri").name_en == "Agrias"
    assert sprites.get("ramuza") is None
    assert sprites.game_path("knight_m") == "fftpack/unit/battle_knight_m_spr.bin"
    for option in sprites.CATALOG:
        top = sprites.hd_top_index(option.stem)
        assert top not in sprites.RAMZA_G2D_TOPS and top + 1 not in sprites.RAMZA_G2D_TOPS
    assert set(sprites._FACE) <= {o.stem for o in sprites.CATALOG}
    assert not set(sprites._FACE.values()) & set(sprites.RAMZA_FACES)
    assert sprites.has_portrait("zaru") and not sprites.has_portrait("ledy")


def _fake_g2d(textures: list[bytes]) -> bytes:
    body = bytearray(b"\0" * 2048)
    toc = bytearray()
    for data in textures:
        packed = b"YOX\0" + struct.pack("<III", 6, len(data), 0) + zlib.compress(data)
        toc += struct.pack("<IIII", len(body), len(packed), 6, 0)
        body += packed + b"\0" * (-len(packed) % 2048)
    struct.pack_into("<4sIII", body, 0, b"YOX\0", 0, len(body), len(textures))
    return bytes(body + toc)


def test_g2d_texture_reads_by_table_index():
    archive = _fake_g2d([b"zero", b"one" * 100, b"two"])
    assert sprites.g2d_texture(archive, 0) == b"zero"
    assert sprites.g2d_texture(archive, 1) == b"one" * 100
    assert sprites.g2d_texture(archive, 2) == b"two"
    with pytest.raises(ValueError):
        sprites.g2d_texture(archive, 3)


def test_sprite_replaces_ramzas_three_sheets(tables, tmp_path):
    plan = mod_builder.plan_build(tables, None, None, sprite_stem="aguri", sprite_name="Agrias")
    assert not plan.is_empty
    assert plan.job_xml is None
    assets = sprites.SpriteAssets(b"SPRITE", b"TOP", b"BOTTOM")
    root = mod_builder.build_mod(plan, tmp_path / "stage", sprite=assets)
    data = root / "FFTIVC" / "data" / "enhanced"
    for name in ("battle_ramuza_spr.bin", "battle_ramuza2_spr.bin", "battle_ramuza3_spr.bin"):
        assert (data / "fftpack" / "unit" / name).read_bytes() == b"SPRITE"
    g2d = data / "system" / "ffto" / "g2d"
    assert sorted(p.name for p in g2d.iterdir()) == [f"tex_{i}.bin" for i in range(830, 836)]
    for top in (830, 832, 834):
        assert (g2d / f"tex_{top}.bin").read_bytes() == b"TOP"
        assert (g2d / f"tex_{top + 1}.bin").read_bytes() == b"BOTTOM"
    assert not (data / "nxd").exists() and not (data / "ui").exists()
    config = json.loads((root / "ModConfig.json").read_text(encoding="utf-8"))
    plugin = config["PluginData"]["SoloRamzaManager"]
    assert plugin["SpriteStem"] == "aguri"
    assert plugin["SpriteName"] == "Agrias"


def test_sprite_writes_colors_and_portrait(tables, tmp_path):
    plan = mod_builder.plan_build(tables, None, None, sprite_stem="zaru", sprite_name="Zalbaag")
    portrait = sprites.ramza_portrait_files(b"FACE", b"PARTS")
    assets = sprites.SpriteAssets(b"SPRITE", b"TOP", b"BOTTOM", b"CLUT", portrait)
    data = mod_builder.build_mod(plan, tmp_path / "stage", sprite=assets) / "FFTIVC" / "data" / "enhanced"
    assert (data / "nxd" / "charclut.nxd").read_bytes() == b"CLUT"
    faces = data / "ui" / "ffto" / "common" / "face"
    assert len(list((faces / "texture").iterdir())) == 12
    assert (faces / "texture" / "wldface_002_10_uitx.tex").read_bytes() == b"FACE"
    assert (faces / "textureparts" / "wldface_003_11_uitx.utexpt").read_bytes() == b"PARTS"


def test_ramza_clut_rows_get_the_sheet_palette():
    classic = struct.pack("<16H", 0, 0x7FFF, 0x001F, *range(13)) + b"\0" * 480
    clut = sprites.classic_clut(classic)
    assert clut[:9] == [0, 0, 0, 248, 248, 248, 248, 0, 0]
    con = sqlite3.connect(":memory:")
    con.execute('CREATE TABLE "CharCLUT" (Key, Key2, CLUTData)')
    con.executemany('INSERT INTO "CharCLUT" VALUES (?, ?, ?)', [(k, k2, "old") for k in (1, 2, 3, 254) for k2 in (0, 1)])
    sprites.apply_ramza_clut(con, clut)
    rows = dict(((k, k2), d) for k, k2, d in con.execute('SELECT * FROM "CharCLUT"'))
    assert json.loads(rows[(3, 1)]) == clut
    assert rows[(254, 0)] == "old"


def test_bag_only_plan_does_not_touch_class(tables, tmp_path):
    bag = [nxd_db.BagItem(240, 150), nxd_db.BagItem(240, 5), nxd_db.BagItem(9999, 1)]
    plan = mod_builder.plan_build(tables, None, None, bag)
    assert plan.job_xml is None and plan.source_job is None
    assert [(b.item_id, b.quantity) for b in plan.bag] == [(240, 99)]  # somado, limitado, inválido fora
    root = mod_builder.build_mod(plan, tmp_path / "stage")
    assert not (root / "FFTIVC" / "tables").exists()
    config = json.loads((root / "ModConfig.json").read_text(encoding="utf-8"))
    assert config["PluginData"]["SoloRamzaManager"]["BagItems"] == [[240, 99]]
