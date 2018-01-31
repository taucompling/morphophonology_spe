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
        self.initialise_segment_table("final_devoicing_segment_table.txt")
        configurations["MORPHEME_BOUNDARY_FLAG"] = True
        self.data = ['ba', 'abF', 'di', 'idF', 'bFi', 'dFa', 'da', 'adF', 'bi', 'ibF', 'dFi', 'bFa', 'badF', 'didF', 'bFibF', 'dFabF', 'babF', 'dabF', 'dibF', 'dFidF', 'bFidF', 'dFadF']

    def test_compare(self):
        data = 1000
        hmm = 10
        rules_set = 1
        configurations["DATA_ENCODING_LENGTH_MULTIPLIER"] = data
        configurations["HMM_ENCODING_LENGTH_MULTIPLIER"] = hmm
        configurations["RULES_SET_ENCODING_LENGTH_MULTIPLIER"] = rules_set
        print("data_m: {}".format(data))
        print("hmm_m: {}".format(hmm))
        print("rule_set_m: {}".format(rules_set))
        initial_result = self.test_initial()
        target_result = self.test_target()
        from_simulation_result1 = self.test_from_simulation1()
        # from_simulation_result2 = self.test_from_simulation2()
        # from_simulation_result3 = self.test_from_simulation3()
        # from_simulation_result4 = self.test_from_simulation4()
        if min([target_result, from_simulation_result1, initial_result]) == target_result:
            print("winner is target")
                # break


    def test_target(self):
        hmm = HMM({'q0': ['q1'],
         'q1': (['qf'], ['ba', 'ab', 'di', 'id', 'bFi', 'dFa', 'da', 'ad', 'bi', 'ib', 'dFi', 'bFa', 'bad', 'dab', 'did', 'bFid', 'bFib', 'dFab', 'bab', 'dib', 'dFid', 'dFad'])
          })

        rule = Rule([], [{"voiceless": "+"}], [{"cons": "+"}], [{"bound": "+"}], True)
        return self.get_energy(hmm, [rule], "target")


    def test_initial(self):
        hmm = {'q0': ['q1'],
              'q1': (['qf'], deepcopy(self.data))
              }
        return self.get_energy(hmm, [], "initial")


    def test_from_simulation1(self):
        hmm = HMM({'q0': ['q1'],
         'q1': (['qf'],  ['ba', 'baFi', 'babF', 'badF', 'bbFa', 'bbFidbF', 'bdFibF', 'bi', 'bibF', 'bidBF', 'dFabFF', 'dFaddF'])
          })
        rule1 = Rule([{'voiceless': '-', 'labial': '+'}], [], [], [{'voiceless': '-', 'labial': '-'}], False)
        rule2 = Rule([{'voiceless': '-', 'high': '-'}], [{'labial': '-'}], [], [{'voiceless': '-'}], False)
        rule3 = Rule([{}], [], [{'cons': '+'}], [{'voiceless': '+', 'bound': '-'}], True)
        return self.get_energy(hmm, [rule1, rule2, rule3], "from_simulation1")



    def get_energy(self, hmm, rule_set_list, case_name):
        grammar = Grammar(hmm, RuleSet(rule_set_list))
        self.write_to_dot_to_file(grammar.get_nfa(), "grammar_nfa")
        hypothesis = Hypothesis(grammar, self.data)
        energy = hypothesis.get_energy()
        print("{}: {}".format(case_name, hypothesis.get_recent_energy_signature()))
        return energy