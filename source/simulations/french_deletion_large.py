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

segment_table_file_name = "french_deletion_new.txt"

data = ['adorab', 'adorabl', 'aktif', 'arab', 'arb', 'arbr', 'brylab', 'brylabl', 'bylab', 'bylabl', 'byvab', 'byvabl', 'dyr', 'fiab', 'fiabl', 'fiksab', 'fiksabl', 'final', 'finir', 'fumab', 'fumabl', 'fur', 'furyr', 'fylar', 'kad', 'kadr', 'kafar', 'kalkyl', 'kapab', 'kapabl', 'karaf', 'kat', 'katr', 'kud', 'kudr', 'kup', 'kupl', 'kyrab', 'kyrabl', 'lavab', 'lavabl', 'luab', 'luabl', 'mais', 'mutar', 'nyl', 'ord', 'ordr', 'orl', 'parkur', 'parl', 'partir', 'pip', 'polar', 'posib', 'posibl', 'postyr', 'potab', 'potabl', 'prut', 'purir', 'put', 'pys', 'ridikyl', 'ryptyr', 'saly', 'sib', 'sibl', 'sid', 'sidr', 'sif', 'sifl', 'sirk', 'sirkl', 'sortir', 'stad', 'stryktyr', 'styktyr', 'sup', 'supl', 'tab', 'tabl', 'tit', 'titr', 'trub', 'trubl', 'tub', 'tubl', 'vivab', 'vivabl', 'yrl']



target_hmm = {'q0': ['q1'],
              'q1': (['qf'], ['adorabl', 'aktif', 'arab', 'arbr', 'brylabl', 'byvabl', 'dyr', 'stad', 'fiabl', 'fiksabl', 'finir', 'fumabl', 'fur', 'furyr', 'fylar', 'kadr', 'kafar', 'kalkyl', 'kapabl', 'karaf', 'katr', 'kudr', 'kupl', 'kyrabl', 'lavabl', 'luabl', 'mais', 'nyl', 'ordr', 'orl', 'final', 'parkur', 'parl', 'partir', 'pip', 'polar', 'posibl', 'postyr', 'potabl', 'prut', 'purir', 'pys', 'ridikyl', 'ryptyr', 'saly', 'sibl', 'sidr', 'sifl', 'sirkl', 'sortir', 'stryktyr', 'supl', 'tabl', 'mutar', 'titr', 'trubl', 'vivabl', 'yrl']),
              }

rule_set = [[[{"liquid": "+"}], [], [{"cons": "+", "son": "-"}], [], False]]

initial_hmm = {'q0': ['q1'],
              'q1': (['qf'], data[:])
             }

target_tuple = (target_hmm, rule_set)

