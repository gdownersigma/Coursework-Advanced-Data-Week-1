from main import parse_claim, find_area_coords, add_coord, find_covered_points


def test_parse_claim_1():
    starting_coord, area = parse_claim('#2 @ 3,1: 5x4')
    assert starting_coord == (3, 1)
    assert area == (5, 4)


def test_parse_claim_2():
    starting_coord, area = parse_claim('#1 @ 1,3: 4x4')
    assert starting_coord == (1, 3)
    assert area == (4, 4)


def test_parse_claim_3():
    starting_coord, area = parse_claim('#3 @ 5,5: 2x2')
    assert starting_coord == (5, 5)
    assert area == (2, 2)


def test_find_area_coords_1():
    start = (0, 0)
    area = (2, 2)
    area_list = [(0, 0), (0, 1), (1, 0), (1, 1)]
    assert find_area_coords(area, start) == area_list


def test_find_area_coords_2():
    start = (3, 1)
    area = (1, 2)
    area_list = [(3, 1), (3, 2)]
    assert find_area_coords(area, start) == area_list


def test_add_coord_1():
    coord = (3, 2)
    test_dict = {}
    add_coord(coord, test_dict)
    assert coord in test_dict.keys()
    assert test_dict[coord] == 1


def test_add_coord_2():
    coord = (3, 2)
    test_dict = {(3, 2): 1}
    add_coord(coord, test_dict)
    assert coord in test_dict.keys()
    assert test_dict[coord] == 2


def test_find_coloured_points_1():
    grid = {}
    claims = ['#1 @ 1,3: 4x4', '#2 @ 3,1: 4x4', '#3 @ 5,5: 2x2']
    assert find_covered_points(claims, grid) == 4
