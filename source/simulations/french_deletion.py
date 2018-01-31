simulation_number = 1

configurations_dict = \
{
"MUTATE_RULE_SET": 1,
"MUTATE_HMM": 1,

"EVOLVE_RULES": True,
"EVOLVE_HMM": True,

"COMBINE_EMISSIONS": 0,
"MERGE_EMISSIONS": 0,
"ADVANCE_EMISSION": 0,
"CLONE_STATE": 0,
"CLONE_EMISSION": 0,
"SPLIT_EMISSION": 0,
"ADD_STATE": 0,
"REMOVE_STATE": 0,
"MERGE_STATES": 0,
"SPLIT_STATES": 0,
"ADD_TRANSITION": 0,
"REMOVE_TRANSITION": 0,
"ADD_SEGMENT_TO_EMISSION": 1,
"REMOVE_SEGMENT_FROM_EMISSION": 1,
"CHANGE_SEGMENT_IN_EMISSION": 1,
"ADD_EMISSION_TO_STATE": 1,
"ADD_EMISSION_FROM_DATA": 0,
"REMOVE_EMISSION_FROM_STATE": 1,

"DATA_ENCODING_LENGTH_MULTIPLIER": 50,
"HMM_ENCODING_LENGTH_MULTIPLIER": 20,
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

"MAX_NUM_OF_INNER_STATES": 1,
"MIN_NUM_OF_INNER_STATES": 1,

"MAX_NUMBER_OF_RULES": 2,
"MIN_NUMBER_OF_RULES": 0,

"MORPHEME_BOUNDARY_FLAG": False,
"LENGTHENING_FLAG": False,
"UNDERSPECIFICATION_FLAG": False,
"WORD_BOUNDARY_FLAG": False,
"RESTRICTIONS_ON_ALPHABET": False,

"CHECK_STALEMATE": False,
"INITIAL_TEMPERATURE": 75,
"THRESHOLD": 1,
"COOLING_RATE": 0.99995,
"DEBUG_LOGGING_INTERVAL": 200,
"CLEAR_MODULES_CACHING_INTERVAL": 1000,
"STEPS_LIMITATION": float("inf"),

"LINEAR_DECAY": False
}


log_file_template = "{}_extra_vowel_french_{}.txt"

segment_table_file_name = "french_deletion_with_h_extra_vowel_segment_table.txt"

data =  ['tab', 'tabl', 'lub', 'lubl', 'tap', 'tapl', 'rud', 'rudl', 'parl', 'birl', 'tpul', 'tbir', 'rdahl', 'tuhl', 'tid', 'ruap', 'dail', 'rlad', 'puard', 'lup', 'lid']

target_hmm = {'q0': ['q1'],
              'q1': (['qf'], ['tabl', 'lubl', 'tapl', 'rudl', 'parl', 'birl', 'tpul', 'tbir', 'rdahl', 'tuhl', 'tid', 'ruap', 'dail', 'rlad', 'puard', 'lup', 'lid']),
              }

rule_set = [[[{"liquid": "+"}], [], [{"cons": "+", "son": "-"}], [], False]]

initial_hmm = {'q0': ['q1'],
              'q1': (['qf'], data[:])
             }

target_tuple = (target_hmm, rule_set)

