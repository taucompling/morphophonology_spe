from __future__ import print_function, division
from io import StringIO
import numpy as np
import re
from segment_table import SegmentTable

NULL_SEGMENT = "-"
NULL_SEGMENT_IDX = -2
NO_TRANSITION_IDX = -1


class ParsingNFA:
    """
    this implementation it not aimed to allow flexible changes to the nfa,
    the nfa is converted from a transducer for order of quick parsing
    """

    def __init__(self):
        self.initial_state = None
        self.final_states = None
        self.arcs_dict = None
        self.probabilities = None
        self.transition_matrix = None

    @classmethod
    def get_from_pyfst_transducer(cls, transducer):
        transducer_symbol_table = SegmentTable().transducer_symbol_table
        nfa = ParsingNFA()
        nfa.final_states = list()
        arcs_dict = dict()
        probabilities = dict()

        num_states = len(list(transducer.states))
        transition_matrix = np.ones((num_states, num_states)) * NO_TRANSITION_IDX

        for state in transducer:
            m = re.match(r".*#(\w*).*", str(state))  # get sate number from the string: "<StdState #x with y arcs>"
            nfa_state1 = m.group(1)
            if state.initial:
                nfa.initial_state = nfa_state1
            if state.final:
                nfa.final_states.append(nfa_state1)

            for arc in state:
                nfa_state2 = str(arc.nextstate)
                output_symbol = transducer_symbol_table.find(arc.olabel)
                if output_symbol == u"\u03b5":
                    output_symbol = NULL_SEGMENT
                if nfa_state1 not in arcs_dict:
                    arcs_dict[nfa_state1] = {}
                    probabilities[nfa_state1] = []
                if output_symbol not in arcs_dict[nfa_state1]:
                    arcs_dict[nfa_state1][output_symbol] = []

                arcs_dict[nfa_state1][output_symbol].append(nfa_state2)
                probabilities[nfa_state1].append((output_symbol, nfa_state2))

                segment_idx = NULL_SEGMENT_IDX if output_symbol == NULL_SEGMENT else arc.olabel
                transition_matrix[int(nfa_state1), int(nfa_state2)] = segment_idx

        nfa.arcs_dict = arcs_dict
        nfa.probabilities = probabilities
        nfa.transition_matrix = transition_matrix
        return nfa

    def get_probability(self, state, value, terminal_state):
        return 1 / len(self.probabilities[state])

    def _get_segment_by_state_dict(self):
        segment_by_state_dict = dict()
        for origin_state in self.probabilities:
            for segment_terminal_state_tuple in self.probabilities[origin_state]:
                segment = segment_terminal_state_tuple[0]
                terminal_state = segment_terminal_state_tuple[1]
                weight = 1
                segment_weight_tuple = (segment, weight)
                if origin_state not in segment_by_state_dict:
                    segment_by_state_dict[origin_state] = dict()
                if terminal_state not in segment_by_state_dict[origin_state]:
                    segment_by_state_dict[origin_state][terminal_state] = [segment_weight_tuple]
                else:
                    for i, existing_tuple in enumerate(segment_by_state_dict[origin_state][terminal_state]):
                        if existing_tuple[0] == segment_weight_tuple[0]:
                            segment_by_state_dict[origin_state][terminal_state][i] = (existing_tuple[0],
                                                                                      (existing_tuple[1] +
                                                                                       segment_weight_tuple[1]))
                            break
                    else:
                        segment_by_state_dict[origin_state][terminal_state].append(segment_weight_tuple)
        return segment_by_state_dict

    def _arcs_dot_representation(self):
        def segment_weight_str(segment_weight_tuple):
            if segment_weight_tuple[1] == 1:
                return segment_weight_tuple[0]
            else:
                return "{} ({})".format(*segment_weight_tuple)

        str_io = StringIO()
        printed_multiple_arcs = list()
        segment_by_state_dict = self._get_segment_by_state_dict()
        for origin_state in self.arcs_dict:
            terminal_state_list = [item for sublist in self.arcs_dict[origin_state].values() for item in sublist]
            for terminal_state in terminal_state_list:
                if len(segment_by_state_dict[origin_state][terminal_state]) > 1:
                    if (origin_state, terminal_state) not in printed_multiple_arcs:
                        combined_label = ""
                        segments = segment_by_state_dict[origin_state][terminal_state]
                        for segment in segments:
                            combined_label += "{} \\n".format(segment_weight_str(segment))

                        combined_label += "\\n" * len(segments)

                        print("\"{}\" -> \"{}\" [label=\"{}\"];".format(
                            origin_state, terminal_state, combined_label), file=str_io, end="\n")

                        printed_multiple_arcs.append((origin_state, terminal_state))

                else:
                    segment = next(
                        iter(segment_by_state_dict[origin_state][terminal_state]))  # get the single element from set
                    print("\"{}\" -> \"{}\" [label=\"{} \\n\"];".format(
                        origin_state, terminal_state, segment_weight_str(segment)), file=str_io, end="\n")

        return str_io.getvalue()

    def draw(self):
        str_io = StringIO()
        print("digraph acceptor {", file=str_io, end="\n")
        print("rankdir=LR", file=str_io, end="\n")
        print("size=\"11,5\"", file=str_io, end="\n")
        print("node [shape = ellipse];", file=str_io, end="\n")

        print("// arcs: source -> dest [label]", file=str_io, end="\n")
        print(self._arcs_dot_representation(), file=str_io, end="")

        print("// start nodes", file=str_io, end="\n")
        print("\"{}\" [style=filled];".format(self.initial_state), file=str_io, end="\n")

        print("// final nodes", file=str_io, end="\n")
        for state in self.final_states:
            print("\"{}\" [peripheries=2];".format(state), file=str_io, end="\n")

        print("}", file=str_io, end="")

        return str_io.getvalue()

    def __str__(self):
        str_io = StringIO()
        print("initial state: {0}".format(self.initial_state), file=str_io, end="\n")
        print("final states: {0}".format(self.final_states), file=str_io, end="\n")
        print("arcs_dict: {0}".format(self.arcs_dict), file=str_io, end="\n")
        print("probabilities: {0}".format(self.probabilities), file=str_io, end="\n")
        return str_io.getvalue()
