from hypothesis import Hypothesis, GAHypothesis
from hmm import HMM, INITIAL_STATE, FINAL_STATE
from grammar import Grammar
from tests.my_test_case import MyTestCase
from rule import Rule
from rule_set import RuleSet
from genetic_algorithm import GeneticAlgorithm
from util import log_hypothesis
from configuration import Configuration

config = Configuration()

class TestGeneticAlgorithm(MyTestCase):
    def setUp(self):
        self.initialise_segment_table("plural_english_segment_table.txt")

    def test_crossover_random(self):
        self.initialise_segment_table("dag_zook_segments_new.txt")
        data = ['kat', 'dot', 'dag', 'kod'] + \
               ['katso', 'dotso', 'dagzo', 'kodzo'] + \
               ['katko', 'dotko', 'daggo', 'kodgo'] + \
               ['katto', 'dotto', 'dagdo', 'koddo']

        config['EVOLVE_RULES'] = True
        config['EVOLVE_HMM'] = True
        config['MAX_NUMBER_OF_RULES'] = 3

        h1 = GAHypothesis(data)
        h2 = GAHypothesis(data)
        print('\nH1\n')
        log_hypothesis(h1)
        print('\nH2\n')
        log_hypothesis(h2)

        offspring_1, offspring_2 = GeneticAlgorithm._crossover(h1, h2)
        print('\nOFFSPRING 1\n')
        log_hypothesis(offspring_1)
        print('\nOFFSPRING 2\n')
        log_hypothesis(offspring_2)

    def test_crossover(self):
        self.initialise_segment_table("dag_zook_segments_new.txt")
        rule_set_1 = RuleSet([Rule(*[[{"cons": "+"}], [{"voice": "-"}], [{"low": "+"}], [{"cont": "-"}], True])])
        rule_set_2 = RuleSet([Rule(*[[{"cons": "+"}], [{"low": "-"}], [{"voice": "-"}], [], False])])
        plural_english_data = 1 * ['kats', 'dogz', 'kat', 'dog']
        hmm_1 = HMM({INITIAL_STATE: ['q1'],
                     'q1': (['q2', FINAL_STATE], ['dag', 'kot']),
                     'q2': ([FINAL_STATE], ['z'])})
        hmm_2 = HMM({INITIAL_STATE: ['q1'],
                     'q1': (['q2'], ['dog', 'kat']),
                     'q2': (['q3'], ['s']),
                     'q3': ([FINAL_STATE], ['z'])})

        grammar_1 = Grammar(hmm_1, rule_set_1)
        grammar_2 = Grammar(hmm_2, rule_set_2)

        hypothesis_1 = Hypothesis(grammar_1, plural_english_data)
        hypothesis_2 = Hypothesis(grammar_2, plural_english_data)
        offspring_1, offspring_2 = GeneticAlgorithm.crossover(hypothesis_1, hypothesis_2)

        print("*** Parents:\n")
        GeneticAlgorithm.log_hypothesis(hypothesis_1)
        GeneticAlgorithm.log_hypothesis(hypothesis_2)

        print("\n\n*** Offspring:\n")
        GeneticAlgorithm.log_hypothesis(offspring_1)
        GeneticAlgorithm.log_hypothesis(offspring_2)

        offspring_3, offspring_4 = GeneticAlgorithm.crossover(offspring_1, offspring_2)

        print("\n\n*** 2nd gen offspring:\n")
        GeneticAlgorithm.log_hypothesis(offspring_3)
        GeneticAlgorithm.log_hypothesis(offspring_4)