from tests.my_test_case import MyTestCase
from hypothesis import Hypothesis
from hmm import HMM, INITIAL_STATE, FINAL_STATE
from grammar import Grammar
from tests.my_test_case import MyTestCase
from rule import Rule
from rule_set import RuleSet
from copy import deepcopy

from configuration import Configuration

configurations = Configuration()
from random import randint


class T(MyTestCase):
    def setUp(self):
        self.initialise_segment_table("ab_segment_table.txt")
        self.data = ['aabab', 'abab', 'babaabab', 'aba', 'aaba', 'babaa',
                     'bb', 'bab', 'bbaabab', 'babaabb', 'aabb', 'abb']



    def test_compare(self):

        data_multiplier = 1
        hmm_multiplier = 1
        rule_set_multiplier = 1
        configurations["DATA_ENCODING_LENGTH_MULTIPLIER"] = data_multiplier
        configurations["HMM_ENCODING_LENGTH_MULTIPLIER"] = hmm_multiplier
        configurations["RULES_SET_ENCODING_LENGTH_MULTIPLIER"] = rule_set_multiplier
        print("data_multiplier: {}".format(data_multiplier))
        print("hmm_multiplier: {}".format(hmm_multiplier))
        print("rule_set_multiplier: {}".format(rule_set_multiplier))
        target_result = self.test_target()
        initial_result = self.test_initial()
        from_simulation_result1 = self.test_from_simulation1()
        if min([target_result, initial_result, from_simulation_result1]) == target_result:
            print("winner is target")
                # break
        print(0)
        print(target_result - initial_result)
        print(target_result - from_simulation_result1)


    def test_target(self):
        hmm = HMM({'q0': ['q1'],
         'q1': (['qf'], ['aabb', 'abb', 'bbaabb', 'aba', 'aaba', 'bbaa', 'bb'])
          })

        rule = Rule([], [{"cons": "-"}], [{"cons": "+"}], [{"cons": "+"}], False)
        return self.get_energy(hmm, [rule], "target")


    def test_initial(self):
        hmm = {'q0': ['q1'],
              'q1': (['qf'], deepcopy(self.data))
              }
        return self.get_energy(hmm, [], "initial")


    def test_from_simulation1(self):
        hmm = HMM({'q0': ['q1'],
         'q1': (['qf'],  ['abb', 'b', 'bba', 'bbabb', 'bab', 'bbaabb'])
          })
        rule1 = Rule([{}], [{'cons': '-'}], [{'cons': '+'}], [], True)
        rule2 = Rule([], [{}], [{}], [], False)
        return self.get_energy(hmm, [rule1, rule2], "from_simulation1")

    def get_energy(self, hmm, rule_set_list, case_name):
        grammar = Grammar(hmm, RuleSet(rule_set_list))
        hypothesis = Hypothesis(grammar, self.data)
        energy = hypothesis.get_energy()
        print("{}: {}".format(case_name, hypothesis.get_recent_energy_signature()))
        return energy