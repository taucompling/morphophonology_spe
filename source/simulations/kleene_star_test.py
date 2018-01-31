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
        "ADD_SEGMENT_TO_EMISSION": 5,
        "REMOVE_SEGMENT_FROM_EMISSION": 5,
        "CHANGE_SEGMENT_IN_EMISSION": 5,
        "ADD_EMISSION_TO_STATE": 5,
        "REMOVE_EMISSION_FROM_STATE": 5,
        "ADD_EMISSION_FROM_DATA": 0,

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
        "CHANGE_KLEENE_VALUE": 1,

        "MAX_FEATURE_BUNDLE_IN_CONTEXT": 2,

        "MAX_NUM_OF_INNER_STATES": 5,
        "MIN_NUM_OF_INNER_STATES": 1,

        "MAX_NUMBER_OF_RULES": 2,
        "MIN_NUMBER_OF_RULES": 0,

        "MORPHEME_BOUNDARY_FLAG": False,
        "LENGTHENING_FLAG": False,
        "WORD_BOUNDARY_FLAG": False,
        "UNDERSPECIFICATION_FLAG": False,
        "RESTRICTIONS_ON_ALPHABET": False,

        "INITIAL_TEMPERATURE": 50,
        "CHECK_STALEMATE": True,
        "THRESHOLD": 1,
        "COOLING_RATE": 0.999999,
        "DEBUG_LOGGING_INTERVAL": 200,
        "CLEAR_MODULES_CACHING_INTERVAL": 1000,
        "STEPS_LIMITATION": float("inf"),

        "LINEAR_DECAY": False
    }

segment_table_file_name = "plural_english_segment_table.txt"

log_file_template = "{}_kleene_star_test_{}.txt"

data = ['saos', 'sas', 'sa', 'daoz', 'daz', 'da', 'taos', 'tas', 'ta', 'gaoz', 'gaz', 'ga', 'kaos', 'kas', 'ka', 'zaoz',
        'zaz', 'za']

rule = [[{"cons": "+"}], [{"voice": "-"}], [{"voice": "-"}, {"cons": "-", "kleene": True}], [], True]

target_hmm = {'q0': ['q1'],
              'q1': (['q2', 'qf'], ['da', 'ga', 'za', 'ta', 'ka', 'sa']),
              'q2': (['qf'], ['oz', 'z']),
              }

target_tuple = (target_hmm, [rule])
