simulation_number = 1
configurations_dict = \
{
"MUTATE_RULE_SET": 1,
"MUTATE_HMM": 1,


"COMBINE_EMISSIONS": 0,
"ADVANCE_EMISSION": 0,
"CLONE_STATE": 0,
"CLONE_EMISSION": 0,
"ADD_STATE": 0,
"REMOVE_STATE": 0,
"ADD_TRANSITION": 0,
"REMOVE_TRANSITION": 0,
"ADD_SEGMENT_TO_EMISSION": 1,
"REMOVE_SEGMENT_FROM_EMISSION": 1,
"CHANGE_SEGMENT_IN_EMISSION": 1,
"ADD_EMISSION_TO_STATE": 1,
"REMOVE_EMISSION_FROM_STATE": 1,

"DATA_ENCODING_LENGTH_MULTIPLIER": 100,
"HMM_ENCODING_LENGTH_MULTIPLIER": 25,
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

"MAX_FEATURE_BUNDLE_IN_CONTEXT": 2,

"MAX_NUM_OF_INNER_STATES": 1,
"MIN_NUM_OF_INNER_STATES": 1,

"MAX_NUMBER_OF_RULES": 4,
"MIN_NUMBER_OF_RULES": 0,

"MORPHEME_BOUNDARY_FLAG": False,
"LENGTHENING_FLAG": False,
"UNDERSPECIFICATION_FLAG": False,
"WORD_BOUNDARY_FLAG": False,
"RESTRICTIONS_ON_ALPHABET": False,


"INITIAL_TEMPERATURE": 50,
"THRESHOLD": 1,
"COOLING_RATE": 0.9999999,
"DEBUG_LOGGING_INTERVAL": 200,
"CLEAR_MODULES_CACHING_INTERVAL": 1000,
"STEPS_LIMITATION": float("inf"),

"LINEAR_DECAY": False
}


more_words = ['meur', 'ruem', 'gaag', 'deag', 'uat']

inputs = more_words + ['katr', 'derr', 'edr', 'dekruk', 'marut', 'amr', 'damuk', 'gamuk', 'tedruk', 'merrer', 'medr', 'kudr', 'ramutk', 'remr', 'redrem', 'ugr', 'matram', 'gegr', 'memegr', 'rerr', 'magram', 'kakekr', 'tederr', 'kamr', 'ruratr', 'tatum', 'akr', 'mamakr', 'ekr', 'redr', 'makred', 'kutegr', 'darut', 'gamud', 'mudr', 'karrad', 'err', 'ragug', 'taruk', 'gatukd', 'katudt', 'tamug', 'mamudt', 'madum', 'rakutm', 'kamut', 'kamud', 'kakudg', 'mamuk', 'tagurk', 'tarugr', 'dadugk', 'tarumm', 'ramud', 'kaduk']

data = more_words +['katur', 'derur', 'edur', 'dekuruk', 'maYrut', 'amur', 'daYmuk', 'gaYmuk', 'teduruk', 'merurer', 'medur', 'kudur', 'raYmutk', 'remur', 'redurem', 'ugur', 'maturam', 'gegur', 'memegur', 'rerur', 'maguram', 'kakekur', 'tederur', 'kamur', 'ruratur', 'taYtum', 'akur', 'mamakur', 'ekur', 'redur', 'makured', 'kutegur', 'daYrut', 'gaYmud', 'mudur', 'karurad', 'erur', 'raYgug', 'taYruk', 'gaYtukd', 'kaYtudt', 'taYmug', 'maYmudt', 'maYdum', 'raYkutm', 'kaYmut', 'kaYmud', 'kaYkudg', 'maYmuk', 'taYgurk', 'taYrugur', 'daYdugk', 'taYrumm', 'raYmud', 'kaYduk']


#exponential
log_file_template = "{}_icelandic_umlaut_no_morphology_high_temp_{}.txt"

segment_table_file_name = "icelandic_umlaut_no_morphology_segment_table.txt"


target_hmm = {'q0': ['q1'],
              'q1': (['qf'], inputs)
              }

umlaut_rule = [[], [{"round": "+", "back": "-"}],  [{"low": "+"}],  [{"cons": "+"}, {"round": "+"}], True]
u_epenthesis_rule = [[], [{"low": "-", "back": "+"}], [{"cons": "+"}], [{"rhotic": "+"}], True]


target_tuple = (target_hmm, [umlaut_rule, u_epenthesis_rule])


initial_hmm = {'q0': ['q1'],
               'q1': (['qf'], data[:])}