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
"ADD_STATE": 1,
"REMOVE_STATE": 1,
"MERGE_STATES": 1,
"SPLIT_STATES": 1,
"ADD_TRANSITION": 1,
"REMOVE_TRANSITION": 1,
"ADD_SEGMENT_TO_EMISSION": 5,
"REMOVE_SEGMENT_FROM_EMISSION": 5,
"CHANGE_SEGMENT_IN_EMISSION": 5,
"ADD_EMISSION_TO_STATE": 5,
"ADD_EMISSION_FROM_DATA": 0,
"REMOVE_EMISSION_FROM_STATE": 5,

"DATA_ENCODING_LENGTH_MULTIPLIER": 25,
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

"MAX_NUM_OF_INNER_STATES": 4,
"MIN_NUM_OF_INNER_STATES": 1,

"MAX_NUMBER_OF_RULES": 4,
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

#exponential
log_file_template = "{}_dag_zook_two_rules_new_{}.txt"

segment_table_file_name = "dag_zook_segments_new.txt"

data = ['daot', 'daotada', 'daotasaat', 'daotatask', 'daotazoka', 'daotkazka', 'daotko', 'dkoz', 'dkozada', 'dkozasaat', 'dkozatask', 'dkozazoka', 'dkozgo', 'dkozkazka', 'dog', 'dogda', 'doggo', 'dogkazka', 'dogsaat', 'dogtask', 'dogzoka', 'dok', 'dokkazka', 'dokko', 'doksaat', 'doksoka', 'dokta', 'doktask', 'gdaas', 'gdaasada', 'gdaasasaat', 'gdaasatask', 'gdaasazoka', 'gdaaskazka', 'gdaasko', 'gkas', 'gkasada', 'gkasasaat', 'gkasatask', 'gkasazoka', 'gkaskazka', 'gkasko', 'kaos', 'kaosada', 'kaosasaat', 'kaosatask', 'kaosazoka', 'kaoskazka', 'kaosko', 'kat', 'katada', 'katasaat', 'katatask', 'katazoka', 'katkazka', 'katko', 'kood', 'koodada', 'koodasaat', 'koodatask', 'koodazoka', 'koodgo', 'koodkazka', 'ksoag', 'ksoagda', 'ksoaggo', 'ksoagkazka', 'ksoagsaat', 'ksoagtask', 'ksoagzoka', 'ogtad', 'ogtadada', 'ogtadasaat', 'ogtadatask', 'ogtadazoka', 'ogtadgo', 'ogtadkazka', 'oktado', 'oktadoda', 'oktadogo', 'oktadokazka', 'oktadosaat', 'oktadotask', 'oktadozoka', 'skaz', 'skazada', 'skazasaat', 'skazatask', 'skazazoka', 'skazgo', 'skazkazka', 'tak', 'takkazka', 'takko', 'taksaat', 'taksoka', 'takta', 'taktask', 'taso', 'tasoda', 'tasogo', 'tasokazka', 'tasosaat', 'tasotask', 'tasozoka']

from fst import EPSILON

target_hmm = {'q0': ['q1'],
              'q1': (['q2'],  ['tak', 'dog', 'kat', 'daot', 'kood', 'gkas', 'dkoz', 'skaz', 'gdaas', 'dok', 'ksoag', 'ogtad', 'taso', 'kaos', 'oktado']),
              'q2': (['qf'], ['zoka', 'go', 'da', 'saat', 'task', 'kazka', EPSILON])}

epenthesis_rule = [[], [{"low": "+"}], [{"coronal": "+"}], [{"coronal": "+"}], True]
assimilation_rule = [[{"cons": "+"}], [{"voice": "-"}], [{"voice": "-"}], [], True]


target_tuple = (target_hmm, [epenthesis_rule, assimilation_rule])
