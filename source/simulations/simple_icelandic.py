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


"INITIAL_TEMPERATURE": 50,
"THRESHOLD": 1,
"COOLING_RATE": 0.9999999,
"DEBUG_LOGGING_INTERVAL": 200,
"CLEAR_MODULES_CACHING_INTERVAL": 1000,
"STEPS_LIMITATION": float("inf"),

"LINEAR_DECAY": False
}

#exponential
log_file_template = "{}_simple_icelandic_{}.txt"

segment_table_file_name = "simple_icelandic_segment_table.txt"

data = [u'taauriurip', u'taauriuruuur', u'taauri', u'taauruuma', u'taauruuptau', u'duurpiamurip', u'duurpiamuruuur', u'duurpiamuma', u'duurpiamuptau', u'duurpiam', u'duumuurip', u'duumuuruuur', u'duumuuma', u'duumuuptau', u'duumu', u'muuurpiurip', u'muuurpiuruuur', u'muuurpi', u'muuurpuuma', u'muuurpuuptau', u'uuraimpaurip', u'uuraimpauruuur', u'uuraimpauma', u'uuraimpauptau', u'uuraimpa', u'uuuriapurip', u'uuuriapuruuur', u'uuuriapuma', u'uuuriapuptau', u'uuuriap', u'puduuriurip', u'puduuriuruuur', u'puduuri', u'puduuruuma', u'puduuruuptau', u'piimuururip', u'piimuururuuur', u'piimuuruma', u'piimuuruptau', u'piimuur', u'patiiurip', u'patiiuruuur', u'patii', u'patiuuma', u'patiuuptau']

target_hmm = {'q0': ['q1'],
              'q1': (['q2', 'qf'], ['miurpi', 'durpiam', 'puduri', 'uraimpa', 'patii', 'uuriap', 'duumu', 'piimur', 'taari']),
              'q2': (['qf'], ['uma', 'rip', 'uptau', 'riur'])}


rounding_rule = [[{"high": "+"}], [{"round": "+"}], [], [{"round": "+"}], True]
epenthesis_rule = [[], [{"round": "+"}], [], [{"rhotic": "+"}], True]



target_tuple = (target_hmm, [rounding_rule, epenthesis_rule])
