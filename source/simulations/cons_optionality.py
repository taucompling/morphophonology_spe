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

"DATA_ENCODING_LENGTH_MULTIPLIER": 10,
"HMM_ENCODING_LENGTH_MULTIPLIER": 10,
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
"SWITCH_TARGET_CHANGE": 0,

"ADD_FEATURE_BUNDLE": 1,
"REMOVE_FEATURE_BUNDLE": 1,
"CHANGE_EXISTING_FEATURE_BUNDLE": 1,

"ADD_FEATURE": 1,
"REMOVE_FEATURE": 1,
"CHANGE_FEATURE_VALUE": 1,

"MAX_FEATURE_BUNDLE_IN_CONTEXT": 1,

"MAX_NUM_OF_INNER_STATES": 2,
"MIN_NUM_OF_INNER_STATES": 1,

"MAX_NUMBER_OF_RULES": 4,
"MIN_NUMBER_OF_RULES": 0,

"CEIL_LOG2": False,
"MORPHEME_BOUNDARY_FLAG": False,
"LENGTHENING_FLAG": False,
"UNDERSPECIFICATION_FLAG": False,
"DEBUG_LOGGING_INTERVAL": 200,
"CLEAR_MODULES_CACHING_INTERVAL": 1000,
}

segment_table_file_name = "cons_optionality_segment_table.txt"

log_file_template = "{}_rhotic_optionality_two_states_limit_{}.txt"

data = [u'dagko', u'dagat', u'dagagod', u'dagoto', u'dag', u'dorarat', u'doraragod', u'doraroto', u'dorako', u'doraat', u'doraagod', u'doraoto', u'dora', u'dtorat', u'dtoragod', u'dtoroto', u'dtoko', u'dtoat', u'dtoagod', u'dtooto', u'dto', u'gtarat', u'gtaragod', u'gtaroto', u'gtako', u'gtaat', u'gtaagod', u'gtaoto', u'gta', u'kratorat', u'kratoragod', u'kratoroto', u'kratoko', u'kratoat', u'kratoagod', u'kratooto', u'krato', u'rakarat', u'rakaragod', u'rakaroto', u'rakako', u'rakaat', u'rakaagod', u'rakaoto', u'raka', u'ardko', u'ardat', u'ardagod', u'ardoto', u'ard', u'odarat', u'odaragod', u'odaroto', u'odako', u'odaat', u'odaagod', u'odaoto', u'oda']

target_hmm = {'q0': ['q1'],
              'q1': (['q2','qf'],  ['ard', 'dag', 'dora', 'dto', 'gta', 'krato', 'oda', 'raka']),
              'q2': (['qf'], ['at', 'agod', 'ko', 'oto'])}

epenthesis_rule = [[], [{"rhotic": "+"}], [{"cons": "-"}], [{"cons": "-"}], False]


target_tuple = (target_hmm, [epenthesis_rule])

