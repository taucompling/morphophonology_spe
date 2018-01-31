simulation_number = 1

configurations_dict = \
{
"MUTATE_RULE_SET": 1,
"MUTATE_HMM": 1,

"EVOLVE_RULES": True,
"EVOLVE_HMM": False,

"COMBINE_EMISSIONS": 1,
"ADVANCE_EMISSION": 1,
"CLONE_STATE": 0,
"CLONE_EMISSION": 1,
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
"CHANGE_KLEENE_VALUE": 0,

"ADD_FEATURE": 1,
"REMOVE_FEATURE": 1,
"CHANGE_FEATURE_VALUE": 1,
"CHANGE_KLEENE_VALUE": 0,

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


segment_table_file_name = "plural_english_segment_table.txt"

log_file_template = "{}_two_rules_november_{}.txt"

data = [u'dagdod', u'daggos', u'dagzook', u'dagsad', u'dag', u'dgodod', u'dgogos', u'dgozook', u'dgosad', u'dgo', u'dottod', u'dotkos', u'dotsook', u'dotsad', u'dot', u'tozazook', u'tozasad', u'tozdod', u'tozgos', u'toz', u'gasazook', u'gasasad', u'gastod', u'gaskos', u'gas', u'gdasazook', u'gdasasad', u'gdastod', u'gdaskos', u'gdas', u'koddod', u'kodgos', u'kodzook', u'kodsad', u'kod', u'ktadod', u'ktagos', u'ktazook', u'ktasad', u'kta', u'kattod', u'katkos', u'katsook', u'katsad', u'kat', u'skozazook', u'skozasad', u'skozdod', u'skozgos', u'skoz']

target_hmm = {'q0': ['q1'],
              'q1': (['q2','qf'], ['dag', 'kat', 'dot', 'kod', 'gas', 'toz', 'kta', 'dgo', 'skoz', 'gdas']),
              'q2': (['qf'], ['zook', 'gos', 'dod', 'sad'])}

epenthesis_rule = [[], [{"low": "+"}], [{"cons": "+", "cont": "+"}], [{"cons": "+", "cont": "+"}], True]
assimilation_rule = [[{"cons": "+"}], [{"voice": "-"}], [{"voice": "-"}], [], True]

rule_set = [epenthesis_rule, assimilation_rule]

target_tuple = (target_hmm, rule_set)
