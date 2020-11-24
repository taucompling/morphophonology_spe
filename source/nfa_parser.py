from math import log
from copy import copy, deepcopy

from automata.parsing_nfa import NULL_SEGMENT
from segment_table import MORPHEME_BOUNDARY, WORD_BOUNDARY

ignored_segments = [NULL_SEGMENT, MORPHEME_BOUNDARY, WORD_BOUNDARY]


class TableCell:
    def __init__(self, output, back_pointers):
        self.output = output
        self.back_pointers = back_pointers

    def __repr__(self):
        return "Output: {}, back pointers: {}".format(self.output, " | ".join(str(self.back_pointers)))


class BackPointer:
    def __init__(self, probability, state_back_pointers, position_back_pointer):
        self.probability = probability
        self.state_back_pointer = state_back_pointers
        self.position_back_pointer = position_back_pointer

    def __repr__(self):
        return "{:.2f}, ({}, {})".format(self.probability, self.state_back_pointer, self.position_back_pointer)

    def __str__(self):
        return self.__repr__()


def nfa_parser_get_all_parses(nfa, observation):
    observation = " " + observation + " "
    observation_length = len(observation)
    table = [{} for _ in range(observation_length)]

    # Initialize the first column
    for segment in nfa.arcs_dict.get(nfa.initial_state, []):
        for state2 in nfa.arcs_dict[nfa.initial_state][segment]:
            probability = nfa.get_probability(nfa.initial_state, segment, state2)
            back_pointer = BackPointer(probability, nfa.initial_state, -1)
            table_cell = TableCell(segment, [back_pointer])
            if probability:
                if segment in ignored_segments:
                    table[0][state2] = table_cell
                elif segment == observation[1]:
                    table[1][state2] = table_cell

    # fill out the rest of the table
    for position in range(1, observation_length):
        states = deepcopy(table[position - 1])
        while states:
            new_states = set()

            for state1 in states:
                if state1 in nfa.final_states:
                    continue
                for segment in nfa.arcs_dict.get(state1, []):
                    for state2 in nfa.arcs_dict[state1][segment]:
                        probability = nfa.get_probability(state1, segment, state2)
                        back_pointer = BackPointer(probability, state1, position - 1)
                        table_cell = TableCell(segment, [back_pointer])
                        if segment in ignored_segments:
                            if state2 not in table[position - 1]:
                                table[position - 1][state2] = table_cell
                                new_states.add(state2)
                            else:
                                table[position - 1][state2].back_pointers.append(back_pointer)
                        elif segment == observation[position]:
                            if state2 not in table[position]:
                                table[position][state2] = table_cell
                            else:
                                table[position][state2].back_pointers.append(back_pointer)
            states = new_states

    # Recursively backtrack all paths
    backward_parse_paths = []
    for final_state in nfa.final_states:
        if final_state not in table[-2]:
            continue
        parse_path(nfa, table, final_state, observation_length - 2, 0, [], backward_parse_paths)

    full_parse_paths = [list(reversed(_)) for _ in backward_parse_paths]

    return full_parse_paths


def parse_path(nfa, table, state, position, step, path, all_paths):
    if position == -1:
        if state == nfa.initial_state:
            path.append(state)
            all_paths.append(path)
        return
    else:
        for _back_pointer in table[position][state].back_pointers:
            _path = copy(path)
            _path.append(state)
            parse_path(nfa, table,
                       _back_pointer.state_back_pointer,
                       _back_pointer.position_back_pointer,
                       step + 1,
                       _path,
                       all_paths)


def nfa_parser_get_most_probable_parse(nfa, observation):
    observation = " " + observation + " "
    observation = observation
    observation_length = len(observation)
    table = [{} for _ in range(observation_length)]

    # Initialize the first column
    for segment in nfa.arcs_dict.get(nfa.initial_state, []):
        for state2 in nfa.arcs_dict[nfa.initial_state][segment]:
            probability = nfa.get_probability(nfa.initial_state, segment, state2)
            back_pointer = BackPointer(log(probability), nfa.initial_state, 0)
            table_cell = TableCell(segment, [back_pointer])
            if probability:
                if segment in ignored_segments:
                    table[0][state2] = table_cell
                elif segment == observation[1]:
                    table[1][state2] = table_cell

    # fill out the rest of the table
    for position in range(1, observation_length):
        states = deepcopy(table[position - 1])
        while states:
            new_states = set()

            for state1 in states:
                if state1 in nfa.final_states:
                    continue
                for segment in nfa.arcs_dict.get(state1, []):
                    for state2 in nfa.arcs_dict[state1][segment]:
                        probability = nfa.get_probability(state1, segment, state2)
                        if probability:
                            combined_probability = log(probability) + table[position - 1][state1].back_pointers[0].probability
                            back_pointer = BackPointer(combined_probability, state1, position-1)
                            table_cell = TableCell(segment, [back_pointer])
                            if segment in ignored_segments:
                                if state2 not in table[position - 1]:
                                    table[position - 1][state2] = table_cell
                                    new_states.add(state2)
                                elif combined_probability > table[position-1][state2].back_pointers[0].probability:
                                    table[position - 1][state2] = table_cell
                                    new_states.add(state2)
                            elif segment == observation[position]:
                                if state2 not in table[position]:
                                    table[position][state2] = table_cell
                                elif combined_probability > table[position][state2].back_pointers[0].probability:
                                    table[position][state2] = table_cell
            states = new_states

    # print_table(table, observation)

    optimal_final_state = None
    optimal_probability = float("-inf")
    for final_state in nfa.final_states:
        if final_state in table[-2]:
            probability = table[-2][final_state].back_pointers[0].probability
            if probability > optimal_probability:
                optimal_final_state = final_state
                optimal_probability = probability

    if not optimal_final_state:
        return None

    current_state = optimal_final_state
    current_position = len(table) - 2
    backward_states_path = [current_state]
    backward_outputs_path = list()
    while True:
        current_cell = table[current_position][current_state]
        current_state = current_cell.back_pointers[0].state_back_pointer
        current_position = current_cell.back_pointers[0].position_back_pointer
        current_output = current_cell.output
        backward_states_path.append(current_state)
        backward_outputs_path.append(current_output)
        if current_state == nfa.initial_state:
            break

    states_path = list(reversed(backward_states_path))
    outputs_path = list(reversed(backward_outputs_path))
    return states_path, outputs_path


# for debugging
def print_table(table, observation):
    print("table:")
    for i, segment in enumerate(observation):
        items = list(table[i].items())
        items = sorted(items)
        items = ["{}: {}".format(item[0], item[1]) for item in items]
        row = " , ".join(items)
        print(repr(segment), "[{}]".format(row))
