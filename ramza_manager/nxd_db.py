"""
Tabelas nex (.nxd) do jogo: extração para um SQLite de referência, leitura de
nomes e geração dos .nxd modificados.

Por que precisamos disso:
- o custo de JP que o jogo usa de verdade está na tabela nex `Ability`
  (JpCost1 = byte baixo, JpCost2 = byte alto); o <JPCost> do AbilityData.xml é
  ignorado. A tabela nex `Job` guarda o nome da classe e uma cópia do
  skillset (`jobcommand+Id`);
- os itens de bônus (pacote da Deluxe Edition) estão em SystemBonusItem
  (título/descrição), SystemBonusItemContents (o que vem no pacote) e
  SystemBonusSpecialItem (item + quantidade + legenda).

Um .nxd no mod substitui o arquivo inteiro do jogo, então sempre partimos de
uma cópia do banco original e mexemos só nas linhas necessárias.
Fluxo de exportação baseado em mod_studio/qt/nxd_export.py (GPL-3).
"""

from __future__ import annotations

import shutil
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable, Optional

from . import ff16tools, game_install, i18n

LineCb = Optional[Callable[[str], None]]

LANGUAGES = ("en", "ja", "de", "fr", "cs", "ct", "ko")

# Tabelas por idioma (arquivo <nome>.<idioma>.nxd) e tabelas únicas (<nome>.nxd).
LOCALIZED_TABLES = ("Ability", "Job", "JobCommand", "Item", "SystemBonusItem", "SystemBonusSpecialItem")
SHARED_TABLES = ("SystemBonusItemContents",)

# Colunas de texto de Job-<idioma> copiadas da classe escolhida para as do
# Ramza. Unknown4/Unknown6 são as formas femininas (nome/descrição).
JOB_TEXT_COLUMNS = ("Name", "Unknown4", "Description", "Unknown6")

# Pacote de bônus da Deluxe Edition (SystemBonusEntitlement 2). O de
# pré-venda é o 1.
DELUXE_BONUS_KEY = 2
# Testado no jogo: uma linha nova de SystemBonusSpecialItem com Key 100 aparece
# na descrição mas o item NÃO é entregue. Por isso só usamos caminhos que a
# própria Deluxe usa: item avulso direto no pacote ("Item:N") e, para
# quantidade > 1, a linha 3 do SpecialItem (Phoenix Down x10 original);
# quantidades extras ganham linhas em sequência logo após a maior existente.
DELUXE_QUANTITY_SPECIAL_KEY = 3
# SystemBonusSpecialItem cujo UnionId começa assim são as cores do Ramza,
# não itens. Mantidas no pacote.
COLOR_UNION_PREFIX = "120:"
MAX_QUANTITY = 99


@dataclass
class BagItem:
    item_id: int
    quantity: int


def nxd_filename(table: str) -> str:
    """'Ability-en' -> 'ability.en.nxd'; 'SystemBonusItemContents' -> 'systembonusitemcontents.nxd'."""
    if "-" in table:
        prefix, lang = table.rsplit("-", 1)
        return f"{prefix.lower()}.{lang}.nxd"
    return f"{table.lower()}.nxd"


def needed_filenames() -> list[str]:
    names = [nxd_filename(f"{t}-{lang}") for t in LOCALIZED_TABLES for lang in LANGUAGES]
    return names + [nxd_filename(t) for t in SHARED_TABLES]


REQUIRED_TABLES = {f"{t}-en" for t in LOCALIZED_TABLES} | set(SHARED_TABLES)


# ---------------------------------------------------------------------------
# Extração
# ---------------------------------------------------------------------------

def extract_vanilla_db(game_root: Path, cli: Path, cache: Path, db_path: Path, line_cb: LineCb = None) -> Path:
    """
    Extrai as tabelas necessárias (.nxd) dos .pac originais da versão
    Enhanced e converte para `db_path`. Só lê a pasta do jogo.
    """
    log = line_cb or (lambda _msg: None)
    unpack_dir = cache / "unpacked"
    stage_dir = cache / "stage_nxd"
    for d in (unpack_dir, stage_dir):
        shutil.rmtree(d, ignore_errors=True)
        d.mkdir(parents=True)

    needed = needed_filenames()
    packs = game_install.vanilla_pack_files(game_install.enhanced_pack_dir(game_root))
    if not packs:
        raise RuntimeError(i18n.t("nxd_no_pac"))

    for pack in packs:
        if all((unpack_dir / "nxd" / name).exists() for name in needed):
            break
        log(i18n.t("nxd_scanning", name=pack.name))
        code = ff16tools.unpack_pack(cli, pack, unpack_dir, "nxd/", None)
        if code != 0:
            raise RuntimeError(i18n.t("nxd_ff16_fail", name=pack.name, code=code))

    missing = [n for n in needed if not (unpack_dir / "nxd" / n).exists()]
    required = {nxd_filename(t) for t in REQUIRED_TABLES}
    if required & set(missing):
        raise RuntimeError(i18n.t("nxd_missing", names=", ".join(sorted(required & set(missing)))))
    if missing:
        log(i18n.t("nxd_warn", names=", ".join(missing)))

    for name in needed:
        src = unpack_dir / "nxd" / name
        if src.exists():
            shutil.copy(src, stage_dir / name)

    log(i18n.t("nxd_sqlite"))
    tmp_db = db_path.with_suffix(".tmp")
    tmp_db.unlink(missing_ok=True)
    code = ff16tools.nxd_to_sqlite(cli, stage_dir, tmp_db, None)
    if code != 0 or not tmp_db.exists():
        raise RuntimeError(i18n.t("nxd_sqlite_fail", code=code))
    tmp_db.replace(db_path)
    shutil.rmtree(unpack_dir, ignore_errors=True)
    shutil.rmtree(stage_dir, ignore_errors=True)
    log(i18n.t("nxd_ready"))
    return db_path


# ---------------------------------------------------------------------------
# Leitura
# ---------------------------------------------------------------------------

def _tables(con: sqlite3.Connection) -> set[str]:
    return {r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table'")}


def _columns(con: sqlite3.Connection, table: str) -> list[str]:
    return [r[1] for r in con.execute(f'PRAGMA table_info("{table}")')]


def is_valid_db(db_path: Path) -> bool:
    """True se o banco tem todas as tabelas que esta versão do app usa."""
    if not db_path.is_file():
        return False
    try:
        con = sqlite3.connect(str(db_path))
        try:
            return REQUIRED_TABLES <= _tables(con)
        finally:
            con.close()
    except sqlite3.Error:
        return False


def read_names(db_path: Path, prefix: str, language: str = "en") -> dict[int, str]:
    con = sqlite3.connect(str(db_path))
    try:
        return _names(con, f"{prefix}-{language}")
    finally:
        con.close()


def _names(con: sqlite3.Connection, table: str) -> dict[int, str]:
    # Item-ja/ko deixam Name vazio e usam NameSingular.
    cols = [c for c in ("Name", "NameSingular") if c in _columns(con, table)]
    rows = con.execute(f'SELECT Key, {", ".join(cols)} FROM "{table}"').fetchall()
    return {int(r[0]): next((v for v in r[1:] if v), "") for r in rows}


def read_jp_costs(db_path: Path, language: str = "en") -> dict[int, int]:
    con = sqlite3.connect(str(db_path))
    try:
        rows = con.execute(f'SELECT Key, JpCost1, JpCost2 FROM "Ability-{language}"').fetchall()
    finally:
        con.close()
    return {int(k): (int(a or 0) & 0xFF) | ((int(b or 0) & 0xFF) << 8) for k, a, b in rows}


def read_bonus_items(db_path: Path, bonus_key: int = DELUXE_BONUS_KEY) -> list[BagItem]:
    """Os itens (sem as cores do Ramza) que vêm hoje no pacote de bônus."""
    con = sqlite3.connect(str(db_path))
    try:
        specials = {
            int(k): (u or "", int(q or 1))
            for k, u, q in con.execute('SELECT Key, UnionId, Quantity FROM "SystemBonusSpecialItem-en"')
        }
        items = []
        for (union,) in con.execute(
            'SELECT UnionId FROM "SystemBonusItemContents" WHERE Key = ? ORDER BY Key2', (bonus_key,)
        ):
            kind, _, ref = (union or "").partition(":")
            if kind == "Item":
                items.append(BagItem(int(ref), 1))
            elif kind == "SystemBonusSpecialItem":
                target, qty = specials.get(int(ref), ("", 1))
                if target.startswith("Item:"):
                    items.append(BagItem(int(target.split(":")[1]), qty))
        return items
    finally:
        con.close()


# ---------------------------------------------------------------------------
# Edição
# ---------------------------------------------------------------------------

def apply_class_edits(
    con: sqlite3.Connection,
    ability_ids: Iterable[int],
    jp_cost: int,
    source_job_id: int,
    target_job_ids: Iterable[int],
    custom_name: Optional[str] = None,
    custom_description: str = "",
    skillset_name: Optional[str] = None,
    target_command_ids: Iterable[int] = (),
) -> list[str]:
    """
    - Ability-<idioma>: JpCost das habilidades do skillset -> jp_cost.
    - Job-<idioma>: nas linhas do Ramza, `jobcommand+Id` e nome/descrição da
      classe escolhida. O resto da linha (retrato, tipo, ajuda) fica do Ramza.

    Classe customizada (`target_command_ids` preenchido): o Ramza mantém os
    próprios skillsets, que ganham o nome `skillset_name` em
    JobCommand-<idioma>; o nome da classe (e a descrição, se houver) é
    `custom_name` em todos os idiomas.
    """
    ability_ids = sorted(set(ability_ids))
    target_job_ids = list(target_job_ids)
    target_command_ids = list(target_command_ids)
    low, high = jp_cost & 0xFF, (jp_cost >> 8) & 0xFF
    changed: list[str] = []
    present = _tables(con)
    for lang in LANGUAGES:
        table = f"Ability-{lang}"
        if table in present and ability_ids:
            marks = ",".join("?" * len(ability_ids))
            con.execute(
                f'UPDATE "{table}" SET JpCost1 = ?, JpCost2 = ? WHERE Key IN ({marks})',
                [low, high, *ability_ids],
            )
            changed.append(table)

        table = f"Job-{lang}"
        if table in present:
            cols = ["jobcommand+Id", *JOB_TEXT_COLUMNS]
            select = ", ".join(f'"{c}"' for c in cols)
            row = con.execute(f'SELECT {select} FROM "{table}" WHERE Key = ?', (source_job_id,)).fetchone()
            if row is None:
                continue
            values = dict(zip(cols, row))
            if custom_name:
                values["Name"] = values["Unknown4"] = custom_name
                if custom_description:
                    values["Description"] = values["Unknown6"] = custom_description
            elif not values.get("Name"):
                # Idioma sem tradução para esta classe: mantém o texto do
                # Ramza, troca só o skillset.
                values = {"jobcommand+Id": values["jobcommand+Id"]}
            if target_command_ids:
                values.pop("jobcommand+Id")  # continua o skillset próprio do Ramza
            assign = ", ".join(f'"{c}" = ?' for c in values)
            for target in target_job_ids:
                con.execute(f'UPDATE "{table}" SET {assign} WHERE Key = ?', [*values.values(), target])
            changed.append(table)

        table = f"JobCommand-{lang}"
        if table in present and target_command_ids and skillset_name:
            marks = ",".join("?" * len(target_command_ids))
            con.execute(f'UPDATE "{table}" SET Name = ? WHERE Key IN ({marks})', [skillset_name, *target_command_ids])
            changed.append(table)
    return changed


def _resort(con: sqlite3.Connection, table: str, order: str) -> None:
    """Regrava a tabela ordenada (o FF16Tools grava as linhas na ordem do SQLite)."""
    con.execute(f'CREATE TEMP TABLE "_resort" AS SELECT * FROM "{table}" ORDER BY {order}')
    con.execute(f'DELETE FROM "{table}"')
    con.execute(f'INSERT INTO "{table}" SELECT * FROM "_resort"')
    con.execute('DROP TABLE "_resort"')


def apply_bag_edits(
    con: sqlite3.Connection,
    bag: list[BagItem],
    fallback_names: dict[int, str],
    bonus_key: int = DELUXE_BONUS_KEY,
) -> list[str]:
    """
    Troca o conteúdo do pacote de bônus pela lista `bag`, mantendo as cores
    do Ramza. Itens avulsos entram direto ("Item:N"); itens com quantidade
    usam linhas de SystemBonusSpecialItem (ver DELUXE_QUANTITY_SPECIAL_KEY).
    """
    present = _tables(con)
    specials_en = {
        int(k): (u or "")
        for k, u in con.execute('SELECT Key, UnionId FROM "SystemBonusSpecialItem-en"')
    }

    def is_color(union: str) -> bool:
        kind, _, ref = union.partition(":")
        return kind == "SystemBonusSpecialItem" and specials_en.get(int(ref), "").startswith(COLOR_UNION_PREFIX)

    old_rows = con.execute(
        'SELECT UnionId, DLCFlags FROM "SystemBonusItemContents" WHERE Key = ? ORDER BY Key2', (bonus_key,)
    ).fetchall()
    kept = [(u, f) for u, f in old_rows if is_color(u or "")]

    # Linhas de quantidade: primeiro a 3 (a do pacote original), depois
    # chaves novas em sequência.
    next_key = max(specials_en, default=0) + 1
    quantity_keys: dict[int, int] = {}  # índice na bag -> Key do SpecialItem
    for index, entry in enumerate(bag):
        if entry.quantity > 1:
            if DELUXE_QUANTITY_SPECIAL_KEY not in quantity_keys.values():
                quantity_keys[index] = DELUXE_QUANTITY_SPECIAL_KEY
            else:
                quantity_keys[index] = next_key
                next_key += 1

    new_rows = []
    for index, entry in enumerate(bag):
        if index in quantity_keys:
            new_rows.append((f"SystemBonusSpecialItem:{quantity_keys[index]}", 0))
        else:
            new_rows.append((f"Item:{entry.item_id}", 0))
    new_rows += kept

    con.execute('DELETE FROM "SystemBonusItemContents" WHERE Key = ?', (bonus_key,))
    con.executemany(
        'INSERT INTO "SystemBonusItemContents" (Key, Key2, DLCFlags, UnionId) VALUES (?, ?, ?, ?)',
        [(bonus_key, i, flags, union) for i, (union, flags) in enumerate(new_rows)],
    )
    _resort(con, "SystemBonusItemContents", "Key, Key2")
    changed = ["SystemBonusItemContents"]

    kept_special_keys = [int(u.split(":")[1]) for u, _f in kept]
    for lang in LANGUAGES:
        special_table = f"SystemBonusSpecialItem-{lang}"
        if special_table not in present:
            continue
        item_table = f"Item-{lang}"
        names = _names(con, item_table) if item_table in present else {}
        captions = []
        for index, entry in enumerate(bag):
            name = names.get(entry.item_id) or fallback_names.get(entry.item_id) or f"Item {entry.item_id}"
            caption = f"{name} × {entry.quantity}" if entry.quantity > 1 else name
            captions.append(caption)
            key = quantity_keys.get(index)
            if key is None:
                continue
            con.execute(f'DELETE FROM "{special_table}" WHERE Key = ?', (key,))
            con.execute(
                f'INSERT INTO "{special_table}" (Key, DLCFlags, Comment, UnionId, Quantity, Caption) '
                "VALUES (?, 0, NULL, ?, ?, ?)",
                (key, f"Item:{entry.item_id}", entry.quantity, caption),
            )
        if quantity_keys:
            _resort(con, special_table, "Key")
            changed.append(special_table)

        bonus_table = f"SystemBonusItem-{lang}"
        if bonus_table in present:
            for key in kept_special_keys:
                row = con.execute(f'SELECT Caption FROM "{special_table}" WHERE Key = ?', (key,)).fetchone()
                if row and row[0]:
                    captions.append(row[0])
            description = "\n".join(f"- {c}" for c in captions)
            con.execute(f'UPDATE "{bonus_table}" SET Description = ? WHERE Key = ?', (description, bonus_key))
            changed.append(bonus_table)
    return changed


def build_nxd_files(
    vanilla_db: Path,
    cli: Path,
    work_dir: Path,
    class_edit: Optional[dict] = None,
    bag: Optional[list[BagItem]] = None,
    fallback_item_names: Optional[dict[int, str]] = None,
    line_cb: LineCb = None,
) -> list[Path]:
    """
    Copia o banco original, aplica as edições e gera os .nxd.

    class_edit: argumentos de apply_class_edits (ability_ids, jp_cost,
    source_job_id, target_job_ids), ou None para não mexer na classe.
    bag: lista da bolsa, ou None para não mexer no pacote de bônus.
    """
    shutil.rmtree(work_dir, ignore_errors=True)
    out_dir = work_dir / "nxd_out"
    out_dir.mkdir(parents=True)
    staged = work_dir / "staged.sqlite"
    shutil.copy(vanilla_db, staged)

    tables: list[str] = []
    con = sqlite3.connect(str(staged))
    try:
        if class_edit:
            tables += apply_class_edits(con, **class_edit)
        if bag is not None:
            tables += apply_bag_edits(con, bag, fallback_item_names or {})
        con.commit()
    finally:
        con.close()
    if not tables:
        return []

    if line_cb:
        line_cb(i18n.t("nxd_generating", tables=", ".join(tables)))
    code = ff16tools.sqlite_to_nxd(cli, staged, out_dir, tables, None)
    if code != 0:
        raise RuntimeError(i18n.t("nxd_to_nxd_fail", code=code))

    produced = []
    for table in tables:
        path = out_dir / nxd_filename(table)
        if not path.exists():
            raise RuntimeError(i18n.t("nxd_not_generated", name=path.name))
        produced.append(path)
    return produced
