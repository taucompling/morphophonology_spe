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
log_file_template = "{}_opacity_39M_{}.txt"

segment_table_file_name = "dag_zook_segments_new.txt"

data = ['ag', 'agdot', 'aggat', 'aggozka', 'agktas', 'agsaat', 'agtask', 'agtod', 'agtodadot', 'agtodasaat', 'agtodatask', 'agtodazoka', 'agtodgat', 'agtodgozka', 'agtodktas', 'agzoka', 'daot', 'daotasaat', 'daotasoka', 'daotatask', 'daotatot', 'daotkat', 'daotkozka', 'daotktas', 'dkaz', 'dkazadot', 'dkazasaat', 'dkazatask', 'dkazazoka', 'dkazgat', 'dkazgozka', 'dkazktas', 'dog', 'dogdot', 'doggat', 'doggozka', 'dogktas', 'dogsaat', 'dogtask', 'dogzoka', 'gdaas', 'gdaasasaat', 'gdaasasoka', 'gdaasatask', 'gdaasatot', 'gdaaskat', 'gdaaskozka', 'gdaasktas', 'gkas', 'gkasasaat', 'gkasasoka', 'gkasatask', 'gkasatot', 'gkaskat', 'gkaskozka', 'gkasktas', 'good', 'goodadot', 'goodasaat', 'goodatask', 'goodazoka', 'goodgat', 'goodgozka', 'goodktas', 'kaos', 'kaosasaat', 'kaosasoka', 'kaosatask', 'kaosatot', 'kaoskat', 'kaoskozka', 'kaosktas', 'kat', 'katasaat', 'katasoka', 'katatask', 'katatot', 'katkat', 'katkozka', 'katktas', 'koad', 'koadadot', 'koadasaat', 'koadatask', 'koadazoka', 'koadgat', 'koadgozka', 'koadktas', 'ksoag', 'ksoagdot', 'ksoaggat', 'ksoaggozka', 'ksoagktas', 'ksoagsaat', 'ksoagtask', 'ksoagzoka', 'oktado', 'oktadodot', 'oktadogat', 'oktadogozka', 'oktadoktas', 'oktadosaat', 'oktadotask', 'oktadozoka', 'osko', 'oskodot', 'oskogat', 'oskogozka', 'oskoktas', 'oskosaat', 'oskotask', 'oskozoka', 'ozka', 'ozkadot', 'ozkagat', 'ozkagozka', 'ozkaktas', 'ozkasaat', 'ozkatask', 'ozkazoka', 'saas', 'saasasaat', 'saasasoka', 'saasatask', 'saasatot', 'saaskat', 'saaskozka', 'saasktas', 'sak', 'sakkat', 'sakkozka', 'sakktas', 'saksaat', 'saksoka', 'saktask', 'saktot', 'skod', 'skodadot', 'skodasaat', 'skodatask', 'skodazoka', 'skodgat', 'skodgozka', 'skodktas', 'taso', 'tasodot', 'tasogat', 'tasogozka', 'tasoktas', 'tasosaat', 'tasotask', 'tasozoka', 'tok', 'tokkat', 'tokkozka', 'tokktas', 'toksaat', 'toksoka', 'toktask', 'toktot', 'toot', 'tootasaat', 'tootasoka', 'tootatask', 'tootatot', 'tootkat', 'tootkozka', 'tootktas', 'zook', 'zookkat', 'zookkozka', 'zookktas', 'zooksaat', 'zooksoka', 'zooktask', 'zooktot']


from fst import EPSILON

target_hmm = {'q0': ['q1'],
              'q1': (['q2'], ['sak', 'dog', 'kat', 'daot', 'good', 'gkas', 'dkaz', 'skod', 'gdaas', 'tok',
                              'ksoag', 'agtod', 'taso', 'kaos', 'oktado', 'koad', 'osko', 'ozka', 'ag',
                              'zook', 'saas', 'toot']),
              'q2': (['qf'], ['zoka', 'gat', 'dot', 'saat', 'tsk', 'gozka', 'ktas', EPSILON])}

assimilation_rule = [[{"cons": "+"}], [{"voice": "-"}], [{"voice": "-"}], [], True]
epenthesis_rule = [[], [{"low": "+"}], [{"coronal": "+"}], [{"coronal": "+"}], True]


target_tuple = (target_hmm, [assimilation_rule, epenthesis_rule])
