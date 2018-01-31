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
"MERGE_EMISSIONS": 0,
"ADVANCE_EMISSION": 1,
"CLONE_STATE": 0,
"CLONE_EMISSION": 1,
"SPLIT_EMISSION": 0,
"ADD_STATE": 1,
"REMOVE_STATE": 1,
"MERGE_STATES": 0,
"SPLIT_STATES": 0,
"ADD_TRANSITION": 1,
"REMOVE_TRANSITION": 1,
"ADD_SEGMENT_TO_EMISSION": 1,
"REMOVE_SEGMENT_FROM_EMISSION": 1,
"CHANGE_SEGMENT_IN_EMISSION": 1,
"ADD_EMISSION_TO_STATE": 1,
"ADD_EMISSION_FROM_DATA": 0,
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

log_file_template = "{}_dag_zook_morphology_only_large_{}.txt"

data = ['sakzoka', 'sakgat', 'sakdot', 'saksaat', 'saktask', 'sakkazka', 'sakoad', 'sakkook', 'sakgo', 'sak', 'dogzoka', 'doggat', 'dogdot', 'dogsaat', 'dogtask', 'dogkazka', 'dogoad', 'dogkook', 'doggo', 'dog', 'katzoka', 'katgat', 'katdot', 'katsaat', 'kattask', 'katkazka', 'katoad', 'katkook', 'katgo', 'kat', 'daotzoka', 'daotgat', 'daotdot', 'daotsaat', 'daottask', 'daotkazka', 'daotoad', 'daotkook', 'daotgo', 'daot', 'goodzoka', 'goodgat', 'gooddot', 'goodsaat', 'goodtask', 'goodkazka', 'goodoad', 'goodkook', 'goodgo', 'good', 'gkaszoka', 'gkasgat', 'gkasdot', 'gkassaat', 'gkastask', 'gkaskazka', 'gkasoad', 'gkaskook', 'gkasgo', 'gkas', 'dkozzoka', 'dkozgat', 'dkozdot', 'dkozsaat', 'dkoztask', 'dkozkazka', 'dkozoad', 'dkozkook', 'dkozgo', 'dkoz', 'skadzoka', 'skadgat', 'skaddot', 'skadsaat', 'skadtask', 'skadkazka', 'skadoad', 'skadkook', 'skadgo', 'skad', 'gdaaszoka', 'gdaasgat', 'gdaasdot', 'gdaassaat', 'gdaastask', 'gdaaskazka', 'gdaasoad', 'gdaaskook', 'gdaasgo', 'gdaas', 'tokzoka', 'tokgat', 'tokdot', 'toksaat', 'toktask', 'tokkazka', 'tokoad', 'tokkook', 'tokgo', 'tok', 'ksoagzoka', 'ksoaggat', 'ksoagdot', 'ksoagsaat', 'ksoagtask', 'ksoagkazka', 'ksoagoad', 'ksoagkook', 'ksoaggo', 'ksoag', 'ogtadzoka', 'ogtadgat', 'ogtaddot', 'ogtadsaat', 'ogtadtask', 'ogtadkazka', 'ogtadoad', 'ogtadkook', 'ogtadgo', 'ogtad', 'tasozoka', 'tasogat', 'tasodot', 'tasosaat', 'tasotask', 'tasokazka', 'tasooad', 'tasokook', 'tasogo', 'taso', 'kaoszoka', 'kaosgat', 'kaosdot', 'kaossaat', 'kaostask', 'kaoskazka', 'kaosoad', 'kaoskook', 'kaosgo', 'kaos', 'oktadozoka', 'oktadogat', 'oktadodot', 'oktadosaat', 'oktadotask', 'oktadokazka', 'oktadooad', 'oktadokook', 'oktadogo', 'oktado', 'koadzoka', 'koadgat', 'koaddot', 'koadsaat', 'koadtask', 'koadkazka', 'koadoad', 'koadkook', 'koadgo', 'koad', 'oskozoka', 'oskogat', 'oskodot', 'oskosaat', 'oskotask', 'oskokazka', 'oskooad', 'oskokook', 'oskogo', 'osko', 'ozkazoka', 'ozkagat', 'ozkadot', 'ozkasaat', 'ozkatask', 'ozkakazka', 'ozkaoad', 'ozkakook', 'ozkago', 'ozka', 'agzoka', 'aggat', 'agdot', 'agsaat', 'agtask', 'agkazka', 'agoad', 'agkook', 'aggo', 'ag', 'zookzoka', 'zookgat', 'zookdot', 'zooksaat', 'zooktask', 'zookkazka', 'zookoad', 'zookkook', 'zookgo', 'zook', 'saaszoka', 'saasgat', 'saasdot', 'saassaat', 'saastask', 'saaskazka', 'saasoad', 'saaskook', 'saasgo', 'saas', 'tootzoka', 'tootgat', 'tootdot', 'tootsaat', 'toottask', 'tootkazka', 'tootoad', 'tootkook', 'tootgo', 'toot']

from fst import EPSILON

target_hmm = {'q0': ['q1'],
              'q1': (['q2'], ['sak', 'dog', 'kat', 'daot', 'good', 'gkas', 'dkoz', 'skad', 'gdaas', 'tok', 'ksoag', 'ogtad', 'taso', 'kaos', 'oktado', 'koad', 'osko', 'ozka', 'ag', 'zook','saas', 'toot']),
              'q2': (['qf'], ['zoka', 'gat', 'dot', 'saat', 'task', 'kazka', 'oad', 'kook', 'go', EPSILON])}


target_tuple = (target_hmm, [])