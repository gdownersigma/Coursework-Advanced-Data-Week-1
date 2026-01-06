def load_input(filename: str) -> list[int]:
    """Take a filename input as a string and return a list of inputs"""
    with open(filename, 'r') as f:
        return f.readlines()


def find_counts(line: str) -> list:
    """returns a tuple(bool,bool): (a letter appears exactly twice, a letter appears exactly 3 times)"""
    unique = set(line)
    output = [False, False]
    for letter in unique:
        if output[0] is True or line.count(letter) == 2:
            output[0] = True
        if output[1] is True or line.count(letter) == 3:
            output[1] = True

    return output


def find_prototype_boxes(box_ids):
    for i, id1 in enumerate(box_ids):
        for id2 in box_ids[i+1:]:
            differences = sum(c1 != c2 for c1, c2 in zip(id1, id2))

            if differences == 1:
                return ''.join(c1 for c1, c2 in zip(id1, id2) if c1 == c2)


# Read your input
with open('input.txt') as f:
    box_ids = f.read().strip().split('\n')

print(find_prototype_boxes(box_ids))

if __name__ == "__main__":
    input = load_input('input.txt')
    pair_counts = 0
    triplet_counts = 0
    for line in input:
        temp_counts = find_counts(line)
        pair_counts += temp_counts[0]
        triplet_counts += temp_counts[1]
    print(pair_counts*triplet_counts)

    print(find_prototype_boxes(input))
