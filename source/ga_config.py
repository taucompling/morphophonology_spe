from os import getenv
from math import floor

# Genetic Algorithm params

DEFAULT_CXPB_MUTPB = (0.2, 0.8, False)  # (crossover rate, mutation rate, VAR_AND / VAR_OR)

SELECTION_METHOD = 'rank'  # ['tournament', 'rank']
RANK_SELECTION_PRESSURE = 1.7  # Range: [1.1, 2.0]
TOURNAMENT_SIZE = 2

CROSSOVER_COOLING_RATE = 1.0
MUTATION_COOLING_RATE = 1.0

# Island Model

NUM_ISLANDS = int(getenv('SPE_NUM_ISLANDS', 3))
TOTAL_GENERATIONS = 50000
MIGRATION_INTERVAL = 50
ISLAND_POPULATION = 200
MIGRATION_RATIO = 0.1
ISLAND_ELITE_SIZE = floor(ISLAND_POPULATION * 0.05)
LAMBDA = floor(ISLAND_POPULATION / 0.8)  # denominator must be 1 or smaller
MIGRATION_SCHEME = 'round_robin'  # ['fixed', 'round_robin']

# Logging
LOGGER_ENVIRONMENT = 'local'  # ['aws', 'azure', 'local']
HALL_OF_FAME_HYPOTHESES = 1
HALL_OF_FAME_DEBUG_INTERVAL = 50
DUMP_ALL_POPULATION_EVERY_N_GENERATIONS = float("inf")
PROCESS_NAME_PREFIX = 'island'
LOG_NAME_PREFIX = 'genetic_log'
LOG_DEBUG_NAME_PREFIX = 'genetic_log_debug'
UPLOAD_ISLAND_RECORD_TO_S3_EVERY_N_GENERATIONS = 100
UPLOAD_LOG_TO_S3_EVERY_N_LINES = 1000

# Incest prevention

PREVENT_INCEST = False
INCEST_THRESHOLD = 300

# Crossover

CROSSOVER_BOTH_HMM_AND_RULES = False
CROSSOVER_HMM_WEIGHT = 1  # Weights for HMM/Rules crossover (in case CROSSOVER_BOTH_HMM_AND_RULES is False)
CROSSOVER_RULES_WEIGHT = 1

# Mutation

MUTATE_BOTH_HMM_AND_RULES = False
MAX_MUTATIONS = 1
RANDOM_HYPOTHESIS_BY_MUTATIONS = False
RANDOM_INIT_WARMUP_STEPS = 10000
ACCEPT_WORSE_PROBAB = 0.2
UNPARSABLE_WORD_PENALTY = 1000
UNPARSABLE_HYPOTHESIS_DISTANCE = 1000000

# Rule set

RULE_SET_CROSSOVER = 'uniform'  # ['uniform', 'pivot']

# HMM

HMM_CROSSOVER_FUNCTION = 'emissions'  # ['emissions', 'matrix', 'subgraph', 'connected_component']
LIMIT_CROSSOVER_RESULT_NUM_OF_STATES = True
MAX_CROSSOVERS = 1
RANDOM_HMM_MAX_EMISSION_LENGTH = 5
RANDOM_HMM_MAX_EMISSIONS_PER_STATE = 10
RANDOM_HMM_METHOD = 'simple'  # ['simple', 'matrix']
HMM_RANDOM_EMISSIONS_BY_DATA = False  # HMM random emissions will be substrings of data words
DEFAULT_HMM_BY_RANDOM_PROBAB = 0.0
EXPLICIT_HMM_BY_RANDOM_PROBAB = 0.0
TRANSITION_MATRIX_TRANSITION_PROBABILITY = 0.1

# Custom Genetic Algorithm params

CUSTOM_CXPB_MUTPB_VALUES_PER_ISLAND = []  # Add tuples in form (CXPB, MUTPB, VAR_AND/VAR_OR) to set custom config per island
CUSTOM_CONFIG_PER_ISLAND = {}  # Set simulation configuration fields for specific islands. E.g. for island 64: {64: {  "MUTATE_RULE_SET": 10, "MUTATE_HMM": 1 }}

# Misc

PARSER_TYPE = 'openfst'  # ['python', 'openfst']
LIMIT_TRANSDUCER_NUM_OF_STATES = 1000  # grammar transducers with too many states will return energy 'inf'
CACHE_TYPE = 'none'  # ['redis', 'mem', 'none']
CACHE_RULE_SET_TRANSDUCERS = False
CLEAR_RULE_SET_CACHE_INTERVAL = 100
