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
"ADD_SEGMENT_BY_FEATURE_BUNDLE": 0,

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
"MUTATE_RIGHT_CONTEXT": 5,
"MUTATE_OBLIGATORY": 1,
"SWITCH_TARGET_CHANGE": 0,

"ADD_FEATURE_BUNDLE": 5,
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

"CEIL_LOG2": False,
"MORPHEME_BOUNDARY_FLAG": False,
"LENGTHENING_FLAG": False,
"UNDERSPECIFICATION_FLAG": False,
"WORD_BOUNDARY_FLAG": False,
"RESTRICTIONS_ON_ALPHABET": False,

"TRANSDUCER_STATES_LIMIT": 1000,
"DEBUG_LOGGING_INTERVAL": 200,
"CLEAR_MODULES_CACHING_INTERVAL": 1000,
}



inputs = ['meur', 'ruem', 'gaag', 'deag', 'uat', 'katr', 'derr', 'edr', 'dekruk', 'marut', 'amr', 'damuk', 'gamuk', 'tedruk', 'merrer', 'medr', 'kudr', 'ramutk', 'remr', 'redrem', 'ugr', 'matram', 'gegr', 'memegr', 'rerr', 'magram', 'kakekr', 'tederr', 'kamr', 'ruratr', 'tatum', 'akr', 'mamakr', 'ekr', 'redr', 'makred', 'kutegr', 'darut', 'gamud', 'mudr', 'karrad', 'err', 'ragug', 'taruk', 'gatukd', 'katudt', 'tamug', 'mamudt', 'madum', 'rakutm', 'kamut', 'kamud', 'kakudg', 'mamuk', 'tagurk', 'tarugr', 'dadugk', 'tarumm', 'ramud', 'kaduk']

data = [u'akr', u'amr', u'mudr', u'merrer', u'maYmuk', u'meur', u'maYdum', u'maYmudt', u'magram', u'memegr', u'maYrut', u'mamakr', u'matram', u'makred', u'medr', u'raYmud', u'redr', u'raYmutk', u'remr', u'redrem', u'raYkutm', u'raYgug', u'rerr', u'ruratr', u'ruem', u'edr', u'ekr', u'err', u'taYtum', u'tederr', u'taYrumm', u'taYmug', u'taYrugr', u'taYruk', u'taYgurk', u'tedruk', u'daYdugk', u'daYrut', u'dekruk', u'derr', u'deag', u'daYmuk', u'uat', u'ugr', u'kaYduk', u'kaYtudt', u'karrad', u'kamr', u'katr', u'kakekr', u'kaYmut', u'kaYmud', u'kaYkudg', u'kutegr', u'kudr', u'gegr', u'gaYmud', u'gaYmuk', u'gaag', u'gaYtukd']


#exponential
log_file_template = "{}_icelandic_umlaut_no_morphology_only_Y_{}.txt"

segment_table_file_name = "icelandic_umlaut_no_morphology_segment_table.txt"


target_hmm = {'q0': ['q1'],
              'q1': (['qf'], inputs)
              }

umlaut_rule = [[], [{"round": "+", "back": "-"}],  [{"low": "+"}],  [{"cons": "+"}, {"round": "+"}], True]


target_tuple = (target_hmm, [umlaut_rule])


initial_hmm = {'q0': ['q1'],
               'q1': (['qf'], data[:])}