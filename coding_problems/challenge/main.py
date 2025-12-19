# need a function to check if the value is up or down

# need a function to loop through the instruction and return the total items being carried.

# maybe function to make sure its not below 0.

def what_action(char: str) -> int:
    """Returns 1 if pickup, 0 if nothing, -1 if put down."""
    if char == '^':
        return 1
    elif char == 'v':
        return -1
    else:
        return 0


def loop_instruction(instruction: str) -> int:
    """Returns the total items held."""
    items_in_hand = 0
    for action in instruction:
        items_in_hand += what_action(action)
        if items_in_hand < 0:
            items_in_hand = 0
    return items_in_hand


# function to find the max load at any point from an instruction

def find_max_load(instruction: str) -> int:
    """Find the maximum load a robot carries at any time."""
    items_in_hand = 0
    max_items_held = 0
    for action in instruction:
        items_in_hand += what_action(action)
        if items_in_hand < 0:
            items_in_hand = 0
            if items_in_hand > max_items_held:
                max_items_held = items_in_hand
    return max_items_held


# function to loop through instruction set and store a list of the max load, return index of the max


def find_heaviest_max(instruction_set: list[str]) -> int:
    """Returns the index of the instruction with heaviest max."""
    maxes = []
    for instruction in instruction_set:
        maxes.append(find_max_load(instruction))
    return maxes.index(max(maxes))


# create a list of tuples with load in index 0 and distance in index 1

# function to handle the logic for looping each instruction

def find_longest_distance_max_load(instructions: str) -> int:
    """Returns the distance under maximum load"""
    items_held = 0
    distance_moved = 0
    movements = []
    for action in instructions:
        if what_action(action) == 0:
            distance_moved += 1
        elif items_held == 0 and what_action(action) == -1:
            items_held = 0
            continue
        movements.append((items_held, distance_moved))
        items_held += what_action(action)
        distance_moved = 0

    maximum_load = 0
    max_distance_at_largest_load = 0
    for movement in movements:
        if movement[0] > maximum_load:
            maximum_load = movement[0]

    for movement in movements:
        if movement[0] == maximum_load and max_distance_at_largest_load < movement[1]:
            max_distance_at_largest_load = movement[1]

    return max_distance_at_largest_load


def find_total_energy(instructions: str) -> int:
    items_held = 0
    distance_moved = 0
    movements = []
    for action in instructions:
        if what_action(action) == 0:
            distance_moved += 1
        elif items_held == 0 and what_action(action) == -1:
            items_held = 0
            continue
        movements.append((items_held, distance_moved))
        items_held += what_action(action)
        distance_moved = 0
    total_energy = 0
    for movement in movements:
        total_energy += movement[0] * movement[1]

    return total_energy


if __name__ == '__main__':
    print(find_total_energy('^..^..^..'))
