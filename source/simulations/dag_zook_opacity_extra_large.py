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

data = ['ag', 'agdaatas', 'agdot', 'aggas', 'aggat', 'aggo', 'aggozka', 'agktas', 'agoad', 'agook', 'agsaat', 'agtask', 'agtatko', 'agtod', 'agtodadaatas', 'agtodadot', 'agtodasaat', 'agtodatask', 'agtodatatko', 'agtodazoka', 'agtodgas', 'agtodgat', 'agtodgo', 'agtodgozka', 'agtodktas', 'agtodoad', 'agtodook', 'agzoka', 'daot', 'daotasaat', 'daotasoka', 'daotataatas', 'daotatask', 'daotatatko', 'daotatot', 'daotkas', 'daotkat', 'daotko', 'daotkozka', 'daotktas', 'daotoad', 'daotook', 'dkaz', 'dkazadaatas', 'dkazadot', 'dkazasaat', 'dkazatask', 'dkazatatko', 'dkazazoka', 'dkazgas', 'dkazgat', 'dkazgo', 'dkazgozka', 'dkazktas', 'dkazoad', 'dkazook', 'dog', 'dogdaatas', 'dogdot', 'doggas', 'doggat', 'doggo', 'doggozka', 'dogktas', 'dogoad', 'dogook', 'dogsaat', 'dogtask', 'dogtatko', 'dogzoka', 'gdaas', 'gdaasasaat', 'gdaasasoka', 'gdaasataatas', 'gdaasatask', 'gdaasatatko', 'gdaasatot', 'gdaaskas', 'gdaaskat', 'gdaasko', 'gdaaskozka', 'gdaasktas', 'gdaasoad', 'gdaasook', 'gkas', 'gkasasaat', 'gkasasoka', 'gkasataatas', 'gkasatask', 'gkasatatko', 'gkasatot', 'gkaskas', 'gkaskat', 'gkasko', 'gkaskozka', 'gkasktas', 'gkasoad', 'gkasook', 'good', 'goodadaatas', 'goodadot', 'goodasaat', 'goodatask', 'goodatatko', 'goodazoka', 'goodgas', 'goodgat', 'goodgo', 'goodgozka', 'goodktas', 'goodoad', 'goodook', 'kaos', 'kaosasaat', 'kaosasoka', 'kaosataatas', 'kaosatask', 'kaosatatko', 'kaosatot', 'kaoskas', 'kaoskat', 'kaosko', 'kaoskozka', 'kaosktas', 'kaosoad', 'kaosook', 'kat', 'katasaat', 'katasoka', 'katataatas', 'katatask', 'katatatko', 'katatot', 'katkas', 'katkat', 'katko', 'katkozka', 'katktas', 'katoad', 'katook', 'koad', 'koadadaatas', 'koadadot', 'koadasaat', 'koadatask', 'koadatatko', 'koadazoka', 'koadgas', 'koadgat', 'koadgo', 'koadgozka', 'koadktas', 'koadoad', 'koadook', 'ksoag', 'ksoagdaatas', 'ksoagdot', 'ksoaggas', 'ksoaggat', 'ksoaggo', 'ksoaggozka', 'ksoagktas', 'ksoagoad', 'ksoagook', 'ksoagsaat', 'ksoagtask', 'ksoagtatko', 'ksoagzoka', 'oktado', 'oktadodaatas', 'oktadodot', 'oktadogas', 'oktadogat', 'oktadogo', 'oktadogozka', 'oktadoktas', 'oktadooad', 'oktadoook', 'oktadosaat', 'oktadotask', 'oktadotatko', 'oktadozoka', 'osko', 'oskodaatas', 'oskodot', 'oskogas', 'oskogat', 'oskogo', 'oskogozka', 'oskoktas', 'oskooad', 'oskoook', 'oskosaat', 'oskotask', 'oskotatko', 'oskozoka', 'ozka', 'ozkadaatas', 'ozkadot', 'ozkagas', 'ozkagat', 'ozkago', 'ozkagozka', 'ozkaktas', 'ozkaoad', 'ozkaook', 'ozkasaat', 'ozkatask', 'ozkatatko', 'ozkazoka', 'saas', 'saasasaat', 'saasasoka', 'saasataatas', 'saasatask', 'saasatatko', 'saasatot', 'saaskas', 'saaskat', 'saasko', 'saaskozka', 'saasktas', 'saasoad', 'saasook', 'sak', 'sakkas', 'sakkat', 'sakko', 'sakkozka', 'sakktas', 'sakoad', 'sakook', 'saksaat', 'saksoka', 'saktaatas', 'saktask', 'saktatko', 'saktot', 'skod', 'skodadaatas', 'skodadot', 'skodasaat', 'skodatask', 'skodatatko', 'skodazoka', 'skodgas', 'skodgat', 'skodgo', 'skodgozka', 'skodktas', 'skodoad', 'skodook', 'taso', 'tasodaatas', 'tasodot', 'tasogas', 'tasogat', 'tasogo', 'tasogozka', 'tasoktas', 'tasooad', 'tasoook', 'tasosaat', 'tasotask', 'tasotatko', 'tasozoka', 'tok', 'tokkas', 'tokkat', 'tokko', 'tokkozka', 'tokktas', 'tokoad', 'tokook', 'toksaat', 'toksoka', 'toktaatas', 'toktask', 'toktatko', 'toktot', 'toot', 'tootasaat', 'tootasoka', 'tootataatas', 'tootatask', 'tootatatko', 'tootatot', 'tootkas', 'tootkat', 'tootko', 'tootkozka', 'tootktas', 'tootoad', 'tootook', 'zook', 'zookkas', 'zookkat', 'zookko', 'zookkozka', 'zookktas', 'zookoad', 'zookook', 'zooksaat', 'zooksoka', 'zooktaatas', 'zooktask', 'zooktatko', 'zooktot']



from fst import EPSILON

target_hmm = {'q0': ['q1'],
              'q1': (['q2'], ['sak', 'dog', 'kat', 'daot', 'good', 'gkas', 'dkaz', 'skod', 'gdaas', 'tok',
                              'ksoag', 'agtod', 'taso', 'kaos', 'oktado', 'koad', 'osko', 'ozka', 'ag',
                              'zook', 'saas', 'toot']),
              'q2': (['qf'],
                     ['zoka', 'gat', 'dot', 'saat', 'tsk', 'gozka', 'oad', 'ook', 'go', 'ktas', 'gas', 'daats',
                      'tatko', EPSILON])}

assimilation_rule = [[{"cons": "+"}], [{"voice": "-"}], [{"voice": "-"}], [], True]
epenthesis_rule = [[], [{"low": "+"}], [{"coronal": "+"}], [{"coronal": "+"}], True]


target_tuple = (target_hmm, [assimilation_rule, epenthesis_rule])
