from tests.my_test_case import MyTestCase
from configuration import Configuration
from hypothesis import Hypothesis
from rule_set import RuleSet
from hmm import HMM
from util import timeit_best_of_N
from simulated_annealing import SimulatedAnnealing


configurations = Configuration()


class TestRuntime(MyTestCase):
    def test_simulated_annealing_runtime(self):
        import simulations.turkish_vowel_harmony as current_simulation
        configurations.load_configurations_from_dict(current_simulation.configurations_dict)
        self.initialise_segment_table('turkish_segment_table.txt')

        initial_hmm = None
        initial_rule_set = None
        initial_hypothesis = Hypothesis.create_initial_hypothesis(current_simulation.data, initial_hmm, initial_rule_set)
        target_tuple = current_simulation.target_tuple
        data = current_simulation.data
        target_rule_set = RuleSet.load_form_flat_list(target_tuple[1])
        target_hypothesis = Hypothesis.create_hypothesis(HMM(target_tuple[0]), target_rule_set, data)
        target_energy = target_hypothesis.get_energy()

        simulated_annealing = SimulatedAnnealing(initial_hypothesis, target_energy)
        simulated_annealing.before_loop()

        # mutate hypothesis for some time before measuring steps
        for i in range(500):
            simulated_annealing.make_step()

        @timeit_best_of_N
        def make_step_profiled():
            simulated_annealing.make_step()

        make_step_profiled()

    def test_hypothesis_get_energy_runtime(self):
        import simulations.catalan_small as current_simulation
        self.initialise_simulation(current_simulation)

        hypothesis_str = """
        Energy: 4063.0
Unparsed words: 0
Fitness: 4063.0
HMM: states ['q1', 'q2', 'q3', 'q4'], transitions {'q1': ['q2', 'q4'], 'q2': ['qf'], 'q0': ['q1'], 'q3': [], 'q4': ['qf']}, emissions {'q1': ['kamp', 'mal', 'blank', 'metal', 'kalent', 'plasa', 'plan', 'silen', 'kap', 'kuzi', 'kasa', 'kuzin', 'sile', 'pla'], 'q2': ['m'], 'q3': [], 'q4': ['a', 'ik', 'et', 's']}
HMM:
q0: ['q1']
q1: ['q2', 'q4'], ['blank', 'kalent', 'kamp', 'kap', 'kasa', 'kuzi', 'kuzin', 'mal', 'metal', 'pla', 'plan', 'plasa', 'sile', 'silen']
q2: ['qf'], ['m']
q3: [], []
q4: ['qf'], ['a', 'et', 'ik', 's']
q0->q1->q4->qf
q0->q1->q2->qf
Rule Set:
transducer_generated:
Rule([{'nasal': '+'}], [], [], [{'WB': True}], True) | ['m', 'n'] --> ε / []__[['W']] obligatory: True
Rule([{'voice': '-'}], [], [{'nasal': '+'}], [{'WB': True}], True) | ['s', 'p', 't', 'k'] --> ε / [['m', 'n']]__[['W']] obligatory: True
not transducer_generated:
        """
        hypothesis = self.get_hypothesis_from_string(hypothesis_str)

        @timeit_best_of_N
        def get_energy():
            hypothesis.get_energy()
            hypothesis.invalidate_energy()

        get_energy()

    def test_hypothesis_mutation_runtime(self):
        import simulations.turkish_vowel_harmony as current_simulation
        configurations.load_configurations_from_dict(current_simulation.configurations_dict)
        self.initialise_segment_table('turkish_segment_table.txt')

        N_mutations = 100

        initial_hmm = None
        initial_rule_set = None
        hypothesis = Hypothesis.create_initial_hypothesis(current_simulation.data, initial_hmm, initial_rule_set)

        @timeit_best_of_N
        def mutate_N_times(hypothesis, N):
            current_hypothesis = hypothesis
            for i in range(N):
                try:
                    _, current_hypothesis = current_hypothesis.get_neighbor()
                except Exception:
                    continue

        mutate_N_times(hypothesis, N_mutations)
