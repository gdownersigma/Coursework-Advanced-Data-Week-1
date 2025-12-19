"""Script to find how many measurements increased from the previous measurement."""


def get_input(filename: str) -> list[int]:
    """Returns a list of all the data from the file as integers."""
    with open(filename, 'r') as f:
        data = f.read().split('\n')
        data = [int(d) for d in data]
        return data


def is_near_end(index: int, length: int) -> bool:
    """Returns False if the index will reach past the end of the list."""
    if index+2 >= length:
        return False
    return True


def is_triple_increasing(index_1: int, index_2: int, data: list[int]) -> bool:
    """Returns True when index1 plus two items infront > index2 plus two items in front."""
    if not is_near_end(index_2, len(data)):
        return False

    sum1 = sum([data[index_1], data[index_1 + 1], data[index_1 + 2]])
    sum2 = sum([data[index_2], data[index_2 + 1], data[index_2 + 2]])

    print(sum1, sum2)

    if sum2 > sum1:
        return True

    return False


if __name__ == "__main__":
    data = get_input('data.txt')
    increasing_count = 0
    for index, number in enumerate(data):
        if index == 0:
            continue
        increasing_count += is_triple_increasing(index, index+1, data)
    print(increasing_count)
