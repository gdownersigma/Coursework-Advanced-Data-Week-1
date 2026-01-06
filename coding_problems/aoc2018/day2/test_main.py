from main import find_counts


def test_find_counts_both_false():
    assert find_counts("abcdef") == [False, False]


def test_find_counts_both_true():
    assert find_counts("bababc") == [True, True]


def test_find_counts_one_true():
    assert find_counts("baxagc") == [True, False]


def test_find_counts_multiple_true():
    assert find_counts("babagc") == [True, False]
