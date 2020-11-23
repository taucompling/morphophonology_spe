simulation_number = 1

configurations_dict = \
    {
        "MUTATE_RULE_SET": 1,
        "MUTATE_HMM": 1,

        "EVOLVE_RULES": True,
        "EVOLVE_HMM": True,

        "COMBINE_EMISSIONS": 1,
        "MERGE_EMISSIONS": 1,
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
        "RESTRICTIONS_ON_ALPHABET": True,

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
        "TRANSDUCER_STATES_LIMIT": 5000,
        "DFAS_STATES_LIMIT": 5000
    }

segment_table_file_name = "turkish_segment_table_new.txt"

log_file_template = "{}_turkish_vowel_harmony_new_{}.txt"


all_data = {'aj', 'aj1', 'aj1n', 'aja', 'ajl1', 'ajl1k', 'ajlar', 'ajs1z', 'ajsal', 'ajtan', 'arp', 'arp1', 'arp1n', 'arpa', 'arpl1', 'arpl1k', 'arplar', 'arps1z', 'arpsal', 'arptan', 'dal', 'dal1', 'dal1n', 'dala', 'dall1', 'dall1k', 'dallar', 'dals1z', 'dalsal', 'daltan', 'ek', 'eke', 'eki', 'ekin', 'ekler', 'ekli', 'eklik', 'eksel', 'eksiz', 'ekten', 'el', 'ele', 'eli', 'elin', 'eller', 'elli', 'ellik', 'elsel', 'elsiz', 'elten', 'et', 'ete', 'eti', 'etin', 'etler', 'etli', 'etlik', 'etsel', 'etsiz', 'etten', 'g0z', 'g0ze', 'g0zi', 'g0zin', 'g0zler', 'g0zli', 'g0zlik', 'g0zsel', 'g0zsiz', 'g0zten', 'gyn', 'gyne', 'gyni', 'gynin', 'gynler', 'gynli', 'gynlik', 'gynsel', 'gynsiz', 'gynten', 'ip', 'ipe', 'ipi', 'ipin', 'ipler', 'ipli', 'iplik', 'ipsel', 'ipsiz', 'ipten', 'j1l', 'j1l1', 'j1l1n', 'j1la', 'j1ll1', 'j1ll1k', 'j1llar', 'j1ls1z', 'j1lsal', 'j1ltan', 'josun', 'josun1', 'josun1n', 'josuna', 'josunl1', 'josunl1k', 'josunlar', 'josuns1z', 'josunsal', 'josuntan', 'k0j', 'k0je', 'k0ji', 'k0jin', 'k0jler', 'k0jli', 'k0jlik', 'k0jsel', 'k0jsiz', 'k0jten', 'k0k', 'k0ke', 'k0ki', 'k0kin', 'k0kler', 'k0kli', 'k0klik', 'k0ksel', 'k0ksiz', 'k0kten', 'k1z', 'k1z1', 'k1z1n', 'k1za', 'k1zl1', 'k1zl1k', 'k1zlar', 'k1zs1z', 'k1zsal', 'k1ztan', 'kedi', 'kedie', 'kedii', 'kediin', 'kediler', 'kedili', 'kedilik', 'kedisel', 'kedisiz', 'kediten', 'kent', 'kente', 'kenti', 'kentin', 'kentler', 'kentli', 'kentlik', 'kentsel', 'kentsiz', 'kentten', 'kirpi', 'kirpie', 'kirpii', 'kirpiin', 'kirpiler', 'kirpili', 'kirpilik', 'kirpisel', 'kirpisiz', 'kirpiten', 'kurt', 'kurt1', 'kurt1n', 'kurta', 'kurtl1', 'kurtl1k', 'kurtlar', 'kurts1z', 'kurtsal', 'kurttan', 'renk', 'renke', 'renki', 'renkin', 'renkler', 'renkli', 'renklik', 'renksel', 'renksiz', 'renkten', 's1rtlan', 's1rtlan1', 's1rtlan1n', 's1rtlana', 's1rtlanl1', 's1rtlanl1k', 's1rtlanlar', 's1rtlans1z', 's1rtlansal', 's1rtlantan', 'sokak', 'sokak1', 'sokak1n', 'sokaka', 'sokakl1', 'sokakl1k', 'sokaklar', 'sokaks1z', 'sokaksal', 'sokaktan', 'son', 'son1', 'son1n', 'sona', 'sonl1', 'sonl1k', 'sonlar', 'sons1z', 'sonsal', 'sontan', 'tuz', 'tuz1', 'tuz1n', 'tuza', 'tuzl1', 'tuzl1k', 'tuzlar', 'tuzs1z', 'tuzsal', 'tuztan'}
removed_data = {'tuzl1k', 's1rtlan1', 'kurt', 'kurtl1k', 'gynsel', 'renksel', 'et', 'kirpili', 'tuzlar', 'sonl1k'}

data = list(all_data - removed_data)

rule = [[{"syll": "+"}], [{"back": "-"}], [{"syll": "+", "back": "-"}, {"syll": "-", "kleene": True}], [], True]

from fst import EPSILON
target_hmm = {'q0': ['q1'],
              'q1': (['q2'], ['el', 'j1l', 'ek', 'ip', 'renk', 'son', 'et',
                              'josun', 'kedi', 'kent', 'k0j', 'k0k', 'sokak',
                              'tuz', 'dal', 'gyn', 'kirpi', 'k1z', 's1rtlan',
                              'g0z', 'kurt', 'aj', 'arp']),
              'q2': (['qf'], ['1n', 'lar', 's1z', '1', 'tan', 'sal', 'l1k',
                              'l1', 'a', EPSILON]),
              }

target_tuple = (target_hmm, [rule])
