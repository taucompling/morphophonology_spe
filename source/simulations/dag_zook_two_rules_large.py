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

"MAX_NUM_OF_INNER_STATES": 4,
"MIN_NUM_OF_INNER_STATES": 1,

"MAX_NUMBER_OF_RULES": 4,
"MIN_NUMBER_OF_RULES": 0,

"MORPHEME_BOUNDARY_FLAG": False,
"LENGTHENING_FLAG": False,
"UNDERSPECIFICATION_FLAG": False,
"WORD_BOUNDARY_FLAG": False,
"RESTRICTIONS_ON_ALPHABET": False,

"CHECK_STALEMATE": False,
"INITIAL_TEMPERATURE": 75,
"THRESHOLD": 1,
"COOLING_RATE": 0.999999,
"DEBUG_LOGGING_INTERVAL": 200,
"CLEAR_MODULES_CACHING_INTERVAL": 1000,
"STEPS_LIMITATION": float("inf"),

"LINEAR_DECAY": False
}

#exponential
log_file_template = "{}_dag_zook_two_rules_large_{}.txt"

segment_table_file_name = "dag_zook_segments_new.txt"

data = ['ag', 'agdot', 'aggat', 'aggo', 'aggozka', 'agktas', 'agoad', 'agook', 'agsaat', 'agtask', 'agtod', 'agtodadot', 'agtodasaat', 'agtodatask', 'agtodazoka', 'agtodgat', 'agtodgo', 'agtodgozka', 'agtodktas', 'agtodoad', 'agtodook', 'agzoka', 'daot', 'daotadot', 'daotasaat', 'daotatask', 'daotazoka', 'daotkat', 'daotko', 'daotkozka', 'daotktas', 'daotoad', 'daotook', 'dkaz', 'dkazadot', 'dkazasaat', 'dkazatask', 'dkazazoka', 'dkazgat', 'dkazgo', 'dkazgozka', 'dkazktas', 'dkazoad', 'dkazook', 'dog', 'dogdot', 'doggat', 'doggo', 'doggozka', 'dogktas', 'dogoad', 'dogook', 'dogsaat', 'dogtask', 'dogzoka', 'gdaas', 'gdaasadot', 'gdaasasaat', 'gdaasatask', 'gdaasazoka', 'gdaaskat', 'gdaasko', 'gdaaskozka', 'gdaasktas', 'gdaasoad', 'gdaasook', 'gkas', 'gkasadot', 'gkasasaat', 'gkasatask', 'gkasazoka', 'gkaskat', 'gkasko', 'gkaskozka', 'gkasktas', 'gkasoad', 'gkasook', 'good', 'goodadot', 'goodasaat', 'goodatask', 'goodazoka', 'goodgat', 'goodgo', 'goodgozka', 'goodktas', 'goodoad', 'goodook', 'kaos', 'kaosadot', 'kaosasaat', 'kaosatask', 'kaosazoka', 'kaoskat', 'kaosko', 'kaoskozka', 'kaosktas', 'kaosoad', 'kaosook', 'kat', 'katadot', 'katasaat', 'katatask', 'katazoka', 'katkat', 'katko', 'katkozka', 'katktas', 'katoad', 'katook', 'koad', 'koadadot', 'koadasaat', 'koadatask', 'koadazoka', 'koadgat', 'koadgo', 'koadgozka', 'koadktas', 'koadoad', 'koadook', 'ksoag', 'ksoagdot', 'ksoaggat', 'ksoaggo', 'ksoaggozka', 'ksoagktas', 'ksoagoad', 'ksoagook', 'ksoagsaat', 'ksoagtask', 'ksoagzoka', 'oktado', 'oktadodot', 'oktadogat', 'oktadogo', 'oktadogozka', 'oktadoktas', 'oktadooad', 'oktadoook', 'oktadosaat', 'oktadotask', 'oktadozoka', 'osko', 'oskodot', 'oskogat', 'oskogo', 'oskogozka', 'oskoktas', 'oskooad', 'oskoook', 'oskosaat', 'oskotask', 'oskozoka', 'ozka', 'ozkadot', 'ozkagat', 'ozkago', 'ozkagozka', 'ozkaktas', 'ozkaoad', 'ozkaook', 'ozkasaat', 'ozkatask', 'ozkazoka', 'saas', 'saasadot', 'saasasaat', 'saasatask', 'saasazoka', 'saaskat', 'saasko', 'saaskozka', 'saasktas', 'saasoad', 'saasook', 'sak', 'sakkat', 'sakko', 'sakkozka', 'sakktas', 'sakoad', 'sakook', 'saksaat', 'saksoka', 'saktask', 'saktot', 'skod', 'skodadot', 'skodasaat', 'skodatask', 'skodazoka', 'skodgat', 'skodgo', 'skodgozka', 'skodktas', 'skodoad', 'skodook', 'taso', 'tasodot', 'tasogat', 'tasogo', 'tasogozka', 'tasoktas', 'tasooad', 'tasoook', 'tasosaat', 'tasotask', 'tasozoka', 'tok', 'tokkat', 'tokko', 'tokkozka', 'tokktas', 'tokoad', 'tokook', 'toksaat', 'toksoka', 'toktask', 'toktot', 'toot', 'tootadot', 'tootasaat', 'tootatask', 'tootazoka', 'tootkat', 'tootko', 'tootkozka', 'tootktas', 'tootoad', 'tootook', 'zook', 'zookkat', 'zookko', 'zookkozka', 'zookktas', 'zookoad', 'zookook', 'zooksaat', 'zooksoka', 'zooktask', 'zooktot']

from fst import EPSILON

target_hmm = {'q0': ['q1'],
              'q1': (['q2'], ['sak', 'dog', 'kat', 'daot', 'good', 'gkas', 'dkaz', 'skod', 'gdaas', 'tok',
                              'ksoag', 'agtod', 'taso', 'kaos', 'oktado', 'koad', 'osko', 'ozka', 'ag',
                              'zook', 'saas', 'toot']),
              'q2': (['qf'], ['zoka', 'gat', 'dot', 'saat', 'tsk', 'gozka', 'oad', 'ook', 'go', 'ktas', EPSILON])}

epenthesis_rule = [[], [{"low": "+"}], [{"coronal": "+"}], [{"coronal": "+"}], True]
assimilation_rule = [[{"cons": "+"}], [{"voice": "-"}], [{"voice": "-"}], [], True]


target_tuple = (target_hmm, [epenthesis_rule, assimilation_rule])
