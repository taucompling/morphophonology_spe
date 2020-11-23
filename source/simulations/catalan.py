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
"ADD_STATE": 1,
"REMOVE_STATE": 1,
"SPLIT_STATES": 1,
"ADD_TRANSITION": 1,
"REMOVE_TRANSITION": 1,
"ADD_SEGMENT_TO_EMISSION": 1,
"REMOVE_SEGMENT_FROM_EMISSION": 1,
"CHANGE_SEGMENT_IN_EMISSION": 1,
"ADD_EMISSION_TO_STATE": 1,
"REMOVE_EMISSION_FROM_STATE": 1,
"ADD_EPSILON_EMISSION_TO_STATE": 1,
"REMOVE_EPSILON_EMISSION_FROM_STATE": 1,

"DATA_ENCODING_LENGTH_MULTIPLIER": 10,
"ADD_EMISSION_FROM_DATA": 0,
"ADD_SEGMENT_BY_FEATURE_BUNDLE": 0,

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
"CHANGE_KLEENE_VALUE": 0,

"ADD_FEATURE": 1,
"REMOVE_FEATURE": 1,
"CHANGE_FEATURE_VALUE": 1,

"MAX_FEATURE_BUNDLE_IN_CONTEXT": 1,

"MAX_NUM_OF_INNER_STATES": 5,
"MIN_NUM_OF_INNER_STATES": 1,

"MAX_NUMBER_OF_RULES": 5,
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


segment_table_file_name = "catalan_segment_table.txt"

log_file_template = "{}_catalan_{}.txt"

data = ['armada', 'armadaa', 'armadaestr', 'armadaet', 'armadaik', 'armadas', 'ban', 'banka', 'bankestr', 'banket', 'bankik', 'banks', 'blan', 'blanka', 'blankestr', 'blanket', 'blankik', 'blanks', 'blau', 'blaua', 'blauestr', 'blauet', 'blauik', 'blaus', 'brut', 'bruta', 'brutestr', 'brutet', 'brutik', 'bruts', 'dolen', 'dolenta', 'dolentestr', 'dolentet', 'dolentik', 'dolents', 'elefan', 'elefanta', 'elefantestr', 'elefantet', 'elefantik', 'elefants', 'espageti', 'espagetia', 'espagetiestr', 'espagetiet', 'espagetiik', 'espagetis', 'espanol', 'espanola', 'espanolestr', 'espanolet', 'espanolik', 'espanols', 'fu', 'fuma', 'fumestr', 'fumet', 'fumik', 'fums', 'gra', 'grana', 'granestr', 'granet', 'granik', 'grans', 'gris', 'grisa', 'grisestr', 'griset', 'grisik', 'griss', 'kaima', 'kaimana', 'kaimanestr', 'kaimanet', 'kaimanik', 'kaimans', 'kalen', 'kalenta', 'kalentestr', 'kalentet', 'kalentik', 'kalents', 'kam', 'kampa', 'kampestr', 'kampet', 'kampik', 'kamps', 'kap', 'kapa', 'kapestr', 'kapet', 'kapik', 'kaps', 'katala', 'katalana', 'katalanestr', 'katalanet', 'katalanik', 'katalans', 'kuzi', 'kuzina', 'kuzinestr', 'kuzinet', 'kuzinik', 'kuzins', 'len', 'lenta', 'lentestr', 'lentet', 'lentik', 'lents', 'leo', 'leona', 'leonestr', 'leonet', 'leonik', 'leons', 'metal', 'metala', 'metalestr', 'metalet', 'metalik', 'metals', 'nasionalisme', 'nasionalismea', 'nasionalismeestr', 'nasionalismeet', 'nasionalismeik', 'nasionalismes', 'nebot', 'nebota', 'nebotestr', 'nebotet', 'nebotik', 'nebots', 'negre', 'negrea', 'negreestr', 'negreet', 'negreik', 'negres', 'pikan', 'pikanta', 'pikantestr', 'pikantet', 'pikantik', 'pikants', 'pla', 'plana', 'planestr', 'planet', 'planik', 'plans', 'plasa', 'plasaa', 'plasaestr', 'plasaet', 'plasaik', 'plasas', 'pri', 'prima', 'primestr', 'primet', 'primik', 'prims', 'profun', 'profunda', 'profundestr', 'profundet', 'profundik', 'profunds', 'sile', 'silena', 'silenestr', 'silenet', 'silenik', 'silens', 'telefo', 'telefona', 'telefonestr', 'telefonet', 'telefonik', 'telefons', 'tin', 'tinka', 'tinkestr', 'tinket', 'tinkik', 'tinks']

from fst import EPSILON

target_hmm = {'q0': ['q1'],
               'q1': (['q2'], ["blank", "kamp", "kalent", "profund", "dolent", "bank", "tink", "pikant", "elefant", "lent", "kuzin", "plan", "silen", "gran", "telefon", "katalan", "kaiman", "leon", "prim", "fum", "kap", "armada", "espanol", "metal", "plasa", "blau", "negre", "gris", "brut", "nebot", "espageti", "nasionalisme"]),
               'q2': (['qf'], ["a", "et", "s", "ik", "estr", EPSILON])
            }

nasal_deletion = [[{"nasal": "+"}], [], [], [{"WB": True}], True]
cluster_simplification = [[{"cont": "-"}], [], [{"nasal": "+"}], [{"WB": True}], True]

rule_set = [nasal_deletion, cluster_simplification]

target_tuple = (target_hmm, rule_set)
