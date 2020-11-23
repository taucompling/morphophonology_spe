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
"MERGE_STATES": 0,
"SPLIT_STATES": 0,
"ADD_TRANSITION": 1,
"REMOVE_TRANSITION": 1,
"ADD_SEGMENT_TO_EMISSION": 1,
"REMOVE_SEGMENT_FROM_EMISSION": 1,
"CHANGE_SEGMENT_IN_EMISSION": 1,
"ADD_EMISSION_TO_STATE": 1,
"ADD_EMISSION_FROM_DATA": 0,
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

"MAX_FEATURE_BUNDLE_IN_CONTEXT": 1,

"MAX_NUM_OF_INNER_STATES": 4,
"MIN_NUM_OF_INNER_STATES": 1,

"MAX_NUMBER_OF_RULES": 3,
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
segment_table_file_name = "english_natural_segments.txt"

log_file_template = "{}_english_devoicing_{}.txt"



data = ['ameiz', 'ameizabl', 'ameizal', 'ameizans', 'ameizer', 'ameizi', 'ameizing', 'ameizion', 'ameizment', 'ameizz', 'analaiz', 'analaizabl', 'analaizal', 'analaizans', 'analaizer', 'analaizi', 'analaizing', 'analaizion', 'analaizment', 'analaizz', 'bang', 'bangabl', 'bangal', 'bangans', 'banger', 'bangi', 'banging', 'bangion', 'bangment', 'bangz', 'brag', 'bragabl', 'bragal', 'bragans', 'brager', 'bragi', 'braging', 'bragion', 'bragment', 'bragz', 'disturb', 'disturbabl', 'disturbal', 'disturbans', 'disturber', 'disturbi', 'disturbing', 'disturbion', 'disturbment', 'disturbz', 'drim', 'drimabl', 'drimal', 'drimans', 'drimer', 'drimi', 'driming', 'drimion', 'drimment', 'drimz', 'drink', 'drinkabl', 'drinkal', 'drinkans', 'drinker', 'drinki', 'drinking', 'drinkion', 'drinkment', 'drinks', 'glu', 'gluabl', 'glual', 'gluans', 'gluer', 'glui', 'gluing', 'gluion', 'glument', 'gluz', 'klaimb', 'klaimbabl', 'klaimbal', 'klaimbans', 'klaimber', 'klaimbi', 'klaimbing', 'klaimbion', 'klaimbment', 'klaimbz', 'klin', 'klinabl', 'klinal', 'klinans', 'kliner', 'klini', 'klining', 'klinion', 'klinment', 'klinz', 'komit', 'komitabl', 'komital', 'komitans', 'komiter', 'komiti', 'komiting', 'komition', 'komitment', 'komits', 'konsider', 'konsiderabl', 'konsideral', 'konsiderans', 'konsiderer', 'konsideri', 'konsidering', 'konsiderion', 'konsiderment', 'konsiderz', 'kontrol', 'kontrolabl', 'kontrolal', 'kontrolans', 'kontroler', 'kontroli', 'kontroling', 'kontrolion', 'kontrolment', 'kontrolz', 'kros', 'krosabl', 'krosal', 'krosans', 'kroser', 'krosi', 'krosing', 'krosion', 'krosment', 'kross', 'park', 'parkabl', 'parkal', 'parkans', 'parker', 'parki', 'parking', 'parkion', 'parkment', 'parks', 'pleis', 'pleisabl', 'pleisal', 'pleisans', 'pleiser', 'pleisi', 'pleising', 'pleision', 'pleisment', 'pleiss', 'raid', 'raidabl', 'raidal', 'raidans', 'raider', 'raidi', 'raiding', 'raidion', 'raidment', 'raidz', 'rent', 'rentabl', 'rental', 'rentans', 'renter', 'renti', 'renting', 'rention', 'rentment', 'rents', 'ski', 'skiabl', 'skial', 'skians', 'skier', 'skii', 'skiing', 'skiion', 'skiment', 'skiz', 'slip', 'slipabl', 'slipal', 'slipans', 'sliper', 'slipi', 'sliping', 'slipion', 'slipment', 'slips', 'spil', 'spilabl', 'spilal', 'spilans', 'spiler', 'spili', 'spiling', 'spilion', 'spilment', 'spilz', 'straik', 'straikabl', 'straikal', 'straikans', 'straiker', 'straiki', 'straiking', 'straikion', 'straikment', 'straiks', 'strap', 'strapabl', 'strapal', 'strapans', 'straper', 'strapi', 'straping', 'strapion', 'strapment', 'straps', 'teik', 'teikabl', 'teikal', 'teikans', 'teiker', 'teiki', 'teiking', 'teikion', 'teikment', 'teiks', 'triger', 'trigerabl', 'trigeral', 'trigerans', 'trigerer', 'trigeri', 'trigering', 'trigerion', 'trigerment', 'trigerz']


words_to_remove = ['straikans', 'klaimbabl', 'analaizer', 'pleisal', 'drinkion']
for word in words_to_remove:
    data.remove(word)

from fst import EPSILON

target_hmm = {'q0': ['q1'], 'q1': (['q2'],
                                   ['rent', 'komit', 'straik', 'drink', 'park', 'teik', 'strap', 'slip', 'kros',
                                    'pleis', 'ameiz', 'analaiz', 'klin', 'kontrol', 'glu', 'ski', 'spil', 'raid',
                                    'bang', 'brag', 'klaimb', 'disturb', 'konsider', 'triger', 'drim']),
              'q2': (['qf'], ['z', 'i', 'ing', 'al', 'er', 'ans', 'abl', 'ment', 'ion', EPSILON])}

assimilation_rule = [[{"son": "-"}], [{"voice": "-"}], [{"voice": "-"}], [], True]

initial_hmm = {'q0': ['q1'],
              'q1': (['qf'], data[:])
             }

target_tuple = (target_hmm, [assimilation_rule])

