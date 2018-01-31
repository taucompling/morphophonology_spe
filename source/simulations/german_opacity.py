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

"DATA_ENCODING_LENGTH_MULTIPLIER": 100,
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

"MAX_FEATURE_BUNDLE_IN_CONTEXT": 1,

"MAX_NUM_OF_INNER_STATES": 5,
"MIN_NUM_OF_INNER_STATES": 1,

"MAX_NUMBER_OF_RULES": 4,
"MIN_NUMBER_OF_RULES": 0,

"WORD_BOUNDARY_FLAG": True,
"MORPHEME_BOUNDARY_FLAG": False,
"LENGTHENING_FLAG": False,
"UNDERSPECIFICATION_FLAG": False,
"RESTRICTIONS_ON_ALPHABET": False,

"INITIAL_TEMPERATURE": 50,
"THRESHOLD": 1,
"COOLING_RATE": 0.9999999,
"DEBUG_LOGGING_INTERVAL": 200,
"CLEAR_MODULES_CACHING_INTERVAL": 1000,
"STEPS_LIMITATION":  float("inf"),

"LINEAR_DECAY": False
}

segment_table_file_name = "german_opacity_segment_table.txt"

log_file_template = "{}_german_opacity_with_WORD_BOUNDARY_FLAG_{}.txt"

data = [u'cicun', u'ciin', u'ci', u'ciacun', u'cia', u'cirin', u'craxun', u'crain', u'cra', u'axtuxun', u'axtuin', u'axtu', u'icnaxun', u'icnain', u'icna', u'naxun', u'nain', u'na', u'truxun', u'truin', u'tru', u'taacun', u'taa', u'tarin', u'tuacun', u'tua', u'turin', u'taniacun', u'tania', u'tanirin', u'tranicun', u'traniin', u'trani']

target_hmm = {'q0': ['q1'],
              'q1': (['q2', 'qf'], ['ci','na','tur','cir','tar','tru','cra','axtu','icna','tanir','trani']),
              'q2': (['qf'], ['in', 'cun'])}

backing_rule = [[{"velar": "+"}], [{"back": "+"}], [{"back":"+", "cons":"-"}], [], True]
vocalization_rule = [[{"low": "+"}], [{"cons":"-", "coronal":"-"}], [], [{"cons":"+"}], True]

target_tuple = (target_hmm, [backing_rule, vocalization_rule])

