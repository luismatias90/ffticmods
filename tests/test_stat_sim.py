from ramza_manager import stat_sim


def test_level_one_is_base_raw_times_multiplier():
    # Squire genérico: HP x100, PA x90.
    assert stat_sim.stat_range("HP", 100, 11, 1) == (30, 31)
    assert stat_sim.stat_range("PA", 90, 60, 1) == (4, 4)


def test_level_up_adds_raw_over_growth_plus_level():
    raw = stat_sim.BASE_RAW["PA"][0]
    expected = raw + raw // (40 + 1)
    expected += expected // (40 + 2)
    assert stat_sim.raw_at_level(raw, 40, 3) == expected


def test_lower_growth_grows_faster():
    fast = stat_sim.stat_range("PA", 100, 30, 99)
    slow = stat_sim.stat_range("PA", 100, 80, 99)
    assert fast[0] > slow[0]


def test_display_caps_and_level_clamp():
    assert stat_sim.stat_range("PA", 255, 1, 99) == (99, 99)
    assert stat_sim.stat_range("HP", 100, 11, 500) == stat_sim.stat_range("HP", 100, 11, 99)
    assert stat_sim.stat_range("HP", 100, 11, 0) == stat_sim.stat_range("HP", 100, 11, 1)


def test_simulate_skips_missing_fields():
    fields = {"PAMultiplier": "120", "PAGrowth": "40", "MAMultiplier": "x", "MAGrowth": "50"}
    result = stat_sim.simulate(fields, 50)
    assert set(result) == {"PA"}
    assert result["PA"] == stat_sim.stat_range("PA", 120, 40, 50)
