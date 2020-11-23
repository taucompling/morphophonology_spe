from hmm import HMM
from grammar import Grammar
from tests.my_test_case import MyTestCase
from rule import Rule
from rule_set import RuleSet
from hypothesis import Hypothesis
from collections import namedtuple
from configuration import Configuration
configuration = Configuration()

SimulationCase = namedtuple('SimulationHypothesis', ['case_name', 'hmm_dict', 'flat_rule_set_list'])

class SimulationTest(MyTestCase):

    def get_energy(self, simulation_case):
        case_name = simulation_case.case_name
        configuration.configurations_dict["case_name"] = case_name
        if isinstance(simulation_case.hmm_dict, HMM):
            hmm = simulation_case.hmm_dict
        else:
            hmm = HMM(simulation_case.hmm_dict)
        if isinstance(simulation_case.flat_rule_set_list, RuleSet):
            rule_set = simulation_case.flat_rule_set_list
        else:
            rule_set_list = []
            for flat_rule in simulation_case.flat_rule_set_list:
                rule_set_list.append(Rule(*flat_rule))
            rule_set = RuleSet(rule_set_list)
        grammar = Grammar(hmm, rule_set)
        self.write_to_dot_file(hmm, "hmm_" + case_name)
        self.write_to_dot_file(grammar.get_nfa(), "grammar_nfa_" + case_name)
        hypothesis = Hypothesis(grammar, self.data)
        energy = hypothesis.get_energy()
        if self.target_energy:
            print("{}: {} distance from target: {}".format(case_name, hypothesis.get_recent_energy_signature(), energy-self.target_energy))
        else:
            print("{}: {}".format(case_name, hypothesis.get_recent_energy_signature()))
        return energy