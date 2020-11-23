from math import log
import numpy as np

from uniform_encoding import UniformEncoding
from feature_bundle import FeatureBundle
from random import random, choice, randint, sample
from configuration import Configuration
from io import StringIO
from itertools import chain
import fst
from scipy.sparse.csgraph import connected_components, breadth_first_order
from fst import EPSILON
from segment_table import SegmentTable, MORPHEME_BOUNDARY, WORD_BOUNDARY
from collections import namedtuple
from util import get_weighted_list, pickle_deepcopy as deepcopy

configurations = Configuration()
uniform_encoding = UniformEncoding()

INITIAL_STATE = 'q0'
FINAL_STATE = 'qf'

ALLOW_DUPLICATE_EMISSIONS = True
REMOVE_ORIG = True

StateTuple = namedtuple('StateTuple', ['start_state', 'end_state'])


class HMM:
    def __init__(self, hmm_dict):
        initial_state_transitions = hmm_dict.pop(INITIAL_STATE)
        self.transitions = {k: v[0] for (k, v) in hmm_dict.items()}
        self.transitions[INITIAL_STATE] = initial_state_transitions
        self.emissions = {k: v[1] for (k, v) in hmm_dict.items()}
        self.inner_states = self._get_inner_states()

    @classmethod
    def create_hmm_from_dicts(cls, transition_dict, emission_dict):
        hmm = HMM({INITIAL_STATE: [FINAL_STATE]})
        hmm.transitions = {k: v for k, v in transition_dict}
        hmm.emissions = {k: v for k, v in emission_dict}
        hmm.inner_states = hmm._get_inner_states()
        return hmm

    @classmethod
    def get_default_hmm(cls):
        segments = SegmentTable().get_segments_symbols(include_boundary_symbols=False)
        return HMM({INITIAL_STATE: ['q1'],
                    'q1': (['q1', FINAL_STATE], segments)})

    def get_transducer(self):
        list_of_transducer_states = TransducerStatesLookup()

        HMM_INITIAL_STATE = INITIAL_STATE
        HMM_FINAL_STATE = FINAL_STATE
        transducer_symbol_table = SegmentTable().transducer_symbol_table
        transducer = fst.Transducer(isyms=transducer_symbol_table, osyms=transducer_symbol_table)
        list_of_transducer_states.append(HMM_INITIAL_STATE)

        state_dict = dict()
        state_dict[HMM_INITIAL_STATE] = StateTuple(None, HMM_INITIAL_STATE)
        for hmm_state in sorted(self.inner_states):  # sorted for consistency in encoding later on
            start_state = "{}_start".format(hmm_state)
            end_state = "{}_end".format(hmm_state)
            list_of_transducer_states.extend([start_state, end_state])
            state_dict[hmm_state] = StateTuple(start_state, end_state)

        # create states
        for hmm_state in self.emissions:
            for emission_index, emission in enumerate(self.emissions[hmm_state]):
                emission_states_list = ["{},{},{}".format(hmm_state, emission_index, segment_index)
                                        for segment_index in range(len(emission) - 1)]

                list_of_transducer_states.extend(emission_states_list)

        list_of_transducer_states.append(HMM_FINAL_STATE)

        initial_state = list_of_transducer_states.index(HMM_INITIAL_STATE)
        final_state = list_of_transducer_states.index(HMM_FINAL_STATE)

        transducer[initial_state].initial = True
        transducer[final_state].final = True

        # transiton arcs
        for hmm_state1 in self.transitions:
            for hmm_state2 in self.transitions[hmm_state1]:
                state1 = list_of_transducer_states.index(state_dict[hmm_state1].end_state)

                if hmm_state2 != HMM_FINAL_STATE:
                    state2 = list_of_transducer_states.index(state_dict[hmm_state2].start_state)
                else:
                    state2 = final_state

                if configurations["MORPHEME_BOUNDARY_FLAG"]:
                    if hmm_state1 != HMM_INITIAL_STATE:
                        arc_label = MORPHEME_BOUNDARY
                    else:
                        arc_label = EPSILON

                elif configurations["WORD_BOUNDARY_FLAG"]:
                    if hmm_state2 == HMM_FINAL_STATE:
                        arc_label = WORD_BOUNDARY
                    else:
                        arc_label = EPSILON

                else:  # nominal case
                    arc_label = EPSILON
                transducer.add_arc(state1, state2, arc_label, arc_label)

        # emission arcs
        for hmm_state in self.emissions:
            start_state = state_dict[hmm_state].start_state
            end_state = state_dict[hmm_state].end_state
            for emission_index, emission in enumerate(self.emissions[hmm_state]):
                string_states_list = [start_state] + ["{},{},{}".format(hmm_state, emission_index, segment_index)
                                                      for segment_index in range(len(emission) - 1)] + [end_state]
                states_list = [list_of_transducer_states.index(state) for state in string_states_list]

                for i in range(len(emission)):
                    transducer.add_arc(states_list[i], states_list[i + 1], emission[i], emission[i])
        transducer = uniform_encoding.get_weighted_transducer(transducer)
        return transducer

    def _get_inner_states(self):
        states = set()
        for state_key in self.transitions:
            states.add(state_key)
            for state_transition in self.transitions[state_key]:
                states.add(state_transition)
        if FINAL_STATE in states:
            states.remove(FINAL_STATE)
        if INITIAL_STATE in states:
            states.remove(INITIAL_STATE)
        return self.sort_state_names(list(states))

    def get_states(self):
        return [INITIAL_STATE] + self.inner_states + [FINAL_STATE]

    def get_transitions(self, state):
        """used in get_encoding_length"""
        return self.transitions.get(state, [])

    def get_emissions(self, state):
        """used in get_encoding_length"""
        return self.emissions.get(state, [])

    def get_all_emissions(self):
        emissions = set()
        for state in self.emissions:
            emissions |= set(self.emissions[state])
        return list(emissions)

    def get_distinct_segments(self):
        distinct_segments = set()
        for emission in self.get_all_emissions():
            distinct_segments = distinct_segments | set(emission)
        return distinct_segments

    def get_encoding_length(self, segment_symbol_length, restrictions_on_alphabet=False):
        encoding_length = 0
        if restrictions_on_alphabet:
            number_of_distinct_symbols = len(self.get_distinct_segments())
            segment_symbol_length = uniform_encoding.log2(number_of_distinct_symbols + 1)
            restriction_set_length = number_of_distinct_symbols * (2 * segment_symbol_length)  # encode segment and delimiter
            encoding_length = restriction_set_length
        states_list = self.get_states()
        states_symbol_length = uniform_encoding.log2(len(states_list) + 1)  # + 1 for the delimiter

        state_symbols_in_transitions = 0
        total_num_of_emissions = 0
        segments_in_emissions = 0

        for state in states_list:
            state_symbols_in_transitions += len(self.get_transitions(state)) + 1  # +1 indicate the origin state

            for emission in self.get_emissions(state):
                total_num_of_emissions += 1
                segments_in_emissions += len(emission)

        num_bits = states_symbol_length + 1
        content_usage = (state_symbols_in_transitions * states_symbol_length) + (
            segments_in_emissions * segment_symbol_length)
        delimiter_usage = (len(states_list) * segment_symbol_length) + \
                          (len(states_list) * states_symbol_length) + \
                          total_num_of_emissions * segment_symbol_length
        encoding_length += num_bits + content_usage + delimiter_usage

        return encoding_length

    def get_underspecified_encoding_length(self):
        states_list = self.get_states()
        states_symbol_length = uniform_encoding.log2(len(states_list) + 1)  # + 1 for the delimiter

        state_symbols_in_transitions = 0
        total_num_of_emissions = 0
        segments_in_emissions = []

        for state in states_list:
            state_symbols_in_transitions += len(self.get_transitions(state)) + 1  # +1 indicate the origin state

            for emission in self.get_emissions(state):
                total_num_of_emissions += 1
                segments_in_emissions.extend(list(emission))

        segments_encoding_length = 0
        for segment in segments_in_emissions:
            if segment == 'T':
                segments_encoding_length += 7
            else:
                segments_encoding_length += 8

        num_bits = states_symbol_length + 1
        content_usage = (state_symbols_in_transitions * states_symbol_length) + segments_encoding_length
        delimiter_usage = (len(states_list) * states_symbol_length)

        encoding_length = num_bits + content_usage + delimiter_usage

        return encoding_length

    def _get_next_state(self):
        state_numbers = [int(x[1:]) for x in self.inner_states]  # remove 'q'
        state_numbers.append(0)
        state_numbers.sort()
        next_state_number = None

        if len(state_numbers) == state_numbers[-1] + 1:
            next_state_number = len(state_numbers)
        else:
            for i in range(len(state_numbers) - 1):
                if state_numbers[i] + 1 != state_numbers[i + 1]:
                    next_state_number = i + 1
                    break

        new_state = 'q{}'.format(next_state_number)

        return new_state

    def draw(self):
        def weight_str(dict_, key, value):
            weight = 1
            if weight != 1:
                return "({})".format(weight)
            else:
                return ""

        str_io = StringIO()
        print("digraph acceptor {", file=str_io, end="\n")
        print("rankdir=LR", file=str_io, end="\n")
        print("size=\"11,5\"", file=str_io, end="\n")
        print("node [shape = ellipse];", file=str_io, end="\n")

        print("//transitions arcs", file=str_io, end="\n")
        for state1 in self.transitions:
            for state2 in self.transitions[state1]:
                print("\"{}\" ->  \"{}\" [label=\"{}\"];".format(state1, state2,
                                                                 weight_str(self.transitions, state1, state2)),
                      file=str_io, end="\n")

        print("//emission tables lines", file=str_io, end="\n")
        for state in self.emissions:
            print("\"{}\" -> {}_emission_table [arrowhead=\"none\",arrowtail=\"none\"]".format(state, state),
                  file=str_io, end="\n")

        print("//emission tables", file=str_io, end="\n")
        for state in self.inner_states:
            emissions_label = ""
            for emission in self.emissions[state]:
                emissions_label += "{} {}\\n".format(emission, weight_str(self.emissions, state, emission))
            print("{}_emission_table [shape=none, label=\"{}\"]".format(state, emissions_label), file=str_io, end="\n")

        print("\"q0\" [style=filled];", file=str_io, end="\n")
        print("\"qf\" [peripheries=2];", file=str_io, end="\n")
        print("}", file=str_io, end="")

        return str_io.getvalue()

    @classmethod
    def crossover(cls, hmm_1, hmm_2):
        num_crossovers = randint(1, configurations["HMM_MAX_CROSSOVERS"])
        offspring_1, offspring_2 = hmm_1, hmm_2
        for _ in range(num_crossovers):
            if configurations["HMM_CROSSOVER_METHOD"] == 'emissions':
                offspring_1, offspring_2 = HMM.crossover_emissions_to_one_parent(offspring_1, offspring_2)
            elif configurations["HMM_CROSSOVER_METHOD"] == 'matrix':
                offspring_1, offspring_2 = HMM.crossover_by_matrix(offspring_1, offspring_2)
            elif configurations["HMM_CROSSOVER_METHOD"] == 'subgraph':
                offspring_1, offspring_2 = HMM.crossover_subgraphs(offspring_1, offspring_2)
            elif configurations["HMM_CROSSOVER_METHOD"] == 'connected_component':
                offspring_1, offspring_2 = HMM.crossover_connected_components(offspring_1, offspring_2)
            else:
                raise ValueError(f"Unknown HMM crossover method: {configurations['HMM_CROSSOVER_METHOD']}")
        return offspring_1, offspring_2

    @classmethod
    def crossover_emissions_to_one_parent(cls, hmm_1, hmm_2):
        """
        1. Randomly choose emissions from parent_2 with probability 1 / log(number of emissions in HMM)
        2. Add chosen emissions to same state in parent_1, if it exists
        """
        hmm_2_emissions = hmm_2.get_all_emissions()
        num_emissions_in_source_hmm = len(hmm_2_emissions)

        if num_emissions_in_source_hmm == 0:
            return hmm_1, hmm_2

        transition_probab = 1 / max(1, log(num_emissions_in_source_hmm, 2))

        offspring_1 = deepcopy(hmm_1)
        offspring_2 = deepcopy(hmm_2)
        offspring_1.ensure_contiguous_state_indices()
        offspring_2.ensure_contiguous_state_indices()

        for source_state in offspring_2.inner_states:
            if source_state not in offspring_1.inner_states:  # state doesn't exist in target hmm
                continue

            for emission in offspring_2.emissions[source_state]:
                should_crossover = random() < transition_probab
                if should_crossover and emission not in offspring_1.emissions[source_state]:
                    offspring_1.emissions[source_state].append(emission)
        return offspring_1, offspring_2

    @classmethod
    def crossover_by_matrix(cls, hmm_1, hmm_2):
        """
        1. Represent both HMMs as transition matrix
        2. Uniformly choose rows from either matrix to switch (each row probab 0.5 from either parent)
        3. Each state that is switched also moves with its emissions from parent
        """
        hmm_1.ensure_contiguous_state_indices()
        hmm_2.ensure_contiguous_state_indices()

        parent_matrix_1 = hmm_1.get_transition_matrix()
        parent_matrix_2 = hmm_2.get_transition_matrix()
        parent_emissions_1 = hmm_1.emissions
        parent_emissions_2 = hmm_2.emissions

        parent_1_dim = len(parent_matrix_1)
        parent_2_dim = len(parent_matrix_2)
        min_dim = min(parent_1_dim, parent_2_dim)
        max_dim = max(parent_1_dim, parent_2_dim)

        switch_states = [choice([True, False]) for _ in range(min_dim)]

        offspring_1_matrix = parent_matrix_1.copy()
        offspring_2_matrix = parent_matrix_2.copy()

        offspring_emissions_1 = deepcopy(parent_emissions_1)
        offspring_emissions_2 = deepcopy(parent_emissions_2)

        for row in range(min_dim):
            state_name_parent_1 = get_state_name(row, parent_1_dim)
            state_name_parent_2 = get_state_name(row, parent_2_dim)

            if switch_states[row]:
                # Switch state transitions
                offspring_1_matrix[row, :min_dim] = parent_matrix_2[row, :min_dim]
                offspring_2_matrix[row, :min_dim] = parent_matrix_1[row, :min_dim]

                # Switch states emissions
                if row > 0 and state_name_parent_1 != FINAL_STATE and state_name_parent_2 != FINAL_STATE:
                    # TODO Maybe switch only some of the emissions?
                    offspring_emissions_1[state_name_parent_1] = parent_emissions_2[state_name_parent_2]
                    offspring_emissions_2[state_name_parent_2] = parent_emissions_1[state_name_parent_1]

        offspring_1 = HMM.hmm_from_transition_matrix(offspring_1_matrix, offspring_emissions_1)
        offspring_2 = HMM.hmm_from_transition_matrix(offspring_2_matrix, offspring_emissions_2)
        return offspring_1, offspring_2

    @classmethod
    def crossover_subgraphs(cls, hmm_1, hmm_2):
        """
        1. Select connected component C_i, including qf
        2. Select entry point to C_i, e_i
        3. BFS from e_i, mark all reached nodes as SG_i
        4. Mark all nodes with arcs to C_i, as A_i
        5. Remove all SG_i nodes and arcs leading to it
        6. Insert SG_i+1
        7. Connect all a_j <in> A_i to e_i+1
        """

        hmm_1.ensure_contiguous_state_indices()
        hmm_2.ensure_contiguous_state_indices()

        states_1 = hmm_1.get_states()
        states_2 = hmm_2.get_states()

        transition_matrix_1 = hmm_1.get_transition_matrix()
        transition_matrix_2 = hmm_2.get_transition_matrix()

        components_to_states_1 = hmm_1.get_connected_components(ignore_final=False, ignore_initial=True)
        components_to_states_2 = hmm_2.get_connected_components(ignore_final=False, ignore_initial=True)

        selected_component_1 = choice(components_to_states_1)
        selected_component_2 = choice(components_to_states_2)

        entry_state_1 = selected_component_1[0]
        entry_state_2 = selected_component_2[0]

        # print('entry 1', entry_state_1)
        # print('entry 2', entry_state_2)

        subgraph_1_states_idx = breadth_first_order(transition_matrix_1, states_1.index(entry_state_1), directed=True,
                                                    return_predecessors=False)
        subgraph_2_states_idx = breadth_first_order(transition_matrix_2, states_2.index(entry_state_2), directed=True,
                                                    return_predecessors=False)

        subgraph_1_state_names = [states_1[s] for s in subgraph_1_states_idx]
        subgraph_2_state_names = [states_2[s] for s in subgraph_2_states_idx]

        # print(subgraph_1_state_names)
        # print(subgraph_2_state_names)

        entry_arcs_1 = cls._get_component_entry_arcs(hmm_1, selected_component_1)
        entry_arcs_2 = cls._get_component_entry_arcs(hmm_2, selected_component_2)

        # print(entry_arcs_1)
        # print(entry_arcs_2)

        offspring_1 = deepcopy(hmm_1)
        offspring_2 = deepcopy(hmm_2)

        HMM._add_subgraph(source_hmm=hmm_2, target_hmm=offspring_1, source_states=subgraph_2_state_names,
                          target_states=subgraph_1_state_names, source_subgraph_entry_state=entry_state_2,
                          target_hmm_entry_arcs=entry_arcs_1)

        HMM._add_subgraph(source_hmm=hmm_1, target_hmm=offspring_2, source_states=subgraph_1_state_names,
                          target_states=subgraph_2_state_names, source_subgraph_entry_state=entry_state_1,
                          target_hmm_entry_arcs=entry_arcs_2)

        if len(offspring_1.inner_states) == 0 or len(offspring_2.inner_states) == 0:
            return hmm_1, hmm_2,

        return offspring_1, offspring_2

    @classmethod
    def crossover_connected_components(cls, hmm_1, hmm_2):
        """
        Crossover of connected components from each HMM.

        - Get connected components from both HMM
        - Select random components from each, switch
        - Crossover emissions
        """

        # hmm_1 = deepcopy(hmm_1)
        # hmm_2 = deepcopy(hmm_2)

        hmm_1.ensure_contiguous_state_indices()
        hmm_2.ensure_contiguous_state_indices()

        components_to_states_1 = hmm_1.get_connected_components()
        components_to_states_2 = hmm_2.get_connected_components()

        selected_component_1 = choice(components_to_states_1)
        selected_component_2 = choice(components_to_states_2)

        entry_state_1 = selected_component_1[0]
        entry_arcs_1 = cls._get_component_entry_arcs(hmm_1, selected_component_1)
        exit_state_1 = selected_component_1[-1]
        exit_arcs_1 = cls._get_component_exit_arcs(hmm_1, selected_component_1)

        entry_state_2 = selected_component_2[0]
        entry_arcs_2 = cls._get_component_entry_arcs(hmm_2, selected_component_2)
        exit_state_2 = selected_component_2[-1]
        exit_arcs_2 = cls._get_component_exit_arcs(hmm_2, selected_component_2)

        # Choose random locus to crossover emissions
        hmm_1_emissions = list(chain(*[hmm_1.emissions[s] for s in selected_component_1]))
        hmm_2_emissions = list(chain(*[hmm_2.emissions[s] for s in selected_component_2]))
        all_emissions = hmm_1_emissions + hmm_2_emissions
        emissions_crossover_point = randint(0, len(all_emissions))

        offspring_1_emissions = all_emissions[:emissions_crossover_point]
        offspring_2_emissions = all_emissions[emissions_crossover_point:]

        offspring_1 = deepcopy(hmm_1)
        offspring_2 = deepcopy(hmm_2)

        # Crossover from hmm2 to hmm1
        HMM._crossover_components(source_hmm=hmm_2, target_hmm=offspring_1,
                                  target_component_states=selected_component_1,
                                  source_component_states=selected_component_2, component_entry_state=entry_state_2,
                                  component_exit_state=exit_state_2, hmm_entry_arcs=entry_arcs_1,
                                  hmm_exit_arcs=exit_arcs_1, target_emissions=offspring_1_emissions)

        # Crossover from hmm1 to hmm2
        HMM._crossover_components(source_hmm=hmm_1, target_hmm=offspring_2,
                                  target_component_states=selected_component_2,
                                  source_component_states=selected_component_1, component_entry_state=entry_state_1,
                                  component_exit_state=exit_state_1, hmm_entry_arcs=entry_arcs_2,
                                  hmm_exit_arcs=exit_arcs_2, target_emissions=offspring_2_emissions)

        return offspring_1, offspring_2

    @staticmethod
    def _get_component_entry_arcs(hmm, component_states):
        entry_arcs = set()
        component_states = set(component_states)
        hmm_states = hmm.get_states()
        for state in component_states:
            entry_arcs |= set([from_state for from_state in hmm_states if
                               state in hmm.transitions.get(from_state, [])])
        entry_arcs -= component_states
        return list(entry_arcs)

    @staticmethod
    def _get_component_exit_arcs(hmm, component_states):
        exit_arcs = set()
        component_states = set(component_states)
        for state in component_states:
            exit_arcs |= set(hmm.transitions[state])
        exit_arcs -= component_states
        return list(exit_arcs)

    @staticmethod
    def _crossover_components(source_hmm, target_hmm, source_component_states, target_component_states,
                              component_entry_state, component_exit_state, hmm_entry_arcs, hmm_exit_arcs,
                              target_emissions):

        if len(target_hmm.inner_states) - len(target_component_states) + len(source_component_states) > configurations[
            "MAX_NUM_OF_INNER_STATES"]:
            return

        # Remove selected component from target HMM
        target_hmm.remove_states(target_component_states)

        # Get new names for crossed-over states in new HMM
        added_states = []
        source_states_to_target_names = {}
        for source_state in source_component_states:
            state_new_name = target_hmm._add_state()
            added_states.append(state_new_name)
            source_states_to_target_names[source_state] = state_new_name

        # Add emissions to crossed-over states
        while target_emissions:
            emission = target_emissions.pop(0)
            state = choice(added_states)
            state_emissions = target_hmm.emissions[state]
            if emission not in state_emissions:
                state_emissions.append(emission)

        for source_state in source_component_states:
            state_new_name = source_states_to_target_names[source_state]

            # Insert component to other graph and rename states
            for to_state in source_hmm.transitions[source_state]:
                if to_state not in source_component_states:  # Only re-connect component internal transitions
                    continue
                to_state_new_name = source_states_to_target_names[to_state]
                target_hmm.transitions[state_new_name].append(to_state_new_name)

            if source_state == component_entry_state:
                for s in hmm_entry_arcs:
                    if s in target_hmm.transitions:
                        target_hmm.transitions[s].append(state_new_name)

            if source_state == component_exit_state:
                target_hmm.transitions[state_new_name] += hmm_exit_arcs

            target_hmm.inner_states = target_hmm._get_inner_states()

    @staticmethod
    def _add_subgraph(source_hmm, target_hmm, source_states, target_states,
                      source_subgraph_entry_state, target_hmm_entry_arcs):

        if configurations["LIMIT_CROSSOVER_RESULT_HMM_NUM_OF_STATES"]:
            if len(target_hmm.inner_states) + 1 - len(target_states) + len(source_states) > configurations[
                "MAX_NUM_OF_INNER_STATES"]:
                return

        # Remove selected component from target HMM
        target_hmm.remove_states(target_states)

        # Get new names for crossed-over states in new HMM
        added_states = []
        source_states_to_target_names = {FINAL_STATE: FINAL_STATE}
        for source_state in source_states:
            if source_state == FINAL_STATE:
                continue

            state_new_name = target_hmm._add_state(force=True)
            added_states.append(state_new_name)
            source_states_to_target_names[source_state] = state_new_name

        for source_state in source_states:
            state_new_name = source_states_to_target_names[source_state]

            # Insert subgraph to other graph and rename states
            if source_state != FINAL_STATE:
                for to_state in source_hmm.transitions[source_state]:
                    if to_state not in source_states:  # Only re-connect subgraph transitions
                        continue
                    to_state_new_name = source_states_to_target_names[to_state]
                    target_hmm.transitions[state_new_name].append(to_state_new_name)

            if source_state == source_subgraph_entry_state:
                for s in target_hmm_entry_arcs:
                    if s in target_hmm.transitions:
                        target_hmm.transitions[s].append(state_new_name)

            # Move emissions with crossed-over states
            if source_state != FINAL_STATE:
                target_hmm.emissions[state_new_name] = source_hmm.emissions[source_state]

            # Re-generate inner states list
            target_hmm.inner_states = target_hmm._get_inner_states()

    @classmethod
    def crossover_old(cls, hmm_1, hmm_2):
        # Choose a subset of states from one parent. Switch them between two parents,
        # each state moving with its outgoing transitions.

        h1_states = set(hmm_1.get_states())
        h2_states = set(hmm_2.get_states())
        h1_inner_states = set(hmm_1.inner_states)
        h2_inner_states = set(hmm_2.inner_states)
        states_intersection = list(h1_inner_states & h2_inner_states)

        offspring_1 = deepcopy(hmm_1)
        offspring_2 = deepcopy(hmm_2)

        if states_intersection:
            states_subset_size = choice(range(1, len(states_intersection) + 1))
            states_to_crossover = sample(states_intersection, states_subset_size)

            for state in states_to_crossover:
                # Transfer transitions between crossed-over states
                h1_transitions_relevant_for_h2 = [to_state for to_state in hmm_1.transitions[state] if
                                                  to_state in h2_states]
                h2_transitions_relevant_for_h1 = [to_state for to_state in hmm_2.transitions[state] if
                                                  to_state in h1_states]
                offspring_1.transitions[state] = h2_transitions_relevant_for_h1
                offspring_2.transitions[state] = h1_transitions_relevant_for_h2

                # Combine emissions
                h1_original_emissions = hmm_1.emissions[state]
                h2_original_emissions = hmm_2.emissions[state]
                offspring_1.emissions[state], offspring_2.emissions[state] = HMM.crossover_emissions(
                    h1_original_emissions, h2_original_emissions)

        return offspring_1, offspring_2

    @staticmethod
    def crossover_emissions(emissions_1, emissions_2):
        crossover_point_1 = choice(range(0, len(emissions_1) + 1))
        crossover_point_2 = choice(range(0, len(emissions_2) + 1))

        offspring_1 = list(set(emissions_1[:crossover_point_1] + emissions_2[crossover_point_2:]))
        offspring_2 = list(set(emissions_2[:crossover_point_2] + emissions_1[crossover_point_1:]))

        return offspring_1, offspring_2

    def get_connected_components(self, ignore_initial=True, ignore_final=True):
        """
        :param ignore_initial, ignore_final: Omit q0 or qf from list of components
        :return: List of lists: list i contains the states in the i-th connected component
        """
        states = self.get_states()
        num_states = len(states)
        transition_matrix = self.get_transition_matrix()
        n_components, labels = connected_components(transition_matrix, directed=True, connection='strong')
        components_to_states = [[] for _ in range(n_components)]
        for state_idx in range(num_states):
            state_component = labels[state_idx]
            components_to_states[state_component].append(states[state_idx])

        if ignore_initial:
            components_to_states.remove([INITIAL_STATE])  # q0 and qf will always be in their own components
        if ignore_final:
            components_to_states.remove([FINAL_STATE])

        components_to_states = [self.sort_state_names(states) for states in components_to_states]
        return components_to_states

    def get_transition_matrix(self):
        states = self.get_states()
        num_states = len(states)
        transition_matrix = np.zeros((num_states, num_states))
        for state in states[:-1]:
            q_from = int(state[1:])
            for to_state in self.transitions[state]:
                if to_state == FINAL_STATE:
                    q_to = len(states) - 1
                else:
                    q_to = int(to_state[1:])
                transition_matrix[q_from, q_to] = 1
        return transition_matrix

    @classmethod
    def hmm_from_transition_matrix(cls, matrix, emissions):
        """
        :param matrix: transition matrix
        :param emissions: identical to HMM.emissions
        """
        hmm_dict = {}
        num_states = len(matrix)
        for idx in range(len(matrix) - 1):
            to_states = [get_state_name(to_idx, num_states) for to_idx in range(len(matrix[idx])) if
                         matrix[idx][to_idx] == 1]
            if idx == 0:
                q = INITIAL_STATE
                hmm_dict[q] = to_states
            else:
                q = get_state_name(idx, num_states)
                hmm_dict[q] = (to_states, emissions[q])
        return cls(hmm_dict)

    # mutations - all mutations return true or false depending on their success
    def make_mutation(self):
        segments = SegmentTable().get_segments_symbols(include_boundary_symbols=False)

        mutation_weights = [
            ([self.combine_emissions, []], configurations["COMBINE_EMISSIONS"]),
            ([self.move_emission, []], configurations["MOVE_EMISSION"]),
            ([self.merge_emissions, []], configurations["MERGE_EMISSIONS"]),
            ([self.merge_states, []], configurations["MERGE_STATES"]),
            ([self.split_state, []], configurations["SPLIT_STATES"]),
            ([self.advance_emission, []], configurations["ADVANCE_EMISSION"]),
            ([self.clone_state, []], configurations["CLONE_STATE"]),
            ([self.clone_emission, []], configurations["CLONE_EMISSION"]),
            ([self.split_emission, []], configurations["SPLIT_EMISSION"]),
            ([self.add_new_state, []], configurations["ADD_STATE"]),
            ([self.remove_random_state, []], configurations["REMOVE_STATE"]),
            ([self.add_transition, []], configurations["ADD_TRANSITION"]),
            ([self.remove_transition, []], configurations["REMOVE_TRANSITION"]),
            ([self.add_segment_to_emission, [segments]], configurations["ADD_SEGMENT_TO_EMISSION"]),
            ([self.remove_segment_from_emission, []], configurations["REMOVE_SEGMENT_FROM_EMISSION"]),
            ([self.change_segment_in_emission, [segments]], configurations["CHANGE_SEGMENT_IN_EMISSION"]),
            ([self.add_emission_to_state, [segments]], configurations["ADD_EMISSION_TO_STATE"]),
            ([self.remove_emission_from_state, []], configurations["REMOVE_EMISSION_FROM_STATE"]),
            ([self.add_segment_by_feature_bundle, []], configurations["ADD_SEGMENT_BY_FEATURE_BUNDLE"])
        ]

        if configurations["UNDERSPECIFICATION_FLAG"]:
            mutation_weights.append(([self.underspecify, []], configurations["UNDERSPECIFY"]))

        mutations_tuple_list = get_weighted_list(mutation_weights)
        mutations_tuple = choice(mutations_tuple_list)
        mutation_result = mutations_tuple[0](*mutations_tuple[1])

        return mutation_result

    def advance_emission(self):
        """ Pick a random state q1. From q1, pick an emission and an outgoing state q2 at random. Create a new state: q0. Add the chosen emission to q0. Remove the chosen emission from q1. Add the transitions: q1 to q0, q0 to q2, and q0 to q0. """

        target_state = choice(self.inner_states)
        target_state_emissions = self.get_emissions(target_state)
        outgoing_states_list = list(set(self.transitions[target_state]) - set([target_state]))
        if len(target_state_emissions) > 1 and len(outgoing_states_list) > 0 and len(self.inner_states) < configurations["MAX_NUM_OF_INNER_STATES"]:
            outgoing_state = choice(outgoing_states_list)
            new_state = self._get_next_state()
            emission = choice(target_state_emissions)

            self.inner_states.append(new_state)
            self.transitions[new_state] = [outgoing_state, new_state]
            self.emissions[new_state] = [emission]

            self.transitions[target_state].append(new_state)
            self.emissions[target_state].remove(emission)
            return True
        else:
            return False

    def _merge_options(self):
        """A very naive way to find the number of states to merge.
        The returned array contains numbers between 2 and n, where each `i`
        appears twice as much as `i + 1`.
        """
        mult = 1
        options = []
        for i in range(len(self.inner_states), 1, -1):
            options += [i] * mult
            mult *= 2
        return options

    def merge_states(self):
        if len(self.inner_states) < 2:
            return False

        total_to_merge = choice(self._merge_options())

        states_to_merge = sample(self.inner_states, total_to_merge)

        new_state = self._get_next_state()
        self.inner_states.append(new_state)

        merged_emissions = set()
        merged_outgoing_transitions = set()
        for state in states_to_merge:
            merged_emissions.update(self.emissions[state])
            merged_outgoing_transitions.update(self.transitions[state])

        self.emissions[new_state] = list(merged_emissions)
        self.transitions[new_state] = list(merged_outgoing_transitions)

        for state in self.transitions:
            add_transition_to_new = False
            for old_state in states_to_merge:
                if old_state in self.transitions[state]:
                    self.transitions[state].remove(old_state)
                    add_transition_to_new = True
            if add_transition_to_new:
                self.transitions[state].append(new_state)

        self.remove_states(states_to_merge)
        return True

    def split_state(self):
        """
        Choose random inner state, split its emissions at random point into two,
         and split them across two new states that will have the same ingoing and outgoing arcs.
        """
        if len(self.inner_states) == configurations["MAX_NUM_OF_INNER_STATES"]:
            return False

        old_state = choice(self.inner_states)
        old_state_transitions = self.transitions[old_state]
        old_emissions = self.emissions[old_state]
        emission_switches = [randint(0, 1) for _ in range(len(old_emissions))]

        state_1_emissions = []
        state_2_emissions = []
        for idx, emission in enumerate(old_emissions):
            if emission_switches[idx] == 0:
                state_1_emissions.append(emission)
            else:
                state_2_emissions.append(emission)

        new_state_1 = self._get_next_state()
        self.inner_states.append(new_state_1)
        self.transitions[new_state_1] = deepcopy(old_state_transitions)
        self.emissions[new_state_1] = state_1_emissions

        new_state_2 = self._get_next_state()
        self.inner_states.append(new_state_2)
        self.transitions[new_state_2] = deepcopy(old_state_transitions)
        self.emissions[new_state_2] = state_2_emissions

        for from_state in self.transitions:
            if old_state in self.transitions[from_state]:
                if new_state_1 not in self.get_transitions(from_state):
                    self.transitions[from_state].append(new_state_1)
                if new_state_2 not in self.get_transitions(from_state):
                    self.transitions[from_state].append(new_state_2)

        self.remove_states([old_state])
        return True

    def combine_emissions(self):
        """pick two emissions - combine them and add them to random state"""
        emissions = self.get_all_emissions()
        if not emissions:
            return False

        emission1 = choice(emissions)
        emission2 = choice(emissions)

        if emission1 == EPSILON or emission2 == EPSILON:
            return False

        new_emission = emission1 + emission2
        state = choice(self.inner_states)
        if new_emission not in self.get_emissions(state):
            self.emissions[state].append(new_emission)
            return True
        else:
            return False

    def move_emission(self):
        """ choose an emission, remove it from its state and add it to another state """
        states_with_emissions = [s for s in self.inner_states if len(self.emissions[s]) > 0]
        if len(states_with_emissions) <= 1:
            return False

        source_state = choice(states_with_emissions)
        emission = choice(self.emissions[source_state])
        target_state = choice(list(set(states_with_emissions) - set([source_state])))

        if emission not in self.emissions[target_state] or ALLOW_DUPLICATE_EMISSIONS:
            self.emissions[target_state].append(emission)
            self.emissions[source_state].remove(emission)
            return True
        else:
            return False

    def merge_emissions(self):
        """ pick first emission, add it to emission, delete the first emission.
            if first state is left empty, delete it entirely. """
        states_with_emissions = [s for s in self.inner_states if len(self.emissions[s]) > 0]
        if not states_with_emissions:
            return False
        source_state = choice(states_with_emissions)
        target_state = choice(states_with_emissions)

        source_emissions = self.get_emissions(source_state)
        target_emissions = self.get_emissions(target_state)

        source_emission_idx = randint(0, len(source_emissions) - 1)
        target_emission_idx = randint(0, len(target_emissions) - 1)
        source_emission = source_emissions[source_emission_idx]
        target_emission = target_emissions[target_emission_idx]

        if source_emission == EPSILON or target_emission == EPSILON:
            return False

        combined_emission = target_emission + source_emission
        source_emissions.remove(source_emission)
        try:
            target_emissions.remove(target_emission)
        except ValueError:  # Source emission = Target emission
            pass
        target_emissions.append(combined_emission)

        if len(source_emissions) == 0:
            self.remove_states([source_state])

        return True

    def clone_state(self):
        """pick an inner state, create a new state with same transitions and emissions,
         if the original state has a transition to itself the original and the new will be connected"""
        if len(self.inner_states) < configurations["MAX_NUM_OF_INNER_STATES"]:
            original_state = choice(self.inner_states)
            cloned_state = self._get_next_state()
            self.inner_states.append(cloned_state)
            self.emissions[cloned_state] = deepcopy(self.emissions[original_state])

            # create incoming connections
            for state in self.transitions:
                if original_state in self.transitions[state]:
                    self.transitions[state].append(cloned_state)

            # copy outgoing connections
            self.transitions[cloned_state] = deepcopy(self.transitions[original_state])

            return True
        else:
            return False

    def split_emission(self):
        """pick one emission - split it in random place, add both parts to state."""
        states_with_emissions = [s for s in self.inner_states if len(self.get_emissions(s)) > 0]
        if not states_with_emissions:
            return False
        source_state = choice(states_with_emissions)
        state_emissions = self.get_emissions(source_state)
        emissions_longer_than_1 = [e for e in state_emissions if len(e) > 1]
        if not emissions_longer_than_1:
            return False

        emission = choice(emissions_longer_than_1)
        split_point = randint(1, len(emission) - 1)
        emission_part_1 = emission[:split_point]
        emission_part_2 = emission[split_point:]

        if ALLOW_DUPLICATE_EMISSIONS or emission_part_1 not in self.emissions[source_state]:
            self.emissions[source_state].append(emission_part_1)
        if ALLOW_DUPLICATE_EMISSIONS or emission_part_2 not in self.emissions[source_state]:
            self.emissions[source_state].append(emission_part_2)

        return True

    def clone_emission(self):
        """pick an emission
           pick an inner state and add the emission to it"""
        emissions = self.get_all_emissions()
        if not emissions:
            return False
        emission = choice(emissions)
        state = choice(self.inner_states)
        if emission not in self.get_emissions(state):
            self.emissions[state].append(emission)
            return True
        else:
            return False

    def add_new_state(self):
        new_state = self._add_state()
        if new_state is not None:
            return True
        else:
            return False

    def _add_state(self, force=False):
        """adds empty state"""
        if force or len(self.inner_states) < configurations["MAX_NUM_OF_INNER_STATES"]:
            new_state = self._get_next_state()
            self.inner_states.append(new_state)
            self.emissions[new_state] = []
            self.transitions[new_state] = []
            return new_state
        else:
            return None

    def remove_random_state(self):
        """select a random inner state and remove it and all its arcs"""
        if len(self.inner_states) > configurations["MIN_NUM_OF_INNER_STATES"]:
            state_to_remove = choice(self.inner_states)
            self.remove_states([state_to_remove])
            return True
        else:
            return False

    def remove_states(self, states_to_remove):
        """removes states with all their arcs, ensuring contiguous numbering of states afterwards """
        for state in states_to_remove:
            self._remove_state(state)

    def _remove_state(self, state_to_remove):
        """removes a state (and all its arcs)"""

        if state_to_remove != FINAL_STATE:
            self.inner_states.remove(state_to_remove)
            del self.emissions[state_to_remove]
            del self.transitions[state_to_remove]

        for state in self.transitions:
            if state_to_remove in self.transitions[state]:
                self.transitions[state].remove(state_to_remove)

    def ensure_contiguous_state_indices(self):
        # Defragment state numbering caused by state removals, e.g: [q0, q1, q7, q8] ==> [q0, q1, q2, q3]
        states = self.inner_states
        state_numbers = [int(x[1:]) for x in self.inner_states]
        state_and_numbers_sorted = sorted(list(zip(states, state_numbers)), key=lambda t: t[1])

        for i, (state, state_num) in enumerate(state_and_numbers_sorted):
            if state_num != (i + 1):
                self._rename_state(state, 'q{}'.format(i + 1))

    def _rename_state(self, orig_state, new_state):
        for state in self.transitions:
            for i in range(len(self.transitions[state])):
                if self.transitions[state][i] == orig_state:
                    self.transitions[state][i] = new_state

        self.transitions[new_state] = self.transitions[orig_state]
        del self.transitions[orig_state]

        self.emissions[new_state] = self.emissions[orig_state]
        del self.emissions[orig_state]

        self.inner_states.remove(orig_state)
        self.inner_states.append(new_state)

    def add_transition(self):
        """picks a state form initial+inner states and add transition
        to other random state (in case initial, not to itself)"""
        state1 = choice(self.inner_states + [INITIAL_STATE])
        state2 = choice(self.inner_states)
        if state2 not in self.get_transitions(state1):
            self.transitions[state1].append(state2)
            return True
        else:
            return False

    def remove_transition(self):
        """picks a state form initial+inner states and remove a transition from it"""
        state1 = choice(self.inner_states + [INITIAL_STATE])
        if not len(self.get_transitions(state1)):
            return False
        else:
            state2 = choice(self.get_transitions(state1))
            self.transitions[state1].remove(state2)
            return True

    def add_segment_to_emission(self, segments):
        """pick an inner state, pick an emission, pick a segment and insert in random position"""
        state = choice(self.inner_states)
        state_emissions = self.get_emissions(state)
        if state_emissions:
            emission = choice(state_emissions)
            if emission == EPSILON:
                return False

            segment = choice(segments)

            insertion_index = randint(0, len(emission))
            new_emission = emission[:insertion_index] + segment + emission[insertion_index:]
            if ALLOW_DUPLICATE_EMISSIONS or new_emission not in self.get_emissions(state):
                self.emissions[state].append(new_emission)
                if REMOVE_ORIG:
                    self.emissions[state].remove(emission)
                return True

        return False

    def remove_segment_from_emission(self):
        """pick an inner state, pick an emission, pick a position and remove from it -
        if the emission is mono-segmental, remove it"""

        state = choice(self.inner_states)
        emissions = self.get_emissions(state)
        if emissions:
            emission = choice(emissions)
            if emission == EPSILON:
                return False

            if not len(emission) == 1:
                deletion_index = randint(0, len(emission) - 1)
                new_emission = emission[:deletion_index] + emission[deletion_index + 1:]
                if ALLOW_DUPLICATE_EMISSIONS or new_emission not in self.get_emissions(state):
                    self.emissions[state].append(new_emission)
            self.emissions[state].remove(emission)
            return True

        return False

    def change_segment_in_emission(self, segments):
        """pick a state, pick an emission, pick a segment, change it"""
        state = choice(self.inner_states)
        emissions = self.get_emissions(state)
        if emissions:
            emission = choice(emissions)
            if emission == EPSILON:
                return False

            # crate new emission
            emission_string_list = list(emission)
            index_of_change = randint(0, len(emission_string_list) - 1)
            old_segment = emission_string_list[index_of_change]
            segments.remove(old_segment)
            new_segment = choice(segments)
            emission_string_list[index_of_change] = new_segment
            new_emission = ''.join(emission_string_list)

            # replace emission
            emissions.remove(emission)
            emissions.append(new_emission)
            return True
        else:
            return False

    def add_emission_to_state(self, segments):
        """pick an inner state, pick a segment or epsilon - add it to state """
        state = choice(self.inner_states)
        segment = choice([EPSILON] + segments)
        state_emissions = self.get_emissions(state)

        if segment == EPSILON and EPSILON not in state_emissions:
            self.emissions[state].append(segment)
            return True
        elif ALLOW_DUPLICATE_EMISSIONS or segment not in state_emissions:
            self.emissions[state].append(segment)
            return True
        else:
            return False

    def remove_emission_from_state(self):
        """pick an inner state, pick an emission - remove it (if state has no emissions - mutation failed)"""
        state = choice(self.inner_states)
        emissions = self.get_emissions(state)
        if emissions:
            emission = choice(emissions)
            self.emissions[state].remove(emission)
            return True
        else:
            return False

    def add_segment_by_feature_bundle(self):
        """
        - randomize a feature bundle
        - expand the feature bundle to its segments
        - select a random inner state
        - find all emissions in state that end with these segments
        - randomly select a new segment and add it to end of these emissions
        """
        random_feature_bundle = FeatureBundle.get_random_feature_bundle(role=None)
        feature_bundle_segments = SegmentTable().get_segments_symbols_by_features(random_feature_bundle.feature_dict)
        random_segment = SegmentTable().get_random_segment_symbol()
        state = choice(self.inner_states)
        for emission_idx, emission in enumerate(self.emissions[state]):
            if emission[-1] in feature_bundle_segments:
                new_emission = emission + random_segment
                self.emissions[state][emission_idx] = new_emission

    def underspecify(self):
        """pick a state, pick an emission, pick a voiced segment - underspecify"""
        state = choice(self.inner_states)
        emissions = self.get_emissions(state)
        if emissions:
            emission = choice(emissions)
            if emission == EPSILON:
                return False

            if "t" in emission or "d" in emission:
                # crate new emission
                emission_string_list = list(emission)
                indices = [i for i, segment in enumerate(emission_string_list) if segment == "t" or segment == "d"]
                index_of_change = choice(indices)
                new_segment = "T"
                emission_string_list[index_of_change] = new_segment
                new_emission = ''.join(emission_string_list)

                # replace emission
                emissions.remove(emission)
                emissions.append(new_emission)
                return True

        return False

    # emission generation

    def generate_emission(self):
        """this will only work with well structured hmm (all inner states with emissions, no dead ends)"""
        result = ""
        current_state = choice(self.transitions[INITIAL_STATE])
        while current_state != FINAL_STATE:
            emission = choice(self.emissions[current_state])
            result += emission
            current_state = choice(self.transitions[current_state])
        return result

    def generate_emissions_list(self, n):
        result = []
        for _ in range(n):
            result.append(self.generate_emission())
        return result

    def __str__(self):
        return u"states {}, transitions {}, emissions {}".format(self.inner_states, self.transitions, self.emissions)

    def __repr__(self):
        # unambiguous representation for hashing - heavier than __str__()
        sorted_states = sorted(self.inner_states)
        sorted_transitions = {state: sorted(self.transitions[state]) for state in sorted_states}
        sorted_emissions = {state: sorted(self.emissions[state]) for state in sorted_states}
        return u"states {}, transitions {}, emissions {}".format(sorted_states, sorted_transitions, sorted_emissions)

    def get_log_lines(self):
        log_lines = list()
        if configurations["RESTRICTIONS_ON_ALPHABET"]:
            log_lines.append("distinct segments: {}".format(self.get_distinct_segments()))
        log_lines.append("HMM:")
        log_lines.append("{}: {}".format(INITIAL_STATE, sorted(self.transitions[INITIAL_STATE])))

        for state in sorted(self.inner_states):
            emissions = sorted(self.emissions[state])
            transitions = sorted(self.transitions[state])
            log_lines.append(u"{}: {}, {}".format(state, sorted(transitions), sorted(emissions)))

        for path in self.get_all_paths():
            log_lines.append("->".join(path))
        # log_lines.append("All Emissions: {}".format(sorted(self.get_all_emissions())))

        return log_lines

    def get_all_paths(self):
        paths = []
        stack = [(INITIAL_STATE, [INITIAL_STATE])]
        while stack:
            (vertex, path) = stack.pop()
            for next in set(self.transitions[vertex]) - set(path):
                if next == FINAL_STATE:
                    paths.append(path + [next])
                else:
                    stack.append((next, path + [next]))
        return paths

    @classmethod
    def get_explicit_hmm(cls, data):
        hmm_dict = {
            INITIAL_STATE: ['q1'],
            'q1': ([FINAL_STATE], deepcopy(data))
        }
        return cls(hmm_dict)

    @classmethod
    def get_random_hmm(cls, data=[]):
        if configurations["RANDOM_HMM_METHOD"] == 'simple':
            return cls.get_random_hmm_simple(data)
        elif configurations["RANDOM_HMM_METHOD"] == 'matrix':
            return cls.get_random_hmm_by_random_transition_matrix(data)
        else:
            raise ValueError(configurations["RANDOM_HMM_METHOD"])

    @classmethod
    def get_random_hmm_simple(cls, data=[]):
        """ Generates a chain of states, e.g q0->q1->q2>qf, of length in range [MIN_NUM_OF_INNER_STATES, MAX_NUM_OF_INNER_STATES].
         Each state is assigned [0, RANDOM_HMM_MAX_EMISSIONS_PER_STATE] random emissions of length [0, RANDOM_HMM_MAX_EMISSION_LENGTH].

        :param data: optional. list of words to use to generate emissions if HMM_RANDOM_EMISSIONS_BY_DATA = True.
        """
        r = np.random.rand()
        if r < configurations["DEFAULT_HMM_BY_RANDOM_PROBAB"]:
            return HMM.get_default_hmm()

        elif r < configurations["DEFAULT_HMM_BY_RANDOM_PROBAB"] + configurations["EXPLICIT_HMM_BY_RANDOM_PROBAB"]:
            return HMM.get_explicit_hmm(data)

        segments = SegmentTable().get_segments_symbols(include_boundary_symbols=False)

        def get_random_emissions_from_data(q):
            # Get substring of data words as random emissions
            emissions = []
            num_emissions = randint(0, configurations["RANDOM_HMM_MAX_EMISSIONS_PER_STATE"])
            if num_emissions == 0:
                return [EPSILON]
            for i in range(num_emissions):
                random_word = choice(data)
                emission_length = min(randint(1, len(random_word)), configurations["RANDOM_HMM_MAX_EMISSION_LENGTH"])

                # If this is the first state, take substring from start of word
                if q == 1:
                    start = 0
                else:
                    start = randint(1, len(random_word) - emission_length + 1)
                emission = random_word[start: start + emission_length]
                if emission:
                    emissions.append(emission)
            return emissions

        def get_random_emissions():
            # Get totally random emissions
            emissions = []
            num_emissions = randint(0, configurations["RANDOM_HMM_MAX_EMISSIONS_PER_STATE"])
            if num_emissions == 0:
                return [EPSILON]
            for _ in range(num_emissions):
                emission_length = randint(1, configurations["RANDOM_HMM_MAX_EMISSION_LENGTH"])
                emission = "".join([choice(segments) for _ in range(emission_length)])
                emissions.append(emission)
            return emissions

        num_inner_states = randint(configurations["MIN_NUM_OF_INNER_STATES"], configurations["MAX_NUM_OF_INNER_STATES"])
        hmm_dict = {}

        for q_from in range(0, num_inner_states + 1):
            from_state = 'q{}'.format(q_from) if q_from != 0 else INITIAL_STATE
            q_to = q_from + 1
            to_state = 'q{}'.format(q_to) if (q_to != num_inner_states + 1) else FINAL_STATE

            state_transitions = [to_state]

            if from_state == INITIAL_STATE:
                hmm_dict[from_state] = state_transitions  # No emissions from q0
            else:
                if configurations["HMM_RANDOM_EMISSIONS_BY_DATA"]:
                    emissions = get_random_emissions_from_data(q_from)
                else:
                    emissions = get_random_emissions()
                hmm_dict[from_state] = (state_transitions, emissions)

        return cls(hmm_dict)

    @classmethod
    def get_random_hmm_by_random_transition_matrix(cls, data=[]):
        """ Generate a random transition matrix of dimension in range [MIN_NUM_OF_INNER_STATES, MAX_NUM_OF_INNER_STATES].
        Make sure at least one path is available from q0 to qf.
        Each state is assigned [0, RANDOM_HMM_MAX_EMISSIONS_PER_STATE] random emissions of length [0, RANDOM_HMM_MAX_EMISSION_LENGTH].

        :param data: optional. list of words to use to generate emissions if HMM_RANDOM_EMISSIONS_BY_DATA = True.
        """

        r = np.random.rand()
        if r < configurations["DEFAULT_HMM_BY_RANDOM_PROBAB"]:
            return HMM.get_default_hmm()

        elif r < configurations["DEFAULT_HMM_BY_RANDOM_PROBAB"] + configurations["EXPLICIT_HMM_BY_RANDOM_PROBAB"]:
            return HMM.get_explicit_hmm(data)

        segments = SegmentTable().get_segments_symbols(include_boundary_symbols=False)

        def get_random_emissions_from_data(q):
            # Get substring of data words as random emissions
            emissions = []
            num_emissions = randint(0, configurations["RANDOM_HMM_MAX_EMISSIONS_PER_STATE"])
            if num_emissions == 0:
                return [EPSILON]
            for i in range(num_emissions):
                random_word = choice(data)
                emission_length = min(randint(1, len(random_word)), configurations["RANDOM_HMM_MAX_EMISSION_LENGTH"])

                # If this is the first state, take substring from start of word
                if q == 1:
                    start = 0
                else:
                    start = randint(1, len(random_word) - emission_length + 1)
                emission = random_word[start: start + emission_length]
                if emission:
                    emissions.append(emission)
            return emissions

        def get_random_emissions():
            # Get totally random emissions
            emissions = []
            num_emissions = randint(0, configurations["RANDOM_HMM_MAX_EMISSIONS_PER_STATE"])
            if num_emissions == 0:
                return [EPSILON]
            for _ in range(num_emissions):
                emission_length = randint(1, configurations["RANDOM_HMM_MAX_EMISSION_LENGTH"])
                emission = "".join([choice(segments) for _ in range(emission_length)])
                emissions.append(emission)
            return emissions

        num_inner_states = randint(configurations["MIN_NUM_OF_INNER_STATES"], configurations["MAX_NUM_OF_INNER_STATES"])

        # Randomize transition matrix
        transition_matrix = np.random.rand(num_inner_states + 2, num_inner_states + 2)
        transition_matrix = (transition_matrix < configurations["TRANSITION_MATRIX_TRANSITION_PROBABILITY"]).astype(int)

        # Backtrack from qf and make sure at least one path from q0 to qf goes through all states
        available_states = list(range(1, num_inner_states + 1))
        q_to = num_inner_states + 1  # qf
        while available_states:
            q_from = choice(available_states)
            transition_matrix[q_from, q_to] = 1
            available_states.remove(q_from)
            q_to = q_from
        transition_matrix[0, q_to] = 1

        # Make sure q0 isn't connected to qf
        transition_matrix[0, -1] = 0
        transition_matrix[-1, 0] = 0

        hmm_dict = {}

        for q_from in range(0, num_inner_states + 1):
            from_state = 'q{}'.format(q_from) if q_from != 0 else INITIAL_STATE
            state_transitions = []

            for q_to in range(1, num_inner_states + 2):
                to_state = 'q{}'.format(q_to) if (q_to != num_inner_states + 1) else FINAL_STATE

                if transition_matrix[q_from, q_to] == 1:
                    state_transitions.append(to_state)

            if from_state == INITIAL_STATE:
                hmm_dict[from_state] = state_transitions  # No emissions from q0
            else:
                if configurations["HMM_RANDOM_EMISSIONS_BY_DATA"]:
                    emissions = get_random_emissions_from_data(q_from)
                else:
                    emissions = get_random_emissions()
                hmm_dict[from_state] = (state_transitions, emissions)

        return cls(hmm_dict)

    @staticmethod
    def sort_state_names(states):
        return sorted(states, key=lambda q: float("inf") if q[1] == 'f' else int(q[1:]))


def get_weighted_list(weighted_choices):
    """
    weighted_choices is a list of tuples
    """
    return [value for value, counter in weighted_choices for _ in range(counter)]


def get_state_name(i, num_states):
    if i == 0:
        return INITIAL_STATE
    elif i == num_states - 1:
        return FINAL_STATE
    else:
        return 'q{}'.format(i)


class TransducerStatesLookup:
    """ Helper class to index transducer states and get their index in O(1) """

    def __init__(self):
        self.next_free_index = 0
        self.state_to_idx = {}

    def append(self, state):
        idx = self.next_free_index
        self.next_free_index += 1
        self.state_to_idx[state] = idx

    def extend(self, list_of_states):
        for state in list_of_states:
            self.append(state)

    def index(self, item):
        return self.state_to_idx[item]
