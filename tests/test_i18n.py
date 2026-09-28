import re

from ramza_manager import i18n

_FIELDS = re.compile(r"\{(\w+)\}")


def test_languages_have_the_same_keys():
    assert set(i18n.STRINGS["pt"]) == set(i18n.STRINGS["en"])


def test_placeholders_match():
    for key in i18n.STRINGS["pt"]:
        pt = _FIELDS.findall(i18n.STRINGS["pt"][key])
        en = _FIELDS.findall(i18n.STRINGS["en"][key])
        assert pt == en, key


def test_switch_language():
    i18n.set_language("en")
    assert i18n.t("btn_wizard") == "Wizard"
    i18n.set_language("pt")
    assert i18n.t("btn_wizard") == "Assistente"
    assert i18n.t("status_missing", n=2) == "Falta configurar 2 item(ns) — veja abaixo"
