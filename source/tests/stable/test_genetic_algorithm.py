from genetic_algorithm import GeneticAlgorithm
from simulations import dag_zook_morphology_only
from simulations import dag_zook_noise
from tests.my_test_case import MyTestCase
import os


class TestGeneticAlgorithm(MyTestCase):
    def setUp(self):
        super(TestGeneticAlgorithm, self).setUp()
        os.environ['SPE_SIMULATION_ID'] = '1'

    def test_keep_elite__noisey(self):
        os.environ['SPE_SIMULATION_ID'] = self.unique('sim')
        self.initialise_simulation(dag_zook_noise)
        testee = GeneticAlgorithm(simulation=dag_zook_noise,
                                  migration_coordinator=None,
                                  result_queue=list(),
                                  island_number=0,
                                  simulation_total_islands=1,
                                  max_generations=10,
                                  simulation_total_generations=10,
                                  initial_generation=0,
                                  initial_population=None)
        testee.evaluate_population()
        testee.keep_elite()
        self.assertGreater(len(testee.elite), 1)

    def test_keep_elite__no_noise(self):
        self.initialise_simulation(dag_zook_morphology_only)
        testee = GeneticAlgorithm(simulation=dag_zook_morphology_only,
                                  migration_coordinator=None,
                                  result_queue=list(),
                                  island_number=0,
                                  simulation_total_islands=1,
                                  max_generations=10,
                                  simulation_total_generations=10,
                                  initial_generation=0,
                                  initial_population=None)
        testee.evaluate_population()
        testee.keep_elite()
        self.assertGreater(len(testee.elite), 1)
