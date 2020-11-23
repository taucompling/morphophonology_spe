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
"ADD_STATE": 1,
"REMOVE_STATE": 1,
"MERGE_STATES": 0,
"SPLIT_STATES": 0,
"ADD_TRANSITION": 1,
"REMOVE_TRANSITION": 1,
"ADD_SEGMENT_TO_EMISSION": 5,
"REMOVE_SEGMENT_FROM_EMISSION": 5,
"CHANGE_SEGMENT_IN_EMISSION": 5,
"ADD_EMISSION_TO_STATE": 5,
"ADD_EMISSION_FROM_DATA": 0,
"REMOVE_EMISSION_FROM_STATE": 5,

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
log_file_template = "{}_opacity_39M_{}.txt"

segment_table_file_name = "dag_zook_segments_new.txt"

data = ['ag', 'agdot', 'aggat', 'aggo', 'agkook', 'agkozka', 'agoad', 'agsaat', 'agtask', 'agtod', 'agtodadot', 'agtodasaat', 'agtodatask', 'agtodazoka', 'agtodgat', 'agtodgo', 'agtodkook', 'agtodkozka', 'agtodoad', 'agzoka', 'daot', 'daotasaat', 'daotasoka', 'daotatask', 'daotatot', 'daotkat', 'daotko', 'daotkook', 'daotkozka', 'daotoad', 'dkaz', 'dkazadot', 'dkazasaat', 'dkazatask', 'dkazazoka', 'dkazgat', 'dkazgo', 'dkazkook', 'dkazkozka', 'dkazoad', 'dog', 'dogdot', 'doggat', 'doggo', 'dogkook', 'dogkozka', 'dogoad', 'dogsaat', 'dogtask', 'dogzoka', 'gdaas', 'gdaasasaat', 'gdaasasoka', 'gdaasatask', 'gdaasatot', 'gdaaskat', 'gdaasko', 'gdaaskook', 'gdaaskozka', 'gdaasoad', 'gkas', 'gkasasaat', 'gkasasoka', 'gkasatask', 'gkasatot', 'gkaskat', 'gkasko', 'gkaskook', 'gkaskozka', 'gkasoad', 'good', 'goodadot', 'goodasaat', 'goodatask', 'goodazoka', 'goodgat', 'goodgo', 'goodkook', 'goodkozka', 'goodoad', 'kaos', 'kaosasaat', 'kaosasoka', 'kaosatask', 'kaosatot', 'kaoskat', 'kaosko', 'kaoskook', 'kaoskozka', 'kaosoad', 'kat', 'katasaat', 'katasoka', 'katatask', 'katatot', 'katkat', 'katko', 'katkook', 'katkozka', 'katoad', 'koad', 'koadadot', 'koadasaat', 'koadatask', 'koadazoka', 'koadgat', 'koadgo', 'koadkook', 'koadkozka', 'koadoad', 'ksoag', 'ksoagdot', 'ksoaggat', 'ksoaggo', 'ksoagkook', 'ksoagkozka', 'ksoagoad', 'ksoagsaat', 'ksoagtask', 'ksoagzoka', 'oktado', 'oktadodot', 'oktadogat', 'oktadogo', 'oktadokook', 'oktadokozka', 'oktadooad', 'oktadosaat', 'oktadotask', 'oktadozoka', 'osko', 'oskodot', 'oskogat', 'oskogo', 'oskokook', 'oskokozka', 'oskooad', 'oskosaat', 'oskotask', 'oskozoka', 'ozka', 'ozkadot', 'ozkagat', 'ozkago', 'ozkakook', 'ozkakozka', 'ozkaoad', 'ozkasaat', 'ozkatask', 'ozkazoka', 'saas', 'saasasaat', 'saasasoka', 'saasatask', 'saasatot', 'saaskat', 'saasko', 'saaskook', 'saaskozka', 'saasoad', 'sak', 'sakkat', 'sakko', 'sakkook', 'sakkozka', 'sakoad', 'saksaat', 'saksoka', 'saktask', 'saktot', 'skod', 'skodadot', 'skodasaat', 'skodatask', 'skodazoka', 'skodgat', 'skodgo', 'skodkook', 'skodkozka', 'skodoad', 'taso', 'tasodot', 'tasogat', 'tasogo', 'tasokook', 'tasokozka', 'tasooad', 'tasosaat', 'tasotask', 'tasozoka', 'tok', 'tokkat', 'tokko', 'tokkook', 'tokkozka', 'tokoad', 'toksaat', 'toksoka', 'toktask', 'toktot', 'toot', 'tootasaat', 'tootasoka', 'tootatask', 'tootatot', 'tootkat', 'tootko', 'tootkook', 'tootkozka', 'tootoad', 'zook', 'zookkat', 'zookko', 'zookkook', 'zookkozka', 'zookoad', 'zooksaat', 'zooksoka', 'zooktask', 'zooktot']

from fst import EPSILON

target_hmm = {'q0': ['q1'],
              'q1': (['q2'], ['sak', 'dog', 'kat', 'daot', 'good', 'gkas', 'dkaz', 'skod', 'gdaas', 'tok', 'ksoag', 'agtod', 'taso', 'kaos', 'oktado', 'koad', 'osko', 'ozka', 'ag', 'zook','saas', 'toot']),
              'q2': (['qf'], ['zoka', 'gat', 'dot', 'saat', 'task', 'kozka', 'oad', 'kook', 'go', EPSILON])}

assimilation_rule = [[{"cons": "+"}], [{"voice": "-"}], [{"voice": "-"}], [], True]
epenthesis_rule = [[], [{"low": "+"}], [{"coronal": "+"}], [{"coronal": "+"}], True]


target_tuple = (target_hmm, [assimilation_rule, epenthesis_rule])
