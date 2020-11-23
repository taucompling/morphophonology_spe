simulation_number = 1
configurations_dict = \
{
"MUTATE_RULE_SET": 1,
"MUTATE_HMM": 1,

"EVOLVE_RULES": True,
"EVOLVE_HMM": True,

"COMBINE_EMISSIONS": 1,
"MERGE_EMISSIONS": 0,
"ADVANCE_EMISSION": 1,
"CLONE_STATE": 0,
"CLONE_EMISSION": 1,
"SPLIT_EMISSION": 0,
"MOVE_EMISSION": 1,
"ADD_STATE": 1,
"REMOVE_STATE": 1,
"MERGE_STATES": 0,
"SPLIT_STATES": 0,
"ADD_TRANSITION": 1,
"REMOVE_TRANSITION": 1,
"ADD_SEGMENT_TO_EMISSION": 1,
"REMOVE_SEGMENT_FROM_EMISSION": 1,
"CHANGE_SEGMENT_IN_EMISSION": 1,
"ADD_EMISSION_TO_STATE": 1,
"ADD_EMISSION_FROM_DATA": 0,
"REMOVE_EMISSION_FROM_STATE": 1,
"ADD_SEGMENT_BY_FEATURE_BUNDLE": 0,

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
"SWITCH_TARGET_CHANGE": 0,

"ADD_FEATURE_BUNDLE": 1,
"REMOVE_FEATURE_BUNDLE": 1,
"CHANGE_EXISTING_FEATURE_BUNDLE": 1,
"CHANGE_KLEENE_VALUE": 0,

"ADD_FEATURE": 1,
"REMOVE_FEATURE": 1,
"CHANGE_FEATURE_VALUE": 1,

"MAX_FEATURE_BUNDLE_IN_CONTEXT": 1,

"MAX_NUM_OF_INNER_STATES": 4,
"MIN_NUM_OF_INNER_STATES": 1,

"MAX_NUMBER_OF_RULES": 5,
"MIN_NUMBER_OF_RULES": 0,

"CEIL_LOG2": False,
"MORPHEME_BOUNDARY_FLAG": False,
"LENGTHENING_FLAG": False,
"WORD_BOUNDARY_FLAG": True,
"UNDERSPECIFICATION_FLAG": False,
"RESTRICTIONS_ON_ALPHABET": True,

"TRANSDUCER_STATES_LIMIT": 1000,
"DEBUG_LOGGING_INTERVAL": 200,
"CLEAR_MODULES_CACHING_INTERVAL": 1000,
}


segment_table_file_name = "catalan_with_engma_segment_table.txt"

log_file_template = "{}_catalan_{}.txt"

data = ['blaq', 'blaqka', 'blaqket', 'blaqkik', 'blaqkkaima', 'blaqkkasa', 'blaqks', 'kalen', 'kalenta', 'kalentet', 'kalentik', 'kalentkaima', 'kalentkasa', 'kalents', 'kam', 'kampa', 'kampet', 'kampik', 'kampkaima', 'kampkasa', 'kamps', 'kap', 'kapa', 'kapet', 'kapik', 'kapkaima', 'kapkasa', 'kaps', 'katala', 'katalana', 'katalanet', 'katalanik', 'katalans', 'katalaqkaima', 'katalaqkasa', 'kuzi', 'kuzina', 'kuzinet', 'kuzinik', 'kuzins', 'kuziqkaima', 'kuziqkasa', 'mal', 'mala', 'malet', 'malik', 'malkaima', 'malkasa', 'mals', 'metal', 'metala', 'metalet', 'metalik', 'metalkaima', 'metalkasa', 'metals', 'pla', 'plana', 'planet', 'planik', 'plans', 'plaqkaima', 'plaqkasa', 'plasa', 'plasaa', 'plasaet', 'plasaik', 'plasakaima', 'plasakasa', 'plasas', 'sile', 'silena', 'silenet', 'silenik', 'silens', 'sileqkaima', 'sileqkasa', 'taq', 'taqka', 'taqket', 'taqkik', 'taqkkaima', 'taqkkasa', 'taqks']


target_hmm = {'q0': ['q1'],
              'q1': (['q2', 'qf'],
                     ['plan', 'kuzin', 'silen', 'katalan', 'kalent', 'blank', 'plasa',
                      'kamp', 'metal', 'kap', 'mal', 'tank']),
              'q2': (['qf'], ['s', 'et', 'ik', 'a', 'kasa', 'kaiman']),
              }

nasal_deletion = [[{"nasal": "+"}], [], [], [{"WB": True}], True]
nasal_place_assimilation = [[{"nasal": "+", "coronal": "+"}], [{"velar": "+", "coronal": "-"}], [], [{"velar": "+"}], True]
cluster_simplification = [[{"cont": "-"}], [], [{"nasal": "+"}], [{"WB": True}], True]

rule_set = [nasal_deletion, nasal_place_assimilation, cluster_simplification]


target_tuple = (target_hmm, rule_set)
