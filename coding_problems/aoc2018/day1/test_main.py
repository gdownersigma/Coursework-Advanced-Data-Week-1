from main import find_first_dupe


def test_find_first_dupe_scenario_1():
    assert find_first_dupe([+3, +3, +4, -2, -4]) == 10


def test_find_first_dupe_scenario_2():
    assert find_first_dupe([-6, +3, +8, +5, -6]) == 5
