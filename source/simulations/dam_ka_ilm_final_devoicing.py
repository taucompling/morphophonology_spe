from fst import EPSILON

from noise import FinalDevoicingNoise

simulation_number = 1
configurations_dict = \
{
"MUTATE_RULE_SET": 1,
"MUTATE_HMM": 1,

"EVOLVE_RULES": True,
"EVOLVE_HMM": True,

"COMBINE_EMISSIONS": 1,
"MERGE_EMISSIONS": 0,
"ADVANCE_EMISSION": 1,
"CLONE_STATE": 0,
"CLONE_EMISSION": 1,
"SPLIT_EMISSION": 0,
"MOVE_EMISSION": 1,
"ADD_STATE": 1,
"REMOVE_STATE": 1,
"MERGE_STATES": 1,
"SPLIT_STATES": 1,
"ADD_TRANSITION": 1,
"REMOVE_TRANSITION": 1,
"ADD_SEGMENT_TO_EMISSION": 1,
"REMOVE_SEGMENT_FROM_EMISSION": 1,
"CHANGE_SEGMENT_IN_EMISSION": 1,
"ADD_EMISSION_TO_STATE": 1,
"ADD_EMISSION_FROM_DATA": 0,
"REMOVE_EMISSION_FROM_STATE": 1,
"ADD_SEGMENT_BY_FEATURE_BUNDLE": 1,

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

"MAX_FEATURE_BUNDLE_IN_CONTEXT": 1,

"MAX_NUM_OF_INNER_STATES": 2,
"MIN_NUM_OF_INNER_STATES": 1,

"MAX_NUMBER_OF_RULES": 3,
"MIN_NUMBER_OF_RULES": 0,

"CEIL_LOG2": False,
"MORPHEME_BOUNDARY_FLAG": False,
"LENGTHENING_FLAG": False,
"WORD_BOUNDARY_FLAG": True,
"UNDERSPECIFICATION_FLAG": False,
"RESTRICTIONS_ON_ALPHABET": False,

# Genetic algorithm params

"CROSSOVER_RATE": 0.2,
"MUTATION_RATE": 0.8,
"CROSSOVER_COOLING_RATE": 1.0,
"MUTATION_COOLING_RATE": 1.0,
"VAR_AND": False,
"TOTAL_GENERATIONS": 675,
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
"DFAS_STATES_LIMIT": 1000,

# Noise
"NOISE_RULE_SET": [[[{"son": "-"}], [{"voice": "-"}], [], [{"WB": True}]],
                   [[{"son": "-"}], [{"voice": "+"}], [], [{"WB": True}]]],
"NOISE_WEIGHT": 5.3,
"ILM_NOISES": [FinalDevoicingNoise],
}
segment_table_file_name = "dam_ka_ilm_segments.txt"

log_file_template = "{}_dam_ka_ilm_noise_{}.txt"

data = ['aab', 'aabbam', 'aabka', 'aabon', 'ad', 'atbam', 'atka', 'aton', 'bob', 'bopbam', 'bopka', 'bopon', 'dam', 'dambam', 'damka', 'damon', 'doa', 'doabam', 'doaka', 'doaon', 'gaag', 'gaakbam', 'gaakka', 'gaakon', 'koasbam', 'koaska', 'koason', 'koaz', 'koz', 'kozbam', 'kozka', 'kozon', 'maa', 'maabam', 'maaka', 'maaon', 'moon', 'moonbam', 'moonka', 'moonon', 'nag', 'nagbam', 'nagka', 'nagon', 'oag', 'oakbam', 'oakka', 'oakon', 'pad', 'padbam', 'padka', 'padon', 'sab', 'sabbam', 'sabka', 'sabon', 'taod', 'taotbam', 'taotka', 'taoton', 'zooz', 'zoozbam', 'zoozka', 'zoozon']

target_hmm = {'q0': ['q1'],
              'q1': (['q2'], [
                  # final voiced obs
                  'pad', 'zooz', 'sab', 'nag', 'aab', 'koz',
                  # final voiceless obs
                  'bop', 'taot', 'gaak', 'koas', 'oak', 'at',
                  # final continants
                  'dam', 'moon', 'doa', 'maa',
              ]),
              'q2': (['qf'], ['on', 'ka', 'bam', EPSILON])}


target_tuple = (target_hmm, [])

