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
"ADD_SEGMENT_TO_EMISSION": 1,
"REMOVE_SEGMENT_FROM_EMISSION": 1,
"CHANGE_SEGMENT_IN_EMISSION": 1,
"ADD_EMISSION_TO_STATE": 1,
"REMOVE_EMISSION_FROM_STATE": 1,

"DATA_ENCODING_LENGTH_MULTIPLIER": 10,
"HMM_ENCODING_LENGTH_MULTIPLIER": 10,
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

"MAX_NUM_OF_INNER_STATES": 4,
"MIN_NUM_OF_INNER_STATES": 1,

"MAX_NUMBER_OF_RULES": 4,
"MIN_NUMBER_OF_RULES": 0,

"WORD_BOUNDARY_FLAG": False,
"MORPHEME_BOUNDARY_FLAG": False,
"LENGTHENING_FLAG": False,
"UNDERSPECIFICATION_FLAG": False,
"RESTRICTIONS_ON_ALPHABET": False,

"INITIAL_TEMPERATURE": 50,
"THRESHOLD": 1,
"COOLING_RATE": 0.999999,
"DEBUG_LOGGING_INTERVAL": 200,
"CLEAR_MODULES_CACHING_INTERVAL": 1000,
"STEPS_LIMITATION":  float("inf"),

"LINEAR_DECAY": False
}

segment_table_file_name = "finnish_coalescence_segment_table.txt"

log_file_template = "{}_finnish_coalescence_more_suffixes_{}.txt"

data = [u'tattiatten', u'tattiataenta', u'tattiadappe', u'tattiamimbe', u'tattiaanmid', u'tattiaanei', u'tattiaaettiema', u'tattiaapentem', u'tattiaademna', u'tattiaatta', u'tattiapiet', u'tattia', u'teimiatten', u'teimiataenta', u'teimiadappe', u'teimiamimbe', u'teimiaanmid', u'teimiaanei', u'teimiaaettiema', u'teimiaapentem', u'teimiaademna', u'teimiaatta', u'teimiapiet', u'teimia', u'dametten', u'dametaenta', u'damedappe', u'damemimbe', u'dameenmid', u'dameenei', u'dameeettiema', u'dameepentem', u'dameedemna', u'dameetta', u'dameanmid', u'dameanei', u'dameaettiema', u'dameapentem', u'dameademna', u'dameatta', u'damepiet', u'dame', u'maettetten', u'maettetaenta', u'maettedappe', u'maettemimbe', u'maetteenmid', u'maetteenei', u'maetteeettiema', u'maetteepentem', u'maetteedemna', u'maetteetta', u'maetteanmid', u'maetteanei', u'maetteaettiema', u'maetteapentem', u'maetteademna', u'maetteatta', u'maettepiet', u'maette', u'niemdaetetten', u'niemdaetetaenta', u'niemdaetedappe', u'niemdaetemimbe', u'niemdaeteenmid', u'niemdaeteenei', u'niemdaeteeettiema', u'niemdaeteepentem', u'niemdaeteedemna', u'niemdaeteetta', u'niemdaeteanmid', u'niemdaeteanei', u'niemdaeteaettiema', u'niemdaeteapentem', u'niemdaeteademna', u'niemdaeteatta', u'niemdaetepiet', u'niemdaete', u'naettabtten', u'naettabtaenta', u'naettabdappe', u'naettabmimbe', u'naettabanmid', u'naettabanei', u'naettabaettiema', u'naettabapentem', u'naettabademna', u'naettabatta', u'naettabpiet', u'naettab', u'ainiatten', u'ainiataenta', u'ainiadappe', u'ainiamimbe', u'ainiaanmid', u'ainiaanei', u'ainiaaettiema', u'ainiaapentem', u'ainiaademna', u'ainiaatta', u'ainiapiet', u'ainia', u'ippemtten', u'ippemtaenta', u'ippemdappe', u'ippemmimbe', u'ippemanmid', u'ippemanei', u'ippemaettiema', u'ippemapentem', u'ippemademna', u'ippematta', u'ippempiet', u'ippem', u'pamintatten', u'pamintataenta', u'pamintadappe', u'pamintamimbe', u'pamintaanmid', u'pamintaanei', u'pamintaaettiema', u'pamintaapentem', u'pamintaademna', u'pamintaatta', u'pamintapiet', u'paminta', u'pimetten', u'pimetaenta', u'pimedappe', u'pimemimbe', u'pimeenmid', u'pimeenei', u'pimeeettiema', u'pimeepentem', u'pimeedemna', u'pimeetta', u'pimeanmid', u'pimeanei', u'pimeaettiema', u'pimeapentem', u'pimeademna', u'pimeatta', u'pimepiet', u'pime', u'bindattten', u'bindattaenta', u'bindatdappe', u'bindatmimbe', u'bindatanmid', u'bindatanei', u'bindataettiema', u'bindatapentem', u'bindatademna', u'bindatatta', u'bindatpiet', u'bindat', u'bentetten', u'bentetaenta', u'bentedappe', u'bentemimbe', u'benteenmid', u'benteenei', u'benteeettiema', u'benteepentem', u'benteedemna', u'benteetta', u'benteanmid', u'benteanei', u'benteaettiema', u'benteapentem', u'benteademna', u'benteatta', u'bentepiet', u'bente']

target_hmm = {'q0': ['q1'],
              'q1': (['q2','qf'], ['maette','pime','dame','bente','niemdaete','teimia','paminta','tattia','ainia', 'bindat', 'ippem', 'naettab']),
              'q2': (['qf'], ['atta','anei','taenta', 'ademna', 'anmid', 'tten', 'aettiema', "apentem", "mimbe", "piet", "dappe"])}

coalescence_rule = [[{"low": "+"}], [{"low": "-"}], [{"cons": "-", "high": "-", "low":"-"}], [], False]

target_tuple = (target_hmm, [coalescence_rule])

initial_rule_set = [coalescence_rule]