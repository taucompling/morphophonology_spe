simulation_number = 1
from fst import EPSILON


configurations_dict = \
{
    "MUTATE_RULE_SET": 1,
    "MUTATE_HMM": 1,

    "EVOLVE_RULES": True,
    "EVOLVE_HMM": True,

    "COMBINE_EMISSIONS": 1,
    "MERGE_EMISSIONS": 0,
    "ADVANCE_EMISSION": 1,
    "MOVE_EMISSION": 1,
    "CLONE_STATE": 0,
    "CLONE_EMISSION": 1,
    "SPLIT_EMISSION": 1,
    "ADD_STATE": 1,
    "REMOVE_STATE": 1,
    "MERGE_STATES": 0,
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

    "MAX_FEATURE_BUNDLE_IN_CONTEXT": 3,

    "MAX_NUM_OF_INNER_STATES": 3,
    "MIN_NUM_OF_INNER_STATES": 1,

    "MAX_NUMBER_OF_RULES": 3,
    "MIN_NUMBER_OF_RULES": 0,

    "MORPHEME_BOUNDARY_FLAG": False,
    "LENGTHENING_FLAG": False,
    "UNDERSPECIFICATION_FLAG": False,
    "WORD_BOUNDARY_FLAG": True,
    "RESTRICTIONS_ON_ALPHABET": False,

    # Genetic algorithm params

    "CROSSOVER_RATE": 0.1,
    "MUTATION_RATE": 0.9,
    "CROSSOVER_COOLING_RATE": 1.0,
    "MUTATION_COOLING_RATE": 1.0,
    "VAR_AND": False,
    "TOTAL_GENERATIONS": 100_000,
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
    "HMM_CROSSOVER_METHOD": "emissions", # ['emissions', 'matrix', 'subgraph', 'connected_component']"
    "LIMIT_CROSSOVER_RESULT_HMM_NUM_OF_STATES": True,
    "HMM_MAX_CROSSOVERS": 1,
    "RANDOM_HMM_MAX_EMISSION_LENGTH": 10,
    "RANDOM_HMM_MAX_EMISSIONS_PER_STATE": 15,
    "RANDOM_HMM_METHOD": 'simple',  # ['simple', 'matrix']
    "HMM_RANDOM_EMISSIONS_BY_DATA": True, # HMM random emissions will be substrings of data words
    "DEFAULT_HMM_BY_RANDOM_PROBAB": 0.0,
    "EXPLICIT_HMM_BY_RANDOM_PROBAB": 0.0,
    "TRANSITION_MATRIX_TRANSITION_PROBABILITY": 0.1,

    # Rule set
    "RULE_SET_CROSSOVER_METHOD": "unilateral", # ['unilateral', 'switch_pairs', 'pivot'],

    # Transducers
    "MINIMIZE_TRANSDUCER": False,
    "TRANSDUCER_STATES_LIMIT": 1000,
    "DFAS_STATES_LIMIT": 1000
}

segment_table_file_name = "finnish_two_rules.txt"

log_file_template = "{}_finnish_two_rules_{}.txt"

data = ['abs', 'absi', 'absias', 'absimpa', 'absiss', 'absissi', 'absist', 'absisti', 'absitten', 'absmainen', 'absn', 'absns', 'absnsi', 'absnt', 'absnti', 'absssa', 'essi', 'essii', 'essiias', 'essiimpa', 'essiiss', 'essiissi', 'essiist', 'essiisti', 'essiitten', 'essimainen', 'essin', 'essins', 'essinsi', 'essint', 'essinti', 'essissa', 'imes', 'imesi', 'imesias', 'imesimpa', 'imesiss', 'imesissi', 'imesist', 'imesisti', 'imesitten', 'imet', 'imeti', 'imetias', 'imetimpa', 'imetiss', 'imetissi', 'imetist', 'imetisti', 'imetitten', 'imetmainen', 'imetn', 'imetns', 'imetnsi', 'imetnt', 'imetnti', 'imetssa', 'mea', 'meai', 'meaias', 'meaimpa', 'meaiss', 'meaissi', 'meaist', 'meaisti', 'meaitten', 'meamainen', 'mean', 'means', 'meansi', 'meant', 'meanti', 'meassa', 'mens', 'mensi', 'mensias', 'mensimpa', 'mensiss', 'mensissi', 'mensist', 'mensisti', 'mensitten', 'ment', 'menti', 'mentias', 'mentimpa', 'mentiss', 'mentissi', 'mentist', 'mentisti', 'mentitten', 'mentmainen', 'mentn', 'mentns', 'mentnsi', 'mentnt', 'mentnti', 'mentssa', 'pans', 'pansi', 'pansias', 'pansimpa', 'pansiss', 'pansissi', 'pansist', 'pansisti', 'pansitten', 'pansmainen', 'pansn', 'pansns', 'pansnsi', 'pansnt', 'pansnti', 'pansssa', 'piis', 'piisi', 'piisias', 'piisimpa', 'piisiss', 'piisissi', 'piisist', 'piisisti', 'piisitten', 'piit', 'piiti', 'piitias', 'piitimpa', 'piitiss', 'piitissi', 'piitist', 'piitisti', 'piititten', 'piitmainen', 'piitn', 'piitns', 'piitnsi', 'piitnt', 'piitnti', 'piitssa', 'pitaa', 'pitaai', 'pitaaias', 'pitaaimpa', 'pitaaiss', 'pitaaissi', 'pitaaist', 'pitaaisti', 'pitaaitten', 'pitaamainen', 'pitaan', 'pitaans', 'pitaansi', 'pitaant', 'pitaanti', 'pitaassa', 'sam', 'sami', 'samias', 'samimpa', 'samiss', 'samissi', 'samist', 'samisti', 'samitten', 'sammainen', 'samn', 'samns', 'samnsi', 'samnt', 'samnti', 'samssa', 'siad', 'siadi', 'siadias', 'siadimpa', 'siadiss', 'siadissi', 'siadist', 'siadisti', 'siaditten', 'siadmainen', 'siadn', 'siadns', 'siadnsi', 'siadnt', 'siadnti', 'siadssa', 'sippas', 'sippasi', 'sippasias', 'sippasimpa', 'sippasiss', 'sippasissi', 'sippasist', 'sippasisti', 'sippasitten', 'sippat', 'sippati', 'sippatias', 'sippatimpa', 'sippatiss', 'sippatissi', 'sippatist', 'sippatisti', 'sippatitten', 'sippatmainen', 'sippatn', 'sippatns', 'sippatnsi', 'sippatnt', 'sippatnti', 'sippatssa', 'sippi', 'sippii', 'sippiias', 'sippiimpa', 'sippiiss', 'sippiissi', 'sippiist', 'sippiisti', 'sippiitten', 'sippimainen', 'sippin', 'sippins', 'sippinsi', 'sippint', 'sippinti', 'sippissa', 'tei', 'teii', 'teiias', 'teiimpa', 'teiiss', 'teiissi', 'teiist', 'teiisti', 'teiitten', 'teimainen', 'tein', 'teins', 'teinsi', 'teint', 'teinti', 'teissa', 'tiad', 'tiadi', 'tiadias', 'tiadimpa', 'tiadiss', 'tiadissi', 'tiadist', 'tiadisti', 'tiaditten', 'tiadmainen', 'tiadn', 'tiadns', 'tiadnsi', 'tiadnt', 'tiadnti', 'tiadssa']



target_hmm = {'q0': ['q1'],
              'q1': (['q2'],
                     ['ment', 'sippat', 'imet', 'piit', 'tiad', 'pans',
                      'pitaa', 'abs', 'mea', 'sam', 'tei', 'sippi', 'essi']),
              'q2': (['qf'],
                     ['i', 'impa', 'n', 'ssa', 'itten', 'ias', 'mainen',
                      'nti', 'isti'])}


t_frication = [[{"coronal": "+", "voice": '-'}], [{"cont": "+"}], [], [{"high": "+"}], False]

i_deletion = [[{"high": "+"}], [], [], [{"WB": True}], False]

rule_set = [t_frication, i_deletion]

target_tuple = (target_hmm, rule_set)