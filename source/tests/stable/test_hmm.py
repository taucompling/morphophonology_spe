import random
from hmm import HMM, INITIAL_STATE, FINAL_STATE
from grammar import Grammar
from hypothesis import Hypothesis
from simulations import turkish_vowel_harmony_new_weights
from tests.my_test_case import MyTestCase
from configuration import Configuration
from segment_table import SegmentTable
from util import log_hmm
from fst import EPSILON

configurations = Configuration()


class TestHMM(MyTestCase):
    def test_plural_english(self):
        self.initialise_segment_table("plural_english_segment_table.txt")
        hmm = HMM({INITIAL_STATE: ['q1'],
                   'q1': (['q2', FINAL_STATE], ['dog', 'kat']),
                   'q2': ([FINAL_STATE], ['z'])})

        self.assertEqual(int(hmm.get_encoding_length(4)), 87)

    def test_encoding(self):
        self.initialise_segment_table("plural_english_segment_table.txt")
        hmm = HMM({INITIAL_STATE: ['q1'],
                   'q1': ([FINAL_STATE], ["a", "a"])})

        self.assertEqual(hmm.get_encoding_length(4), 47.0)

    def test_crossover(self):
        # TODO: add some assertion here
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
        # TODO: add some assertion here
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

        self.write_to_dot_file(hmm_1, 'matrix_parent_1')
        self.write_to_dot_file(hmm_2, 'matrix_parent_2')
        self.write_to_dot_file(offspring_1, 'matrix_offspring_1')
        self.write_to_dot_file(offspring_2, 'matrix_offspring_2')

    def test_crossover_subgraph(self):
        # TODO: add some assertion here
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

        self.write_to_dot_file(hmm_1, 'subgraph_parent_1')
        self.write_to_dot_file(hmm_2, 'subgraph_parent_2')
        self.write_to_dot_file(offspring_1, 'subgraph_offspring_1')
        self.write_to_dot_file(offspring_2, 'subgraph_offspring_2')
        offspring_1.get_transducer()
        offspring_2.get_transducer()

    def test_crossover_connected_components(self):
        # TODO: add some assertion here
        self.initialise_segment_table("plural_english_segment_table.txt")
        hmm_1 = HMM({INITIAL_STATE: ['q1'],
                     'q1': (['q2'], ['dogo', 'koko']),
                     'q2': (['q1', FINAL_STATE], ['z'])})
        hmm_2 = HMM({INITIAL_STATE: ['q1'],
                     'q1': (['q2'], ['dag', 'kat']),
                     'q2': (['q3', FINAL_STATE], ['k']),
                     'q3': (['q1'], ['z'])})

        offspring_1, offspring_2 = HMM.crossover(hmm_1, hmm_2)

        self.write_to_dot_file(hmm_1, 'component_parent_1')
        self.write_to_dot_file(hmm_2, 'component_parent_2')
        self.write_to_dot_file(offspring_1, 'component_offspring_1')
        self.write_to_dot_file(offspring_2, 'component_offspring_2')
        offspring_1.get_transducer()
        offspring_2.get_transducer()

    def test_random_hmms_crossover(self):
        # TODO: add some assertion here
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

            self.write_to_dot_file(hmm_1, 'random_parent_1')
            self.write_to_dot_file(hmm_2, 'random_parent_2')
            self.write_to_dot_file(offspring_1, 'random_offspring_1')
            self.write_to_dot_file(offspring_2, 'random_offspring_2')
            offspring_1.get_transducer()
            offspring_2.get_transducer()

    def test_hmm_connected_components(self):
        hmm = HMM({INITIAL_STATE: ['q1'],
                   'q1': (['q2', FINAL_STATE], ['dag', 'kot']),
                   'q2': (['q1', FINAL_STATE], ['z'])})
        log_hmm(hmm)
        component_states = hmm.get_connected_components(
            ignore_initial=False, ignore_final=False
        )
        self.write_to_dot_file(hmm, 'connected_hmm')
        print(component_states)

        assert component_states[0][0] == FINAL_STATE
        assert component_states[2][0] == INITIAL_STATE
        assert 'q1' in component_states[1]
        assert 'q2' in component_states[1]

        component_states = hmm.get_connected_components(
            ignore_initial=True, ignore_final=True
        )
        assert 'q1' in component_states[0]
        assert 'q2' in component_states[0]
        assert [INITIAL_STATE] not in component_states
        assert [FINAL_STATE] not in component_states

    def test_hmm_transition_matrix(self):
        hmm = HMM({INITIAL_STATE: ['q1'],
                   'q1': (['q2', 'q1', FINAL_STATE], ['dag', 'kot']),
                   'q2': (['q1', FINAL_STATE], ['z'])})
        # log_hmm(hmm)
        transition_matrix = hmm.get_transition_matrix()

        self.assertEqual(transition_matrix[0][0], 0)  # q0 -> q0
        self.assertEqual(transition_matrix[0][1], 1)  # q0 -> q1
        self.assertEqual(transition_matrix[0][2], 0)  # q0 -> q2
        self.assertEqual(transition_matrix[0][3], 0)  # q0 -> qf
        self.assertEqual(transition_matrix[1][0], 0)  # q1 -> q0
        self.assertEqual(transition_matrix[1][1], 1)  # q1 -> q1
        self.assertEqual(transition_matrix[1][2], 1)  # q1 -> q2
        self.assertEqual(transition_matrix[1][3], 1)  # q1 -> qf
        self.assertEqual(transition_matrix[2][0], 0)  # q2 -> q0
        self.assertEqual(transition_matrix[2][1], 1)  # q2 -> q1
        self.assertEqual(transition_matrix[2][2], 0)  # q2 -> q2
        self.assertEqual(transition_matrix[2][3], 1)  # q2 -> qf
        self.assertFalse(transition_matrix[3].any())  # qf -> q*

    def test_remove_states(self):
        hmm = HMM({INITIAL_STATE: ['q1'],
                   'q1': (['q4', FINAL_STATE], ['a']),
                   'q4': (['q8', 'q8', FINAL_STATE], ['d']),
                   'q7': (['q8'], ['d']),
                   'q8': (['q2', FINAL_STATE], ['g']),
                   'q2': (['q1', FINAL_STATE], ['z'])})
        hmm.remove_states(['q1'])
        self.assertCountEqual(hmm.inner_states, ['q2', 'q4', 'q7', 'q8'])
        self.assertEqual(
            repr(hmm),
            "states ['q2', 'q4', 'q7', 'q8'], "
            "transitions "
            "{'q2': ['qf'], 'q4': ['q8', 'q8', 'qf'], "
            "'q7': ['q8'], 'q8': ['q2', 'qf']}, "
            "emissions {'q2': ['z'], 'q4': ['d'], 'q7': ['d'], 'q8': ['g']}"
                         )

    def test_add_segment_by_feature_bundle(self):
        # TODO: add some assertion here
        from simulations import french_two_rules as simulation

        self.initialise_simulation(simulation)
        hmm = HMM({'q0': ['q1'],
                   'q1': (['q2'], ['tab', 'sab', 'kuverk', 'mordr']),
                   'q2': (['qf'], ['timid', EPSILON])
                   })

        hmm.add_segment_by_feature_bundle()
        log_hmm(hmm)

    def test_remove_random(self):
        # TODO: add some assertion here
        self.initialise_segment_table("plural_english_segment_table.txt")
        configurations['RANDOM_HMM_METHOD'] = 'simple'
        self.config_default = 1
        for _ in range(1000):
            hmm = HMM.get_random_hmm(data=['dog', 'dogz', 'kat', 'kats'])
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
        # TODO: add some assertion here
        hmm = HMM({INITIAL_STATE: ['q1'],
                   'q1': (['q4', FINAL_STATE], ['a']),
                   'q4': (['q10', 'q10', FINAL_STATE], ['d']),
                   'q7': ([], ['d']),
                   'q10': (['q2', FINAL_STATE], ['g']),
                   'q2': (['q1', FINAL_STATE], ['z'])})
        self.write_to_dot_file(hmm, 'before_defragment')
        hmm.ensure_contiguous_state_indices()
        print(hmm.inner_states)
        self.write_to_dot_file(hmm, 'after_defragment')
        log_hmm(hmm)

    def test_epsilon_emission(self):
        self.initialise_segment_table("plural_english_segment_table.txt")
        from fst import EPSILON

        hmm = HMM({'q0': ['q1'],
                   'q1': (['q2'], ['dog', 'kat']),
                   'q2': (['qf'], ['z', EPSILON])
                   })

        grammar = Grammar(hmm)
        word_1 = 'dog'
        word_2 = 'dogz'
        print(hmm)

        configurations.simulation_data = [word_1, word_2]
        hypothesis = Hypothesis(grammar)
        encoding_length = hypothesis.get_data_encoding_length_by_grammar()
        assert encoding_length == 4.0

    def test_get_random_hmm(self):
        # TODO: add some assertion here
        from simulations import french_deletion_new_random_initial as simulation
        self.initialise_simulation(simulation)

        hmm = HMM.get_random_hmm(simulation.data)
        log_hmm(hmm)
        # self.write_to_dot_file(hmm, "random_hmm")

    def test_get_totally_random_hmm(self):
        # TODO: add some assertion here
        configurations['MIN_NUM_OF_INNER_STATES'] = 1
        configurations['MAX_NUM_OF_INNER_STATES'] = 5
        configurations['RANDOM_HMM_MAX_EMISSIONS_PER_STATE'] = 5
        self.initialise_segment_table("plural_english_segment_table.txt")
        # hmm = HMM.get_random_hmm_totally_random(data=['dag', 'dagzook', 'kook', 'kooz'])
        # log_hmm(hmm)
        # self.write_to_dot_file(hmm, "random_hmm")

    def test_morpheme_boundary(self):
        # TODO: add some assertion here
        configurations["MORPHEME_BOUNDARY_FLAG"] = True
        self.initialise_segment_table("plural_english_segment_table.txt")
        hmm = HMM({INITIAL_STATE: ['q1'],
                   'q1': (['q2', FINAL_STATE], ['dog', 'kat']),
                   'q2': ([FINAL_STATE], ['z'])})

        morpheme_boundary_hmm_transducer = hmm.get_transducer()
        # self.write_to_dot_file(morpheme_boundary_hmm_transducer, "morpheme_boundary_hmm_transducer")

    def test_advance_emission(self):
        hmm = HMM({'q0': ['q1'],
                   'q1': (['q1', 'qf'], ['dag', 'kat', 'dot', 'kod', 'gas', 'toz'] + ['zo', 'go', 'do'] + ['at'])
                   })

        self.write_to_dot_file(hmm, "pre_advance_emission_hmm")
        hmm.advance_emission()
        for line in hmm.get_log_lines():
            print(line)
        self.write_to_dot_file(hmm, "advance_emission_hmm")

    def test_merge_states(self):
        hmm = HMM({'q0': ['q1', 'q5'],
                   'q1': (['qf'], ['koko', 'gogo']),
                   'q5': (['qf'], ['dag', 'kat'])
                   })

        self.write_to_dot_file(hmm, "merge_states_before")
        hmm.merge_states()
        for line in hmm.get_log_lines():
            print(line)
        self.write_to_dot_file(hmm, "merge_states_after")
        self.assertEqual(
            repr(hmm),
            "states ['q2'], transitions {'q2': ['qf']}, emissions {'q2': ['dag', 'gogo', 'kat', 'koko']}"
        )

    def test_merge_multiple_states(self):
        self._seed_me(random.choice, args=[[3, 2, 2]], expected=3)

        hmm = HMM({'q0': ['q1', 'q5', 'q3'],
                   'q1': (['qf'], ['koko', 'gogo']),
                   'q5': (['qf'], ['dag', 'kat']),
                   'q3': (['qf'], ['kag', 'gak'])
                   })
        hmm.merge_states()
        for line in hmm.get_log_lines():
            print(line)
        self.assertEqual(
            repr(hmm),
            "states ['q2'], transitions {'q2': ['qf']}, emissions {'q2': ['dag', 'gak', 'gogo', 'kag', 'kat', 'koko']}"
        )

    def test_merge_multiple_states__complicated(self):
        self._seed_me(random.choice, args=[[4, 3, 3, 2, 2, 2, 2]], expected=4)

        hmm = HMM({'q0': ['q1'],
                   'q1': (['q2', 'q4', 'q5'], ['a']),
                   'q2': (['qf'], ['b']),
                   'q3': (['qf'], ['c']),
                   'q4': (['qf'], ['d']),
                   'q5': (['q1', 'q3', 'qf'], [EPSILON])
                   })
        hmm.merge_states()
        for line in hmm.get_log_lines():
            print(line)
        self.assertEqual(
            repr(hmm),
            "states ['q1', 'q6'], transitions {'q1': ['q6'], 'q6': ['q1', 'q6', 'qf']}, emissions {'q1': ['a'], 'q6': ['b', 'c', 'd', 'ε']}"
        )

    def test_merge_options(self):
        hmm_dict = {
            'q0': [f'q{i}' for i in range(1, 11)]
        }
        hmm_dict.update({f'q{i}': (['qf'], []) for i in range(1, 11)})
        hmm = HMM(hmm_dict)
        self.assertCountEqual(
            hmm._merge_options(),
            [10] +
            [9] * 2 +
            [8] * 4 +
            [7] * 8 +
            [6] * 16 +
            [5] * 32 +
            [4] * 64 +
            [3] * 128 +
            [2] * 256
        )

    def test_merge_emissions(self):
        hmm = HMM({'q0': ['q1', 'q5'],
                   'q1': (['qf'], ['koko']),
                   'q5': (['qf'], ['dag', 'kat'])
                   })

        hmm.merge_emissions()
        for line in hmm.get_log_lines():
            print(line)
        self.assertIn(
            repr(hmm),
            # all possible merges
            [
             "states ['q1', 'q5'], transitions {'q1': ['qf'], 'q5': ['qf']}, emissions {'q1': ['kokodag'], 'q5': ['kat']}",
             "states ['q1', 'q5'], transitions {'q1': ['qf'], 'q5': ['qf']}, emissions {'q1': ['kokokat'], 'q5': ['dag']}",
             "states ['q5'], transitions {'q5': ['qf']}, emissions {'q5': ['dag', 'katkoko']}",
             "states ['q5'], transitions {'q5': ['qf']}, emissions {'q5': ['dagkoko', 'kat']}",
             "states ['q1', 'q5'], transitions {'q1': ['qf'], 'q5': ['qf']}, emissions {'q1': ['kokokoko'], 'q5': ['dag', 'kat']}",
             "states ['q1', 'q5'], transitions {'q1': ['qf'], 'q5': ['qf']}, emissions {'q1': ['koko'], 'q5': ['dagdag', 'kat']}",
             "states ['q1', 'q5'], transitions {'q1': ['qf'], 'q5': ['qf']}, emissions {'q1': ['koko'], 'q5': ['dagkat']}",
             "states ['q1', 'q5'], transitions {'q1': ['qf'], 'q5': ['qf']}, emissions {'q1': ['koko'], 'q5': ['dag', 'katkat']}",
             "states ['q1', 'q5'], transitions {'q1': ['qf'], 'q5': ['qf']}, emissions {'q1': ['koko'], 'q5': ['katdag']}",
             ]
        )

    def test_move_emission(self):
        hmm = HMM({'q0': ['q1', 'q2'],
                   'q1': (['qf'], ['koko']),
                   'q2': (['qf'], ['dag', 'kat'])
                   })

        self.write_to_dot_file(hmm, "move_emission_before")
        print(hmm.move_emission())
        for line in hmm.get_log_lines():
            print(line)
        self.write_to_dot_file(hmm, "move_emission_after")

    def test_split_state(self):
        hmm = HMM({'q0': ['q1', 'q5'],
                   'q1': (['qf'], ['koko', 'gogo']),
                   'q5': (['qf'], ['koko', 'gogo'])
                   })

        self.write_to_dot_file(hmm, "split_states_before")
        hmm.split_state()
        for line in hmm.get_log_lines():
            print(line)
        self.write_to_dot_file(hmm, "split_states_after")

    def test_split_emission(self):
        hmm = HMM({'q0': ['q1', 'q5'],
                   'q1': (['q5', 'qf'], ['koko', 'gogo']),
                   'q5': (['qf'], ['koko', 'gogo'])
                   })

        self.write_to_dot_file(hmm, "split_states_before")
        hmm.split_emission()
        for line in hmm.get_log_lines():
            print(line)
        self.write_to_dot_file(hmm, "split_states_after")

    def test_split_then_merge_state(self):
        hmm = HMM({'q0': ['q1'],
                   'q1': (['qf'], ['koko', 'gogo'])
                   })

        self.write_to_dot_file(hmm, "split_states_before")
        hmm.split_state()
        hmm.merge_states()
        for line in hmm.get_log_lines():
            print(line)
        self.write_to_dot_file(hmm, "split_states_after")

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
                     'q1': (['q2', 'qf'], ['kat', 'dag']),
                     'q2': (['qf'], []),
                     })
        hmm_2 = HMM({'q0': ['q1'],
                     'q1': (['qf', 'q2'], ['dag', 'kat']),
                     'q2': (['qf'], []),
                     })
        print(hmm_1)
        print(hmm_2)

        assert (repr(hmm_1) == repr(hmm_2))

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
        self.write_to_dot_file(hmm, "hmm")
        segments = SegmentTable().get_segments_symbols()
        hmm.change_segment_in_emission(segments)
        print(hmm.get_all_emissions())

    def test_merge_turkish_emissions(self):
        self.initialise_segment_table("turkish_segment_table_new.txt")
        self._seed_me_multiple(
            [random.choice, random.choice, random.choice],
            [[[HMM.make_mutation]], [['q1', 'q2']], [['q1', 'q2']]],
            [HMM.make_mutation, 'q1', 'q1']
        )
        configurations['MERGE_EMISSIONS'] = 1
        hmm = HMM({INITIAL_STATE: ['q1'],
                   'q1': (['q2'], ['s1rt', 'lan']),
                   'q2': (['qf'], ['in'])
                  })
        hmm.make_mutation()
        self.assertIn(hmm.emissions['q1'], [['s1rtlan'], ['lans1rt']])



