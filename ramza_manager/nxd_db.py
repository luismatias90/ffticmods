"""
Tabelas nex (.nxd) do jogo: extração para um SQLite de referência, leitura de
nomes e geração dos .nxd modificados.

Por que precisamos disso:
- o custo de JP que o jogo usa de verdade está na tabela nex `Ability`
  (JpCost1 = byte baixo, JpCost2 = byte alto); o <JPCost> do AbilityData.xml é
  ignorado. Só lemos esse custo, para a prévia: as skills mantêm o preço
  original. A tabela nex `Job` guarda o nome da classe e uma cópia do
  skillset (`jobcommand+Id`).

Um .nxd no mod substitui o arquivo inteiro do jogo, então sempre partimos de
uma cópia do banco original e mexemos só nas linhas necessárias.
Fluxo de exportação baseado em mod_studio/qt/nxd_export.py (GPL-3).
"""

from __future__ import annotations

import shutil
import sqlite3
from pathlib import Path
from typing import Callable, Iterable, Optional

from . import ff16tools, game_install, i18n

LineCb = Optional[Callable[[str], None]]

LANGUAGES = ("en", "ja", "de", "fr", "cs", "ct", "ko")

# Tabelas por idioma (arquivo <nome>.<idioma>.nxd) e tabelas únicas (<nome>.nxd).
LOCALIZED_TABLES = ("Ability", "Job", "JobCommand", "Item")
SHARED_TABLES: tuple[str, ...] = ()

# Colunas de texto de Job-<idioma> copiadas da classe escolhida para as do
# Ramza. Unknown4/Unknown6 são as formas femininas (nome/descrição).
JOB_TEXT_COLUMNS = ("Name", "Unknown4", "Description", "Unknown6")


def nxd_filename(table: str) -> str:
    """'Ability-en' -> 'ability.en.nxd'; 'Foo' -> 'foo.nxd'."""
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


# ---------------------------------------------------------------------------
# Edição
# ---------------------------------------------------------------------------

def apply_class_edits(
    con: sqlite3.Connection,
    source_job_id: int,
    target_job_ids: Iterable[int],
    custom_name: Optional[str] = None,
    custom_description: str = "",
    skillset_name: Optional[str] = None,
    target_command_ids: Iterable[int] = (),
) -> list[str]:
    """
    - Job-<idioma>: nas linhas do Ramza, `jobcommand+Id` e nome/descrição da
      classe escolhida. O resto da linha (retrato, tipo, ajuda) fica do Ramza.

    Classe customizada (`target_command_ids` preenchido): o Ramza mantém os
    próprios skillsets, que ganham o nome `skillset_name` em
    JobCommand-<idioma>; o nome da classe (e a descrição, se houver) é
    `custom_name` em todos os idiomas.
    """
    target_job_ids = list(target_job_ids)
    target_command_ids = list(target_command_ids)
    changed: list[str] = []
    present = _tables(con)
    for lang in LANGUAGES:
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


def build_nxd_files(
    vanilla_db: Path,
    cli: Path,
    work_dir: Path,
    class_edit: Optional[dict] = None,
    line_cb: LineCb = None,
) -> list[Path]:
    """
    Copia o banco original, aplica as edições e gera os .nxd.

    class_edit: argumentos de apply_class_edits (source_job_id,
    target_job_ids, ...), ou None para não mexer na classe.
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
