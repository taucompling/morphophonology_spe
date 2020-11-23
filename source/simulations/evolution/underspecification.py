from rule import Rule
from rule_set import RuleSet
from segment_table import Segment, SegmentTable, Feature
from copy import deepcopy
simulation_number = 1

cons = Feature('cons')
high = Feature('high')
voice = Feature('voice', values=('-', '+', '0'))
bound = Feature('bound')

a = Segment('a', {cons: '-', high: '-', voice: '-', bound: '-'})
i = Segment('i', {cons: '-', high: '+', voice: '-', bound: '-'})
t = Segment('t', {cons: '+', high: '-', voice: '-', bound: '-'})
d = Segment('d', {cons: '+', high: '-', voice: '+', bound: '-'})
T = Segment('T', {cons: '+', high: '-', voice: '0', bound: '-'})
B = Segment('B', {cons: '-', high: '-', voice: '-', bound: '+'})

segment_table = SegmentTable([a, i, t, d, T, B])



configurations_dict = \
{
"MUTATE_RULE_SET": 1,
"MUTATE_HMM": 1,

"COMBINE_EMISSIONS": 0,
"ADVANCE_EMISSION": 0,
"CLONE_STATE": 0,
"CLONE_EMISSION": 0,
"ADD_STATE": 0,
"REMOVE_STATE": 0,
"ADD_TRANSITION": 0,
"REMOVE_TRANSITION": 0,
"ADD_SEGMENT_TO_EMISSION": 0,
"REMOVE_SEGMENT_FROM_EMISSION": 0,
"CHANGE_SEGMENT_IN_EMISSION": 1,
"ADD_EMISSION_TO_STATE": 0,
"REMOVE_EMISSION_FROM_STATE": 0,
"UNDERSPECIFY": 1,

"DATA_ENCODING_LENGTH_MULTIPLIER": 100,
"HMM_ENCODING_LENGTH_MULTIPLIER": 100,
"RULES_SET_ENCODING_LENGTH_MULTIPLIER": 1,

"MORPHEME_BOUNDARY_FLAG": True,
"LENGTHENING_FLAG": False,
"UNDERSPECIFICATION_FLAG": True,

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

"ADD_FEATURE": 1,
"REMOVE_FEATURE": 1,
"CHANGE_FEATURE_VALUE": 1,

"MAX_FEATURE_BUNDLE_IN_CONTEXT": 1,

"MAX_NUMBER_OF_RULES": 10,
"MIN_NUMBER_OF_RULES": 0,

"MAX_NUM_OF_INNER_STATES": 1,
"MIN_NUM_OF_INNER_STATES": 1,
"DEBUG_LOGGING_INTERVAL": 100,
}


log_file_template = "{}_underspecification_{}.txt"

data = ['dat', 'tat', 'da', 'ta']


target_hmm = {'q0': ['q1'],
              'q1': (['qf'], ['daT', 'taT', 'da', 'ta'])
              }

initial_hmm = {'q0': ['q1'],
              'q1': (['qf'], deepcopy(data))
              }

rule = Rule([{"voice": "0"}], [{"voice": "-"}], [], [{"bound": "+"}], True)



target_tuple = (target_hmm, RuleSet([rule]))