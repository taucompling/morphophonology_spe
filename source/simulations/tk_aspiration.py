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

"DATA_ENCODING_LENGTH_MULTIPLIER": 1000,
"HMM_ENCODING_LENGTH_MULTIPLIER": 50,
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

"MAX_NUM_OF_INNER_STATES": 1,
"MIN_NUM_OF_INNER_STATES": 1,

"MAX_NUMBER_OF_RULES": 2,
"MIN_NUMBER_OF_RULES": 0,

"MORPHEME_BOUNDARY_FLAG": False,
"LENGTHENING_FLAG": False,
"UNDERSPECIFICATION_FLAG": False,
"WORD_BOUNDARY_FLAG": False,
"RESTRICTIONS_ON_ALPHABET": True,

"INITIAL_TEMPERATURE": 50,
"THRESHOLD": 1,
"COOLING_RATE": 0.9999991,
"DEBUG_LOGGING_INTERVAL": 200,
"CLEAR_MODULES_CACHING_INTERVAL": 1000,
"STEPS_LIMITATION": float('inf'),

"LINEAR_DECAY": False,

"RESTRICTIONS_ON_ALPHABET": True
}

segment_table_file_name = "tk_aspiration_segment_table.txt"

log_file_template = "{}_tk_aspiration_with_RESTRICTIONS_ON_ALPHABET_{}.txt"

data = ['ithik', 'thatkha', 'thatthat', 'ikhak', 'khikthak', 'khathiit', 'ithak', 'thikhiat', 'thakhiit', 'khikhi']

target_hmm = {'q0': ['q1'],
              'q1': (['qf'], [word.replace("h", "") for word in data]),
              }

rule = [[], [{"asp": "+"}], [{"stop": "+"}], [{"cons": "-"}], True]

initial_hmm = {'q0': ['q1'],
               'q1': (['qf'], data[:])}


#target_tuple = (target_hmm, RuleSet([rule]))

