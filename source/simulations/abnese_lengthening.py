from rule import Rule
from rule_set import RuleSet
from segment_table import Segment, SegmentTable, Feature
simulation_number = 1

syll = Feature('syll')
cons = Feature('cons')
long = Feature('long')
bound = Feature('bound')

a = Segment('a', {syll: '+', cons: '-', long: '-', bound: '-'})
b = Segment('b', {syll: '-', cons: '+', long: '-', bound: '-'})
lengthening = Segment('Y', {syll: '-', cons: '-', long: '+', bound: '-'})
morpheme_boundary = Segment('B', {syll: '-', cons: '-', long: '-', bound: '+'})

segment_table = SegmentTable([a, b, lengthening, morpheme_boundary])



configurations_dict = \
{
"MUTATE_RULE_SET": 3,
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
"CHANGE_SEGMENT_IN_EMISSION": 0,
"ADD_EMISSION_TO_STATE": 0,
"REMOVE_EMISSION_FROM_STATE": 0,
"INCREASE_TRANSITION_WEIGHT": 0,
"DECREASE_TRANSITION_WEIGHT": 0,
"INCREASE_EMISSION_WEIGHT": 0,
"DECREASE_EMISSION_WEIGHT": 0,

"ADD_RULE": 5,
"REMOVE_RULE": 1,
"DEMOTE_RULE": 1,
"CHANGE_RULE": 20,

"MUTATE_TARGET": 5,
"MUTATE_CHANGE": 5,
"MUTATE_LEFT_CONTEXT": 5,
"MUTATE_RIGHT_CONTEXT": 5,
"MUTATE_OBLIGATORY": 1,
"SWITCH_TARGET_CHANGE": 0,

"ADD_FEATURE_BUNDLE": 1,
"REMOVE_FEATURE_BUNDLE": 1,
"CHANGE_EXISTING_FEATURE_BUNDLE": 3,

"ADD_FEATURE": 1,
"REMOVE_FEATURE": 1,
"CHANGE_FEATURE_VALUE": 1,


"DATA_ENCODING_LENGTH_MULTIPLIER": 10,
"HMM_ENCODING_LENGTH_MULTIPLIER": 1,
"RULES_SET_ENCODING_LENGTH_MULTIPLIER": 1,

"MORPHEME_BOUNDARY_FLAG": True,
"LENGTHENING_FLAG": True,

"MAX_FEATURE_BUNDLE_IN_CONTEXT": 2,

"MAX_NUMBER_OF_RULES": 5,
"MIN_NUMBER_OF_RULES": 0,

"MAX_NUM_OF_INNER_STATES": 1,
"MIN_NUM_OF_INNER_STATES": 1,
"DEBUG_LOGGING_INTERVAL": 200,
"PRINT_PARSE": False,
}


log_file_template = "{}_abnese_lengthening_15_words_10_{}.txt"



data = [u'aabYab', u'abYab', u'abYa', u'aabYa', u'ababababababYa', u'ababYa', u'abababYa', u'bababYab', u'bYab', u'babYab', u'bababYa', u'babababYa', u'babababYab', u'bababababYab', u'babaYa']


target_hmm = {'q0': ['q1'],
              'q1': (['qf'], ['aabb', 'abb', 'aba', 'aaba', 'bbaa', 'bbbb', 'abbba', 'abba',
                         'bb', 'bbb', 'bbba', 'bbbba', 'bbbbb', 'bbbbbb', 'abbbbbba'])
              }

initial_hmm = {'q0': ['q1'],
              'q1': (['qf'], data)
              }



rule1 = Rule([], [{"long": "+"}], [], [{}, {"bound": "+"}], obligatory=True)
rule2 = Rule([], [{"syll": "+"}], [{"cons": "+"}], [{"cons": "+"}], obligatory=True)
target_rule_set = RuleSet([rule1, rule2])


target_tuple = (target_hmm, target_rule_set)