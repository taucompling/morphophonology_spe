simulation_number = 1

configurations_dict = \
    {
        "MUTATE_RULE_SET": 1,
        "MUTATE_HMM": 1,

        "EVOLVE_RULES": True,
        "EVOLVE_HMM": True,

        "COMBINE_EMISSIONS": 0,
        "MERGE_EMISSIONS": 1,
        "ADVANCE_EMISSION": 1,
        "CLONE_STATE": 0,
        "CLONE_EMISSION": 1,
        "SPLIT_EMISSION": 1,
        "MERGE_STATES": 1,
        "SPLIT_STATES": 1,
        "ADD_STATE": 1,
        "REMOVE_STATE": 1,
        "ADD_TRANSITION": 1,
        "REMOVE_TRANSITION": 1,
        "ADD_SEGMENT_TO_EMISSION": 1,
        "REMOVE_SEGMENT_FROM_EMISSION": 1,
        "CHANGE_SEGMENT_IN_EMISSION": 1,
        "ADD_EMISSION_TO_STATE": 1,
        "REMOVE_EMISSION_FROM_STATE": 1,

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

        "INITIAL_TEMPERATURE": 100,
        "CHECK_STALEMATE": True,
        "THRESHOLD": 1,
        "COOLING_RATE": 0.9999995,
        "DEBUG_LOGGING_INTERVAL": 200,
        "CLEAR_MODULES_CACHING_INTERVAL": 1000,
        "STEPS_LIMITATION": float("inf"),

        "LINEAR_DECAY": False
    }

segment_table_file_name = "turkish_segment_table.txt"

log_file_template = "{}_turkish_vowel_harmony_{}.txt"

data = ['rekzik', 'reksep', 'reks0r', 'rekkiz', 'rekk0j', 'rekrys', 'rekel', 'rekip', 'rekjyz', 'rekpyl', 'rek',
        'ilzik', 'ilsep', 'ils0r', 'ilkiz', 'ilk0j', 'ilrys', 'ilel', 'ilip', 'iljyz', 'ilpyl', 'il', 'larz1k',
        'larsap', 'larsor', 'lark1z', 'larkoj', 'larrus', 'laral', 'lar1p', 'larjuz', 'larpul', 'lar', 'posz1k',
        'possap', 'possor', 'posk1z', 'poskoj', 'posrus', 'posal', 'pos1p', 'posjuz', 'pospul', 'pos']

rule = [[{"syll": "+"}], [{"back": "-"}], [{"syll": "+", "back": "-"}, {"syll": "-", "kleene": True}], [], True]

target_hmm = {'q0': ['q1'],
              'q1': (['q2', 'qf'], ['il', 'lar', 'pos', 'rek', '0p']),
              'q2': (['qf'], ['1p', 'al', 'k1z', 'juz', 'pul', 'sap', 'koj', 'sor', 'z1k', 'rus']),
              }

target_tuple = (target_hmm, [rule])
