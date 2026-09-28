"""Diálogo para criar/editar uma classe customizada (classe base + skillset misto)."""

from __future__ import annotations

from typing import Callable, Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QAbstractItemView, QCheckBox, QComboBox, QDialog, QDialogButtonBox, QFormLayout, QGridLayout, QGroupBox,
    QHBoxLayout, QLabel, QLineEdit, QListWidget, QListWidgetItem, QMessageBox, QPlainTextEdit, QPushButton,
    QScrollArea, QSpinBox, QSplitter, QTabWidget, QVBoxLayout, QWidget,
)

from . import custom_class, i18n
from .class_catalog import ClassOption, category_labels
from .custom_class import (
    EQUIP_FLAGS, EQUIP_GROUPS, EVASION_RANGE, GROWTH_RANGE, JUMP_RANGE, MAX_ACTIONS, MAX_DESCRIPTION, MAX_INNATES, MAX_NAME,
    MAX_RSM, MOVE_RANGE, MULTIPLIER_RANGE, STATS, CustomClass,
)
from .tables import Job, ReferenceTables

FILTER_ALL, FILTER_ACTION, FILTER_RSM = "all", "action", "rsm"


class CustomClassDialog(QDialog):
    def __init__(
        self,
        tables: ReferenceTables,
        catalog: list[ClassOption],
        ability_name: Callable[[int], str],
        command_name: Callable[[int], str],
        existing: Optional[CustomClass] = None,
        parent: Optional[QWidget] = None,
    ) -> None:
        super().__init__(parent)
        self.tables = tables
        self.catalog = catalog
        self.ability_name = ability_name
        self.command_name = command_name
        self.actions_pool = custom_class.action_pool(tables)
        self.rsm_pool = custom_class.rsm_pool(tables)
        self._result: Optional[CustomClass] = None

        t = i18n.t
        self.setWindowTitle(t("cc_edit_title") if existing else t("cc_new_title"))
        self.resize(1040, 760)
        root = QVBoxLayout(self)

        form = QFormLayout()
        self.name_edit = QLineEdit()
        self.name_edit.setMaxLength(MAX_NAME)
        self.skillset_edit = QLineEdit()
        self.skillset_edit.setMaxLength(MAX_NAME)
        self.skillset_edit.setPlaceholderText(t("cc_skillset_ph"))
        self.author_edit = QLineEdit()
        self.author_edit.setMaxLength(custom_class.MAX_AUTHOR)
        self.base_combo = QComboBox()
        labels = category_labels()
        for option in catalog:
            self.base_combo.addItem(f"{option.name}  ·  {labels[option.category]}", option.job_id)
        self.base_combo.currentIndexChanged.connect(self._base_changed)
        self.desc_edit = QPlainTextEdit()
        self.desc_edit.setMaximumHeight(56)
        self.desc_edit.setPlaceholderText(t("cc_desc_ph"))
        form.addRow(t("cc_name"), self.name_edit)
        form.addRow(t("cc_skillset"), self.skillset_edit)
        base_row = QHBoxLayout()
        base_row.addWidget(self.base_combo, 1)
        self.btn_copy_base = QPushButton(t("cc_copy_base"))
        self.btn_copy_base.setToolTip(t("cc_copy_base_tip"))
        self.btn_copy_base.clicked.connect(self._copy_base_skills)
        base_row.addWidget(self.btn_copy_base)
        form.addRow(t("cc_base"), base_row)
        form.addRow(t("cc_author"), self.author_edit)
        form.addRow(t("cc_desc"), self.desc_edit)
        root.addLayout(form)
        hint = QLabel(t("cc_base_hint"))
        hint.setWordWrap(True)
        hint.setObjectName("Muted")
        root.addWidget(hint)

        self.pages = QTabWidget()
        body = QSplitter(Qt.Horizontal)
        left = QWidget()
        left_layout = QVBoxLayout(left)
        left_layout.setContentsMargins(0, 0, 0, 0)
        filters = QHBoxLayout()
        self.search = QLineEdit()
        self.search.setPlaceholderText(t("cc_search"))
        self.search.textChanged.connect(self._fill_pool)
        filters.addWidget(self.search, 1)
        self.filter_combo = QComboBox()
        self.filter_combo.addItem(t("cc_filter_all"), FILTER_ALL)
        self.filter_combo.addItem(t("cc_slot_action"), FILTER_ACTION)
        self.filter_combo.addItem(t("cc_slot_rsm"), FILTER_RSM)
        self.filter_combo.currentIndexChanged.connect(self._fill_pool)
        filters.addWidget(self.filter_combo)
        left_layout.addLayout(filters)
        self.pool_list = QListWidget()
        self.pool_list.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.pool_list.itemDoubleClicked.connect(lambda _i: self._add_selected())
        left_layout.addWidget(self.pool_list, 1)
        self.btn_add = QPushButton(t("btn_add"))
        self.btn_add.clicked.connect(self._add_selected)
        left_layout.addWidget(self.btn_add)
        body.addWidget(left)

        right = QWidget()
        right_layout = QVBoxLayout(right)
        right_layout.setContentsMargins(0, 0, 0, 0)
        self.lbl_actions = QLabel()
        self.action_list = self._make_slot_list()
        self.lbl_rsm = QLabel()
        self.rsm_list = self._make_slot_list()
        right_layout.addWidget(self.lbl_actions)
        right_layout.addWidget(self.action_list, 3)
        right_layout.addWidget(self.lbl_rsm)
        right_layout.addWidget(self.rsm_list, 2)
        buttons = QHBoxLayout()
        for label, slot in ((t("cc_up"), lambda: self._move(-1)), (t("cc_down"), lambda: self._move(1)),
                            (t("btn_remove"), self._remove_selected), (t("btn_clear"), self._clear)):
            btn = QPushButton(label)
            btn.clicked.connect(slot)
            buttons.addWidget(btn)
        buttons.addStretch()
        right_layout.addLayout(buttons)
        self.lbl_special = QLabel()
        self.lbl_special.setWordWrap(True)
        self.lbl_special.setTextFormat(Qt.RichText)
        right_layout.addWidget(self.lbl_special)
        body.addWidget(right)
        body.setSizes([520, 480])
        self.pages.addTab(body, t("cc_page_skills"))
        self.pages.addTab(self._build_job_page(), t("cc_page_job"))
        root.addWidget(self.pages, 1)

        box = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        box.button(QDialogButtonBox.Save).setText(t("cc_save"))
        box.button(QDialogButtonBox.Cancel).setText(t("cc_cancel"))
        box.accepted.connect(self._accept)
        box.rejected.connect(self.reject)
        root.addWidget(box)

        self._base_fields: dict[str, str] = {}
        self._apply_base(self._base_job(), force=True)
        if existing:
            self._load(existing)
        self._fill_pool()
        self._update_counts()

    # ------------------------------------------------ atributos e equipamento

    def _build_job_page(self) -> QWidget:
        t = i18n.t
        page = QWidget()
        outer = QVBoxLayout(page)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet("QScrollArea, QScrollArea > QWidget > QWidget { background: transparent; }")
        inner = QWidget()
        layout = QVBoxLayout(inner)
        scroll.setWidget(inner)
        outer.addWidget(scroll)

        top = QHBoxLayout()
        stats_box = QGroupBox(t("cc_box_stats"))
        grid = QGridLayout(stats_box)
        grid.addWidget(QLabel(f"<b>{t('cc_col_mult')}</b>"), 0, 1)
        grid.addWidget(QLabel(f"<b>{t('cc_col_growth')}</b>"), 0, 3)
        self.mult_spins: dict[str, QSpinBox] = {}
        self.growth_spins: dict[str, QSpinBox] = {}
        self.base_labels: dict[str, QLabel] = {}
        for row, stat in enumerate(STATS, 1):
            grid.addWidget(QLabel(f"<b>{stat}</b>"), row, 0)
            for col, (spins, bounds, key) in enumerate(
                ((self.mult_spins, MULTIPLIER_RANGE, f"{stat}Multiplier"),
                 (self.growth_spins, GROWTH_RANGE, f"{stat}Growth"))):
                spin = self._spin(bounds)
                spins[stat] = spin
                grid.addWidget(spin, row, 1 + col * 2)
                label = QLabel()
                self.base_labels[key] = label
                grid.addWidget(label, row, 2 + col * 2)
        hint = QLabel(t("cc_stats_hint"))
        hint.setWordWrap(True)
        grid.addWidget(hint, len(STATS) + 1, 0, 1, 5)
        top.addWidget(stats_box, 3)

        move_box = QGroupBox(t("cc_box_move"))
        form = QGridLayout(move_box)
        self.move_spin = self._spin(MOVE_RANGE)
        self.jump_spin = self._spin(JUMP_RANGE)
        self.evasion_spin = self._spin(EVASION_RANGE)
        self.evasion_spin.setSuffix(" %")
        for row, (label, spin, key) in enumerate((("Move", self.move_spin, "Move"),
                                                  ("Jump", self.jump_spin, "Jump"),
                                                  (t("cc_evasion"), self.evasion_spin, "CharacterEvasion"))):
            form.addWidget(QLabel(f"<b>{label}</b>"), row, 0)
            form.addWidget(spin, row, 1)
            base = QLabel()
            self.base_labels[key] = base
            form.addWidget(base, row, 2)
        mev = QLabel(t("cc_no_mev"))
        mev.setWordWrap(True)
        form.addWidget(mev, 3, 0, 1, 3)
        form.setRowStretch(4, 1)
        top.addWidget(move_box, 2)
        layout.addLayout(top)

        innate_box = QGroupBox(t("cc_box_innate"))
        innate_grid = QGridLayout(innate_box)
        self.innate_combos: list[QComboBox] = []
        choices = sorted(custom_class.innate_pool(self.tables), key=lambda i: self.ability_name(i).lower())
        for index in range(MAX_INNATES):
            combo = QComboBox()
            combo.addItem(i18n.t("none_f"), 0)
            for ab_id in choices:
                combo.addItem(self.ability_name(ab_id), ab_id)
            self.innate_combos.append(combo)
            innate_grid.addWidget(combo, index // 2, index % 2)
        self.lbl_base_innate = QLabel()
        self.lbl_base_innate.setWordWrap(True)
        innate_grid.addWidget(self.lbl_base_innate, 2, 0, 1, 2)
        layout.addWidget(innate_box)

        equip_box = QGroupBox(t("cc_box_equip"))
        equip_grid = QGridLayout(equip_box)
        self.equip_checks: dict[str, QCheckBox] = {}
        row = 0
        for group, flags in EQUIP_GROUPS.items():
            equip_grid.addWidget(QLabel(f"<b>{t('cc_equip_' + group)}</b>"), row, 0, 1, 5)
            row += 1
            for index, flag in enumerate(flags):
                check = QCheckBox(flag)
                self.equip_checks[flag] = check
                equip_grid.addWidget(check, row + index // 5, index % 5)
            row += (len(flags) + 4) // 5
        layout.addWidget(equip_box)

        reset = QPushButton(t("cc_reset_base"))
        reset.clicked.connect(lambda: self._apply_base(self._base_job(), force=True))
        row = QHBoxLayout()
        row.addWidget(reset)
        row.addStretch()
        layout.addLayout(row)
        layout.addStretch()
        return page

    @staticmethod
    def _spin(bounds: tuple[int, int]) -> QSpinBox:
        spin = QSpinBox()
        spin.setRange(*bounds)
        spin.setMaximumWidth(90)
        return spin

    def _base_job(self) -> Optional[Job]:
        return self.tables.jobs.get(self.base_combo.currentData())

    def _job_widgets(self) -> list[tuple[str, QSpinBox]]:
        pairs = [(f"{s}Multiplier", self.mult_spins[s]) for s in STATS]
        pairs += [(f"{s}Growth", self.growth_spins[s]) for s in STATS]
        pairs += [("Move", self.move_spin), ("Jump", self.jump_spin), ("CharacterEvasion", self.evasion_spin)]
        return pairs

    def _innates_now(self) -> list[int]:
        return [c.currentData() for c in self.innate_combos if c.currentData()]

    def _equip_now(self) -> set[str]:
        return {flag for flag, check in self.equip_checks.items() if check.isChecked()}

    def _set_job_values(self, job: Job) -> None:
        for key, spin in self._job_widgets():
            spin.setValue(int(job.fields.get(key, "0") or 0))
        self._set_innates(job.innate_ability_ids)
        equip = set(job.equippable)
        for flag, check in self.equip_checks.items():
            check.setChecked(flag in equip)

    def _set_innates(self, ids: list[int]) -> None:
        ids = list(ids[:MAX_INNATES]) + [0] * (MAX_INNATES - len(ids[:MAX_INNATES]))
        for combo, ab_id in zip(self.innate_combos, ids):
            index = combo.findData(ab_id)
            if index < 0:  # inata fora da lista (não deve acontecer): entra como opção
                combo.addItem(self.ability_name(ab_id), ab_id)
                index = combo.count() - 1
            combo.setCurrentIndex(index)

    def _apply_base(self, job: Optional[Job], force: bool = False) -> None:
        """
        Troca a classe base. Campos que o usuário não mexeu (iguais à base
        anterior) seguem a nova base; os editados ficam. `force` volta tudo.
        """
        if job is None:
            return
        old = Job(0, "", self._base_fields) if self._base_fields else None
        new_fields = job.fields
        for key, spin in self._job_widgets():
            if force or old is None or spin.value() == int(old.fields.get(key, "0") or 0):
                spin.setValue(int(new_fields.get(key, "0") or 0))
        if force or old is None or self._innates_now() == old.innate_ability_ids:
            self._set_innates(job.innate_ability_ids)
        if force or old is None or self._equip_now() == set(old.equippable):
            equip = set(job.equippable)
            for flag, check in self.equip_checks.items():
                check.setChecked(flag in equip)
        self._base_fields = dict(new_fields)
        for key, label in self.base_labels.items():
            label.setText(i18n.t("cc_base_value", value=new_fields.get(key, "?")))
        names = ", ".join(self.ability_name(i) for i in job.innate_ability_ids) or i18n.t("none_f")
        self.lbl_base_innate.setText(i18n.t("cc_base_value", value=names))

    def _base_changed(self, *_args) -> None:
        self._apply_base(self._base_job())
        self._update_counts()

    def _overrides(self) -> dict:
        """Só o que difere da classe base atual."""
        base = Job(0, "", self._base_fields)
        out: dict = {"multipliers": {}, "growths": {}}
        for stat in STATS:
            for key, spins, target in ((f"{stat}Multiplier", self.mult_spins, "multipliers"),
                                       (f"{stat}Growth", self.growth_spins, "growths")):
                value = spins[stat].value()
                if value != int(base.fields.get(key, "0") or 0):
                    out[target][stat] = value
        for attr, key, spin in (("move", "Move", self.move_spin), ("jump", "Jump", self.jump_spin),
                                ("evasion", "CharacterEvasion", self.evasion_spin)):
            out[attr] = spin.value() if spin.value() != int(base.fields.get(key, "0") or 0) else None
        innates = self._innates_now()
        out["innates"] = innates if innates != base.innate_ability_ids else None
        equip = self._equip_now()
        out["equip"] = [f for f in EQUIP_FLAGS if f in equip] if equip != set(base.equippable) else None
        return out

    # ----------------------------------------------------------- helpers

    def _make_slot_list(self) -> QListWidget:
        lst = QListWidget()
        lst.setSelectionMode(QAbstractItemView.ExtendedSelection)
        lst.itemDoubleClicked.connect(lambda _i: self._remove_selected())
        lst.itemSelectionChanged.connect(lambda l=lst: self._focus_slot(l))
        return lst

    def _focus_slot(self, lst: QListWidget) -> None:
        # Uma seleção por vez entre as duas listas, para ↑/↓/Remover saberem onde agir.
        other = self.rsm_list if lst is self.action_list else self.action_list
        if lst.selectedItems() and other.selectedItems():
            other.blockSignals(True)
            other.clearSelection()
            other.blockSignals(False)

    def _label(self, ab_id: int, pool: dict[int, int]) -> str:
        ability = self.tables.abilities.get(ab_id)
        kind = ability.ability_type if ability else ""
        return f"{self.ability_name(ab_id)}  ·  {self.command_name(pool.get(ab_id, 0))}  ·  {kind}"

    def _slot_item(self, ab_id: int, pool: dict[int, int]) -> QListWidgetItem:
        item = QListWidgetItem(self._label(ab_id, pool))
        item.setData(Qt.UserRole, ab_id)
        item.setToolTip(f"Ability {ab_id}")
        return item

    @staticmethod
    def _ids(lst: QListWidget) -> list[int]:
        return [lst.item(i).data(Qt.UserRole) for i in range(lst.count())]

    def _load(self, klass: CustomClass) -> None:
        self.name_edit.setText(klass.name)
        self.skillset_edit.setText(klass.skillset if klass.skillset != klass.name else "")
        self.author_edit.setText(klass.author)
        self.desc_edit.setPlainText(klass.description)
        index = self.base_combo.findData(klass.base_job)
        if index >= 0:
            self.base_combo.setCurrentIndex(index)
        if klass.base_job in self.tables.jobs:
            self._apply_base(self.tables.jobs[klass.base_job], force=True)
            self._set_job_values(klass.effective_job(self.tables))
        self._set_lists(klass.actions, klass.rsm)

    def _set_lists(self, actions: list[int], rsm: list[int]) -> None:
        self.action_list.clear()
        self.rsm_list.clear()
        for ab_id in actions:
            if ab_id in self.actions_pool:
                self.action_list.addItem(self._slot_item(ab_id, self.actions_pool))
        for ab_id in rsm:
            if ab_id in self.rsm_pool:
                self.rsm_list.addItem(self._slot_item(ab_id, self.rsm_pool))
        self._update_counts()

    def _fill_pool(self, *_args) -> None:
        needle = self.search.text().strip().lower()
        mode = self.filter_combo.currentData()
        self.pool_list.clear()
        sources = []
        if mode in (FILTER_ALL, FILTER_ACTION):
            sources.append(self.actions_pool)
        if mode in (FILTER_ALL, FILTER_RSM):
            sources.append(self.rsm_pool)
        for pool in sources:
            for ab_id, cmd_id in sorted(pool.items(), key=lambda kv: (kv[1], kv[0])):
                label = self._label(ab_id, pool)
                if needle and needle not in label.lower():
                    continue
                self.pool_list.addItem(self._slot_item(ab_id, pool))

    def _update_counts(self, *_args) -> None:
        t = i18n.t
        self.lbl_actions.setText(t("cc_actions_count", n=self.action_list.count(), max=MAX_ACTIONS))
        self.lbl_rsm.setText(t("cc_rsm_count", n=self.rsm_list.count(), max=MAX_RSM))
        special = custom_class.special_abilities(self.tables, self._current(strict=False))
        if special:
            names = ", ".join(self.ability_name(i) for i in special)
            self.lbl_special.setText(t("cc_special_warn", names=names))
        else:
            self.lbl_special.setText("")

    # ----------------------------------------------------------- actions

    def _add_selected(self) -> None:
        full = []
        for item in self.pool_list.selectedItems():
            ab_id = item.data(Qt.UserRole)
            if ab_id in self.actions_pool:
                target, pool, limit = self.action_list, self.actions_pool, MAX_ACTIONS
            else:
                target, pool, limit = self.rsm_list, self.rsm_pool, MAX_RSM
            if ab_id in self._ids(target):
                continue
            if target.count() >= limit:
                full.append(self.ability_name(ab_id))
                continue
            target.addItem(self._slot_item(ab_id, pool))
        self._update_counts()
        if full:
            QMessageBox.information(self, i18n.t("cc_full_title"),
                                    i18n.t("cc_full_body", a=MAX_ACTIONS, r=MAX_RSM, names=", ".join(full)))

    def _active_slot_list(self) -> Optional[QListWidget]:
        for lst in (self.action_list, self.rsm_list):
            if lst.selectedItems():
                return lst
        return None

    def _remove_selected(self) -> None:
        lst = self._active_slot_list()
        if lst is None:
            return
        for row in sorted((lst.row(i) for i in lst.selectedItems()), reverse=True):
            lst.takeItem(row)
        self._update_counts()

    def _move(self, delta: int) -> None:
        lst = self._active_slot_list()
        if lst is None or len(lst.selectedItems()) != 1:
            return
        row = lst.currentRow()
        new_row = row + delta
        if 0 <= new_row < lst.count():
            item = lst.takeItem(row)
            lst.insertItem(new_row, item)
            lst.setCurrentRow(new_row)

    def _clear(self) -> None:
        self.action_list.clear()
        self.rsm_list.clear()
        self._update_counts()

    def _copy_base_skills(self) -> None:
        job = self.tables.jobs.get(self.base_combo.currentData())
        command = self.tables.command_for(job) if job else None
        if command is None:
            return
        actions = self._ids(self.action_list) + [i for i in command.action_ids if i not in self._ids(self.action_list)]
        rsm = self._ids(self.rsm_list) + [i for i in command.rsm_ids if i not in self._ids(self.rsm_list)]
        self._set_lists(actions[:MAX_ACTIONS], rsm[:MAX_RSM])

    def _current(self, strict: bool = True) -> CustomClass:
        name = " ".join(self.name_edit.text().split())
        skillset = " ".join(self.skillset_edit.text().split()) or name
        return CustomClass(
            name=name,
            skillset=skillset,
            base_job=self.base_combo.currentData() if self.base_combo.count() else 0,
            actions=self._ids(self.action_list),
            rsm=self._ids(self.rsm_list),
            author=" ".join(self.author_edit.text().split()),
            description=self.desc_edit.toPlainText().strip()[:MAX_DESCRIPTION],
            **(self._overrides() if strict else {}),
        )

    def _accept(self) -> None:
        klass = self._current()
        if not klass.name:
            QMessageBox.warning(self, i18n.t("cc_invalid_title"), i18n.t("cc_need_name"))
            return
        if not klass.ability_ids:
            QMessageBox.warning(self, i18n.t("cc_invalid_title"), i18n.t("cc_need_skills"))
            return
        self._result = klass
        self.accept()

    def result_class(self) -> Optional[CustomClass]:
        return self._result
