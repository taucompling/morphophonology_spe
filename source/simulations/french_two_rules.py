simulation_number = 1

configurations_dict = \
    {
        "MUTATE_RULE_SET": 1,
        "MUTATE_HMM": 1,

        "EVOLVE_RULES": True,
        "EVOLVE_HMM": True,

        "COMBINE_EMISSIONS": 0,
        "MERGE_EMISSIONS": 0,
        "ADVANCE_EMISSION": 1,
        "CLONE_STATE": 0,
        "CLONE_EMISSION": 1,
        "SPLIT_EMISSION": 0,
        "ADD_STATE": 1,
        "REMOVE_STATE": 1,
        "MERGE_STATES": 1,
        "SPLIT_STATES": 0,
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

        "ADD_FEATURE": 1,
        "REMOVE_FEATURE": 1,
        "CHANGE_FEATURE_VALUE": 1,
        "CHANGE_KLEENE_VALUE": 0,

        "MAX_FEATURE_BUNDLE_IN_CONTEXT": 2,

        "MAX_NUM_OF_INNER_STATES": 5,
        "MIN_NUM_OF_INNER_STATES": 1,

        "MAX_NUMBER_OF_RULES": 5,
        "MIN_NUMBER_OF_RULES": 0,

        "MORPHEME_BOUNDARY_FLAG": True,
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

log_file_template = "{}_french_two_rules_{}.txt"

segment_table_file_name = "french_two_rules.txt"

data = ['arb', 'arbbrylab', 'arbbrylabl', 'arbprobab', 'arbprobabl', 'arbpuri', 'arbr', 'arbrbrylab', 'arbrbrylabl', 'arbrebrylab', 'arbrebrylabl', 'arbreprobab', 'arbreprobabl', 'arbrepuri', 'arbresal', 'arbrprobab', 'arbrprobabl', 'arbrpuri', 'arbrsal', 'arbsal', 'film', 'filmbrylab', 'filmbrylabl', 'filmebrylab', 'filmebrylabl', 'filmeprobab', 'filmeprobabl', 'filmepuri', 'filmesal', 'filmprobab', 'filmprobabl', 'filmpuri', 'filmsal', 'furyr', 'furyrbrylab', 'furyrbrylabl', 'furyrprobab', 'furyrprobabl', 'furyrpuri', 'furyrsal', 'karaf', 'karafbrylab', 'karafbrylabl', 'karafprobab', 'karafprobabl', 'karafpuri', 'karafsal', 'krab', 'krabbrylab', 'krabbrylabl', 'krabprobab', 'krabprobabl', 'krabpuri', 'krabsal', 'kup', 'kupbrylab', 'kupbrylabl', 'kupl', 'kuplbrylab', 'kuplbrylabl', 'kuplebrylab', 'kuplebrylabl', 'kupleprobab', 'kupleprobabl', 'kuplepuri', 'kuplesal', 'kuplprobab', 'kuplprobabl', 'kuplpuri', 'kuplsal', 'kupprobab', 'kupprobabl', 'kuppuri', 'kupsal', 'liv', 'livbrylab', 'livbrylabl', 'livprobab', 'livprobabl', 'livpuri', 'livr', 'livrbrylab', 'livrbrylabl', 'livrebrylab', 'livrebrylabl', 'livreprobab', 'livreprobabl', 'livrepuri', 'livresal', 'livrprobab', 'livrprobabl', 'livrpuri', 'livrsal', 'livsal', 'ord', 'ordbrylab', 'ordbrylabl', 'ordprobab', 'ordprobabl', 'ordpuri', 'ordr', 'ordrbrylab', 'ordrbrylabl', 'ordrebrylab', 'ordrebrylabl', 'ordreprobab', 'ordreprobabl', 'ordrepuri', 'ordresal', 'ordrprobab', 'ordrprobabl', 'ordrpuri', 'ordrsal', 'ordsal', 'tab', 'tabbrylab', 'tabbrylabl', 'tabl', 'tablbrylab', 'tablbrylabl', 'tablebrylab', 'tablebrylabl', 'tableprobab', 'tableprobabl', 'tablepuri', 'tablesal', 'tablprobab', 'tablprobabl', 'tablpuri', 'tablsal', 'tabprobab', 'tabprobabl', 'tabpuri', 'tabsal', 'vit', 'vitbrylab', 'vitbrylabl', 'vitprobab', 'vitprobabl', 'vitpuri', 'vitr', 'vitrbrylab', 'vitrbrylabl', 'vitrebrylab', 'vitrebrylabl', 'vitreprobab', 'vitreprobabl', 'vitrepuri', 'vitresal', 'vitrprobab', 'vitrprobabl', 'vitrpuri', 'vitrsal', 'vitsal']


from fst import EPSILON

target_hmm = {'q0': ['q1'],
              'q1': (['q3'],
                     ['ordr', 'tabl', 'arbr', 'livr',
                      'vitr', 'kupl', 'film', 'krab', 'karaf', 'furyr']),
              'q3': (['qf'], ['sal', 'probabl', 'brylabl', 'puri', EPSILON])}

schwa_epenthesis = [[], [{"cons": "-", "high": "-", "low": "-", "labial": "-"}], [{"cons": "+"}, {"cons": "+"}],
                    [{"MB": True}, {"cons": "+"}], False]
l_deletion = [[{"liquid": "+"}], [], [{"cons": "+", "son": "-"}], [{"MB": True}], False]

rule_set = [schwa_epenthesis, l_deletion]

# initial_hmm = {'q0': ['q1'],
#                'q1': (['qf'], data[:])
#                }

target_tuple = (target_hmm, rule_set)
