from hmm import HMM
from rule_set import RuleSet
from rule import Rule
from grammar import Grammar
from tests.my_test_case import MyTestCase
from configuration import Configuration
from fst import EPSILON

configurations = Configuration()
import random
import itertools
from functools import reduce
from hypothesis import Hypothesis
from random import shuffle, sample
from fst import EPSILON


class CorpusGenerator(MyTestCase):

    def get_all_outputs(self, hmm, *rules):
        rule_set = []
        real_rules = []
        if rules:
            for rule in rules:
                if not isinstance(rule, Rule):
                    rule = Rule(*rule)
                real_rules.append(rule)

            rule_set = RuleSet(real_rules)

        if isinstance(hmm, dict):
            hmm = HMM(hmm)

        grammar = Grammar(hmm, rule_set)
        all_outputs = grammar.get_all_outputs()
        print(all_outputs)
        print(len(all_outputs))

    def test_generate_kleene_test(self):
        self.initialise_segment_table("plural_english_segment_table.txt")
        hmm = HMM({'q0': ['q1'],
                   'q1': (['q2', 'qf'], ['da', 'ga', 'za', 'ta', 'ka', 'sa']),
                   'q2': (['qf'], ['oz', 'z']),
                   })
        rule = [[{"cons": "+"}], [{"voice": "-"}], [{"voice": "-"}, {"cons": "-", "kleene": True}], [], True]

        self.get_all_outputs(hmm, rule)

    def test_generate_morphology_only(self):
        self.initialise_segment_table("plural_english_segment_table.txt")

        hmm = HMM({'q0': ['q1'],
                   'q1': (['q2', 'q3', 'qf'], ['dag', 'kat', 'dot', 'kod', 'gas', 'toz']),
                   'q2': (['q3', 'qf'], ['zook', 'gos', 'dod']),
                   'q3': (['qf'], ['aso', 'akt', 'ata'])})

        self.get_all_outputs(hmm)

    def test_abnese_lengthening(self):
        configurations["BRACKET_TRANSDUCER"] = True
        self.initialise_segment_table("abnese_lengthening_segment_table.txt")
        configurations["MORPHEME_BOUNDARY_FLAG"] = True
        configurations["LENGTHENING_FLAG"] = True
        hmm = HMM({'q0': ['q1'],
                   'q1': (['qf'], ['aabb', 'abb', 'aba', 'aaba', 'bbaa', 'bbbb', 'abbba', 'abba',
                                   'bb', 'bbb', 'bbba', 'bbbba', 'bbbbb', 'bbbbbb', 'abbbbbba'])
                   })

        rule1 = Rule([], [{"long": "+"}], [], [{}, {"bound": "+"}], obligatory=True)
        rule2 = Rule([], [{"syll": "+"}], [{"cons": "+"}], [{"cons": "+"}], obligatory=True)
        self.get_all_outputs(hmm, rule1, rule2)

    def test_kat_zako_aso(self):
        self.initialise_segment_table("plural_english_segment_table.txt")
        hmm = HMM({'q0': ['q1'],
                   'q1': (['q2', 'q3', 'qf'], ['dag', 'kat', 'dot', 'kod', 'gas', 'toz']),
                   'q2': (['q3', 'qf'], ['zako', 'gos', 'dod']),
                   'q3': (['qf'], ['aso', 'okt', 'ota'])})

        epenthesis_rule = Rule.load(
            [[], [{"cons": "-", "low": "+"}], [{"cons": "+", "cont": "+"}], [{"cons": "+", "cont": "+"}], True])
        assimilation_rule = Rule.load([[{"cons": "+"}], [{"voice": "-"}], [{"voice": "-"}], [], True])
        deletion_rule = Rule([{"cons": "-", "low": "-"}], [], [{"cons": "-", "low": "-"}], [], obligatory=True)

        rule_set = RuleSet([epenthesis_rule, assimilation_rule, deletion_rule])

        grammar = Grammar(hmm, rule_set)
        all_outputs = grammar.get_all_outputs()
        print(all_outputs)
        print(len(all_outputs))

    def test_dag_zook(self):
        from simulations import dag_zook_devoicing as simulation
        self.initialise_simulation(simulation)
        self.initialise_segment_table("plural_english_segment_table.txt")
        hmm = HMM({'q0': ['q1'],
                   'q1': (['q2', 'qf'], ['dag', 'kat', 'dot', 'kod', 'gas', 'toz', 'ata', 'aso']),
                   'q2': (['qf'], ['zook', 'gos', 'dod'])})
        assimilation_rule = Rule.load([[{"cons": "+"}], [{"voice": "-"}], [{"voice": "-"}], [], True])
        rule_set = RuleSet([assimilation_rule])

        grammar = Grammar(hmm, rule_set)
        all_outputs = grammar.get_all_outputs()
        print(all_outputs)
        print(len(all_outputs))

    def test_dag_zook__ilm(self):
        from simulations import dag_zook_ilm
        self.initialise_simulation(dag_zook_ilm)
        self.initialise_segment_table("dag_zook_segments_new.txt")
        hmm = HMM({'q0': ['q1'],
                   'q1': (['q2'],
                          ['sak', 'dog', 'kat', 'daot', 'good', 'gkas', 'dkaz',
                           'skod', 'gdaas', 'tok','ksoag', 'agtod', 'taso',
                           'kaos', 'oktado', 'koad', 'osko', 'ozka', 'ag',
                           'zook', 'saas', 'toot']),
                   'q2': (['qf'],
                          ['zoka', 'gat', 'dot', 'saat', 'tsk', 'gozka', 'oad',
                           'ook', 'go', 'ktas', EPSILON])})
        # assimilation_rule = Rule.load([[{"cons": "+"}], [{"voice": "-"}], [{"voice": "-"}], [], True])
        # rule_set = RuleSet([assimilation_rule])

        grammar = Grammar(hmm, RuleSet([]))
        all_outputs = grammar.get_all_outputs()
        print(all_outputs)
        print(len(all_outputs))

    def test_russian(self):
        from simulations import russian_devoicing as simulation
        self.initialise_simulation(simulation)
        self.initialise_segment_table("russian_segment_table.txt")
        hmm = simulation.target_hmm
        devoice = Rule.load([[{"cons": "+"}], [{"voice": "-"}], [], [{'WB': True}], False])
        rule_set = RuleSet([#Rule.load(simulation.xdel1),
                            Rule.load(simulation.devoicing_rule),
            Rule.load(simulation.xdel2)
        ])

        grammar = Grammar(hmm, rule_set)
        all_outputs = grammar.get_all_outputs()
        print(all_outputs)
        print(len(all_outputs))

    def test_english_morphology_only(self):
        from simulations import english_morphology_only as simulation
        self.initialise_simulation(simulation)

        hmm = HMM({'q0': ['q1'], 'q1': (['q2'],
                                        ['rent', 'komit', 'straik', 'drink', 'park', 'teik', 'strap', 'slip', 'kros',
                                         'pleis', 'ameiz', 'analaiz', 'klin', 'kontrol', 'glu', 'ski', 'spil', 'raid',
                                         'bang', 'brag', 'klaimb', 'disturb', 'konsider', 'triger', 'drim']),
                   'q2': (['qf'], ['z', 'i', 'ing', 'al', 'er', 'ans', 'abl', 'ment', 'ion', EPSILON])})
        rule_set = RuleSet([])

        grammar = Grammar(hmm, rule_set)
        all_outputs = grammar.get_all_outputs()
        print(sorted(all_outputs))
        print(len(all_outputs))
        h = Hypothesis(grammar)
        print(h.get_energy())
        print(h.get_recent_energy_signature())

    def test_tom_sawyer_english_aspiration(self):
        from simulations import tom_sawyer_english_aspiration as simulation
        self.initialise_simulation(simulation)

        target_data = simulation.data_without_aspiration
        hmm = HMM({'q0': ['q1'], 'q1': (['qf'], target_data)})

        aspiration_rule = Rule.load([[], [{"sg": "+"}], [{"cont": "-", "voice": "-"}], [{"cons": "-"}], True])
        rule_set = RuleSet([aspiration_rule])

        grammar = Grammar(hmm, rule_set)
        all_outputs = grammar.get_all_outputs()
        print(sorted(all_outputs))
        print(len(all_outputs))
        h = Hypothesis(grammar)
        print(h.get_energy())
        print(h.get_recent_energy_signature())

    def test_english_devoicing(self):
        from simulations import english_devoicing as simulation
        self.initialise_simulation(simulation)

        hmm = HMM({'q0': ['q1'], 'q1': (['q2'],
                                        ['rent', 'komit', 'straik', 'drink', 'park', 'teik', 'strap', 'slip', 'kros',
                                         'pleis', 'ameiz', 'analaiz', 'klin', 'kontrol', 'glu', 'ski', 'spil', 'raid',
                                         'bang', 'brag', 'klaimb', 'disturb', 'konsider', 'triger', 'drim']),
                   'q2': (['qf'], ['z', 'i', 'ing', 'al', 'er', 'ans', 'abl', 'ment', 'ion', EPSILON])})

        # hmm = HMM(simulation.initial_hmm)

        assimilation_rule = Rule.load([[{"son": "-"}], [{"voice": "-"}], [{"voice": "-"}], [], True])
        rule_set = RuleSet([assimilation_rule])

        grammar = Grammar(hmm, rule_set)
        all_outputs = grammar.get_all_outputs()
        print(sorted(all_outputs))
        print(len(all_outputs))
        h = Hypothesis(grammar)
        self.write_to_dot_file(hmm.get_transducer(), 'english')
        print(h.get_energy())
        print(h.get_recent_energy_signature())

    def test_english_two_rules(self):
        from simulations import english_two_rules as simulation
        self.initialise_simulation(simulation)

        hmm = HMM({'q0': ['q1'], 'q1': (['q2'],
                                        ['rent', 'komit', 'straik', 'drink', 'park', 'teik', 'strap', 'slip', 'kros',
                                         'pleis', 'ameiz', 'analaiz', 'klin', 'kontrol', 'glu', 'ski', 'spil', 'raid',
                                         'bang', 'brag', 'klaimb', 'disturb', 'konsider', 'triger', 'drim']),
                   'q2': (['qf'], ['z', 'i', 'ing', 'al', 'er', 'ans', 'abl', 'ment', 'ion', EPSILON])})

        epenthesis_rule = Rule.load([[], [{"high": "+", "back": "-"}], [{"strident": "+"}], [{"strident": "+"}], True])
        assimilation_rule = Rule.load([[{"son": "-"}], [{"voice": "-"}], [{"voice": "-"}], [], True])
        rule_set = RuleSet([epenthesis_rule, assimilation_rule])

        grammar = Grammar(hmm, rule_set)
        all_outputs = grammar.get_all_outputs()
        print(sorted(all_outputs))
        print(len(all_outputs))
        h = Hypothesis(grammar)
        print(h.get_energy())
        print(h.get_recent_energy_signature())

    def test_english_opacity(self):
        from simulations import english_opacity as simulation
        self.initialise_simulation(simulation)

        hmm = HMM({'q0': ['q1'], 'q1': (['q2'],
                                        ['rent', 'komit', 'straik', 'drink', 'park', 'teik', 'strap', 'slip', 'kros',
                                         'pleis', 'ameiz', 'analaiz', 'klin', 'kontrol', 'glu', 'ski', 'spil', 'raid',
                                         'bang', 'brag', 'klaimb', 'disturb', 'konsider', 'triger', 'drim']),
                   'q2': (['qf'], ['z', 'i', 'ing', 'al', 'er', 'ans', 'abl', 'ment', 'ion', EPSILON])})

        assimilation_rule = Rule.load([[{"son": "-"}], [{"voice": "-"}], [{"voice": "-"}], [], True])
        epenthesis_rule = Rule.load([[], [{"high": "+", "back": "-"}], [{"strident": "+"}], [{"strident": "+"}], True])

        rule_set = RuleSet([assimilation_rule , epenthesis_rule])

        grammar = Grammar(hmm, rule_set)
        all_outputs = grammar.get_all_outputs()
        print(sorted(all_outputs))
        print(len(all_outputs))
        h = Hypothesis(grammar)
        # print(h.get_energy())
        # print(h.get_recent_energy_signature())

    def test_dag_zook_devoicing_large(self):
        self.initialise_segment_table("dag_zook_segments_new.txt")
        hmm = HMM({'q0': ['q1'],
                   'q1': (['q2'], ['sak', 'dog', 'kat', 'daot', 'good', 'gkas', 'dkaz', 'skod', 'gdaas', 'tok',
                                   'ksoag', 'agtod', 'taso', 'kaos', 'oktado', 'koad', 'osko', 'ozka', 'ag',
                                   'zook', 'saas', 'toot']),
                   'q2': (['qf'], ['zoka', 'gat', 'dot', 'saat', 'tsk', 'gozka', 'oad', 'ook', 'go', 'ktas', EPSILON])})
        assimilation_rule = Rule.load([[{"cons": "+"}], [{"voice": "-"}], [{"voice": "-"}], [], True])
        rule_set = RuleSet([assimilation_rule])

        grammar = Grammar(hmm, rule_set)
        all_outputs = grammar.get_all_outputs()
        print(sorted(all_outputs))
        print(len(all_outputs))

    def test_dag_zook_large(self):
        self.initialise_segment_table("plural_english_segment_table.txt")
        hmm = HMM({'q0': ['q1'],
                   'q1': (['q2'],  ['sak', 'dog', 'kat', 'daot', 'good', 'gkas', 'dkoz', 'skad', 'gdaas', 'tok', 'ksoag', 'ogtad', 'taso', 'kaos', 'oktado', 'koad', 'osko', 'ozka', 'ag', 'zook','saas', 'toot']),
                   'q2': (['qf'], ['zoka', 'gat', 'dot', 'saat', 'task', 'kazka', 'oad', 'kook', 'go', EPSILON])})
        assimilation_rule = Rule.load([[{"cons": "+"}], [{"voice": "-"}], [{"voice": "-"}], [], True])
        rule_set = RuleSet([assimilation_rule])

        grammar = Grammar(hmm, rule_set)
        all_outputs = grammar.get_all_outputs()
        print(all_outputs)
        print(len(all_outputs))

    def test_dag_zook_morphology_only(self):
        self.initialise_segment_table("plural_english_segment_table.txt")
        hmm = HMM({'q0': ['q1'],
                   'q1': (['q2', 'qf'], ['dag', 'kat', 'dot', 'kod', 'gas', 'toz', 'ata', 'aso']),
                   'q2': (['qf'], ['zook', 'gos', 'dod'])})
        rule_set = RuleSet([])

        grammar = Grammar(hmm, rule_set)
        all_outputs = grammar.get_all_outputs()
        print(all_outputs)
        print(len(all_outputs))

    def test_dag_zook_morphology_only_large(self):
        self.initialise_segment_table("plural_english_segment_table.txt")
        hmm = HMM({'q0': ['q1'],
                   'q1': (['q2'], ['sak', 'dog', 'kat', 'daot', 'good', 'gkas', 'dkoz', 'skad', 'gdaas', 'tok', 'ksoag', 'ogtad', 'taso', 'kaos', 'oktado', 'koad', 'osko', 'ozka', 'ag', 'zook','saas', 'toot']),
                   'q2': (['qf'], ['zoka', 'gat', 'dot', 'saat', 'task', 'kazka', 'oad', 'kook', 'go', EPSILON])})
        rule_set = RuleSet([])

        grammar = Grammar(hmm, rule_set)
        all_outputs = grammar.get_all_outputs()
        print(all_outputs)
        print(len(all_outputs))

    def test_dag_zook_morphology_only_large(self):
        self.initialise_segment_table("plural_english_segment_table.txt")
        hmm = HMM({'q0': ['q1'],
                   'q1': (['q2'], ['sak', 'dog', 'kat', 'daot', 'good', 'gkas', 'dkoz', 'skad', 'gdaas', 'tok', 'ksoag', 'ogtad', 'taso', 'kaos', 'oktado', 'koad', 'osko', 'ozka', 'ag', 'zook','saas', 'toot']),
                   'q2': (['qf'], ['zoka', 'gat', 'dot', 'saat', 'task', 'kazka', 'oad', 'kook', 'go', EPSILON])})
        rule_set = RuleSet([])

        grammar = Grammar(hmm, rule_set)
        all_outputs = grammar.get_all_outputs()
        print(all_outputs)
        print(len(all_outputs))

    # 'skoz', 'gdas',   'kta', 'dgo'

    def test_dag_zook_two_rules(self):
        self.initialise_segment_table("dag_zook_segments_new.txt")
        hmm = HMM({'q0': ['q1'],
              'q1': (['q2'],  ['tak', 'dog', 'kat', 'daot', 'kood', 'gkas', 'dkoz', 'skaz', 'gdaas', 'dok', 'ksoag', 'ogtad', 'taso', 'kaos', 'oktado']),
              'q2': (['qf'], ['zoka', 'go', 'da', 'saat', 'task', 'kazka', EPSILON])})

        epenthesis_rule = Rule.load([[], [{"low": "+"}], [{"coronal": "+"}], [{"coronal": "+"}], True])
        assimilation_rule = Rule.load([[{"cons": "+"}], [{"voice": "-"}], [{"voice": "-"}], [], True])
        rule_set = RuleSet([epenthesis_rule, assimilation_rule])

        grammar = Grammar(hmm, rule_set)
        all_outputs = grammar.get_all_outputs()
        all_outputs.sort()
        print(all_outputs)
        print(len(all_outputs))

    def test_dag_zook_two_rules_large(self):
        self.initialise_segment_table("dag_zook_segments_new.txt")
        hmm = HMM({'q0': ['q1'],
                   'q1': (['q2'], ['sak', 'dog', 'kat', 'daot', 'good', 'gkas', 'dkaz', 'skod', 'gdaas', 'tok',
                                   'ksoag', 'agtod', 'taso', 'kaos', 'oktado', 'koad', 'osko', 'ozka', 'ag',
                                   'zook', 'saas', 'toot']),
                   'q2': (['qf'], ['zoka', 'gat', 'dot', 'saat', 'tsk', 'gozka', 'oad', 'ook', 'go', 'ktas', EPSILON])})

        epenthesis_rule = Rule.load([[], [{"low": "+"}], [{"coronal": "+"}], [{"coronal": "+"}], True])
        assimilation_rule = Rule.load([[{"cons": "+"}], [{"voice": "-"}], [{"voice": "-"}], [], True])
        rule_set = RuleSet([epenthesis_rule, assimilation_rule])

        grammar = Grammar(hmm, rule_set)
        all_outputs = grammar.get_all_outputs()
        all_outputs.sort()
        print(all_outputs)
        print(len(all_outputs))

    def test_dag_zook_opacity(self):
        from simulations import dag_zook_opacity as simulation
        self.initialise_simulation(simulation)

        # self.initialise_segment_table("dag_zook_segments_new.txt")

        hmm = HMM({'q0': ['q1'],
              'q1': (['q2'],  ['tak', 'dog', 'kat', 'daot', 'kood', 'gkas', 'dkoz', 'skaz', 'gdaas', 'dok', 'ksoag', 'ogtad', 'taso', 'kaos', 'oktado']),
              'q2': (['qf'], ['zoka', 'go', 'da', 'saat', 'task', 'kazka', EPSILON])})
        assimilation_rule = Rule.load([[{"cons": "+"}], [{"voice": "-"}], [{"voice": "-"}], [], True])
        epenthesis_rule = Rule.load([[], [{"low": "+"}], [{"coronal": "+"}], [{"coronal": "+"}], True])
        rule_set = RuleSet([assimilation_rule, epenthesis_rule])

        # only epenthesis:   ('kod' 'tooz' 'skoz') * ('zok' 'doad' 'saad')  9
        # only assimilation:  ('dok', 'kaok'  'tak') * ('zok', 'gos', 'doad')     9
        # both:   ('kat', 'doot' 'gaoas' 'gdaas') *('zook','dod','sad') = 12
        grammar = Grammar(hmm, rule_set)
        all_outputs = sorted(grammar.get_all_outputs())
        print(all_outputs)
        print(len(all_outputs))

    def test_dag_zook_opacity_large(self):
        from simulations import dag_zook_opacity_large
        self.initialise_simulation(dag_zook_opacity_large)

        hmm = HMM({'q0': ['q1'],
                   'q1': (['q2'], ['sak', 'dog', 'kat', 'daot', 'good', 'gkas', 'dkaz', 'skod', 'gdaas', 'tok',
                                   'ksoag', 'agtod', 'taso', 'kaos', 'oktado', 'koad', 'osko', 'ozka', 'ag',
                                   'zook', 'saas', 'toot']),
                   'q2': (['qf'], ['zoka', 'gat', 'dot', 'saat', 'tsk', 'gozka', 'oad', 'ook', 'go', 'ktas', EPSILON])})
        assimilation_rule = Rule.load([[{"cons": "+"}], [{"voice": "-"}], [{"voice": "-"}], [], True])
        epenthesis_rule = Rule.load([[], [{"low": "+"}], [{"coronal": "+"}], [{"coronal": "+"}], True])
        rule_set = RuleSet([assimilation_rule, epenthesis_rule])

        grammar = Grammar(hmm, rule_set)
        all_outputs = sorted(grammar.get_all_outputs())
        print(all_outputs)
        print(len(all_outputs))

    def test_dag_zook_opacity_medium(self):
        from simulations import dag_zook_opacity_large
        self.initialise_simulation(dag_zook_opacity_large)

        hmm = HMM({'q0': ['q1'],
                   'q1': (['q2'], ['sak', 'dog', 'kat', 'daot', 'good', 'gkas', 'dkaz', 'skod', 'gdaas', 'tok',
                                   'ksoag', 'agtod', 'taso', 'kaos', 'oktado', 'koad', 'osko', 'ozka', 'ag',
                                   'zook', 'saas', 'toot']),
                   'q2': (['qf'], ['zoka', 'gat', 'dot', 'saat', 'tsk', 'gozka', 'ktas', EPSILON])})
        assimilation_rule = Rule.load([[{"cons": "+"}], [{"voice": "-"}], [{"voice": "-"}], [], True])
        epenthesis_rule = Rule.load([[], [{"low": "+"}], [{"coronal": "+"}], [{"coronal": "+"}], True])
        rule_set = RuleSet([assimilation_rule, epenthesis_rule])

        grammar = Grammar(hmm, rule_set)
        all_outputs = sorted(grammar.get_all_outputs())
        print(all_outputs)
        print(len(all_outputs))

    def test_dag_zook_opacity_extra_large(self):
        from simulations import dag_zook_opacity_large
        self.initialise_simulation(dag_zook_opacity_large)

        hmm = HMM({'q0': ['q1'],
                   'q1': (['q2'], ['sak', 'dog', 'kat', 'daot', 'good', 'gkas', 'dkaz', 'skod', 'gdaas', 'tok',
                                   'ksoag', 'agtod', 'taso', 'kaos', 'oktado', 'koad', 'osko', 'ozka', 'ag',
                                   'zook', 'saas', 'toot']),
                   'q2': (['qf'],
                          ['zoka', 'gat', 'dot', 'saat', 'tsk', 'gozka', 'oad', 'ook', 'go', 'ktas', 'gas', 'daats',
                           'tatko', EPSILON])})
        assimilation_rule = Rule.load([[{"cons": "+"}], [{"voice": "-"}], [{"voice": "-"}], [], True])
        epenthesis_rule = Rule.load([[], [{"low": "+"}], [{"coronal": "+"}], [{"coronal": "+"}], True])
        rule_set = RuleSet([assimilation_rule, epenthesis_rule])

        grammar = Grammar(hmm, rule_set)
        all_outputs = sorted(grammar.get_all_outputs())
        print(all_outputs)
        print(len(all_outputs))

    def test_dag_zook_optionality(self):
        self.initialise_segment_table("opacity_segment_table.txt")
        hmm = HMM({'q0': ['q1'],
                   'q1': (
                       ['q2', 'qf'],
                       ['tak', 'dog', 'kat', 'doot', 'kod', 'gaoas', 'tooz', 'skoz', 'gdaas', 'dok', 'kaok']),
                   'q2': (['qf'], ['zok', 'gos', 'doad', 'saad'])})
        epenthesis_rule = Rule.load([[], [{"cons": "-", "low": "+"}], [{"coronal": "+"}], [{"coronal": "+"}], False])
        rule_set = RuleSet([epenthesis_rule])

        grammar = Grammar(hmm, rule_set)
        all_outputs = grammar.get_all_outputs()
        print(all_outputs)
        print(len(all_outputs))

    def test_rhotic_optionality(self):
        self.initialise_segment_table("cons_optionality_segment_table.txt")
        hmm = HMM({'q0': ['q1'],
                   'q1': (['q2', 'qf'], ['ard', 'dag', 'dora', 'dto', 'gta', 'krato', 'oda', 'raka']),
                   'q2': (['qf'], ['at', 'agod', 'ko', 'oto'])})
        epenthesis_rule = Rule.load([[], [{"rhotic": "+"}], [{"cons": "-"}], [{"cons": "-"}], False])
        rule_set = RuleSet([epenthesis_rule])

        grammar = Grammar(hmm, rule_set)
        all_outputs = grammar.get_all_outputs()
        print(all_outputs)
        print(len(all_outputs))

    def test_dag_zook_opacity_2(self):
        self.initialise_segment_table("opacity_segment_table.txt")
        hmm = HMM({'q0': ['q1'],
                   'q1': (
                       ['q2', 'qf'],
                       ['tak', 'dog', 'kat', 'daot', 'kod', 'gkas', 'dkoz', 'skaz', 'gdaas', 'dok', 'ksaok']),
                   'q2': (['qf'], ['zoka', 'go', 'da', 'saat'])})
        assimilation_rule = Rule.load([[{"cons": "+"}], [{"voice": "-"}], [{"voice": "-"}], [], True])
        epenthesis_rule = Rule.load([[], [{"low": "+"}], [{"coronal": "+"}], [{"coronal": "+"}], True])
        rule_set = RuleSet([assimilation_rule, epenthesis_rule])

        # only epenthesis:   ('kod' 'tooz' 'skoz') * ('zok' 'doad' 'saad')  9
        # only assimilation:  ('dok', 'kaok'  'tak') * ('zok', 'gos', 'doad')     9
        # both:   ('kat', 'doot' 'gaoas' 'gdaas') *('zook','dod','sad') = 12
        grammar = Grammar(hmm, rule_set)
        all_outputs = grammar.get_all_outputs()
        all_outputs.sort()
        print(all_outputs)
        print(len(all_outputs))

    def test_german_opacity(self):
        configurations["WORD_BOUNDARY_FLAG"] = True
        self.initialise_segment_table("german_opacity_segment_table.txt")
        hmm = HMM({'q0': ['q1'],
                   'q1': (
                       ['q2', 'qf'], ['ci', 'na', 'tur', 'cir', 'tar', 'tru', 'cra', 'axtu', 'icna', 'tanir', 'trani']),
                   'q2': (['qf'], ['in', 'cun'])})

        backing_rule = Rule.load([[{"velar": "+"}], [{"back": "+"}], [{"back": "+", "cons": "-"}], [], True])
        vocalization_rule = Rule.load([[{"low": "+"}], [{"cons": "-", "coronal": "-"}], [], [{"cons": "+"}], True])

        print(backing_rule.get_segment_representation())
        print(vocalization_rule.get_segment_representation())
        rule_set = RuleSet([backing_rule, vocalization_rule])

        grammar = Grammar(hmm, rule_set)
        all_outputs = grammar.get_all_outputs()
        print(all_outputs)
        print(len(all_outputs))
        assert "turin" in all_outputs
        assert "tua" in all_outputs
        assert "tuain" not in all_outputs

    def test_german_vocalization_only(self):
        configurations["WORD_BOUNDARY_FLAG"] = True
        self.initialise_segment_table("german_opacity_segment_table.txt")
        hmm = HMM({'q0': ['q1'],
                   'q1': (
                       ['q2', 'qf'], ['ci', 'na', 'tur', 'cir', 'tar', 'tru', 'cra', 'axtu', 'icna', 'tanir', 'trani']),
                   'q2': (['qf'], ['in', 'cun'])})

        vocalization_rule = Rule.load([[{"low": "+"}], [{"cons": "-", "coronal": "-"}], [], [{"cons": "+"}], True])

        print(vocalization_rule.get_segment_representation())
        rule_set = RuleSet([vocalization_rule])

        grammar = Grammar(hmm, rule_set)
        all_outputs = grammar.get_all_outputs()
        print(all_outputs)
        print(len(all_outputs))
        assert "turin" in all_outputs
        assert "tua" in all_outputs
        assert "tuain" not in all_outputs

    def test_mini_german_opacity(self):
        configurations["WORD_BOUNDARY_FLAG"] = True
        self.initialise_segment_table("german_opacity_segment_table.txt")
        hmm = HMM({'q0': ['q1'],
                   'q1': (['q2', 'qf'], ['tur']),
                   'q2': (['qf'], ['in', 'cun'])})

        backing_rule = Rule.load([[{"velar": "+"}], [{"back": "+"}], [{"back": "+", "cons": "-"}], [], True])
        vocalization_rule = Rule.load([[{"low": "+"}], [{"cons": "-", "coronal": "-"}], [], [{"cons": "+"}], True])

        print(backing_rule.get_segment_representation())
        print(vocalization_rule.get_segment_representation())
        rule_set = RuleSet([backing_rule, vocalization_rule])

        grammar = Grammar(hmm, rule_set)
        all_outputs = grammar.get_all_outputs()
        print(all_outputs)
        print(len(all_outputs))

    def test_finnish_coalescence(self):
        self.initialise_segment_table("finnish_coalescence_segment_table.txt")
        hmm = HMM({'q0': ['q1'],
                   'q1': (['q2', 'qf'],
                          ['maette', 'pime', 'dame', 'bente', 'niemdaete', 'teimia', 'paminta', 'tattia', 'ainia',
                           'bindat', 'ippem', 'naettab']),
                   'q2': (['qf'],
                          ['atta', 'anei', 'taenta', 'ademna', 'anmid', 'tten', 'aettiema', "apentem", "mimbe", "piet",
                           "dappe"])})
        rule = Rule.load([[{"low": "+"}], [{"low": "-"}], [{"cons": "-", "high": "-", "low": "-"}], [], False])

        rule_set = RuleSet([rule])
        print(rule.get_segment_representation())
        grammar = Grammar(hmm, rule_set)
        all_outputs = grammar.get_all_outputs()
        print(all_outputs)
        print(len(all_outputs))

    def test_icelandic_umlaut(self):
        self.initialise_segment_table("icelandic_umlaut_segment_table.txt")
        hmm = HMM({'q0': ['q1'],
                   'q1': (['q2', 'qf'],
                          ['dam', 'mudat', 'durpam', 'rat', 'epura', 'parmat', 'puduret', 'pa', 'remp', 'murta',
                           'peta']),
                   'q2': (['qf'], ['r', 'um', 'ramt', 'umda'])})
        umlaut_rule = Rule.load([[{"low": "+"}], [{"round": "+"}], [], [{"cons": "+"}, {"round": "+"}], True])
        epenthesis_rule = Rule.load([[], [{"low": "-", "round": "+"}], [{"cons": "+"}], [{"rhotic": "+"}], True])
        rule_set = RuleSet([umlaut_rule, epenthesis_rule])
        grammar = Grammar(hmm, rule_set)
        all_outputs = grammar.get_all_outputs()
        print(all_outputs)
        print(len(all_outputs))

    def test_vowel_harmony(self):
        self.initialise_segment_table("vowel_harmony_segment_table.txt")
        hmm = HMM({'q0': ['q1'],
                   'q1': (['q2', 'qf'], ['ga', 'ge', 'sa', 'se']),
                   'q2': (['q3', 'qf'], ['da', 'ka']),
                   'q3': (['qf'], ['ta', 'za'])
                   })
        rule = Rule.load([[{"back": "+"}], [{"back": "-"}], [{"cons": "-", "back": "-"}, {"cons": "+"}], [], True])
        rule_set = RuleSet([rule])
        grammar = Grammar(hmm, rule_set)
        all_outputs = grammar.get_all_outputs()
        print(all_outputs)
        print(len(all_outputs))

    def test_simple_icelandic(self):
        self.initialise_segment_table("simple_icelandic_segment_table.txt")

        new_hmm = {'q0': ['q1'],
                   'q1': (
                       ['q2', 'qf'],
                       ['mirpi', 'drpiam', 'pudri', 'raimpa', 'patii', 'uriap', 'duumu', 'piimr', 'taari']),
                   'q2': (['qf'], ['uma', 'rip', 'uptau', 'rir'])}

        # hmm = HMM({'q0': ['q1'],
        #      'q1': (['q2', 'qf'], ['mirpi', 'drpiam', 'pudri', 'raimpa', 'patii', 'uriap', 'duumu', 'piimr', 'taari']),
        #      'q2': (['qf'], ['uma', 'rip', 'uptau', 'rir'])})


        rounding_rule = Rule([{"high": "+"}], [{"round": "+"}], [], [{"round": "+"}], obligatory=True)
        epenthesis_rule = Rule([], [{"round": "+"}], [], [{"rhotic": "+"}], obligatory=True)
        self.get_all_outputs(new_hmm, rounding_rule, epenthesis_rule)

    def test_manual_vowel_harmony(self):
        corpus = list()
        for stem in ['ga', 'ge', 'sa', 'se']:
            word = stem
            for i in range(3):
                for tuple1 in itertools.product(['da', 'ka'], repeat=i):
                    suffix1 = ''.join(tuple1)
                    word = word + suffix1
                    for j in range(3):
                        for tuple2 in itertools.product(['za', 'ta'], repeat=j):
                            suffix2 = ''.join(tuple2)
                            word = word + suffix2
                            if "e" in word:
                                word = word.replace("a", "e")
                            corpus.append(word)
                            word = stem + suffix1
                    word = stem

        base = [u'gakata', u'gakaza', u'gaka', u'gadata', u'gadaza', u'gada', u'ga', u'gekete', u'gekeze', u'geke',
                u'gedete', u'gedeze', u'gede', u'ge', u'sakata', u'sakaza', u'saka', u'sadata', u'sadaza', u'sada',
                u'sa', u'sekete', u'sekeze', u'seke', u'sedete', u'sedeze', u'sede', u'se']
        print(len(corpus))
        print(corpus)
        sample_corpus = random.sample(corpus, 100)
        print(sample_corpus)

        final_corpus = list(set(base + sample_corpus))
        print(len(final_corpus))
        print(final_corpus)

    def test_turkish(self):
        self.initialise_segment_table("turkish_segment_table.txt")
        hmm = HMM({'q0': ['q1'],
                   'q1': (['q2', 'qf'], ['ga', 'ge', 'gu', 'gy', 'sa', 'se', 'su', 'sy']),
                   'q2': (['q3', 'qf'], ['da', 'ku']),
                   'q3': (['qf'], ['ta', 'zu'])
                   })
        rule = Rule.load([[{"back": "+"}], [{"back": "-"}], [{"cons": "-", "back": "-"}, {"cons": "+"}], [], True])
        rule_set = RuleSet([rule])
        grammar = Grammar(hmm, rule_set)
        all_outputs = grammar.get_all_outputs()
        print(all_outputs)
        print(len(all_outputs))

    def test_manual_turkish(self):
        corpus = list()
        for stem in ['ga', 'ge', 'gu', 'gy', 'sa', 'se', 'su', 'sy']:
            word = stem
            for i in range(3):
                for tuple1 in itertools.product(['da', 'ku'], repeat=i):
                    suffix1 = ''.join(tuple1)
                    word = word + suffix1
                    for j in range(3):
                        for tuple2 in itertools.product(['zu', 'ta'], repeat=j):
                            suffix2 = ''.join(tuple2)
                            word = word + suffix2
                            if "e" in word or "y" in word:
                                word = word.replace("a", "e")
                                word = word.replace("u", "y")
                            corpus.append(word)
                            word = stem + suffix1
                    word = stem

        base = [u'gadata', u'gadazu', u'gada', u'gakuta', u'gakuzu', u'gaku', u'ga', u'gedete', u'gedezy', u'gede',
                u'gekyte', u'gekyzy', u'geky', u'ge', u'gudata', u'gudazu', u'guda', u'gukuta', u'gukuzu', u'guku',
                u'gu', u'gydete', u'gydezy', u'gyde', u'gykyte', u'gykyzy', u'gyky', u'gy', u'sadata', u'sadazu',
                u'sada', u'sakuta', u'sakuzu', u'saku', u'sa', u'sedete', u'sedezy', u'sede', u'sekyte', u'sekyzy',
                u'seky', u'se', u'sudata', u'sudazu', u'suda', u'sukuta', u'sukuzu', u'suku', u'su', u'sydete',
                u'sydezy', u'syde', u'sykyte', u'sykyzy', u'syky', u'sy']
        print(len(corpus))
        print(corpus)
        sample_corpus = random.sample(corpus, 100)
        print(sample_corpus)

        final_corpus = list(set(base + sample_corpus))
        print(len(final_corpus))
        print(final_corpus)

    def test_real_english_segmentation(self):
        def get_combined_list(suffixes_string, stems_string):
            stem_list = stems_string.split()
            suffixes_string = suffixes_string.replace("NULL", "")
            suffixes_list = suffixes_string.split(".")
            result_list = list()
            for stem in stem_list:
                for suffix in suffixes_list:
                    result_list.append(stem + suffix)
            return result_list

        singnature_and_vaules_tuples = [
            ("NULL.ed.ing.s", "accent add administer afford alert amount appeal assault attempt"),
            ("NULL.ed.er.ing.s", "attack back bath boil borrow charm condition demand down flow"),
            ("NULL.s",
             "abberation abolitionist abortion absence abstractionist abutment accolade accommodation accomodation"),
            ("e.ed.es.ing", "achiev assum brac chang charg compris conced conclud decid describ"),
            ("e.ed.er.es.ing", "advertis announc bak challeng consum enforc gaz glaz invad liv pac"),
            ("NULL.ed.ing", "applaud arrest astound blast bless bloom boast bolster broaden cater"),
            ("NULL.er.ing.s", "blow bomb broadcast deal draw drink dwell farm feed feel"),
            (
                "NULL.d.s",
                "abbreviate accommodate aggravate apprentice arcade balance barbecue bruise catalogue costume"),
            ("NULL.ed.s", "acclaim beckon benefit blend blister bogey bother breakfast buffet burden")
        ]

        # print words
        # result_list = list()
        # for tuple_ in singnature_and_vaules_tuples:
        #     result_list.extend(get_combined_list(*tuple_))
        # print(result_list)


        # print suffixes
        # print(list(set(".".join([tuple_[0] for tuple_ in singnature_and_vaules_tuples]).split("."))))

        # print stems
        print(sorted((list(set(" ".join([tuple_[1] for tuple_ in singnature_and_vaules_tuples]).split())))))

    def test_german_final_devoicing(self):
        from simulations import german_final_devoicing
        configurations.load_configuration_for_simulation(german_final_devoicing)
        self.initialise_segment_table("german_final_devoicing.txt")
        hmm = HMM({'q0': ['q1', 'q2'],
                   'q1': (['q2', 'q3'], ['aus']),
                   'q2': (['q3'], ['kebab', 'hund', 'tab', 'tag', 'betsug',
                                   'kan', 'tsang', 'aktsend', 'katz', 'umtsug',
                                   'hetz', 'kotz',  'gantz', 'bang', 'knosb',
                                   'begab', 'atvokad', 'adaptiv', 'aktiv',
                                   'devod', 'defekd', 'deftig', 'fiktiv', 'tief'
                                   ]),
                   'q3': (['qf'], [EPSILON, 'e', 'ken', 's', 'en', 'esten']),
                   })
        rule_set = RuleSet([])
        grammar = Grammar(hmm, rule_set)
        all_outputs = grammar.get_all_outputs()
        print(all_outputs)
        print(len(all_outputs))

    def test_german_final_devoicing__less_segments(self):
        from simulations import german_final_devoicing_less_segments
        configurations.load_configuration_for_simulation(german_final_devoicing_less_segments)
        self.initialise_segment_table("german_final_devoicing_less_segments.txt")
        hmm = HMM({'q0': ['q2'],
                   'q2': (['q3'], ['tag', 'katz', 'kotz', 'tsog', 'gag', 'ego',
                                   'zag', 'kaz', 'asked', 'keg', 'akd', 'tsokd',
                                   'kozag', 'zektz', 'kokz', 'steg', 'gasd',
                                   'gosd'
                                   ]),
                   'q3': (['qf'], [EPSILON, 'e', 's']),
                   })
        rule_set = RuleSet([])
        grammar = Grammar(hmm, rule_set)
        all_outputs = grammar.get_all_outputs()
        print(all_outputs)
        print(len(all_outputs))

    def test_dag_zook_noise(self):
        from simulations import dag_zook_noise
        self.initialise_simulation(dag_zook_noise)

        hmm = HMM(dag_zook_noise.target_hmm)
        grammar = Grammar(hmm, RuleSet([Rule(*r) for r in dag_zook_noise.rule_set]))
        all_outputs = grammar.get_all_outputs(with_noise=False)
        noise_outputs = grammar.get_all_outputs(with_noise=True)
        print(all_outputs)
        print((len(all_outputs)))

        print("Possible noise:")
        print(set(noise_outputs) - set(all_outputs))


    def test_german_final_devoicing__minimal(self):
        from simulations import german_final_devoicing_minimal__with_noise
        configurations.load_configuration_for_simulation(german_final_devoicing_minimal__with_noise)
        self.initialise_segment_table("german_final_devoicing.txt")
        hmm = HMM({'q0': ['q1'],
                   'q1': (['q2'], ['kebab', 'hund', 'tab', 'tag', 'betsug',
                                   'kan', 'tsang', 'aktsend', 'katz', 'umtsug',
                                   'hetz', 'kotz',  'gantz', 'bang', 'knosb',
                                   'begab', 'atvokad', 'aktiv',
                                   'devod', 'deftig',
                                   ]),
                   'q2': (['qf'], [EPSILON, 'e', 'ken', 'en', 'esten']),
                   })
        rule = Rule(*[[{"nasal": "-", "cons": "+"}], [{"voice": "-"}], [], [{"WB": True}], True])
        rule_set = RuleSet([rule])
        grammar = Grammar(hmm, rule_set)
        all_outputs = grammar.get_all_outputs()
        print(all_outputs)
        print(len(all_outputs))

    def test_german_final_devoicing__mini_minimal(self):
        from simulations import german_final_devoicing_minimal__with_noise
        configurations.load_configuration_for_simulation(german_final_devoicing_minimal__with_noise)
        self.initialise_segment_table("german_final_devoicing.txt")
        hmm = HMM({'q0': ['q1'],
                   'q1': (['q2'], ['kebab', 'hund', 'tab', 'tag', 'betsug',
                                   'kan', 'tsang', 'aktsend', 'katz', 'umtsug',
                                   ]),
                   'q2': (['qf'], [EPSILON, 'e', 'ken', 'en', 'esten']),
                   })
        rule = Rule(*[[{"nasal": "-", "cons": "+"}], [{"voice": "-"}], [], [{"WB": True}], True])
        rule_set = RuleSet([rule])
        grammar = Grammar(hmm, rule_set)
        all_outputs = grammar.get_all_outputs()
        print(all_outputs)
        print(len(all_outputs))

    def test_(self):
        vowels = ['a', 'i']
        consonants = ['b', 'd', 'p', 't']
        segments = vowels + consonants

        words_pool = []
        from itertools import product

        min_word_size = 3
        max_word_size = 6

        for i in range(min_word_size, max_word_size + 1):
            words_pool.extend([''.join(t) for t in product(''.join(segments), repeat=i)])

        forbiden_sequences = [''.join(t) for t in product(''.join(vowels), repeat=3)] + \
                             [''.join(t) for t in product(''.join(consonants), repeat=3)]

        words_pool = [word for word in words_pool if
                      not any(forbiden_sequence in word for forbiden_sequence in forbiden_sequences)]

        words_pool = [word.replace('t', 'dF').replace('p', 'bF') for word in words_pool]

        words_pool = [word for word in words_pool if (word[-1] in ['F'] + vowels)]

        random.shuffle(words_pool)

        F_ratio = 0.8

        F_words = [word for word in words_pool if (word[-1] in ['F'])]
        V_words = [word for word in words_pool if (word[-1] in vowels)]

        V_words_allowed = int(len(F_words) * (1 / F_ratio) - len(F_words))
        V_words = V_words[:V_words_allowed]
        words_pool = V_words + F_words
        random.shuffle(words_pool)

        from collections import defaultdict
        from math import ceil
        words_by_F_less_length_dict = defaultdict(list)

        for word in words_pool:
            words_by_F_less_length_dict[len(word.replace('F', ''))].append(word)

        number_of_words_to_select = 50
        number_of_words_to_select_from_each = int(ceil(number_of_words_to_select / len(words_by_F_less_length_dict)))

        words = []
        for key_ in words_by_F_less_length_dict:
            words.extend(words_by_F_less_length_dict[key_][:number_of_words_to_select_from_each])

        print(words)
        print(len(words))

        words_with_removed_final_F = []
        for word in words:
            if word[-1] == 'F':
                words_with_removed_final_F.append(word[:-1])
            else:
                words_with_removed_final_F.append(word)

        print(words_with_removed_final_F)

    def test_2(self):
        class CorpusGenerator:
            def __init__(self, consonants, vowels, list_of_syllables):
                self.consonants = consonants
                self.vowels = vowels
                self.list_of_syllables = list_of_syllables

            def get_words(self, limit=None):
                words = []
                if limit:
                    syllable_limit = limit / len(self.list_of_syllables)

                for syllable in self.list_of_syllables:
                    syllable_words = self.get_words_from_syllable(syllable)
                    if limit:
                        if syllable_limit < len(syllable_words):
                            syllable_words = sample(syllable_words, syllable_limit)
                    words.extend(syllable_words)

                return list(set(words))

            def get_words_from_syllable(self, syllable):
                def binary_concatenation(A, B):
                    return [a + b for a in A for b in B]

                def concatenate(sets):
                    return reduce(binary_concatenation, sets)

                mapping = {'C': consonants,
                           'V': vowels}
                words = concatenate([mapping[i] for i in syllable])
                return words

        consonants = ['m', 'r', 't', 'd', 'k', 'g']
        vowels = ['e', 'a', 'u']
        syllables = ["CVCVC", "CVCCVC", "CVCVCC", "CVCC", "VCC"]
        corpus_generator = CorpusGenerator(consonants, vowels, syllables)

        words = corpus_generator.get_words(limit=1000)

        # print(sample_words)


        self.initialise_segment_table("icelandic_umlaut_no_morphology_segment_table.txt")

        result_tuples = []
        for word in words:
            hmm = HMM({'q0': ['q1'],
                       'q1': (['qf'], [word])
                       })
            umlaut_rule = Rule.load(
                [[], [{"round": "+", "back": "-"}], [{"low": "+"}], [{"cons": "+"}, {"round": "+"}], True])
            u_epenthesis_rule = Rule.load([[], [{"low": "-", "back": "+"}], [{"cons": "+"}], [{"rhotic": "+"}], True])
            rule_set = RuleSet([umlaut_rule, u_epenthesis_rule])
            grammar = Grammar(hmm, rule_set)
            output = grammar.get_all_outputs()[0]
            result_tuples.append((word, output))

        Y_counter = 0
        Cr_counter = 0
        aCu_counter = 0

        Cr_list = ["{}r".format(cons) for cons in consonants]
        aCu_list = ["a{}u".format(cons) for cons in consonants]

        selected_tuples = []
        for result_tuple in result_tuples:

            if "Y" in result_tuple[1] and Y_counter < 25:
                selected_tuples.append(result_tuple)
                Y_counter += 1

            elif any(substring in result_tuple[1] for substring in aCu_list) and aCu_counter < 5:
                selected_tuples.append(result_tuple)
                aCu_counter += 1

            elif any(substring in result_tuple[0] for substring in Cr_list) and Cr_counter < 25:
                selected_tuples.append(result_tuple)
                Cr_counter += 1

        print(selected_tuples)

    def test_icelandic_umlaut_no_morphology_only_Y(self):
        self.initialise_segment_table("icelandic_umlaut_no_morphology_segment_table.txt")
        inputs = ['meur', 'ruem', 'gaag', 'deag', 'uat', 'katr', 'derr', 'edr', 'dekruk', 'marut', 'amr', 'damuk',
                  'gamuk', 'tedruk', 'merrer', 'medr', 'kudr', 'ramutk', 'remr', 'redrem', 'ugr', 'matram', 'gegr',
                  'memegr', 'rerr', 'magram', 'kakekr', 'tederr', 'kamr', 'ruratr', 'tatum', 'akr', 'mamakr', 'ekr',
                  'redr', 'makred', 'kutegr', 'darut', 'gamud', 'mudr', 'karrad', 'err', 'ragug', 'taruk', 'gatukd',
                  'katudt', 'tamug', 'mamudt', 'madum', 'rakutm', 'kamut', 'kamud', 'kakudg', 'mamuk', 'tagurk',
                  'tarugr', 'dadugk', 'tarumm', 'ramud', 'kaduk']

        hmm = {'q0': ['q1'],
               'q1': (['qf'], inputs)
               }

        rule = [[], [{"round": "+", "back": "-"}], [{"low": "+"}], [{"cons": "+"}, {"round": "+"}], True]

        self.get_all_outputs(hmm, rule)

    def test_generate_turkish_corpus(self):
        self.initialise_segment_table("turkish_segment_table.txt")
        stems = ['ip', 'el', 'k1z', 'jyz', 'pul', 'sap', 'k0j', 'sor']
        suffixes = ['lar', '1n']

        # base_corpus = self.genereate_corpus(stems, suffixes)

        rule = [[{"syll": "+"}], [{"back": "-"}], [{"syll": "+", "back": "-"}, {"syll": "-", "kleene": True}], [], True]

        target_hmm = {'q0': ['q1'],
                      'q1': (['q2', 'qf'], ['il', 'lar', 'pos', 'rek']),
                      'q2': (['qf'], ['1p', 'al', 'k1z', 'juz', 'pul', 'sap', 'koj', 'sor', 'z1k', 'rus']),
                      }

        self.get_all_outputs(target_hmm, rule)

    def test_generate_turkish_corpus_new(self):
            from simulations import turkish_vowel_harmony_new
            self.initialise_simulation(turkish_vowel_harmony_new)

            # base_corpus = self.genereate_corpus(stems, suffixes)

            rule = [[{"syll": "+"}], [{"back": "-"}], [{"syll": "+", "back": "-"}, {"syll": "-", "kleene": True}], [],
                    True]

            target_hmm = {'q0': ['q1'],
                          'q1': (['q2'], ['gyn', 'g0z', 'ip', 'kedi', 'kent', 'kurt', 'renk', 'j1l', 'tuz', 'sokak']),

                          'q2': (['qf'], ['lar', 's1z', '1', 'tan', 'sal', 'l1k', 'a', EPSILON]),
                          }


            # target_hmm = {'q0': ['q1'],
            #               'q1': (['q2'], ['gyn', 'g0z', 'k0k', 'kent', 'renk', 'kurt', 'j1l', 'tuz', 'josun',
            #                               'dal', 'ip', 'el', 'kedi', 'k1z', 'son', 'sokak',
            #                               'k0j', 'kirpi',
            #                               ]),
            #
            #               'q2': (['qf'], ['1n', 'lar', 's1z', '1', 'tan', 'sal', 'l1k', 'l1', 'a', EPSILON]),
            #               }

            rule = Rule(*rule)
            rule_set = RuleSet([rule])
            grammar = Grammar(target_hmm, rule_set)
            all_outputs = grammar.get_all_outputs()
            #all_outputs = random.sample(all_outputs, 200)
            print(all_outputs)
            print(len(all_outputs))


    def test_generate_french_deletion_corpus(self):
        from simulations import french_deletion_new
        self.initialise_simulation(french_deletion_new)

        hmm = HMM({'q0': ['q1'],
              'q1': (['qf'], ['absans', 'admir', 'adorabl', 'aktif', 'arab', 'arbr', 'brylabl', 'byvabl', 'dyr', 'fiabl', 'fiksabl', 'final', 'finir', 'fumabl', 'fur', 'furyr', 'fylar', 'kadr', 'kafar', 'kalkyl', 'kapabl', 'karaf', 'katr', 'kudr', 'kupl', 'kyrabl', 'lavabl', 'luabl', 'mais', 'mutar', 'nyl', 'ordr', 'orl', 'ovni', 'parkur', 'parl', 'partir', 'pip', 'polar', 'posibl', 'postyr', 'potabl', 'prut', 'purir', 'pys', 'ridikyl', 'ryptyr', 'saly', 'sibl', 'sidr', 'sifl', 'sirkl', 'sortir', 'stad', 'stryktyr', 'subtil', 'supl', 'tabl', 'titr', 'trubl', 'vivabl', 'yrl']),
              })

        l_deletion = Rule.load([[{"liquid": "+"}], [], [{"cons": "+", "son": "-"}], [], False])
        rule_set = RuleSet([l_deletion])
        grammar = Grammar(hmm, rule_set)
        all_outputs = grammar.get_all_outputs()
        print(sorted(all_outputs))
        print(len(all_outputs))

    def test_generate_french_deletion_no_sab_corpus(self):
        # configurations['WORD_BOUNDARY_FLAG'] = True
        from simulations import french_deletion_new_no_sab as simulation
        self.initialise_simulation(simulation)
        self.initialise_segment_table("french_deletion_new.txt")
        hmm = HMM({'q0': ['q1'],
                   'q1': (['qf'],
                          ['adorabl', 'aktif', 'arab', 'arbr', 'brylabl', 'byvabl', 'dyr', 'stad', 'fiabl', 'fiksabl',
                           'finir', 'fumabl', 'fur', 'furyr', 'fylar', 'kadr', 'kafar', 'kalkyl', 'kapabl', 'karaf',
                           'katr', 'kudr', 'kupl', 'kyrabl', 'lavabl', 'luabl', 'mais', 'nyl', 'ordr', 'orl', 'final',
                           'parkur', 'parl', 'partir', 'pip', 'polar', 'posibl', 'postyr', 'potabl', 'prut', 'purir',
                           'pys', 'ridikyl', 'ryptyr', 'saly', 'sibl', 'sidr', 'sifl', 'sirkl', 'sortir', 'stryktyr',
                           'supl', 'tabl', 'mutar', 'titr', 'trubl', 'vivabl', 'yrl', 'sabl']),
              })

        l_deletion = Rule.load([[{"liquid": "+"}], [], [{"cons": "+", "son": "-"}], [], False])
        rule_set = RuleSet([l_deletion])
        grammar = Grammar(hmm, rule_set)
        all_outputs = grammar.get_all_outputs()
        print(sorted(all_outputs))
        print(len(all_outputs))

    def test_generate_french_two_rules_corpus(self):
        from simulations import french_two_rules as simulation
        self.initialise_simulation(simulation)
        hmm = HMM({'q0': ['q1'],
                   'q1': (['q2'],
                          ['klop', 'kylt', 'provok', 'prut', 'klad', 'krab', 'mordr', 'tabl', 'arbr', 'parl',
                           'yrl', 'tyrk', 'kurb', 'kapt', 'kupl', 'film', 'odor', 'amur', 'karaf', 'furyr', 'byl',
                           'batir', 'purpr', 'kuverkl', 'filtr', 'rompr', 'dartr', 'bibl', 'ofr', 'vitr']),
                   'q2': (['qf'], ['kif', 'timid', 'fad', 'mal', 'byvabl', 'puri', 'abil', 'ivr', 'dubl', 'futr', 'byfl', 'formidabl', 'probabl', EPSILON])
                   # 'q3': (['qf'], ['posibl', 'probabl', 'brylabl', 'byvabl', 'puri', 'ridikyl'])
                   # 'q2': (['q4'], ['mord', 'parl', 'frap']),
                   # 'q4': (['qf'], ['la', 'nu'])
                   })
        schwa_epenthesis = Rule.load([[], [{"center": "+"}], [{"cons": "+"}, {"cons": "+"}], [{"MB": True}, {"cons": "+"}], False])
        l_deletion = Rule.load([[{"liquid": "+"}], [], [{"cons": "+", "son": "-"}], [{"MB": True}], False])
        rule_set = RuleSet([schwa_epenthesis, l_deletion])
        grammar = Grammar(hmm, rule_set)
        grammar_transducer = grammar.get_transducer()
        print(len(grammar_transducer))
        self.write_to_dot_file(grammar_transducer, 'french_two_rules')
        h = Hypothesis(grammar)
        h.get_energy()

        # self.write_to_dot_file(hmm.get_transducer(), "french_hmm_transducer")

        all_outputs = grammar.get_all_outputs()
        print(sorted(all_outputs))
        print(len(all_outputs))

        print(h.get_recent_energy_signature())

    def test_generate_french_two_rules_boundary_symbol_corpus(self):
        from simulations import french_two_rules_boundary_symbol as simulation
        self.initialise_simulation(simulation)
        hmm = HMM({'q0': ['q1'],
                   'q1': (['q2'],
                          ['klop', 'kylt', 'provok', 'prut', 'klad', 'krab', 'mordr', 'tabl', 'arbr', 'parl',
                           'yrl', 'burk', 'kurb', 'kapt', 'kupl', 'film', 'odor', 'amur', 'karaf', 'furyr', 'byl',
                           'batir', 'purpr', 'kuverkl', 'filtr', 'rompr', 'dartr']),
                   'q2': (['q3', 'qf'], ['X']),
                   'q3': (['q4'], ['kif', 'timid', 'fad', 'mal', 'byvabl', 'puri', 'abil', 'ivr']),
                   'q4': (['qf'], ['X'])})

        schwa_epenthesis = Rule.load([[], [{"center": "+"}], [{"cons": "+"}, {"cons": "+"}], [{"mb": "+"}, {"cons": "+"}], False])
        l_deletion = Rule.load([[{"liquid": "+"}], [], [{"cons": "+", "son": "-"}], [{"mb": "+"}], False])
        rule_set = RuleSet([l_deletion, schwa_epenthesis])
        grammar = Grammar(hmm, rule_set)
        trans = grammar.get_transducer()
        # print(len(trans))
        self.write_to_dot_file(trans, 'french_mb_transducer')

        all_outputs = grammar.get_all_outputs()
        print(sorted(all_outputs))
        print(len(all_outputs))
        hypo = Hypothesis(grammar)
        print(hypo.get_energy())
        print(hypo.get_recent_energy_signature())

    def test_generate_french_two_rules_small_corpus(self):
        from simulations import french_two_rules_extra_small as simulation
        self.initialise_simulation(simulation)
        hmm = HMM({'q0': ['q1'],
                   'q1': (['q3'],
                          ['tabl', 'arbr', 'livr', 'kuverkl', 'fil', 'parl', 'purpr', 'filtr', 'krab', 'klop', 'grat',
                          'sak', 'strof', 'esclav', 'rob']),
                   'q3': (['qf'], ['sal', 'fiabl', 'supl', 'puri', 'abil', 'timid', 'bas', 'fad', EPSILON])}
                  )
        schwa_epenthesis = Rule.load([[], [{"center": "+"}], [{"cons": "+"}, {"cons": "+"}], [{"MB": True}, {"cons": "+"}], False])
        l_deletion = Rule.load([[{"liquid": "+"}], [], [{"cons": "+", "son": "-"}], [{"MB": True}], False])
        rule_set = RuleSet([schwa_epenthesis, l_deletion])
        self.write_to_dot_file(hmm.get_transducer(), 'french_true_mb_hmm_transducer')
        grammar = Grammar(hmm, rule_set)
        trans = grammar.get_transducer()
        self.write_to_dot_file(trans, 'bleeding_transducer')
        all_outputs = grammar.get_all_outputs()
        print(sorted(all_outputs))
        print(len(all_outputs))

    def test_generate_french_two_rules_extra_small_corpus(self):
        from simulations import french_two_rules_extra_small as simulation
        self.initialise_simulation(simulation)
        hmm = HMM({'q0': ['q1'],
                   'q1': (['q2'],
                          ['tabl', 'arbr', 'livr', 'mordr', 'parl', 'atrap', 'motiv', 'bit', 'port']),
                   'q2': (['qf'], ['arab', 'puri', 'timid', 'abil', EPSILON])}
                  )
        schwa_epenthesis = Rule.load([[], [{"center": "+"}], [{"cons": "+"}, {"cons": "+"}], [{"MB": True}, {"cons": "+"}], False])
        l_deletion = Rule.load([[{"liquid": "+"}], [], [{"cons": "+", "son": "-"}], [{"MB": True}], False])
        rule_set = RuleSet([schwa_epenthesis, l_deletion])
        grammar = Grammar(hmm, rule_set)
        all_outputs = grammar.get_all_outputs()
        print(sorted(all_outputs))
        print(len(all_outputs))
        h = Hypothesis(grammar)
        print(h.get_energy())
        print(h.get_recent_energy_signature())

    def test_generate_french_two_rules_extra_small_boundary_symbol_corpus(self):
        from simulations import french_two_rules_extra_small_boundary_symbol as simulation
        self.initialise_simulation(simulation)
        hmm = HMM({'q0': ['q1'],
                   'q1': (['q2'],
                          ['tabl', 'arbr', 'livr', 'mordr', 'parl', 'atrap', 'motiv', 'bit', 'port']),
                   'q2': (['q3', 'qf'], ['X']),
                   'q3': (['q4'], ['arab', 'puri', 'timid', 'abil']),
                   'q4': (['qf'], ['X'])}
                  )
        schwa_epenthesis = Rule.load([[], [{"center": "+"}], [{"cons": "+"}, {"cons": "+"}], [{"mb": "+"}, {"cons": "+"}], False])
        l_deletion = Rule.load([[{"liquid": "+"}], [], [{"cons": "+", "son": "-"}], [{"mb": "+"}], False])

        rule_set = RuleSet([schwa_epenthesis, l_deletion])
        grammar = Grammar(hmm, rule_set)
        self.write_to_dot_file(hmm.get_transducer(), 'french_mb_hmm_transducer')

        all_outputs = grammar.get_all_outputs()
        print(sorted(all_outputs))
        print(len(all_outputs))
        # h = Hypothesis(grammar)
        # trans = grammar.get_transducer()
        # print(len(trans))
        # self.write_to_dot_file(trans, 'french_mb_transducer')
        # print(h.get_energy())
        # print(h.get_recent_energy_signature())

    def test_generate_catalan_small_corpus(self):
        from simulations import catalan_small
        self.initialise_simulation(catalan_small)

        target_hmm = HMM({'q0': ['q1'],
                          'q1': (['q2', 'qf'],
                                 ['plan', 'kuzin', 'silen', 'kaiman', 'katalan', 'kalent', 'blank', 'plasa', 'kasa',
                                  'kamp', 'metal', 'kap', 'mal']),
                          'q2': (['qf'], ['s', 'et', 'ik', 'a']),
                          })

        nasal_deletion = Rule.load([[{"nasal": "+"}], [], [], [{"WB": True}], True])
        cluster_simplification = Rule.load([[{"cont": "-"}], [], [{"nasal": "+"}], [{"WB": True}], True])
        target_rule_set = RuleSet([nasal_deletion, cluster_simplification])
        target_grammar = Grammar(target_hmm, target_rule_set)

        all_outputs = target_grammar.get_all_outputs()
        print(sorted(all_outputs))
        print(len(all_outputs))


    def test_generate_catalan_small_corpus_word_boundary_hack(self):
        # same as catalan_small but with hackish WB using extra segment

        from simulations import catalan_small_wb
        self.initialise_simulation(catalan_small_wb)

        hmm = HMM({'q0': ['q1'],
              'q1': (['q2', 'q3'],
                     ['plan', 'kuzin', 'silen', 'kaiman', 'katalan', 'kalent', 'blank', 'plasa', 'kasa',
                      'kamp', 'metal', 'kap', 'mal']),
              'q2': (['q3'], ['s', 'et', 'ik', 'a']),
              'q3': (['qf'], ['X']),
              })

        nasal_deletion = Rule.load([[{"nasal": "+"}], [], [], [{"wb": "+"}], True])
        cluster_simplification = Rule.load([[{"cont": "-"}], [], [{"nasal": "+"}], [{"wb": "+"}], True])
        rule_set = RuleSet([nasal_deletion, cluster_simplification])
        grammar = Grammar(hmm, rule_set)
        all_outputs = grammar.get_all_outputs()
        print(sorted(all_outputs))
        print(len(all_outputs))

        h = Hypothesis(grammar)
        print(h.get_energy())
        print(h.get_recent_energy_signature())

    def test_generate_catalan_with_engma(self):
        from simulations import catalan_small_with_engma
        self.initialise_simulation(catalan_small_with_engma)

        target_hmm = HMM({'q0': ['q1'],
                          'q1': (['q2', 'qf'],
                                 ['plan', 'kuzin', 'silen', 'katalan', 'kalent', 'blank', 'plasa',
                                  'kamp', 'metal', 'kap', 'mal', 'tank']),
                          'q2': (['qf'], ['s', 'et', 'ik', 'a', 'kasa', 'kaiman']),
                          })

        nasal_deletion = Rule.load([[{"nasal": "+"}], [], [], [{"WB": True}], True])
        nasal_place_assimilation = Rule.load([[{"nasal": "+", "coronal": "+"}], [{"velar": "+", "coronal": "-"}], [], [{"velar": "+"}], True])
        cluster_simplification = Rule.load([[{"cont": "-"}], [], [{"nasal": "+"}], [{"WB": True}], True])
        target_rule_set = RuleSet([nasal_deletion, nasal_place_assimilation, cluster_simplification])
        target_grammar = Grammar(target_hmm, target_rule_set)

        all_outputs = target_grammar.get_all_outputs()
        print(sorted(all_outputs))
        print(len(all_outputs))

        h = Hypothesis(target_grammar)
        print(h.get_energy())
        print(h.get_recent_energy_signature())

    def test_generate_catalan_corpus(self):
        configurations['WORD_BOUNDARY_FLAG'] = True
        self.initialise_segment_table("catalan_segment_table.txt")
        hmm = HMM({'q0': ['q1'],
                   'q1': (['q2'], ["blank", "kamp", "kalent", "profund", "dolent", "bank", "tink", "pikant", "elefant", "lent", "kuzin", "plan", "silen", "gran", "telefon", "katalan", "kaiman", "leon", "prim", "fum", "kap", "armada", "espanol", "metal", "plasa", "blau", "negre", "gris", "brut", "nebot", "espageti", "nasionalisme"]),
                   'q2': (['qf'], ["a", "et", "s", "ik", "estr", EPSILON])
                   })

        nasal_deletion = Rule.load([[{"nasal": "+"}], [], [], [{"WB": True}], True])
        cluster_simplification = Rule.load([[{"cont": "-"}], [], [{"nasal": "+"}], [{"WB": True}], True])
        rule_set = RuleSet([nasal_deletion, cluster_simplification])
        grammar = Grammar(hmm, rule_set)
        all_outputs = grammar.get_all_outputs()
        print(sorted(all_outputs))
        print(len(all_outputs))

    def test_generate_catalan_wb_corpus(self):
        from simulations import catalan_wb as simulation
        self.initialise_simulation(simulation)

        hmm = HMM({'q0': ['q1'],
                   'q1': (['q2', 'q3'],
                          ["blank", "kamp", "kalent", "profund", "dolent", "bank", "tink", "pikant", "elefant", "lent",
                           "kuzin", "plan", "silen", "gran", "telefon", "katalan", "kaiman", "leon", "prim", "fum",
                           "kap", "armada", "espanol", "metal", "plasa", "blau", "negre", "gris", "brut", "nebot",
                           "espageti", "nasionalisme"]),
                   'q2': (['q3'], ["a", "et", "s", "ik", "estr"]),
                   'q3': (['qf'], ["X"])
                   })

        nasal_deletion = Rule.load([[{"nasal": "+"}], [], [], [{"wb": "+"}], True])
        cluster_simplification = Rule.load([[{"cont": "-"}], [], [{"nasal": "+"}], [{"wb": "+"}], True])
        rule_set = RuleSet([nasal_deletion, cluster_simplification])
        grammar = Grammar(hmm, rule_set)
        all_outputs = grammar.get_all_outputs()
        print(sorted(all_outputs))
        print(len(all_outputs))

    def test_word_boundary_corpus(self):
        configurations['WORD_BOUNDARY_FLAG'] = True
        self.initialise_segment_table("dag_zook_segments_new.txt")
        hmm = HMM({'q0': ['q1'],
                   'q1': (['q2', 'qf'], ['dag', 'kad', 'dod', 'kod', 'kos', 'toz', 'atz', 'kaz', 'god', 'goz']),
                   'q2': (['qf'], ['a', 'o'])
                   })

        final_devoicing = Rule.load([[{"cons": "+"}], [{"voice": "-"}], [], [{"WB": True}], True])
        rule_set = RuleSet([final_devoicing])
        grammar = Grammar(hmm, rule_set)
        all_outputs = grammar.get_all_outputs()
        print(sorted(all_outputs))
        print(len(all_outputs))

    def test_generate_catalan_corpus(self):
        self.initialise_segment_table("catalan_segment_table.txt")
        hmm = HMM({'q0': ['q1'],
                   'q1': (['q2', 'q3'], ["blank", "kamp", "kalent", "profund", "dolent", "bank", "tink", "pikant", "elefant", "lent", "kuzin", "plan", "silen", "gran", "telefon", "katalan", "kaiman", "leon", "prim", "fum", "kap", "kasa", "mal", "metal", "plasa", "blau", "negre", "gris", "brut", "nebot"]),
                   'q2': (['q3'], ["a", "et", "s", "ik", "estr"]),
                   'q3': (['qf'], ['X']),
                   })

        nasal_deletion = Rule.load([[{"nasal": "+"}], [], [], [{"WB": "+"}], True])
        cluster_simplification = Rule.load([[{"cont": "-"}], [], [{"nasal": "+"}], [{"WB": "+"}], True])
        rule_set = RuleSet([nasal_deletion, cluster_simplification])
        grammar = Grammar(hmm, rule_set)
        all_outputs = grammar.get_all_outputs()
        print(sorted(all_outputs))
        print(len(all_outputs))
        # all_outputs = [string + 'W' for string in all_outputs]
        # print(all_outputs)
        # print(len(all_outputs))

    def test_turkish_rule(self):
        self.initialise_segment_table("turkish_segment_table.txt")

        word = 'ippppar'
        rule = [[{"syll": "+"}], [{"back": "-"}], [{"syll": "+", "back": "-"}, {"syll": "-", "kleene": True}], [], True]
        # rule = [[{"back": "+"}], [{"back": "-"}], [], [], True]
        rule = Rule(*rule)
        ruleset = RuleSet([rule])
        print(ruleset.get_outputs_of_word(word))

    def test_generate_finnish_two_rules(self):
        from simulations import finnish_two_rules as simulation
        self.initialise_simulation(simulation)
        hmm = HMM({'q0': ['q1'],
                   'q1': (['q2'],
                          ['ment', 'sippat', 'imet', 'piit', 'tiad', 'pans',
                           'pitaa', 'abs', 'mea', 'sam', 'tei', 'sippi', 'essi']),
                   'q2': (['qf'],
                          ['i', 'impa', 'n', 'ssa', 'itten', 'ias', 'mainen',
                           'nti', 'isti'])})
        t_frication = Rule.load([[{"coronal": "+", "voice": '-'}], [{"cont": "+"}], [], [{"high": "+"}], False])
        i_deletion = Rule.load([[{"high": "+"}], [], [], [{"WB": True}], False])
        rule_set = RuleSet([t_frication, i_deletion])
        grammar = Grammar(hmm, rule_set)
        grammar_transducer = grammar.get_transducer()
        print(len(grammar_transducer))
        self.write_to_dot_file(grammar_transducer, 'finnish_two_rules')
        h = Hypothesis(grammar)
        h.get_energy()

        # self.write_to_dot_file(hmm.get_transducer(), "finnish_hmm_transducer")

        all_outputs = grammar.get_all_outputs()
        print(sorted(all_outputs))
        print(len(all_outputs))

        print(h.get_recent_energy_signature())



    def genereate_corpus(self, stems, suffixes):
        final_corpus = []
        for stem in stems:
            for suffix in suffixes + ['']:
                final_corpus.append(stem + suffix)
        return final_corpus

        corpus = list()
        for stem in stems:
            word = stem
            for i in range(3):
                for tuple1 in itertools.product(['da', 'ka'], repeat=i):
                    suffix1 = ''.join(tuple1)
                    word = word + suffix1
                    for j in range(3):
                        for tuple2 in itertools.product(['za', 'ta'], repeat=j):
                            suffix2 = ''.join(tuple2)
                            word = word + suffix2
                            if "e" in word:
                                word = word.replace("a", "e")
                            corpus.append(word)
                            word = stem + suffix1
                    word = stem

        base = [u'gakata', u'gakaza', u'gaka', u'gadata', u'gadaza', u'gada', u'ga', u'gekete', u'gekeze', u'geke',
                u'gedete', u'gedeze', u'gede', u'ge', u'sakata', u'sakaza', u'saka', u'sadata', u'sadaza', u'sada',
                u'sa', u'sekete', u'sekeze', u'seke', u'sedete', u'sedeze', u'sede', u'se']
        print(len(corpus))
        print(corpus)
        sample_corpus = random.sample(corpus, 100)
        print(sample_corpus)

        final_corpus = list(set(base + sample_corpus))
        print(len(final_corpus))
        print(final_corpus)

    def test_turkish_vh_new_weights(self):
        from simulations import turkish_vowel_harmony_new_weights
        self.initialise_simulation(turkish_vowel_harmony_new_weights)
        target_hmm = self.simulation.target_hmm
        target_rule_set = RuleSet.load_from_flat_list(self.simulation.target_tuple[1])
        grammar = Grammar(target_hmm, target_rule_set)
        all_outputs = grammar.get_all_outputs()
        print(sorted(all_outputs))

    def test_tak_soog__noise(self):
        from simulations import dag_zook_noise_voicing
        self.initialise_simulation(dag_zook_noise_voicing)
        target_hmm = self.simulation.target_hmm
        target_rule_set = RuleSet.load_from_flat_list(
            self.simulation.target_tuple[1])
        grammar = Grammar(target_hmm, target_rule_set)
        all_outputs = grammar.get_all_outputs(with_noise=False)
        print(sorted(all_outputs))

    def test_dag_zook__noise(self):
        from simulations import dag_zook_noise
        self.initialise_simulation(dag_zook_noise)
        target_hmm = self.simulation.target_hmm
        target_rule_set = RuleSet.load_from_flat_list(
            self.simulation.target_tuple[1])
        grammar = Grammar(target_hmm, target_rule_set)
        all_outputs = grammar.get_all_outputs(with_noise=False)
        print(sorted(all_outputs))

    def test_tag_soo__ilm(self):
        from simulations import tag_soo_ilm_final_devoicing
        self.initialise_simulation(tag_soo_ilm_final_devoicing)
        target_hmm = self.simulation.target_hmm
        target_rule_set = RuleSet.load_from_flat_list(
            self.simulation.target_tuple[1])
        grammar = Grammar(target_hmm, target_rule_set)
        all_outputs = grammar.get_all_outputs(with_noise=False)
        print(sorted(all_outputs))

    def test_corpus_generator_ilm(self):
        from simulations import dam_ka_ilm_final_devoicing
        # with voicing
        self.initialise_simulation(dam_ka_ilm_final_devoicing)
        target_hmm = self.simulation.target_hmm
        voicing_rule = [[{"son": "-"}], [{"voice": "+"}], [], [{"WB": True}], True]
        target_rule_set = RuleSet.load_from_flat_list([voicing_rule])
        grammar = Grammar(target_hmm, target_rule_set)
        all_outputs = grammar.get_all_outputs(with_noise=False)
        print(sorted(all_outputs))

    def test_corpus_generator_ilm2(self):
        from simulations import dam_ka_ilm_final_devoicing
        # no voicing
        self.initialise_simulation(dam_ka_ilm_final_devoicing)
        target_hmm = self.simulation.target_hmm
        grammar = Grammar(target_hmm, [])
        all_outputs = grammar.get_all_outputs(with_noise=False)
        print(sorted(all_outputs))


