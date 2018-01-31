simulation_number = 1
configurations_dict = \
{
"MUTATE_RULE_SET": 1,
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

"MAX_FEATURE_BUNDLE_IN_CONTEXT": 2,

"MAX_NUM_OF_INNER_STATES": 4,
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
"COOLING_RATE": 0.999999,
"DEBUG_LOGGING_INTERVAL": 200,
"CLEAR_MODULES_CACHING_INTERVAL": 1000,
"STEPS_LIMITATION": float("inf"),

"LINEAR_DECAY": False
}

#exponential
log_file_template = "{}_icelandic_umlaut_{}.txt"

segment_table_file_name = "icelandic_umlaut_segment_table.txt"

data = [u'parmAtum', u'parmAtumda', u'parmatur', u'parmaturamt', u'parmat', u'paum', u'paumda', u'par', u'paramt', u'pa', u'puduretur', u'pudureturamt', u'puduret', u'puduretum', u'puduretumda', u'petaum', u'petaumda', u'petar', u'petaramt', u'peta', u'epuraum', u'epuraumda', u'epurar', u'epuraramt', u'epura', u'dAmum', u'dAmumda', u'damur', u'damuramt', u'dam', u'durpAmum', u'durpAmumda', u'durpamur', u'durpamuramt', u'durpam', u'murtaum', u'murtaumda', u'murtar', u'murtaramt', u'murta', u'mudAtum', u'mudAtumda', u'mudatur', u'mudaturamt', u'mudat', u'rAtum', u'rAtumda', u'ratur', u'raturamt', u'rat', u'rempur', u'rempuramt', u'remp', u'rempum', u'rempumda']

target_hmm = {'q0': ['q1'],
              'q1': (['q2','qf'],  ['dam', 'mudat', 'durpam', 'rat', 'epura', 'parmat', 'puduret', 'pa', 'remp', 'murta', 'peta']),
              'q2': (['qf'], ['r', 'um', 'ramt', 'umda'])}

umlaut_rule = [[{"low": "+"}], [{"round": "+"}],  [],  [{"cons": "+"}, {"round": "+"}], True]
epenthesis_rule = [[], [{"low": "-", "round": "+"}], [{"cons": "+"}], [{"rhotic": "+"}], True]



target_tuple = (target_hmm, [umlaut_rule, epenthesis_rule])
