# need a function to check if the value is up or down

# need a function to loop through the instruction and return the total items being carried.

# maybe function to make sure its not below 0.

from main import what_action, loop_instruction, find_heaviest_max, find_max_load


def test_what_action_pickup():
    assert what_action('^') == 1


def test_what_action_putdown():
    assert what_action('v') == -1


def test_what_action_nothing():
    assert what_action('.') == 0


def test_loop_instruction1():
    assert loop_instruction('^^^....v..^.v') == 2


def test_loop_instruction2():
    assert loop_instruction('.^.^.^.^.^') == 5


def test_loop_instruction3():
    assert loop_instruction('vvv...^') == 1


def test_find_max_load1():
    assert find_max_load('^^v^^^^vvv') == 5


def test_find_max_load2():
    assert find_max_load('vvvv^^^vvv') == 3


def test_find_max_load3():
    assert find_max_load('^^^^^^^') == 7


def test_find_heaviest_max1():
    assert find_heaviest_max(["^v^", "^^", "^^^^^vvvvv"]) == 2


def test_find_heaviest_max3():
    assert find_heaviest_max(["^^^^vvvvv^^", "^^^."]) == 0
