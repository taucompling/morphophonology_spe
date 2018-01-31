# from rule import Rule
# from rule_set import RuleSet
# from segment_table import Segment, SegmentTable, Feature
# simulation_number = 1
#
#
# cons = Feature('cons')
# voice = Feature('voice')
# velar = Feature('velar')
# cont = Feature('cont')
# low = Feature('low')
#
#
# d = Segment('d', {cons: '+', voice: '+', velar: '-', cont: '-', low: '-'})
# t = Segment('t', {cons: '+', voice: '-', velar: '-', cont: '-', low: '-'})
# g = Segment('g', {cons: '+', voice: '+', velar: '+', cont: '-', low: '-'})
# k = Segment('k', {cons: '+', voice: '-', velar: '+', cont: '-', low: '-'})
# z = Segment('z', {cons: '+', voice: '+', velar: '-', cont: '+', low: '-'})
# s = Segment('s', {cons: '+', voice: '-', velar: '-', cont: '+', low: '-'})
# a = Segment('a', {cons: '-', voice: '+', velar: '-', cont: '+', low: '+'})
# o = Segment('o', {cons: '-', voice: '+', velar: '-', cont: '+', low: '-'})
#
# segment_table = SegmentTable([d, t, g, k, z, s, a, o])


configurations_dict = \
{
"MUTATE_RULE_SET": 0,
"MUTATE_HMM": 1,

"EVOLVE_RULES": False,
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
"ADD_EMISSION_FROM_DATA": 0,
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

"MAX_FEATURE_BUNDLE_IN_CONTEXT": 1,

"MAX_NUM_OF_INNER_STATES": 5,
"MIN_NUM_OF_INNER_STATES": 1,

"MAX_NUMBER_OF_RULES": 3,
"MIN_NUMBER_OF_RULES": 0,

"MORPHEME_BOUNDARY_FLAG": False,
"LENGTHENING_FLAG": False,
"WORD_BOUNDARY_FLAG": False,
"UNDERSPECIFICATION_FLAG": False,
"RESTRICTIONS_ON_ALPHABET": False,

"CHECK_STALEMATE": False,
"INITIAL_TEMPERATURE": 50,
"THRESHOLD": 10**-1,
"COOLING_RATE": 0.999995,
"DEBUG_LOGGING_INTERVAL": 200,
"CLEAR_MODULES_CACHING_INTERVAL": 1000,
"STEPS_LIMITATION": float('inf'),

"PRINT_PARSE": False,
"LINEAR_DECAY": False
}

segment_table_file_name = "plural_english_segment_table.txt"

log_file_template = "{}_dag_zook_morphology_only_{}.txt"



data = [u'dagzook', u'daggos', u'dagdod', u'dag', u'katzook', u'katgos', u'katdod', u'kat', u'dotzook', u'dotgos', u'dotdod', u'dot', u'kodzook', u'kodgos', u'koddod', u'kod', u'gaszook', u'gasgos', u'gasdod', u'gas', u'tozzook', u'tozgos', u'tozdod', u'toz', u'atazook', u'atagos', u'atadod', u'ata', u'asozook', u'asogos', u'asodod', u'aso']

target_hmm = {'q0': ['q1'],
              'q1': (['q2','qf'], ['dag', 'kat', 'dot', 'kod', 'gas', 'toz', 'ata', 'aso']),
              'q2': (['qf'], ['zook', 'gos', 'dod'])}


target_tuple = (target_hmm, [])

