import time

from puzzle import *


def unique_equals_constraints():
    return [Constraint("equal", ("nationality", "brit"), ("colour", "red")),
            Constraint("equal", ("nationality", "swede"), ("pet", "dog")),
            Constraint("equal", ("nationality", "dane"), ("beverage", "tea")),
            Constraint("equal", ("colour", "green"), ("beverage", "coffee")),
            Constraint("equal", ("cigar", "pallmall"), ("pet", "bird")),
            Constraint("equal", ("cigar", "dunhill"), ("colour", "yellow")),
            Constraint("equal", ("cigar", "bluemasters"), ("beverage", "beer")),
            Constraint("equal", ("nationality", "german"), ("cigar", "prince"))]


def unique_next_to_constraints():
    return [Constraint("next_to", ("nationality", "norwegian"), ("colour", "blue")),
            Constraint("next_to", ("cigar", "blend"), ("beverage", "water")),
            Constraint("next_to", ("cigar", "blend"), ("pet", "cat")),
            Constraint("next_to", ("cigar", "dunhill"), ("pet", "horse"))]


def unique_left_of_constraints():
    return [Constraint("left_of", ("colour", "green"), ("colour", "white"))]


def print_ordered_constraints(ordered_constraints):
    for i in range(5):
        for constraint in ordered_constraints[i]:
            print constraint


def generate_possibilities(original_list):
    return [original_list[:], original_list[:], original_list[:], original_list[:], original_list[:]]


def instantiate_puzzle():
    colour_poss = ["red", "yellow", "blue", "green", "white"]
    nationality_poss = ["brit", "swede", "dane", "norwegian", "german"]
    beverage_poss = ["tea", "coffee", "milk", "beer", "water"]
    cigar_poss = ["pallmall", "dunhill", "blend", "bluemasters", "prince"]
    pet_poss = ["dog", "bird", "cat", "horse", "fish"]

    colour = generate_possibilities(colour_poss)
    nationality = generate_possibilities(nationality_poss)
    beverage = generate_possibilities(beverage_poss)
    cigar = generate_possibilities(cigar_poss)
    pet = generate_possibilities(pet_poss)

    descriptors_order = ["colour", "nationality", "beverage", "cigar", "pet"]
    puzzle = [colour, nationality, beverage, cigar, pet]
    all_values_for_descriptors = [colour_poss, nationality_poss, beverage_poss, cigar_poss, pet_poss]

    puzzle = Puzzle(puzzle, descriptors_order, all_values_for_descriptors)
    return puzzle


def order_constraints(order, duplicated_constraints):
    ordered_constraints = [[], [], [], [], []]

    for constraint in duplicated_constraints:
        order_index = order.index(constraint.master_descriptor)
        ordered_constraints[order_index].append(constraint)

    return ordered_constraints


def duplicate_and_reverse_constraints(unique_constraints):
    formatted_constraints = []
    for constraint in unique_constraints:
        relationship = constraint.relationship
        if relationship == "left_of":
            relationship = "right_of"
        reversed_constraint = Constraint(relationship, (constraint.slave_descriptor, constraint.slave_value),
                                         (constraint.master_descriptor, constraint.master_value))
        formatted_constraints.append(constraint)
        formatted_constraints.append(reversed_constraint)
    return formatted_constraints


def instantiate_ordered_constraints(order):
    unique_constraints = unique_next_to_constraints() + unique_left_of_constraints() + unique_equals_constraints()
    duplicated_constraints = duplicate_and_reverse_constraints(unique_constraints)

    return order_constraints(order, duplicated_constraints)


def test_enforce():
    puzzle = instantiate_puzzle()
    constraints = instantiate_ordered_constraints(puzzle.descriptors_order)

    # Solving begins
    start_time = time.time()
    set_up_constraints = [Constraint("equal", ("house", 1), ("nationality", "norwegian")),
                          Constraint("equal", ("house", 3), ("beverage", "milk"))]
    set_up(puzzle, set_up_constraints)
    prune_possibilities(constraints, puzzle)

    print("--- %s seconds ---" % (time.time() - start_time))
    print(puzzle)


def test_add_possible_houses():
    where = "right_of"
    house_index_list = [0,2]

    possible_houses = add_possible_houses(where, house_index_list)

    print(possible_houses)


def test_instantiate_puzzle():
    print(instantiate_puzzle())


def test_instantiate_constraints():
    puzzle = instantiate_puzzle()
    print_ordered_constraints(instantiate_ordered_constraints(puzzle.descriptors_order))


if __name__ == "__main__":
    test_enforce()
