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
"ADD_SEGMENT_TO_EMISSION": 1,
"REMOVE_SEGMENT_FROM_EMISSION": 1,
"CHANGE_SEGMENT_IN_EMISSION": 1,
"ADD_EMISSION_TO_STATE": 1,
"ADD_EMISSION_FROM_DATA": 0,
"REMOVE_EMISSION_FROM_STATE": 1,

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

"ADD_FEATURE_BUNDLE": 1,
"REMOVE_FEATURE_BUNDLE": 1,
"CHANGE_EXISTING_FEATURE_BUNDLE": 1,

"ADD_FEATURE": 1,
"REMOVE_FEATURE": 1,
"CHANGE_FEATURE_VALUE": 1,
"CHANGE_KLEENE_VALUE": 0,

"MAX_FEATURE_BUNDLE_IN_CONTEXT": 1,

"MAX_NUM_OF_INNER_STATES": 5,
"MIN_NUM_OF_INNER_STATES": 1,

"MAX_NUMBER_OF_RULES": 3,
"MIN_NUMBER_OF_RULES": 0,

"MORPHEME_BOUNDARY_FLAG": False,
"LENGTHENING_FLAG": False,
"WORD_BOUNDARY_FLAG": False,
"UNDERSPECIFICATION_FLAG": False,
"RESTRICTIONS_ON_ALPHABET": False,

"CHECK_STALEMATE": False,
"INITIAL_TEMPERATURE": 75,
"THRESHOLD": 10**-2,
"COOLING_RATE": 0.9999999,
"DEBUG_LOGGING_INTERVAL": 200,
"CLEAR_MODULES_CACHING_INTERVAL": 1000,
"STEPS_LIMITATION": float('inf'),
"LINEAR_DECAY": False,

"ARITHMETIC_ENCODING_ESTIMATE": True,
"PRINT_PARSE": False
}
segment_table_file_name = "dag_zook_segments_new.txt"

log_file_template = "{}_dag_zook_devoicing_large_{}.txt"



data = ['ag', 'agdot', 'aggat', 'aggo', 'aggozka', 'agktas', 'agoad', 'agook', 'agsaat', 'agtod', 'agtoddot', 'agtodgat', 'agtodgo', 'agtodgozka', 'agtodktas', 'agtodoad', 'agtodook', 'agtodsaat', 'agtodtsk', 'agtodzoka', 'agtsk', 'agzoka', 'daot', 'daotkat', 'daotko', 'daotkozka', 'daotktas', 'daotoad', 'daotook', 'daotsaat', 'daotsoka', 'daottot', 'daottsk', 'dkaz', 'dkazdot', 'dkazgat', 'dkazgo', 'dkazgozka', 'dkazktas', 'dkazoad', 'dkazook', 'dkazsaat', 'dkaztsk', 'dkazzoka', 'dog', 'dogdot', 'doggat', 'doggo', 'doggozka', 'dogktas', 'dogoad', 'dogook', 'dogsaat', 'dogtsk', 'dogzoka', 'gdaas', 'gdaaskat', 'gdaasko', 'gdaaskozka', 'gdaasktas', 'gdaasoad', 'gdaasook', 'gdaassaat', 'gdaassoka', 'gdaastot', 'gdaastsk', 'gkas', 'gkaskat', 'gkasko', 'gkaskozka', 'gkasktas', 'gkasoad', 'gkasook', 'gkassaat', 'gkassoka', 'gkastot', 'gkastsk', 'good', 'gooddot', 'goodgat', 'goodgo', 'goodgozka', 'goodktas', 'goodoad', 'goodook', 'goodsaat', 'goodtsk', 'goodzoka', 'kaos', 'kaoskat', 'kaosko', 'kaoskozka', 'kaosktas', 'kaosoad', 'kaosook', 'kaossaat', 'kaossoka', 'kaostot', 'kaostsk', 'kat', 'katkat', 'katko', 'katkozka', 'katktas', 'katoad', 'katook', 'katsaat', 'katsoka', 'kattot', 'kattsk', 'koad', 'koaddot', 'koadgat', 'koadgo', 'koadgozka', 'koadktas', 'koadoad', 'koadook', 'koadsaat', 'koadtsk', 'koadzoka', 'ksoag', 'ksoagdot', 'ksoaggat', 'ksoaggo', 'ksoaggozka', 'ksoagktas', 'ksoagoad', 'ksoagook', 'ksoagsaat', 'ksoagtsk', 'ksoagzoka', 'oktado', 'oktadodot', 'oktadogat', 'oktadogo', 'oktadogozka', 'oktadoktas', 'oktadooad', 'oktadoook', 'oktadosaat', 'oktadotsk', 'oktadozoka', 'osko', 'oskodot', 'oskogat', 'oskogo', 'oskogozka', 'oskoktas', 'oskooad', 'oskoook', 'oskosaat', 'oskotsk', 'oskozoka', 'ozka', 'ozkadot', 'ozkagat', 'ozkago', 'ozkagozka', 'ozkaktas', 'ozkaoad', 'ozkaook', 'ozkasaat', 'ozkatsk', 'ozkazoka', 'saas', 'saaskat', 'saasko', 'saaskozka', 'saasktas', 'saasoad', 'saasook', 'saassaat', 'saassoka', 'saastot', 'saastsk', 'sak', 'sakkat', 'sakko', 'sakkozka', 'sakktas', 'sakoad', 'sakook', 'saksaat', 'saksoka', 'saktot', 'saktsk', 'skod', 'skoddot', 'skodgat', 'skodgo', 'skodgozka', 'skodktas', 'skodoad', 'skodook', 'skodsaat', 'skodtsk', 'skodzoka', 'taso', 'tasodot', 'tasogat', 'tasogo', 'tasogozka', 'tasoktas', 'tasooad', 'tasoook', 'tasosaat', 'tasotsk', 'tasozoka', 'tok', 'tokkat', 'tokko', 'tokkozka', 'tokktas', 'tokoad', 'tokook', 'toksaat', 'toksoka', 'toktot', 'toktsk', 'toot', 'tootkat', 'tootko', 'tootkozka', 'tootktas', 'tootoad', 'tootook', 'tootsaat', 'tootsoka', 'toottot', 'toottsk', 'zook', 'zookkat', 'zookko', 'zookkozka', 'zookktas', 'zookoad', 'zookook', 'zooksaat', 'zooksoka', 'zooktot', 'zooktsk']


from fst import EPSILON

target_hmm = {'q0': ['q1'],
              'q1': (['q2'], ['sak', 'dog', 'kat', 'daot', 'good', 'gkas', 'dkaz', 'skod', 'gdaas', 'tok',
                              'ksoag', 'agtod', 'taso', 'kaos', 'oktado', 'koad', 'osko', 'ozka', 'ag',
                              'zook', 'saas', 'toot']),
              'q2': (['qf'], ['zoka', 'gat', 'dot', 'saat', 'tsk', 'gozka', 'oad', 'ook', 'go', 'ktas', EPSILON])}

assimilation_rule = [[{"cons": "+"}], [{"voice": "-"}], [{"voice": "-"}], [], True]


target_tuple = (target_hmm, [assimilation_rule])

