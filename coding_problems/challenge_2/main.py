def parse_input():
    with open('input.txt', 'r') as f:
        return f.readlines()


def parse_claim(claim: str) -> tuple:
    """Takes the claim input and returns co-ordinate tuple, area tuple."""
    # 3 @ 5,5: 2x2
    claim = claim.split(' ')
    start = claim[2][:-1].split(',')
    start = (int(start[0]), int(start[1]))

    area = claim[3].split('x')
    area = (int(area[0]), int(area[1]))

    return start, area


# function to find all the co-ordinates needed to be filled

def find_area_coords(area: tuple, start: tuple) -> list:
    """Returns a list of tuple co-ordinates covered by the fabric."""
    area_points = []
    for x in range(area[0]):
        for y in range(area[1]):
            area_points.append((x+start[0], y+start[1]))
    return area_points


# function to add a co-ordinate to the grid.

def add_coord(coord: tuple, grid: dict) -> None:
    """Add the coord to the grid if not there already and set its value to 1,
        if there already, add 1."""
    if coord in grid.keys():
        grid[coord] += 1
    else:
        grid[coord] = 1


# function to find the count of values in the grid greater than 1

def find_covered_points(claims: list[str], grid: dict):
    """Returns how many values in the dict are greater than 1"""
    for claim in claims:
        start, area = parse_claim(claim)
        coords = find_area_coords(area, start)
        for coord in coords:
            add_coord(coord, grid)

    counter = 0
    for value in grid.values():
        if value > 1:
            counter += 1

    return counter


if __name__ == "__main__":
    data = parse_input()
    grid = {}
    print(find_covered_points(data, grid))
