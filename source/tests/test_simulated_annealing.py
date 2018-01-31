from collections import Counter
from hypothesis import Hypothesis
from hmm import HMM
from grammar import Grammar
from tests.my_test_case import MyTestCase
from rule import Rule
from rule_set import RuleSet
from simulated_annealing import SimulatedAnnealing
from configuration import Configuration
configurations = Configuration()

class TestSimulatedAnnealing(MyTestCase):
    def test_get_parsing_results(self):
        self.initialise_segment_table("abnese_lengthening_segment_table.txt")
        configurations["MORPHEME_BOUNDARY_FLAG"] = True
        configurations["LENGTHENING_FLAG"] = True
        configurations["HMM_ENCODING_LENGTH_MULTIPLIER"] = 100
        configurations["DATA_ENCODING_LENGTH_MULTIPLIER"] = 20
        hmm = HMM({'q0': ['q1'],
         'q1': (['qf'], ['aabb', 'abb', 'bbaabb', 'aba', 'aaba', 'bbaa'])
          })

        rule1 = Rule([], [{"long": "+"}], [], [{}, {"bound": "+"}], obligatory=True)
        rule2 = Rule([], [{"syll": "+"}], [{"cons": "+"}], [{"cons": "+"}], obligatory=True)
        rule_set = RuleSet([rule1, rule2])

        grammar = Grammar(hmm, rule_set)
        data = [u'baba:a', u'babaab:ab', u'ab:a', u'aab:a', u'aab:ab', u'ab:ab']

        hypothesis = Hypothesis(grammar, data)
        simulated_annealing = SimulatedAnnealing(hypothesis, 0)
        print(simulated_annealing._get_parsing_results())


    def test_linear_decay(self):
        initial = 50
        stop = 1
        exponential_decay_rate = 0.999995
        #exponential
        exponential_int_values = list()
        temp = initial
        num_of_steps = 0
        while temp > stop:
            temp *= exponential_decay_rate
            exponential_int_values.append(int(temp))
            num_of_steps += 1
        print(Counter(exponential_int_values))
        #linear
        linear_int_values = list()
        linear_decay_rate = (initial-stop)/num_of_steps
        temp = initial
        while temp > stop:
            temp -= linear_decay_rate
            linear_int_values.append(int(temp))
        print(Counter(linear_int_values))


    def test_get_parsing_results_infinite(self):
        self.initialise_segment_table("abnese_lengthening_segment_table.txt")
        configurations["MORPHEME_BOUNDARY_FLAG"] = True
        configurations["LENGTHENING_FLAG"] = True
        configurations["HMM_ENCODING_LENGTH_MULTIPLIER"] = 100
        configurations["DATA_ENCODING_LENGTH_MULTIPLIER"] = 20
        hmm = HMM({'q0': ['q1'],
         'q1': (['qf'], ['ab:a', 'baaa', 'baab', 'baab:a'])
          })

        rule = Rule([], [{'long': '-'}], [], [{}], obligatory=False)
        rule_set = RuleSet([rule])

        grammar = Grammar(hmm, rule_set)
        data = [u'baba:a', u'babaab:ab', u'ab:a', u'aab:a', u'aab:ab', u'ab:ab']

        hypothesis = Hypothesis(grammar, data)
        simulated_annealing = SimulatedAnnealing(hypothesis, 0)
        print(simulated_annealing._get_parsing_results())
