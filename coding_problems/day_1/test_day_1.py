from day_1 import is_increasing, get_input


def test_is_increasing_yes():
    assert is_increasing(4, 8) == True


def test_is_increasing_no():
    assert is_increasing(8, 4) == False


def test_is_increasing_same():
    assert is_increasing(8, 8) == False


def test_get_input_correct_type():
    assert type(get_input('test_data.txt')) == list


def test_get_input_is_ints():
    data = get_input('test_data.txt')
    assert type(data[0]) == int
    assert type(data[1]) == int
    assert type(data[2]) == int
