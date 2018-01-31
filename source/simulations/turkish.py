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


segment_table_file_name = "turkish_segment_table.txt"

log_file_template = "{}_turkish_{}.txt"

data = [u'gu', u'sukuzu', 'sakuzuzu', 'gydezyzy', 'gudadata', u'gy', 'gudakuzuta', u'ge', 'sekydezyzy', 'sadadata', u'ga', u'sudazu', 'gykydetezy', 'gudadatata', u'gukuta', 'sededezyzy', u'gudazu', u'sakuta', 'gudatazu', u'syde', 'gekykyte', 'gedezyte', 'sededetezy', 'sykykyzyzy', 'guta', u'gydezy', 'sededezy', 'sedetete', u'guda', u'sydete', 'gydedezy', 'sukukuzu', 'sykydetete', u'syky', u'gedete', 'gedeky', 'gazuta', 'gedekytezy', 'sudakuzu', u'sadazu', u'gada', 'gedede', u'guku', 'gykyzyte', 'sadadazu', 'gekyzyte', u'gekyzy', u'gykyte', u'sekyzy', 'sukuda', 'sydedezy', 'gededete', u'gadata', 'gykykyte', 'sukutazu', 'gadatata', 'gakudazu', 'gudatata', 'gudadatazu', 'sukuzuzu', 'gedetezy', u'sykyzy', 'sykytete', 'gedezyzy', 'sekydetete', 'gukudatazu', 'sekytezy', u'gekyte', u'gakuzu', 'gukuda', 'gudakutata', 'gukutata', 'gukudata', 'sekykyzyzy', u'sekyte', 'sykykyzyte', 'sykykytezy', 'guzuzu', u'sydezy', 'gykyde', 'gudadazuzu', 'gykykytezy', 'gukukuzuzu', 'sudakuta', 'sutata', u'sykyte', 'sydekyzyzy', 'sedekyte', 'sukuzuta', 'sudatazu', 'gukukuzu', 'gakutazu', 'gakudazuta', 'sakudazuzu', u'gadazu', 'sutazu', 'gukukutata', 'gazuzu', 'sudadatata', u'saku', 'gakuda', 'gadakuzuta', u'sedete', u'gakuta', 'gakudatata', 'gadakuta', 'gekytezy', 'gadakutazu', u'sukuta', 'sukudazuta', 'sadadatazu', 'sadakuzuta', 'gykykytete', u'gukuzu', u'sudata', u'suda', u'gudata', u'gedezy', u'sakuzu', u'gede', 'gydezyte', u'gyde', 'syzyzy', u'geky', 'gete', u'gydete', u'gaku', 'sadazuta', u'suku', 'sykydetezy', u'sada', u'gyky', u'sede', u'sadata', 'gydekyzy', 'sadaku', u'seky', u'sy', 'sazuzu', u'gykyzy', u'su', u'sedezy', 'gedekyzyte', 'gekykytete', 'sukudazuzu', 'sydedete', u'sa', u'se']

target_hmm = {'q0': ['q1'],
              'q1': (['q3', 'q2', 'qf'], ['ga', 'ge', 'gu', 'gy', 'sa', 'se', 'su', 'sy']),
              'q2': (['q3','q2','qf'], ['da', 'ku']),
              'q3': (['q3', 'qf'], ['ta', 'zu'])
                }

rule = [[{"back": "+"}], [{"back": "-"}], [{"cons": "-", "back": "-"}, {"cons": "+"}], [], True]

target_tuple = (target_hmm, [rule])

