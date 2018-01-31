from hmm import HMM, INITIAL_STATE, FINAL_STATE
from grammar import Grammar
from hypothesis import Hypothesis
from tests.my_test_case import MyTestCase
from configuration import Configuration
from segment_table import SegmentTable
from util import log_hmm

configurations = Configuration()


class TestHMM(MyTestCase):
    def test_plural_english(self):
        self.initialise_segment_table("plural_english_segment_table.txt")
        hmm = HMM({INITIAL_STATE: ['q1'],
                   'q1': (['q2', FINAL_STATE], ['dog', 'kat']),
                   'q2': ([FINAL_STATE], ['z'])})

        print(hmm)
        print(hmm.get_encoding_length(4))

    def test_encoding(self):
        self.initialise_segment_table("plural_english_segment_table.txt")
        hmm = HMM({INITIAL_STATE: ['q1'],
                   'q1': ([FINAL_STATE], ["a", "a"])})

        print(hmm.get_encoding_length(4))

    def test_crossover(self):
        hmm_1 = HMM({INITIAL_STATE: ['q1'],
                     'q1': (['q2', FINAL_STATE], ['koko', 'dogo']),
                     'q2': ([FINAL_STATE], ['zz'])})
        hmm_2 = HMM({INITIAL_STATE: ['q1'],
                     'q1': (['q2'], ['dog', 'kat']),
                     'q2': (['q3'], ['s']),
                     'q3': ([FINAL_STATE], ['z'])})
        print("Parent 1")
        log_hmm(hmm_1)
        print()

        print("Parent 2")
        log_hmm(hmm_2)

        offspring_1, offspring_2 = HMM.crossover(hmm_1, hmm_2)
        print()
        print("Offspring 1")
        log_hmm(offspring_1)

        print()
        print("Offspring 2")
        log_hmm(offspring_2)

    def test_crossover_by_matrix(self):
        hmm_1 = HMM({INITIAL_STATE: ['q1', 'q2'],
                     'q1': (['q2', FINAL_STATE], ['koko', 'dogo']),
                     'q2': ([FINAL_STATE], ['zz'])})
        hmm_2 = HMM({INITIAL_STATE: ['q1'],
                     'q1': (['q2'], ['dog', 'kat']),
                     'q2': (['q3'], ['s']),
                     'q3': ([FINAL_STATE], ['z'])})
        print("Parent 1")
        log_hmm(hmm_1)
        print("Parent 2")
        log_hmm(hmm_2)

        offspring_1, offspring_2 = HMM.crossover_by_matrix(hmm_1, hmm_2)
        print("Offspring 1")
        log_hmm(offspring_1)
        print("Offspring 2")
        log_hmm(offspring_2)

        self.write_to_dot_to_file(hmm_1, 'matrix_parent_1')
        self.write_to_dot_to_file(hmm_2, 'matrix_parent_2')
        self.write_to_dot_to_file(offspring_1, 'matrix_offspring_1')
        self.write_to_dot_to_file(offspring_2, 'matrix_offspring_2')


    def test_crossover_subgraph(self):
        self.initialise_segment_table("plural_english_segment_table.txt")
        hmm_1 = HMM({INITIAL_STATE: ['q1'],
                     'q1': (['q1', 'q2'], ['da']),
                     'q2': ([FINAL_STATE], ['s'])})

        hmm_2 = HMM({INITIAL_STATE: ['q1'],
                     'q1': (['q2'], ['ko']),
                     'q2': (['q3'], ['bo']),
                     'q3': (['q4'], ['go']),
                     'q4': ([FINAL_STATE], ['z'])})

        offspring_1, offspring_2 = HMM.crossover_subgraphs(hmm_1, hmm_2)

        self.write_to_dot_to_file(hmm_1, 'subgraph_parent_1')
        self.write_to_dot_to_file(hmm_2, 'subgraph_parent_2')
        self.write_to_dot_to_file(offspring_1, 'subgraph_offspring_1')
        self.write_to_dot_to_file(offspring_2, 'subgraph_offspring_2')
        offspring_1.get_transducer()
        offspring_2.get_transducer()

    def test_crossover_connected_components(self):
        self.initialise_segment_table("plural_english_segment_table.txt")
        hmm_1 = HMM({INITIAL_STATE: ['q1'],
                     'q1': (['q2'], ['dogo', 'koko']),
                     'q2': (['q1', FINAL_STATE], ['z'])})
        hmm_2 = HMM({INITIAL_STATE: ['q1'],
                     'q1': (['q2'], ['dag', 'kat']),
                     'q2': (['q3', FINAL_STATE], ['k']),
                     'q3': (['q1'], ['z'])})

        offspring_1, offspring_2 = HMM.crossover(hmm_1, hmm_2)

        self.write_to_dot_to_file(hmm_1, 'component_parent_1')
        self.write_to_dot_to_file(hmm_2, 'component_parent_2')
        self.write_to_dot_to_file(offspring_1, 'component_offspring_1')
        self.write_to_dot_to_file(offspring_2, 'component_offspring_2')
        offspring_1.get_transducer()
        offspring_2.get_transducer()

    def test_random_hmms_crossover(self):
        self.initialise_segment_table("plural_english_segment_table.txt")
        for _ in range(1):
            hmm_1 = HMM.get_random_hmm(data=['dag', 'zook', 'kook', 'kooz'])
            hmm_2 = HMM.get_random_hmm(data=['dag', 'zook', 'kook', 'kooz'])
            print('HMM 1')
            log_hmm(hmm_1)
            print('HMM 2')
            log_hmm(hmm_2)

            offspring_1, offspring_2 = HMM.crossover(hmm_1, hmm_2)
            print('Offspring 1')
            print('HMM', offspring_1.inner_states, 'TRANSITIONS', offspring_1.transitions, 'EMISSIONS',
                  offspring_1.emissions)
            print('Offspring 2')
            print('HMM', offspring_2.inner_states, 'TRANSITIONS', offspring_2.transitions, 'EMISSIONS',
                  offspring_2.emissions)

            self.write_to_dot_to_file(hmm_1, 'random_parent_1')
            self.write_to_dot_to_file(hmm_2, 'random_parent_2')
            self.write_to_dot_to_file(offspring_1, 'random_offspring_1')
            self.write_to_dot_to_file(offspring_2, 'random_offspring_2')
            offspring_1.get_transducer()
            offspring_2.get_transducer()

    def test_hmm_connected_components(self):
        hmm = HMM({INITIAL_STATE: ['q1'],
                   'q1': (['q2', FINAL_STATE], ['dag', 'kot']),
                   'q2': (['q1', FINAL_STATE], ['z'])})
        log_hmm(hmm)
        component_states = hmm.get_connected_components(ignore_initial_and_final_states=False)
        self.write_to_dot_to_file(hmm, 'connected_hmm')
        print(component_states)

        assert component_states[0][0] == FINAL_STATE
        assert component_states[2][0] == INITIAL_STATE
        assert 'q1' in component_states[1]
        assert 'q2' in component_states[1]

        component_states = hmm.get_connected_components(ignore_initial_and_final_states=True)
        assert 'q1' in component_states[0]
        assert 'q2' in component_states[0]
        assert [INITIAL_STATE] not in component_states
        assert [FINAL_STATE] not in component_states

    def test_hmm_transition_matrix(self):
        hmm = HMM({INITIAL_STATE: ['q1'],
                   'q1': (['q2', 'q1', FINAL_STATE], ['dag', 'kot']),
                   'q2': (['q1', FINAL_STATE], ['z'])})
        log_hmm(hmm)
        transition_matrix = hmm.get_transition_matrix()
        print(transition_matrix)

    def test_remove_states(self):
        hmm = HMM({INITIAL_STATE: ['q1'],
                   'q1': (['q4', FINAL_STATE], ['a']),
                   'q4': (['q8', 'q8', FINAL_STATE], ['d']),
                   'q7': (['q8'], ['d']),
                   'q8': (['q2', FINAL_STATE], ['g']),
                   'q2': (['q1', FINAL_STATE], ['z'])})
        hmm.remove_states(['q1'])
        print(hmm.inner_states)
        self.write_to_dot_to_file(hmm, 'after_remove')
        log_hmm(hmm)

    def test_remove_random(self):
        self.initialise_segment_table("plural_english_segment_table.txt")
        for _ in range(100000):
            hmm = HMM.get_random_hmm()
            try:
                hmm.make_mutation()
                # hmm.remove_random_state()
                hmm.get_transducer()
            except Exception:
                from traceback import print_exc
                log_hmm(hmm)
                print_exc()
                break

    def test_defragment_states(self):
        hmm = HMM({INITIAL_STATE: ['q1'],
                   'q1': (['q4', FINAL_STATE], ['a']),
                   'q4': (['q10', 'q10', FINAL_STATE], ['d']),
                   'q7': ([], ['d']),
                   'q10': (['q2', FINAL_STATE], ['g']),
                   'q2': (['q1', FINAL_STATE], ['z'])})
        self.write_to_dot_to_file(hmm, 'before_defragment')
        hmm.ensure_contiguous_state_indices()
        print(hmm.inner_states)
        self.write_to_dot_to_file(hmm, 'after_defragment')
        log_hmm(hmm)

    def test_epsilon_emission(self):
        self.initialise_segment_table("plural_english_segment_table.txt")
        from fst import EPSILON

        hmm = HMM({'q0': ['q1'],
                   'q1': (['q2'], ['dog', 'kat']),
                   'q2': (['qf'], ['z', EPSILON])
                   })
        self.write_to_dot_to_file(hmm, 'epsilon_hmm')

        hmm_transducer = hmm.get_transducer()
        self.write_to_dot_to_file(hmm_transducer, 'epsilon_hmm_transducer')

        grammar = Grammar(hmm, None)
        word_1 = 'dog'
        word_2 = 'dogz'
        print(hmm)

        hypothesis = Hypothesis(grammar, [word_1, word_2])
        encoding_length = hypothesis.get_data_encoding_length_by_grammar()
        assert encoding_length == 4.0

        print(hmm.add_epsilon_emission_to_state())
        print(hmm.add_epsilon_emission_to_state())
        print(hmm.add_epsilon_emission_to_state())
        print(hmm.remove_epsilon_emission_from_state())
        print(hmm.remove_epsilon_emission_from_state())
        print(hmm.add_epsilon_emission_to_state())

        self.write_to_dot_to_file(hmm, 'epsilon_hmm_after_mutation')

    def test_get_random_hmm(self):
        configurations['MIN_NUM_OF_INNER_STATES'] = 1
        configurations['MAX_NUM_OF_INNER_STATES'] = 5
        configurations['RANDOM_HMM_MAX_EMISSIONS_PER_STATE'] = 5
        self.initialise_segment_table("plural_english_segment_table.txt")
        hmm = HMM.get_random_hmm(data=['dag', 'dagzook', 'kook', 'kooz'])
        log_hmm(hmm)
        self.write_to_dot_to_file(hmm, "random_hmm")

    def test_get_totally_random_hmm(self):
        configurations['MIN_NUM_OF_INNER_STATES'] = 1
        configurations['MAX_NUM_OF_INNER_STATES'] = 5
        configurations['RANDOM_HMM_MAX_EMISSIONS_PER_STATE'] = 5
        self.initialise_segment_table("plural_english_segment_table.txt")
        hmm = HMM.get_random_hmm_totally_random(data=['dag', 'dagzook', 'kook', 'kooz'])
        log_hmm(hmm)
        self.write_to_dot_to_file(hmm, "random_hmm")

    def test_morpheme_boundary(self):
        configurations["MORPHEME_BOUNDARY_FLAG"] = True
        self.initialise_segment_table("plural_english_segment_table.txt")
        hmm = HMM({INITIAL_STATE: ['q1'],
                   'q1': (['q2', FINAL_STATE], ['dog', 'kat']),
                   'q2': ([FINAL_STATE], ['z'])})

        morpheme_boundary_hmm_transducer = hmm.get_transducer()
        self.write_to_dot_to_file(morpheme_boundary_hmm_transducer, "morpheme_boundary_hmm_transducer")

    def test_advance_emission(self):
        hmm = HMM({'q0': ['q1'],
                   'q1': (['q1', 'qf'], ['dag', 'kat', 'dot', 'kod', 'gas', 'toz'] + ['zo', 'go', 'do'] + ['at'])
                   })

        self.write_to_dot_to_file(hmm, "pre_advance_emission_hmm")
        hmm.advance_emission()
        for line in hmm.get_log_lines():
            print(line)
        self.write_to_dot_to_file(hmm, "advance_emission_hmm")

    def test_merge_states(self):
        hmm = HMM({'q0': ['q1', 'q5'],
                   'q1': (['qf'], ['koko', 'gogo']),
                   'q5': (['qf'], ['dag', 'kat'])
                   })

        self.write_to_dot_to_file(hmm, "merge_states_before")
        hmm.merge_states()
        for line in hmm.get_log_lines():
            print(line)
        self.write_to_dot_to_file(hmm, "merge_states_after")

    def test_merge_emissions(self):
        hmm = HMM({'q0': ['q1', 'q5'],
                   'q1': (['qf'], ['koko']),
                   'q5': (['qf'], ['dag', 'kat'])
                   })

        self.write_to_dot_to_file(hmm, "merge_states_before")
        hmm.merge_emissions()
        for line in hmm.get_log_lines():
            print(line)
        self.write_to_dot_to_file(hmm, "merge_states_after")

    def test_split_state(self):
        hmm = HMM({'q0': ['q1', 'q5'],
                   'q1': (['qf'], ['koko', 'gogo']),
                   'q5': (['qf'], ['koko', 'gogo'])
                   })

        self.write_to_dot_to_file(hmm, "split_states_before")
        hmm.split_state()
        for line in hmm.get_log_lines():
            print(line)
        self.write_to_dot_to_file(hmm, "split_states_after")

    def test_split_emission(self):
        hmm = HMM({'q0': ['q1', 'q5'],
                   'q1': (['q5', 'qf'], ['koko', 'gogo']),
                   'q5': (['qf'], ['koko', 'gogo'])
                   })

        self.write_to_dot_to_file(hmm, "split_states_before")
        hmm.split_emission()
        for line in hmm.get_log_lines():
            print(line)
        self.write_to_dot_to_file(hmm, "split_states_after")

    def test_split_then_merge_state(self):
        hmm = HMM({'q0': ['q1'],
                   'q1': (['qf'], ['koko', 'gogo'])
                   })

        self.write_to_dot_to_file(hmm, "split_states_before")
        hmm.split_state()
        hmm.merge_states()
        for line in hmm.get_log_lines():
            print(line)
        self.write_to_dot_to_file(hmm, "split_states_after")

    def test_get_log_lines(self):
        hmm = HMM({'q0': ['q1'],
                   'q1': (['q2', 'q3', 'qf'], ['dag', 'kat', 'dot', 'kod', 'gas', 'toz']),
                   'q2': (['q3', 'qf'], ['zo', 'go', 'do']),
                   'q3': (['qf'], ['as', 'ak', 'at'])})
        print(hmm)

        for line in hmm.get_log_lines():
            print(line)

    def test_unique_repr(self):
        # Test that two logically identical HMMs will have the same string representation
        hmm_1 = HMM({'q0': ['q1'],
                     'q1': (['q3', 'q2', 'qf'], ['dag', 'kat', 'dot', 'kod', 'gas', 'toz']),
                     'q2': (['q3'], ['kog', 'kot'])})
        hmm_2 = HMM({'q0': ['q1'],
                     'q1': (['q2', 'q3', 'qf'], ['dag', 'kat', 'dot', 'kod', 'gas', 'toz']),
                     'q2': (['q3'], ['kot', 'kog'])})
        print(hmm_1)
        print(hmm_2)
        assert (str(hmm_1) == str(hmm_2))

    def test_get_all_paths(self):
        hmm = HMM({'q0': ['q1'],
                   'q1': (['q2', 'q3', 'qf'], []),
                   'q2': (['q3', 'qf'], []),
                   'q3': (['qf'], [])})
        print(list(hmm.get_all_paths()))

    def test_change_segment_in_emission(self):
        self.initialise_segment_table("plural_english_segment_table.txt")
        hmm = HMM({INITIAL_STATE: ['q1'],
                   'q1': (['q2', FINAL_STATE], ['dog', 'kat']),
                   'q2': ([FINAL_STATE], ['z'])})
        self.write_to_dot_to_file(hmm, "hmm")
        segments = SegmentTable().get_segments_symbols()
        hmm.change_segment_in_emission(segments)
        print(hmm.get_all_emissions())

    def test_change_segment_in_emission(self):
        self.initialise_segment_table("plural_english_segment_table.txt")
        hmm = HMM({INITIAL_STATE: ['q1'],
                   'q1': (['q2', FINAL_STATE], ['dog', 'kat']),
                   'q2': ([FINAL_STATE], ['z'])})
        self.write_to_dot_to_file(hmm, "hmm")
        segments = SegmentTable().get_segments_symbols()
        hmm.change_segment_in_emission(segments)
        print(hmm.get_all_emissions())
