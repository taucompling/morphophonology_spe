from tests.my_test_case import MyTestCase
from hypothesis import Hypothesis
from hmm import HMM, INITIAL_STATE, FINAL_STATE
from grammar import Grammar
from tests.my_test_case import MyTestCase
from rule import Rule
from rule_set import RuleSet

from configuration import Configuration

configurations = Configuration()
from random import randint

class T(MyTestCase):
    def setUp(self):
        self.initialise_segment_table("abnese_lengthening_segment_table.txt")
        configurations["MORPHEME_BOUNDARY_FLAG"] = True
        configurations["LENGTHENING_FLAG"] = True
        self.data = [u'aabYab', u'abYab', u'abYa', u'aabYa', u'ababYa', u'abababYa', u'bababYab', u'babaYa', u'bYab', u'babYab', u'bababYa', u'babababYa']

    def test_compare(self):
        i = 10
        j = 1
        z = 1
        configurations["DATA_ENCODING_LENGTH_MULTIPLIER"] = i
        configurations["HMM_ENCODING_LENGTH_MULTIPLIER"] = j
        configurations["RULES_SET_ENCODING_LENGTH_MULTIPLIER"] = z
        print("data_m: {}".format(i))
        print("hmm_m: {}".format(j))
        print("rule_set_m: {}".format(z))
        initial_result = self.test_abnese_lengthening_initial()
        target_result = self.test_abnese_lengthening_target()
        from_simulation_result1 = self.test_from_simulation1()
        # from_simulation_result2 = self.test_from_simulation2()
        # from_simulation_result3 = self.test_from_simulation3()
        # from_simulation_result4 = self.test_from_simulation4()
        if min([target_result, from_simulation_result1, initial_result]) == target_result:
            print("winner is target")
                # break


    def test_abnese_lengthening_target(self):
        hmm = HMM({'q0': ['q1'],
              'q1': (['qf'], ['aabb', 'abb', 'aba', 'aaba', 'bbaa', 'bbbb', 'abbba', 'abba',
                         'bb', 'bbb', 'bbba', 'bbbba'])
              })

        rule1 = Rule([], [{"long": "+"}], [], [{}, {"bound": "+"}], obligatory=True)
        rule2 = Rule([], [{"syll": "+"}], [{"cons": "+"}], [{"cons": "+"}], obligatory=True)
        return self.get_energy(hmm, [rule1, rule2], "target")


    def test_from_simulation1(self):
        hmm = HMM({'q0': ['q1'],
      'q1': (['qf'], [u'aabYa', u'aabYb', u'bYb', u'babbYa', u'babbbYa', u'bbaYa', u'bbabYb'])
      })

        rule1 = Rule([{}], [], [], [{'cons': '-', 'syll': '+'}, {'cons': '+'}], False)
        rule2 = Rule([], [{'syll': '+'}], [{'cons': '+', 'syll': '-', 'bound': '-', 'long': '-'}], [{'cons': '+', 'syll': '-'}], True)
        return self.get_energy(hmm, [rule1, rule2], "simulation1")

    def test_abnese_lengthening_initial(self):
        hmm = HMM({'q0': ['q1'],
      'q1': (['qf'], self.data)
      })
        return self.get_energy(hmm, [], "initial")


    def get_energy(self, hmm, rule_set_list, case_name):
        grammar = Grammar(hmm, RuleSet(rule_set_list))
        self.write_to_dot_file(grammar.get_nfa(), "grammar_nfa_" + case_name)
        hypothesis = Hypothesis(grammar, self.data)
        energy = hypothesis.get_energy()
        print("{}: {}".format(case_name, hypothesis.get_recent_energy_signature()))
        return energy