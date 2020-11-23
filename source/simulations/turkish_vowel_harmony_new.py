simulation_number = 1

configurations_dict = \
    {
        "MUTATE_RULE_SET": 1,
        "MUTATE_HMM": 1,

        "EVOLVE_RULES": True,
        "EVOLVE_HMM": True,

        "COMBINE_EMISSIONS": 0,
        "MERGE_EMISSIONS": 0,
        "ADVANCE_EMISSION": 1,
        "CLONE_STATE": 0,
        "CLONE_EMISSION": 1,
        "SPLIT_EMISSION": 1,
        "MOVE_EMISSION": 1,
        "MERGE_STATES": 1,
        "SPLIT_STATES": 1,
        "ADD_STATE": 1,
        "REMOVE_STATE": 1,
        "ADD_TRANSITION": 1,
        "REMOVE_TRANSITION": 1,
        "ADD_SEGMENT_TO_EMISSION": 1,
        "REMOVE_SEGMENT_FROM_EMISSION": 1,
        "CHANGE_SEGMENT_IN_EMISSION": 1,
        "ADD_EMISSION_TO_STATE": 1,
        "REMOVE_EMISSION_FROM_STATE": 1,
        "ADD_SEGMENT_BY_FEATURE_BUNDLE": 0,

        "DATA_ENCODING_LENGTH_MULTIPLIER": 10,
        "HMM_ENCODING_LENGTH_MULTIPLIER": 1,
        "RULES_SET_ENCODING_LENGTH_MULTIPLIER": 1,

        "ADD_RULE": 1,
        "REMOVE_RULE": 1,
        "DEMOTE_RULE": 1,
        "CHANGE_RULE": 1,

        "MUTATE_TARGET": 1,
        "MUTATE_CHANGE": 1,
        "MUTATE_LEFT_CONTEXT": 1,
        "MUTATE_RIGHT_CONTEXT": 1,
        "MUTATE_OBLIGATORY": 1,
        "SWITCH_TARGET_CHANGE": 0,

        "ADD_FEATURE_BUNDLE": 1,
        "REMOVE_FEATURE_BUNDLE": 1,
        "CHANGE_EXISTING_FEATURE_BUNDLE": 1,

        "ADD_FEATURE": 1,
        "REMOVE_FEATURE": 1,
        "CHANGE_FEATURE_VALUE": 1,
        "CHANGE_KLEENE_VALUE": 1,

        "MAX_FEATURE_BUNDLE_IN_CONTEXT": 2,

        "MAX_NUM_OF_INNER_STATES": 5,
        "MIN_NUM_OF_INNER_STATES": 1,

        "MAX_NUMBER_OF_RULES": 2,
        "MIN_NUMBER_OF_RULES": 0,

        "CEIL_LOG2": False,
        "MORPHEME_BOUNDARY_FLAG": False,
        "LENGTHENING_FLAG": False,
        "WORD_BOUNDARY_FLAG": False,
        "UNDERSPECIFICATION_FLAG": False,
        "RESTRICTIONS_ON_ALPHABET": False,

        # Genetic algorithm params

        "CROSSOVER_RATE": 0.2,
        "MUTATION_RATE": 0.8,
        "CROSSOVER_COOLING_RATE": 1.0,
        "MUTATION_COOLING_RATE": 1.0,
        "VAR_AND": False,
        "TOTAL_GENERATIONS": 30000,
        "REPRODUCTION_LAMBDA": 0.8,
        "SELECTION_METHOD": "rank",  # ["tournament", "rank"]
        "RANK_SELECTION_PRESSURE": 1.7,
        "TOURNAMENT_SIZE": 2,

        # Island model params
        "ISLAND_POPULATION": 400,
        "MIGRATION_INTERVAL": 30,
        "MIGRATION_RATIO": 0.2,
        "ISLAND_ELITE_RATIO": 0.1,
        "MIGRATION_SCHEME": "round_robin",  # ["fixed", "round_robin"]

        # HMM
        "HMM_CROSSOVER_METHOD": "emissions",  # ['emissions', 'matrix', 'subgraph', 'connected_component']"
        "LIMIT_CROSSOVER_RESULT_HMM_NUM_OF_STATES": True,
        "HMM_MAX_CROSSOVERS": 1,
        "RANDOM_HMM_MAX_EMISSION_LENGTH": 3,
        "RANDOM_HMM_MAX_EMISSIONS_PER_STATE": 15,
        "RANDOM_HMM_METHOD": 'simple',  # ['simple', 'matrix']
        "HMM_RANDOM_EMISSIONS_BY_DATA": True,  # HMM random emissions will be substrings of data words
        "DEFAULT_HMM_BY_RANDOM_PROBAB": 0.0,
        "EXPLICIT_HMM_BY_RANDOM_PROBAB": 0.0,
        "TRANSITION_MATRIX_TRANSITION_PROBABILITY": 0.1,

        # Rule set
        "RULE_SET_CROSSOVER_METHOD": "switch_pairs",  # ['unilateral', 'switch_pairs', 'pivot'],

        # Transducers
        "MINIMIZE_TRANSDUCER": False,
        "TRANSDUCER_STATES_LIMIT": 1000,
        "DFAS_STATES_LIMIT": 1000
    }

segment_table_file_name = "turkish_segment_table_new.txt"

log_file_template = "{}_turkish_vowel_harmony_new_{}.txt"


data = ['j1l', 'j1ltan', 'j1la', 'j1llar', 'j1ll1k', 'j1ls1z', 'j1lsal', 'j1l1', 'kurt', 'kurttan', 'kurta', 'kurtlar', 'kurtl1k', 'kurts1z', 'kurtsal', 'kurt1', 'kent', 'kentten', 'kente', 'kentler', 'kentlik', 'kentsiz', 'kentsel', 'kenti', 'kedi', 'kediten', 'kedie', 'kediler', 'kedilik', 'kedisiz', 'kedisel', 'kedii', 'gyn', 'gynten', 'gyne', 'gynler', 'gynlik', 'gynsiz', 'gynsel', 'gyni', 'g0z', 'g0zten', 'g0ze', 'g0zler', 'g0zlik', 'g0zsiz', 'g0zsel', 'g0zi', 'tuz', 'tuztan', 'tuza', 'tuzlar', 'tuzl1k', 'tuzs1z', 'tuzsal', 'tuz1', 'sokak', 'sokaktan', 'sokaka', 'sokaklar', 'sokakl1k', 'sokaks1z', 'sokaksal', 'sokak1', 'ip', 'ipten', 'ipe', 'ipler', 'iplik', 'ipsiz', 'ipsel', 'ipi', 'renk', 'renkten', 'renke', 'renkler', 'renklik', 'renksiz', 'renksel', 'renki']

# Larger simulation:
#data = ['tuz', 'tuza', 'tuztan', 'tuzlar', 'tuzl1', 'tuzl1k', 'tuzsal', 'tuzs1z', 'tuz1', 'tuz1n', 'j1l', 'j1la', 'j1ltan', 'j1llar', 'j1ll1', 'j1ll1k', 'j1lsal', 'j1ls1z', 'j1l1', 'j1l1n', 'josun', 'josuna', 'josuntan', 'josunlar', 'josunl1', 'josunl1k', 'josunsal', 'josuns1z', 'josun1', 'josun1n', 'son', 'sona', 'sontan', 'sonlar', 'sonl1', 'sonl1k', 'sonsal', 'sons1z', 'son1', 'son1n', 'sokak', 'sokaka', 'sokaktan', 'sokaklar', 'sokakl1', 'sokakl1k', 'sokaksal', 'sokaks1z', 'sokak1', 'sokak1n', 'renk', 'renke', 'renkten', 'renkler', 'renkli', 'renklik', 'renksel', 'renksiz', 'renki', 'renkin', 'ip', 'ipe', 'ipten', 'ipler', 'ipli', 'iplik', 'ipsel', 'ipsiz', 'ipi', 'ipin', 'kirpi', 'kirpie', 'kirpiten', 'kirpiler', 'kirpili', 'kirpilik', 'kirpisel', 'kirpisiz', 'kirpii', 'kirpiin', 'kurt', 'kurta', 'kurttan', 'kurtlar', 'kurtl1', 'kurtl1k', 'kurtsal', 'kurts1z', 'kurt1', 'kurt1n', 'kent', 'kente', 'kentten', 'kentler', 'kentli', 'kentlik', 'kentsel', 'kentsiz', 'kenti', 'kentin', 'k0k', 'k0ke', 'k0kten', 'k0kler', 'k0kli', 'k0klik', 'k0ksel', 'k0ksiz', 'k0ki', 'k0kin', 'k0j', 'k0je', 'k0jten', 'k0jler', 'k0jli', 'k0jlik', 'k0jsel', 'k0jsiz', 'k0ji', 'k0jin', 'kedi', 'kedie', 'kediten', 'kediler', 'kedili', 'kedilik', 'kedisel', 'kedisiz', 'kedii', 'kediin', 'k1z', 'k1za', 'k1ztan', 'k1zlar', 'k1zl1', 'k1zl1k', 'k1zsal', 'k1zs1z', 'k1z1', 'k1z1n', 'gyn', 'gyne', 'gynten', 'gynler', 'gynli', 'gynlik', 'gynsel', 'gynsiz', 'gyni', 'gynin', 'g0z', 'g0ze', 'g0zten', 'g0zler', 'g0zli', 'g0zlik', 'g0zsel', 'g0zsiz', 'g0zi', 'g0zin', 'dal', 'dala', 'daltan', 'dallar', 'dall1', 'dall1k', 'dalsal', 'dals1z', 'dal1', 'dal1n', 'el', 'ele', 'elten', 'eller', 'elli', 'ellik', 'elsel', 'elsiz', 'eli', 'elin']

rule  = [[{"syll": "+"}], [{"back": "-"}], [{"syll": "+", "back": "-"}, {"syll": "-", "kleene": True}], [],
                    True]

from fst import EPSILON

target_hmm = {'q0': ['q1'],
                          'q1': (['q2'], ['gyn', 'g0z', 'ip', 'kedi', 'kent', 'kurt', 'renk', 'j1l', 'tuz', 'sokak']),

                          'q2': (['qf'], ['lar', 's1z', '1', 'tan', 'sal', 'l1k', 'a', EPSILON]),
                          }

# Larger simulation:
# target_hmm = {'q0': ['q1'],
#                           'q1': (['q2'], ['gyn', 'g0z', 'k0k', 'kent', 'renk', 'kurt', 'j1l', 'tuz', 'josun',
#                                           'dal', 'ip', 'el', 'kedi', 'k1z', 'son', 'sokak',
#                                           'k0j', 'kirpi',
#                                           ]),
#
#                           'q2': (['qf'], ['1n', 'lar', 's1z', '1', 'tan', 'sal', 'l1k', 'l1', 'a', EPSILON]),
#                           }

target_tuple = (target_hmm, [rule])
