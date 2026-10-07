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


def test_relevel_up_matches_level_up_formula():
    raw = stat_sim.BASE_RAW["PA"][0]
    assert stat_sim.relevel("PA", raw, 40, 1, 50) == stat_sim.raw_at_level(raw, 40, 50)


def test_relevel_down_undoes_level_up():
    for growth in (11, 48, 95):
        start = 491520
        up = stat_sim.relevel("HP", start, growth, 1, 99)
        assert stat_sim.relevel("HP", up, growth, 99, 1) == start
        assert stat_sim.relevel("HP", up, growth, 99, 99) == up


def test_relevel_from_scratch_ignores_current_raw():
    expected = stat_sim.raw_at_level(sum(stat_sim.BASE_RAW["HP"]) // 2, 11, 30)
    assert stat_sim.relevel("HP", 123, 11, 80, 30, from_scratch=True) == expected


def test_growths_and_multipliers_skip_bad_fields():
    fields = {"PAGrowth": "40", "MAGrowth": "0", "HPGrowth": "x", "PAMultiplier": "120", "MPMultiplier": "?"}
    assert stat_sim.growths(fields) == {"PA": 40}
    assert stat_sim.multipliers(fields) == {"PA": 120}
