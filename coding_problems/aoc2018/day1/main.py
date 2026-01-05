"""script for AOC 2018 day 1"""


def read_input(filename: str) -> list[int]:
    """Read all the frequencies and return the integer values"""
    with open(filename, 'r') as f:
        data = f.readlines()
    return [int(d) for d in data]


def has_been(current_total: int, prev_totals: list[int]) -> bool:
    """Returns true if current total has been in previous totals."""
    if current_total in prev_totals:
        return True
    return False


def find_first_dupe(input_data: list[int]) -> int:
    """Finds the first frequency reached twice while cycling through the input data."""
    current_total = 0
    prev_totals = []
    while True:
        for number in input_data:
            if has_been(current_total, prev_totals):
                return current_total
            prev_totals.append(current_total)
            current_total += number


if __name__ == "__main__":
    input_data = read_input('input.txt')
    print(find_first_dupe(input_data))
