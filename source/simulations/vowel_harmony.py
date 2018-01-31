simulation_number = 1

configurations_dict = \
{
"MUTATE_RULE_SET": 1,
"MUTATE_HMM": 1,


"COMBINE_EMISSIONS": 1,
"ADVANCE_EMISSION": 1,
"CLONE_STATE": 0,
"CLONE_EMISSION": 1,
"ADD_STATE": 1,
"REMOVE_STATE": 1,
"ADD_TRANSITION": 1,
"REMOVE_TRANSITION": 1,
"ADD_SEGMENT_TO_EMISSION": 5,
"REMOVE_SEGMENT_FROM_EMISSION": 5,
"CHANGE_SEGMENT_IN_EMISSION": 5,
"ADD_EMISSION_TO_STATE": 5,
"REMOVE_EMISSION_FROM_STATE": 5,

"DATA_ENCODING_LENGTH_MULTIPLIER": 100,
"HMM_ENCODING_LENGTH_MULTIPLIER": 5,
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

"MAX_FEATURE_BUNDLE_IN_CONTEXT": 2,

"MAX_NUM_OF_INNER_STATES": 5,
"MIN_NUM_OF_INNER_STATES": 1,

"MAX_NUMBER_OF_RULES": 2,
"MIN_NUMBER_OF_RULES": 0,

"MORPHEME_BOUNDARY_FLAG": False,
"LENGTHENING_FLAG": False,
"UNDERSPECIFICATION_FLAG": False,

"INITIAL_TEMPERATURE": 50,
"THRESHOLD": 1,
"COOLING_RATE": 0.999999,
"DEBUG_LOGGING_INTERVAL": 200,
"CLEAR_MODULES_CACHING_INTERVAL": 1000,
"STEPS_LIMITATION": float("inf"),

"LINEAR_DECAY": False
}
segment_table_file_name = "vowel_harmony_segment_table.txt"

log_file_template = "{}_harmony_5_100_{}.txt"

data = ['sadadatata', 'gekezeze', u'ge', u'ga', 'sekekeze', 'gadatata', 'gakakaza', u'gakaza', 'sata', 'sededeteze', 'sekeketete', 'sakada', 'sakakazaza', 'sededezete', u'sakata', 'sedetete', 'sekedeze', 'sadadazaza', 'gakadazaza', 'gekekezete', 'sakatata', 'sakakataza', u'gedete', 'sekedezeze', u'gada', 'gedede', 'gekekete', 'gadataza', u'sadaza', 'gedeketeze', 'gezeze', 'gekedezete', u'gadata', 'gadakatata', 'gadadatata', 'sazaza', 'seteze', 'geketeze', 'gakadatata', u'gakata', 'gadadazaza', 'gedeteze', 'sekekete', 'sadadazata', 'gadadaza', 'sakakatata', u'gekeze', 'gadakazaza', 'gadakazata', 'gadadataza', 'sadakazaza', 'gakakata', u'gedeze', 'gedekeze', 'gadakata', 'sakazata', 'sakakaza', 'gededeteze', u'sadata', 'gezete', 'gekede', 'sekekezete', 'gedetete', 'sedeke', u'gadaza', 'sekeke', u'saka', 'sedekezete', 'sedede', 'sedezete', 'sazata', u'sedete', 'gekeke', u'sakaza', 'gazaza', 'sadakata', 'gadadazata', u'sekeze', u'gekete', 'sekezeze', 'gekedetete', 'gedeke', u'gede', u'gaka', 'sedezeze', 'sakadata', 'gete', 'gedezete', u'geke', 'sakadazata', 'gakadata', u'sekete', 'gadazaza', u'sada', 'gekekeze', 'sededetete', 'sekede', 'sekedete', 'sadaka', 'sedekete', u'sede', 'seketeze', 'gekeketeze', u'sa', 'sete', 'gekedeteze', 'sadazaza', u'sedeze', 'setete', 'gekedeze', u'seke', 'sakadataza', u'se']

target_hmm = {'q0': ['q1'],
              'q1': (['q3', 'q2', 'qf'], ['ga', 'ge', 'sa', 'se']),
              'q2': (['q3','q2','qf'], ['da', 'ka']),
              'q3': (['q3', 'qf'], ['ta', 'za'])
                }

rule = [[{"back": "+"}], [{"back": "-"}], [{"cons": "-", "back": "-"}, {"cons": "+"}], [], True]

target_tuple = (target_hmm, [rule])



