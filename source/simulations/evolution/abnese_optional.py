from rule import Rule
from rule_set import RuleSet
from segment_table import Segment, SegmentTable, Feature
simulation_number = 1
from copy import deepcopy

cons = Feature('cons')


a = Segment('a', {cons: '-'})
b = Segment('b', {cons: '+'})


segment_table = SegmentTable([a, b])


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
"REMOVE_SEGMENT_FROM_EMISSION": 1,
"CHANGE_SEGMENT_IN_EMISSION": 0,
"ADD_EMISSION_TO_STATE": 0,
"REMOVE_EMISSION_FROM_STATE": 0,
"INCREASE_TRANSITION_WEIGHT": 0,
"DECREASE_TRANSITION_WEIGHT": 0,
"INCREASE_EMISSION_WEIGHT": 0,
"DECREASE_EMISSION_WEIGHT": 0,

"DATA_ENCODING_LENGTH_MULTIPLIER": 25,
"HMM_ENCODING_LENGTH_MULTIPLIER": 100,
"RULES_SET_ENCODING_LENGTH_MULTIPLIER": 1,

"CEIL_LOG2": False,
"MORPHEME_BOUNDARY_FLAG": False,
"LENGTHENING_FLAG": False,

"ADD_RULE": 2,
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
"CHANGE_EXISTING_FEATURE_BUNDLE": 4,

"ADD_FEATURE": 1,
"REMOVE_FEATURE": 1,
"CHANGE_FEATURE_VALUE": 1,

"MAX_FEATURE_BUNDLE_IN_CONTEXT": 1,

"MAX_NUMBER_OF_RULES": 5,
"MIN_NUMBER_OF_RULES": 0,

"MAX_NUM_OF_INNER_STATES": 1,
"MIN_NUM_OF_INNER_STATES": 1,

"PRINT_PARSE": True,
"DEBUG_LOGGING_INTERVAL": 100,
}


log_file_template = "{}_abnese_optinal_{}.txt"



data = ['aabab', 'abab', 'babaabab', 'aba', 'aaba', 'babaa',
                     'bb', 'bab', 'bbaabab', 'babaabb', 'aabb', 'abb']


target_hmm = {'q0': ['q1'],
              'q1': (['qf'], ['aabb', 'abb', 'bbaabb', 'aba', 'aaba', 'bbaa', 'bb'])
              }

initial_hmm = {'q0': ['q1'],
              'q1': (['qf'], deepcopy(data))
              }

rule = Rule([], [{"cons": "-"}], [{"cons": "+"}], [{"cons": "+"}], obligatory=False)
target_rule_set = RuleSet([rule])


target_tuple = (target_hmm, target_rule_set)