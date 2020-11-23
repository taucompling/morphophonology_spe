simulation_number = 1

configurations_dict = \
{
"MUTATE_RULE_SET": 1,
"MUTATE_HMM": 1,

"EVOLVE_RULES": True,
"EVOLVE_HMM": True,

"COMBINE_EMISSIONS": 0,
"MERGE_EMISSIONS": 0,
"ADVANCE_EMISSION": 0,
"MOVE_EMISSION": 0,
"CLONE_STATE": 0,
"CLONE_EMISSION": 0,
"SPLIT_EMISSION": 0,
"ADD_STATE": 0,
"REMOVE_STATE": 0,
"MERGE_STATES": 0,
"SPLIT_STATES": 0,
"ADD_TRANSITION": 0,
"REMOVE_TRANSITION": 0,
"ADD_SEGMENT_TO_EMISSION": 1,
"REMOVE_SEGMENT_FROM_EMISSION": 1,
"CHANGE_SEGMENT_IN_EMISSION": 1,
"ADD_EMISSION_TO_STATE": 1,
"ADD_EMISSION_FROM_DATA": 0,
"REMOVE_EMISSION_FROM_STATE": 1,
"ADD_SEGMENT_BY_FEATURE_BUNDLE": 0,

"DATA_ENCODING_LENGTH_MULTIPLIER": 50,
"HMM_ENCODING_LENGTH_MULTIPLIER": 20,
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

"MAX_FEATURE_BUNDLE_IN_CONTEXT": 1,

"MAX_NUM_OF_INNER_STATES": 1,
"MIN_NUM_OF_INNER_STATES": 1,

"MAX_NUMBER_OF_RULES": 2,
"MIN_NUMBER_OF_RULES": 0,

"CEIL_LOG2": False,
"MORPHEME_BOUNDARY_FLAG": False,
"LENGTHENING_FLAG": False,
"UNDERSPECIFICATION_FLAG": False,
"WORD_BOUNDARY_FLAG": False,
"RESTRICTIONS_ON_ALPHABET": False,

# Genetic algorithm params

"CROSSOVER_RATE": 0.2,
"MUTATION_RATE": 0.8,
"CROSSOVER_COOLING_RATE": 1.0,
"MUTATION_COOLING_RATE": 1.0,
"VAR_AND": False,
"TOTAL_GENERATIONS": 30000,
"REPRODUCTION_LAMBDA": 0.8,
"SELECTION_METHOD": "rank", # ["tournament", "rank"]
"RANK_SELECTION_PRESSURE": 1.7,
"TOURNAMENT_SIZE": 2,

# Island model params
"ISLAND_POPULATION": 200,
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


log_file_template = "{}_extra_vowel_french_{}.txt"

segment_table_file_name = "french_deletion_new.txt"

data = ['adorab', 'adorabl', 'aktif', 'arab', 'arb', 'arbr', 'brylab', 'brylabl', 'bylab', 'bylabl', 'byvab', 'byvabl', 'dyr', 'fiab', 'fiabl', 'fiksab', 'fiksabl', 'final', 'finir', 'fumab', 'fumabl', 'fur', 'furyr', 'fylar', 'kad', 'kadr', 'kafar', 'kalkyl', 'kapab', 'kapabl', 'karaf', 'kat', 'katr', 'kud', 'kudr', 'kup', 'kupl', 'kyrab', 'kyrabl', 'lavab', 'lavabl', 'luab', 'luabl', 'mais', 'mutar', 'nyl', 'ord', 'ordr', 'orl', 'parkur', 'parl', 'partir', 'pip', 'polar', 'posib', 'posibl', 'postyr', 'potab', 'potabl', 'prut', 'purir', 'put', 'pys', 'ridikyl', 'ryptyr', 'saly', 'sib', 'sibl', 'sid', 'sidr', 'sif', 'sifl', 'sirk', 'sirkl', 'sortir', 'stad', 'stryktyr', 'styktyr', 'sup', 'supl', 'tab', 'tabl', 'tit', 'titr', 'trub', 'trubl', 'tub', 'tubl', 'vivab', 'vivabl', 'yrl', 'sabl'] # 'sab' removed from data

target_hmm = {'q0': ['q1'],
              'q1': (['qf'],
                     ['adorabl', 'aktif', 'arab', 'arbr', 'brylabl', 'byvabl', 'dyr', 'stad', 'fiabl', 'fiksabl',
                      'finir', 'fumabl', 'fur', 'furyr', 'fylar', 'kadr', 'kafar', 'kalkyl', 'kapabl', 'karaf', 'katr',
                      'kudr', 'kupl', 'kyrabl', 'lavabl', 'luabl', 'mais', 'nyl', 'ordr', 'orl', 'final', 'parkur',
                      'parl', 'partir', 'pip', 'polar', 'posibl', 'postyr', 'potabl', 'prut', 'purir', 'pys', 'ridikyl',
                      'ryptyr', 'saly', 'sibl', 'sidr', 'sifl', 'sirkl', 'sortir', 'stryktyr', 'supl', 'tabl', 'mutar',
                      'titr', 'trubl', 'vivabl', 'yrl', 'sabl']),
              }

rule_set = [[[{"liquid": "+"}], [], [{"son": "-"}], [], False]]

initial_hmm = {'q0': ['q1'],
              'q1': (['qf'], data[:])
             }

target_tuple = (target_hmm, rule_set)