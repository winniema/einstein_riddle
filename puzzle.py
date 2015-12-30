class Puzzle:
    def __init__(self, puzzle_board, descriptors_order, all_values_for_descriptors):
        self.descriptors_order = descriptors_order
        self.all_values_for_descriptors = all_values_for_descriptors
        self.modified_row_descriptors = []
        self.puzzle_board = puzzle_board

    def __str__(self):
        to_print = ""
        for i in range(5):
            to_print += str(self.puzzle_board[i])
            if i != 4:
                to_print += "\n"
        return to_print

    def get_row_from_descriptor(self, descriptor):
        row_num = self.descriptors_order.index(descriptor)
        return self.puzzle_board[row_num]

    def get_values_for_house_in_row(self, descriptor, house_num):
        row = self.get_row_from_descriptor(descriptor)
        return row[house_num]

    def get_houses_containing_value_in_row(self, descriptor, value):
        row = self.get_row_from_descriptor(descriptor)

        houses_containing_value_in_row = []
        for house_num in range(len(row)):
            if value in row[house_num]:
                houses_containing_value_in_row.append(house_num)

        return houses_containing_value_in_row

    def set_value_for_house_in_row(self, descriptor, house_num, value):
        row = self.get_row_from_descriptor(descriptor)
        row[house_num] = [value]
        added = self.__remove_value_from_other_houses(descriptor, value)
        return added

    def __get_all_values_for_descriptor(self, descriptor):
        row_num = self.descriptors_order.index(descriptor)
        return self.all_values_for_descriptors[row_num]

    def enforce_uniqueness_in_row(self, descriptor):
        # For conditions such as: [['tea', 'water', 'beer'], ['tea', 'beer'], ['tea', 'beer']]
        added = ""
        row = self.get_row_from_descriptor(descriptor)
        all_values = self.__get_all_values_for_descriptor(descriptor)

        current_values_in_row = sum(row, [])
        values_to_set = []

        for value in all_values:
            if current_values_in_row.count(value) == 1:
                values_to_set.append(value)

        for value in values_to_set:
            for house_num in range(len(row)):
                if value in row[house_num]:
                    added = self.set_value_for_house_in_row(descriptor, house_num, value)

        if added == "":
            added = self.__remove_value_from_other_houses(descriptor)

        return added

    def remove_value_from_house_in_row(self, descriptor, house_num, value):
        row = self.get_row_from_descriptor(descriptor)
        house = row[house_num]

        if value in house:
            house.remove(value)
            added = self.__add_row_as_modified(descriptor)

        return added

    def __remove_value_from_other_houses(self, descriptor, value=False):
        # For conditions such as: [['tea', 'water', 'beer'], ['water'], ['tea', 'water', 'beer']]
        added = ""
        row = self.get_row_from_descriptor(descriptor)

        current_values_in_row = sum(row, [])
        values_to_remove = []

        if not value:
            for house_num in range(len(row)):
                if len(row[house_num]) == 1 and current_values_in_row.count(row[house_num][0]) > 1:
                    values_to_remove.append(row[house_num][0])
        else:
            values_to_remove = [value]

        for value in values_to_remove:
            for house in row:
                if value in house and len(house) != 1:
                    house.remove(value)
                    added = self.__add_row_as_modified(descriptor)
        return added

    def __add_row_as_modified(self, descriptor):
        if descriptor not in self.modified_row_descriptors:
            self.modified_row_descriptors.append(descriptor)
        return descriptor


class Constraint:
    def __init__(self, relationship, (master_descriptor, master_value), (slave_descriptor, slave_value)):
        self.master_descriptor = master_descriptor
        self.master_value = master_value
        self.relationship = relationship
        self.slave_descriptor = slave_descriptor
        self.slave_value = slave_value
        self.exhausted = 0

    def __str__(self):
        lead = (self.master_descriptor, self.master_value)
        lag = (self.slave_descriptor, self.slave_value)

        return str(lead) + " =" + self.relationship + "= " + str(lag)

    def set_as_exhausted(self):
        self.exhausted = 1


def set_up(puzzle, set_up_constraints):
    for constraint in set_up_constraints:
        if constraint.master_descriptor != "house":
            return -1

        house_number = constraint.master_value - 1
        puzzle.set_value_for_house_in_row(constraint.slave_descriptor, house_number, constraint.slave_value)


def prune_possibilities(constraints, puzzle):
    while puzzle.modified_row_descriptors:
        current_descriptor = puzzle.modified_row_descriptors.pop(0)
        descriptor_index = puzzle.descriptors_order.index(current_descriptor)
        constraints_for_descriptor = constraints[descriptor_index]

        for constraint in constraints_for_descriptor:
            if constraint.exhausted:
                continue
            if constraint.relationship == "equal":
                added = enforce_equals(puzzle, constraint)
            else:
                added = enforce_next_to(puzzle, constraint)

            if added != "":
                puzzle.enforce_uniqueness_in_row(added)


def enforce_equals(puzzle=Puzzle, constraint=Constraint):
    added = ""
    for house_num in range(5):
        master_house = puzzle.get_values_for_house_in_row(constraint.master_descriptor, house_num)
        slave_house = puzzle.get_values_for_house_in_row(constraint.slave_descriptor, house_num)

        if len(master_house) == 1 and constraint.master_descriptor in master_house:
            added = puzzle.set_value_for_house_in_row(constraint.slave_descriptor, house_num, constraint.slave_value)
            constraint.set_as_exhausted()
            return added

        if constraint.master_value not in master_house and constraint.slave_value in slave_house:
            added = puzzle.remove_value_from_house_in_row(constraint.slave_descriptor, house_num, constraint.slave_value)

    return added


def enforce_next_to(puzzle=Puzzle, constraint=Constraint):
    added = ""
    house_nums_with_value_master = puzzle.get_houses_containing_value_in_row(constraint.master_descriptor, constraint.master_value)
    house_nums_with_value_slave = puzzle.get_houses_containing_value_in_row(constraint.slave_descriptor, constraint.slave_value)

    allowed_houses = add_possible_houses(constraint.relationship, house_nums_with_value_master)
    feasible_houses_for_slave = get_feasible_houses(allowed_houses, house_nums_with_value_slave)

    if len(feasible_houses_for_slave) == 1:
        added = puzzle.set_value_for_house_in_row(constraint.slave_descriptor, feasible_houses_for_slave[0], constraint.slave_value)
        constraint.set_as_exhausted()
        return added

    for house_num in range(5):
        if house_num not in feasible_houses_for_slave and house_num in house_nums_with_value_slave:
            added = puzzle.remove_value_from_house_in_row(constraint.slave_descriptor, house_num, constraint.slave_value)

    return added


def get_feasible_houses(houses_allowed, current_houses):
    feasible_houses = []
    for house_num in current_houses:
        if house_num in houses_allowed:
            feasible_houses.append(house_num)
    return feasible_houses


def add_possible_houses(where, house_nums):
    possible_houses = []

    for house_num in house_nums:
        right = house_num + 1
        left = house_num - 1

        if where is not "left_of":
            if left >= 0 and left not in possible_houses:
                possible_houses.append(left)
        if where is not "right_of":
            if right <= 4 and right not in possible_houses:
                possible_houses.append(right)

    possible_houses.sort()
    return possible_houses




