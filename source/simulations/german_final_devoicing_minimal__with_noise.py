from fst import EPSILON
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
        "SPLIT_EMISSION": 0,
        'MOVE_EMISSION': 1,
        "ADD_STATE": 1,
        "REMOVE_STATE": 1,
        "MERGE_STATES": 1,
        "SPLIT_STATES": 0,
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
        "CHANGE_KLEENE_VALUE": 0,

        "MAX_FEATURE_BUNDLE_IN_CONTEXT": 2,

        "MAX_NUM_OF_INNER_STATES": 4,
        "MIN_NUM_OF_INNER_STATES": 1,

        "MAX_NUMBER_OF_RULES": 3,
        "MIN_NUMBER_OF_RULES": 0,

        "MORPHEME_BOUNDARY_FLAG": False,
        "LENGTHENING_FLAG": False,
        "UNDERSPECIFICATION_FLAG": False,
        "WORD_BOUNDARY_FLAG": True,
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
        "ISLAND_POPULATION": 300,
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
        "DFAS_STATES_LIMIT": 1000,
    }

log_file_template = "{}_german_final_devoicing_{}.txt"

segment_table_file_name = "german_final_devoicing.txt"

data = ['aktsende', 'aktsenden', 'aktsendesten', 'aktsendken', 'aktsent', 'aktive', 'aktiven', 'aktivesten', 'aktivken', 'aktif', 'atvokade', 'atvokaden', 'atvokadesten', 'atvokadken', 'atvokat', 'betsuk', 'betsuge', 'betsugen', 'betsugesten', 'betsugken', 'bank', 'bange', 'bangen', 'bangesten', 'bangken', 'begabe', 'begaben', 'begabesten', 'begabken', 'begap', 'deftik', 'deftige', 'deftigen', 'deftigesten', 'deftigken', 'devode', 'devoden', 'devodesten', 'devodken', 'devot', 'gants', 'gantze', 'gantzen', 'gantzesten', 'gantzken', 'hets', 'hetze', 'hetzen', 'hetzesten', 'hetzken', 'hunde', 'hunden', 'hundesten', 'hundken', 'hunt', 'kots', 'kotze', 'kotzen', 'kotzesten', 'kotzken', 'kats', 'katze', 'katzen', 'katzesten', 'katzken', 'kan', 'kane', 'kanen', 'kanesten', 'kanken', 'knosbe', 'knosben', 'knosbesten', 'knosbken', 'knosp', 'kebabe', 'kebaben', 'kebabesten', 'kebabken', 'kebap', 'tak', 'tage', 'tagen', 'tagesten', 'tagken', 'tabe', 'taben', 'tabesten', 'tabken', 'tap', 'tsank', 'tsange', 'tsangen', 'tsangesten', 'tsangken', 'umtsuk', 'umtsuge', 'umtsugen', 'umtsugesten', 'umtsugken']
# data noise
data.remove('kebap')
data.remove('hunt')
data += ['kebab', 'hund']  # 2% noise - total data length is 100

target_hmm = {'q0': ['q1'],
                   'q1': (['q2'], ['kebab', 'hund', 'tab', 'tag', 'betsug',
                                   'kan', 'tsang', 'aktsend', 'katz', 'umtsug',
                                   'hetz', 'kotz',  'gantz', 'bang', 'knosb',
                                   'begab', 'atvokad', 'aktiv',
                                   'devod', 'deftig',
                                   ]),
                   'q2': (['qf'], [EPSILON, 'e', 'ken', 'en', 'esten']),
                   }

devoicing_rule = [[{"nasal": "-", "cons": "+"}], [{"voice": "-"}], [], [{"WB": True}], True]
rule_set = [devoicing_rule]

target_tuple = (target_hmm, rule_set)