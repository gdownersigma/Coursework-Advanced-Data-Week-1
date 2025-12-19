"""Script to find how many measurements increased from the previous measurement."""


def get_input(filename: str) -> list[int]:
    """Returns a list of all the data from the file as integers."""
    with open(filename, 'r') as f:
        data = f.read().split('\n')
        data = [int(d) for d in data]
        return data


def is_increasing(prev_number: int, number: int) -> bool:
    """Returns True when the number is increasing from the previous number, otherwise returns False."""
    if number > prev_number:
        return True

    return False


if __name__ == "__main__":
    data = get_input('data.txt')
    increasing_count = 0
    for index, number in enumerate(data):
        if index == 0:
            continue
        increasing_count += is_increasing(data[index-1], number)
    print(increasing_count)
