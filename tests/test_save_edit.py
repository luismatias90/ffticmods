import struct
import zlib

import pytest

from ramza_manager import save_edit as se


def _fake_save(slots=2) -> bytes:
    """fftsave.bin com `slots` slots usados, Ramza na 1ª unidade e um genérico na 2ª."""
    data = bytearray(se.HEADER_SIZE + 3 * se.SLOT_SIZE)
    struct.pack_into("<II", data, 0, se.HEADER_SIZE, 0)
    for index in range(slots):
        base = se.HEADER_SIZE + index * se.SLOT_SIZE
        data[base:base + 4] = b"SC\x11\x01"
        title = "ＦＦＴ　ＦＩＬＥ０{}".format(index + 1).encode("cp932")
        data[base + 4:base + 4 + len(title)] = title
        struct.pack_into("<I", data, base + se.SLOT_TIME, 1790807370)
        ramza = base + se.UNIT_START
        data[ramza:ramza + 3] = bytes([3, 0, 3])
        data[ramza + se.LEVEL], data[ramza + se.BRAVE], data[ramza + se.FAITH] = 12, 70, 65
        struct.pack_into("<H", data, ramza + se.JP, 150 + index)
        generic = ramza + se.UNIT_SIZE
        data[generic:generic + 3] = bytes([0x80, 0xFF, 0x4A])
    se.update_checksum(data)
    return bytes(data)


def test_parse_slots():
    slots = se.parse_slots(_fake_save())
    assert [s.index for s in slots] == [0, 1]
    assert slots[0].title == "FFT FILE01"
    assert slots[1].ramza == se.RamzaStats(level=12, brave=70, faith=65, jp=151)


def test_edit_slot_touches_only_ramza_and_checksum():
    data = _fake_save()
    edited = se.edit_slot(data, 1, jp=9999, brave=97, faith=10)
    assert se.parse_slots(edited)[1].ramza == se.RamzaStats(level=12, brave=97, faith=10, jp=9999)
    assert se.parse_slots(edited)[0].ramza == se.parse_slots(data)[0].ramza
    assert struct.unpack_from("<I", edited, 4)[0] == zlib.crc32(edited[se.HEADER_SIZE:])
    diff = [i for i in range(len(data)) if data[i] != edited[i]]
    ramza = se.HEADER_SIZE + se.SLOT_SIZE + se.UNIT_START
    assert set(diff) <= {4, 5, 6, 7, ramza + se.BRAVE, ramza + se.FAITH, ramza + se.JP, ramza + se.JP + 1}


def test_edit_slot_clamps_values():
    edited = se.edit_slot(_fake_save(), 0, jp=70000, brave=250, faith=-3)
    assert se.parse_slots(edited)[0].ramza == se.RamzaStats(level=12, brave=100, faith=0, jp=9999)


def test_edit_slot_rejects_empty_slot():
    with pytest.raises(se.SaveError):
        se.edit_slot(_fake_save(slots=1), 1, 9999, 70, 70)


def _png(chunks) -> bytes:
    return se.PNG_SIGNATURE + b"".join(se._chunk_bytes(kind, body) for kind, body in chunks)


def test_replace_save_chunk_keeps_thumbnail():
    original = _png([(b"IHDR", b"hdr"), (b"ffTo", b"old"), (b"IDAT", b"picture"), (b"IEND", b"")])
    packed = _png([(b"IHDR", b"other"), (b"ffTo", b"new data"), (b"IDAT", b"blank"), (b"IEND", b"")])
    result = se._chunks(se.replace_save_chunk(original, packed))
    assert result == [(b"IHDR", b"hdr"), (b"ffTo", b"new data"), (b"IDAT", b"picture"), (b"IEND", b"")]


def test_replace_save_chunk_needs_a_save():
    with pytest.raises(se.SaveError):
        se.replace_save_chunk(b"not a png", b"")


def test_items_are_added_to_inventory():
    data = bytearray(_fake_save())
    pos = se.HEADER_SIZE + se.INVENTORY
    data[pos + 240], data[pos + 186] = 61, 98
    se.update_checksum(data)
    items = [se.BagItem(240, 3), se.BagItem(186, 5), se.BagItem(240, 1), se.BagItem(9999, 1), se.BagItem(1, 0)]
    edited = se.edit_slot(bytes(data), 0, 9999, 70, 65, items)
    inventory = se.parse_slots(edited)[0].inventory
    assert inventory[240] == 65 and inventory[186] == 99  # somado, limitado a 99
    assert inventory[1] == 0
    assert se.parse_slots(edited)[1].inventory == se.parse_slots(bytes(data))[1].inventory


def test_merge_items():
    items = [se.BagItem(240, 3), se.BagItem(240, 2), se.BagItem(19, 1), se.BagItem(300, 1)]
    assert se.merge_items(items, valid_ids={240}) == [se.BagItem(240, 5)]
    assert se.merge_items(items) == [se.BagItem(240, 5), se.BagItem(19, 1)]
