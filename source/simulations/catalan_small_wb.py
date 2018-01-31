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
"ADD_SEGMENT_TO_EMISSION": 1,
"REMOVE_SEGMENT_FROM_EMISSION": 1,
"CHANGE_SEGMENT_IN_EMISSION": 1,
"ADD_EMISSION_TO_STATE": 1,
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
"CHANGE_KLEENE_VALUE": 0,

"ADD_FEATURE": 1,
"REMOVE_FEATURE": 1,
"CHANGE_FEATURE_VALUE": 1,

"MAX_FEATURE_BUNDLE_IN_CONTEXT": 1,

"MAX_NUM_OF_INNER_STATES": 5,
"MIN_NUM_OF_INNER_STATES": 1,

"MAX_NUMBER_OF_RULES": 5,
"MIN_NUMBER_OF_RULES": 0,

"MORPHEME_BOUNDARY_FLAG": False,
"LENGTHENING_FLAG": False,
"WORD_BOUNDARY_FLAG": False,
"UNDERSPECIFICATION_FLAG": False,
"RESTRICTIONS_ON_ALPHABET": False,

"CHECK_STALEMATE": True,
"INITIAL_TEMPERATURE": 75,
"THRESHOLD": 1,
"COOLING_RATE": 0.9999995,
"DEBUG_LOGGING_INTERVAL": 200,
"CLEAR_MODULES_CACHING_INTERVAL": 1000,
"STEPS_LIMITATION": float('inf'),

"LINEAR_DECAY": False
}


segment_table_file_name = "catalan_segment_table_small_wb.txt"

log_file_template = "{}_catalan_{}.txt"

data = ['blanX', 'blankaX', 'blanketX', 'blankikX', 'blanksX', 'kaimaX', 'kaimanaX', 'kaimanetX', 'kaimanikX', 'kaimansX', 'kalenX', 'kalentaX', 'kalentetX', 'kalentikX', 'kalentsX', 'kamX', 'kampaX', 'kampetX', 'kampikX', 'kampsX', 'kapX', 'kapaX', 'kapetX', 'kapikX', 'kapsX', 'kasaX', 'kasaaX', 'kasaetX', 'kasaikX', 'kasasX', 'katalaX', 'katalanaX', 'katalanetX', 'katalanikX', 'katalansX', 'kuziX', 'kuzinaX', 'kuzinetX', 'kuzinikX', 'kuzinsX', 'malX', 'malaX', 'maletX', 'malikX', 'malsX', 'metalX', 'metalaX', 'metaletX', 'metalikX', 'metalsX', 'plaX', 'planaX', 'planetX', 'planikX', 'plansX', 'plasaX', 'plasaaX', 'plasaetX', 'plasaikX', 'plasasX', 'sileX', 'silenaX', 'silenetX', 'silenikX', 'silensX']

target_hmm = {'q0': ['q1'],
              'q1': (['q2', 'q3'],
                     ['plan', 'kuzin', 'silen', 'kaiman', 'katalan', 'kalent', 'blank', 'plasa', 'kasa',
                      'kamp', 'metal', 'kap', 'mal']),
              'q2': (['q3'], ['s', 'et', 'ik', 'a']),
              'q3': (['qf'], ['X']),
              }

nasal_deletion = [[{"nasal": "+"}], [], [], [{"wb": "+"}], True]
cluster_simplification = [[{"cont": "-"}], [], [{"nasal": "+"}], [{"wb": "+"}], True]

rule_set = [nasal_deletion, cluster_simplification]

target_tuple = (target_hmm, rule_set)
