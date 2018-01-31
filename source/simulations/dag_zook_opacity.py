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
"ADD_STATE": 1,
"REMOVE_STATE": 1,
"MERGE_STATES": 1,
"SPLIT_STATES": 1,
"ADD_TRANSITION": 1,
"REMOVE_TRANSITION": 1,
"ADD_SEGMENT_TO_EMISSION": 5,
"REMOVE_SEGMENT_FROM_EMISSION": 5,
"CHANGE_SEGMENT_IN_EMISSION": 5,
"ADD_EMISSION_TO_STATE": 5,
"ADD_EMISSION_FROM_DATA": 0,
"REMOVE_EMISSION_FROM_STATE": 5,

"DATA_ENCODING_LENGTH_MULTIPLIER": 25,
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

data = ['daot', 'daotasaat', 'daotasoka', 'daotata', 'daotatask', 'daotkazka', 'daotko', 'dkoz', 'dkozada', 'dkozasaat', 'dkozatask', 'dkozazoka', 'dkozgo', 'dkozkazka', 'dog', 'dogda', 'doggo', 'dogkazka', 'dogsaat', 'dogtask', 'dogzoka', 'dok', 'dokkazka', 'dokko', 'doksaat', 'doksoka', 'dokta', 'doktask', 'gdaas', 'gdaasasaat', 'gdaasasoka', 'gdaasata', 'gdaasatask', 'gdaaskazka', 'gdaasko', 'gkas', 'gkasasaat', 'gkasasoka', 'gkasata', 'gkasatask', 'gkaskazka', 'gkasko', 'kaos', 'kaosasaat', 'kaosasoka', 'kaosata', 'kaosatask', 'kaoskazka', 'kaosko', 'kat', 'katasaat', 'katasoka', 'katata', 'katatask', 'katkazka', 'katko', 'kood', 'koodada', 'koodasaat', 'koodatask', 'koodazoka', 'koodgo', 'koodkazka', 'ksoag', 'ksoagda', 'ksoaggo', 'ksoagkazka', 'ksoagsaat', 'ksoagtask', 'ksoagzoka', 'ogtad', 'ogtadada', 'ogtadasaat', 'ogtadatask', 'ogtadazoka', 'ogtadgo', 'ogtadkazka', 'oktado', 'oktadoda', 'oktadogo', 'oktadokazka', 'oktadosaat', 'oktadotask', 'oktadozoka', 'skaz', 'skazada', 'skazasaat', 'skazatask', 'skazazoka', 'skazgo', 'skazkazka', 'tak', 'takkazka', 'takko', 'taksaat', 'taksoka', 'takta', 'taktask', 'taso', 'tasoda', 'tasogo', 'tasokazka', 'tasosaat', 'tasotask', 'tasozoka']

from fst import EPSILON

target_hmm = {'q0': ['q1'],
              'q1': (['q2'],  ['tak', 'dog', 'kat', 'daot', 'kood', 'gkas', 'dkoz', 'skaz', 'gdaas', 'dok', 'ksoag', 'ogtad', 'taso', 'kaos', 'oktado']),
              'q2': (['qf'], ['zoka', 'go', 'da', 'saat', 'task', 'kazka', EPSILON])}

assimilation_rule = [[{"cons": "+"}], [{"voice": "-"}], [{"voice": "-"}], [], True]
epenthesis_rule = [[], [{"low": "+"}], [{"coronal": "+"}], [{"coronal": "+"}], True]


target_tuple = (target_hmm, [assimilation_rule, epenthesis_rule])
