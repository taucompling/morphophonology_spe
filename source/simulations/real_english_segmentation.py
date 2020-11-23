simulation_number = 1
configurations_dict = \
{
"MUTATE_RULE_SET": 0,
"MUTATE_HMM": 1,


"COMBINE_EMISSIONS": 1,
"ADVANCE_EMISSION": 1,
"CLONE_STATE": 0,
"CLONE_EMISSION": 1,
"ADD_STATE": 1,
"REMOVE_STATE": 1,
"ADD_TRANSITION": 1,
"REMOVE_TRANSITION": 1,
"ADD_SEGMENT_TO_EMISSION": 5,
"REMOVE_SEGMENT_FROM_EMISSION": 5,
"CHANGE_SEGMENT_IN_EMISSION": 5,
"ADD_EMISSION_TO_STATE": 5,
"REMOVE_EMISSION_FROM_STATE": 5,

"DATA_ENCODING_LENGTH_MULTIPLIER": 10,
"HMM_ENCODING_LENGTH_MULTIPLIER": 1,
"RULES_SET_ENCODING_LENGTH_MULTIPLIER": 1,

"ADD_RULE": 0,
"REMOVE_RULE": 0,
"DEMOTE_RULE": 0,
"CHANGE_RULE": 0,

"MUTATE_TARGET": 0,
"MUTATE_CHANGE": 0,
"MUTATE_LEFT_CONTEXT": 0,
"MUTATE_RIGHT_CONTEXT": 0,
"MUTATE_OBLIGATORY": 0,

"ADD_FEATURE_BUNDLE": 0,
"REMOVE_FEATURE_BUNDLE": 0,
"CHANGE_EXISTING_FEATURE_BUNDLE": 0,

"ADD_FEATURE": 0,
"REMOVE_FEATURE": 0,
"CHANGE_FEATURE_VALUE": 0,

"MAX_FEATURE_BUNDLE_IN_CONTEXT": 1,

"MAX_NUM_OF_INNER_STATES": 5,
"MIN_NUM_OF_INNER_STATES": 1,

"MAX_NUMBER_OF_RULES": 4,
"MIN_NUMBER_OF_RULES": 0,

"WORD_BOUNDARY_FLAG": False,
"CEIL_LOG2": False,
"MORPHEME_BOUNDARY_FLAG": False,
"LENGTHENING_FLAG": False,
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

segment_table_file_name = "real_english_segmentation_segment_table.txt"

log_file_template = "{}_real_english_segmentation_double_temperature_{}.txt"

data = ['abberation', 'abberations', 'abbreviate', 'abbreviated', 'abbreviates', 'abolitionist', 'abolitionists', 'abortion', 'abortions', 'absence', 'absences', 'abstractionist', 'abstractionists', 'abutment', 'abutments', 'accent', 'accented', 'accenting', 'accents', 'acclaim', 'acclaimed', 'acclaims', 'accolade', 'accolades', 'accommodate', 'accommodated', 'accommodates', 'accommodation', 'accommodations', 'accomodation', 'accomodations', 'achieve', 'achieved', 'achieves', 'achieving', 'add', 'added', 'adding', 'adds', 'administer', 'administered', 'administering', 'administers', 'advertise', 'advertised', 'advertiser', 'advertises', 'advertising', 'afford', 'afforded', 'affording', 'affords', 'aggravate', 'aggravated', 'aggravates', 'alert', 'alerted', 'alerting', 'alerts', 'amount', 'amounted', 'amounting', 'amounts', 'announce', 'announced', 'announcer', 'announces', 'announcing', 'appeal', 'appealed', 'appealing', 'appeals', 'applaud', 'applauded', 'applauding', 'apprentice', 'apprenticed', 'apprentices', 'arcade', 'arcaded', 'arcades', 'arrest', 'arrested', 'arresting', 'assault', 'assaulted', 'assaulting', 'assaults', 'assume', 'assumed', 'assumes', 'assuming', 'astound', 'astounded', 'astounding', 'attack', 'attacked', 'attacker', 'attacking', 'attacks', 'attempt', 'attempted', 'attempting', 'attempts', 'back', 'backed', 'backer', 'backing', 'backs', 'bake', 'baked', 'baker', 'bakes', 'baking', 'balance', 'balanced', 'balances', 'barbecue', 'barbecued', 'barbecues', 'bath', 'bathed', 'bather', 'bathing', 'baths', 'beckon', 'beckoned', 'beckons', 'benefit', 'benefited', 'benefits', 'blast', 'blasted', 'blasting', 'blend', 'blended', 'blends', 'bless', 'blessed', 'blessing', 'blister', 'blistered', 'blisters', 'bloom', 'bloomed', 'blooming', 'blow', 'blower', 'blowing', 'blows', 'boast', 'boasted', 'boasting', 'bogey', 'bogeyed', 'bogeys', 'boil', 'boiled', 'boiler', 'boiling', 'boils', 'bolster', 'bolstered', 'bolstering', 'bomb', 'bomber', 'bombing', 'bombs', 'borrow', 'borrowed', 'borrower', 'borrowing', 'borrows', 'bother', 'bothered', 'bothers', 'brace', 'braced', 'braces', 'bracing', 'breakfast', 'breakfasted', 'breakfasts', 'broadcast', 'broadcaster', 'broadcasting', 'broadcasts', 'broaden', 'broadened', 'broadening', 'bruise', 'bruised', 'bruises', 'buffet', 'buffeted', 'buffets', 'burden', 'burdened', 'burdens', 'catalogue', 'catalogued', 'catalogues', 'cater', 'catered', 'catering', 'challenge', 'challenged', 'challenger', 'challenges', 'challenging', 'change', 'changed', 'changes', 'changing', 'charge', 'charged', 'charges', 'charging', 'charm', 'charmed', 'charmer', 'charming', 'charms', 'comprise', 'comprised', 'comprises', 'comprising', 'concede', 'conceded', 'concedes', 'conceding', 'conclude', 'concluded', 'concludes', 'concluding', 'condition', 'conditioned', 'conditioner', 'conditioning', 'conditions', 'consume', 'consumed', 'consumer', 'consumes', 'consuming', 'costume', 'costumed', 'costumes', 'deal', 'dealer', 'dealing', 'deals', 'decide', 'decided', 'decides', 'deciding', 'demand', 'demanded', 'demander', 'demanding', 'demands', 'describe', 'described', 'describes', 'describing', 'down', 'downed', 'downer', 'downing', 'downs', 'draw', 'drawer', 'drawing', 'draws', 'drink', 'drinker', 'drinking', 'drinks', 'dwell', 'dweller', 'dwelling', 'dwells', 'enforce', 'enforced', 'enforcer', 'enforces', 'enforcing', 'farm', 'farmer', 'farming', 'farms', 'feed', 'feeder', 'feeding', 'feeds', 'feel', 'feeler', 'feeling', 'feels', 'flow', 'flowed', 'flower', 'flowing', 'flows', 'gaze', 'gazed', 'gazer', 'gazes', 'gazing', 'glaze', 'glazed', 'glazer', 'glazes', 'glazing', 'invade', 'invaded', 'invader', 'invades', 'invading', 'live', 'lived', 'liver', 'lives', 'living', 'pace', 'paced', 'pacer', 'paces', 'pacing']

target_hmm = {'q0': ['q1'],
            'q1': (['q2','qf'], ['abberation', 'abbreviate', 'abolitionist', 'abortion', 'absence', 'abstractionist', 'abutment', 'accent', 'acclaim', 'accolade', 'accommodate', 'accommodation', 'accomodation', 'achiev', 'add', 'administer', 'advertis', 'afford', 'aggravate', 'alert', 'amount', 'announc', 'appeal', 'applaud', 'apprentice', 'arcade', 'arrest', 'assault', 'assum', 'astound', 'attack', 'attempt', 'back', 'bak', 'balance', 'barbecue', 'bath', 'beckon', 'benefit', 'blast', 'blend', 'bless', 'blister', 'bloom', 'blow', 'boast', 'bogey', 'boil', 'bolster', 'bomb', 'borrow', 'bother', 'brac', 'breakfast', 'broadcast', 'broaden', 'bruise', 'buffet', 'burden', 'catalogue', 'cater', 'challeng', 'chang', 'charg', 'charm', 'compris', 'conced', 'conclud', 'condition', 'consum', 'costume', 'deal', 'decid', 'demand', 'describ', 'down', 'draw', 'drink', 'dwell', 'enforc', 'farm', 'feed', 'feel', 'flow', 'gaz', 'glaz', 'invad', 'liv', 'pac']),
            'q2': (['qf'], ['ing', 'e', 'd', 'ed', 's', 'es', 'er'])
              }


target_tuple = (target_hmm, [])

