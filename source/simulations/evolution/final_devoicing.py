from rule import Rule
from rule_set import RuleSet
from segment_table import Segment, SegmentTable, Feature
from copy import deepcopy
simulation_number = 1


cons = Feature('cons')
high = Feature('high')
labial = Feature('labial')
voiceless = Feature('voiceless')
bound = Feature('bound')

a = Segment('a', {cons: '-', high: '-', labial: '-', voiceless: '-', bound: '-'})
i = Segment('i', {cons: '-', high: '+', labial: '-', voiceless: '-', bound: '-'})
b = Segment('b', {cons: '+', high: '-', labial: '+', voiceless: '-', bound: '-'})
d = Segment('d', {cons: '+', high: '-', labial: '-', voiceless: '-', bound: '-'})
F = Segment('F', {cons: '-', high: '-', labial: '-', voiceless: '+', bound: '-'})
morpheme_boundary = Segment('B', {cons: '-', high: '-', labial: '-', voiceless: '-', bound: '+'})

segment_table = SegmentTable([a, i, b, d, F, morpheme_boundary])



configurations_dict = \
{
"MUTATE_RULE_SET": 2,
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

"DATA_ENCODING_LENGTH_MULTIPLIER": 100,
"HMM_ENCODING_LENGTH_MULTIPLIER": 10,
"RULES_SET_ENCODING_LENGTH_MULTIPLIER": 1,

"MORPHEME_BOUNDARY_FLAG": True,
"LENGTHENING_FLAG": False,

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

"MAX_NUMBER_OF_RULES": 10,
"MIN_NUMBER_OF_RULES": 0,

"MAX_NUM_OF_INNER_STATES": 1,
"MIN_NUM_OF_INNER_STATES": 1,

"INITIAL_TEMPERATURE": 80,
"THRESHOLD": 10**-2,
"COOLING_RATE": 0.999995,
"DEBUG_LOGGING_INTERVAL": 100,
"STEPS_LIMITATION": float('inf'),
"LINEAR_DECAY": False
}


log_file_template = "{}_final_devoicing_{}.txt"

data = ['bFibF', 'iidF', 'dbFi', 'iibF', 'bia', 'addF', 'adFbF', 'bFai', 'babF', 'dFibF', 'idFbF', 'idbF', 'bbibF', 'abidF', 'dFdibF', 'bdFadF', 'biadF', 'ddadF', 'dFbibF', 'ddai', 'dadFbF', 'ddFadF', 'abFibF', 'aidi', 'idFbFidF', 'bbFiadF', 'bFdabFdF', 'idFibFdF', 'aibadF', 'abFadbF', 'dbFidFa', 'aabFai', 'adaabF', 'aabFidF', 'dFbFadbF', 'dbFaabF', 'iddFaabF', 'dFbadFibF', 'bdidibF', 'bFdFiaddF', 'ibFbaidF', 'babFiabF', 'dbiibFdF', 'babdFabF', 'idFbaddF', 'aadFdFabF', 'bFdiaddF', 'aiddFidF']


target_hmm = {'q0': ['q1'],
              'q1': (['qf'], ['bFib', 'iid', 'dbFi', 'iib', 'bia', 'add', 'adFb', 'bFai', 'bab', 'dFib', 'idFb', 'idb', 'bbib', 'abid', 'dFdib', 'bdFad', 'biad', 'ddad', 'dFbib', 'ddai', 'dadFb', 'ddFad', 'abFib', 'aidi', 'idFbFid', 'bbFiad', 'bFdabFd', 'idFibFd', 'aibad', 'abFadb', 'dbFidFa', 'aabFai', 'adaab', 'aabFid', 'dFbFadb', 'dbFaab', 'iddFaab', 'dFbadFib', 'bdidib', 'bFdFiadd', 'ibFbaid', 'babFiab', 'dbiibFd', 'babdFab', 'idFbadd', 'aadFdFab', 'bFdiadd', 'aiddFid'])
              }

initial_hmm = {'q0': ['q1'],
              'q1': (['qf'], deepcopy(data))
              }

rule = Rule([], [{"voiceless": "+"}], [{"cons": "+"}], [{"bound": "+"}], True)
target_rule_set = RuleSet([rule])


target_tuple = (target_hmm, target_rule_set)