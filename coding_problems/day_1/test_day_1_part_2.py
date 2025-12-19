from day_1_part_2 import is_near_end, is_triple_increasing


def test_is_near_end_return_false():
    test_list = [1, 2, 3, 4, 5]
    assert is_near_end(5, len(test_list)) == False


def test_is_near_end_return_false_2():
    test_list = [1, 2, 3, 4, 5]
    assert is_near_end(3, len(test_list)) == False


def test_is_near_end_return_true():
    test_list = [1, 2, 3, 4, 5]
    assert is_near_end(1, len(test_list)) == True


def test_is_near_end_return_true_middle():
    test_list = [1, 2, 3, 4, 5]
    assert is_near_end(2, len(test_list)) == True


def test_is_triple_increasing_yes():
    index1 = 0
    index2 = 1
    data = [1, 2, 3, 4]
    assert is_triple_increasing(index1, index2, data) == True


def test_is_triple_increasing_same():
    index1 = 0
    index2 = 1
    data = [1, 1, 1, 1]
    assert is_triple_increasing(index1, index2, data) == False


def test_is_triple_increasing_no():
    index1 = 0
    index2 = 1
    data = [2, 1, 1, 1]
    assert is_triple_increasing(index1, index2, data) == False
