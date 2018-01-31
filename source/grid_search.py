import random
import itertools
from sys import modules
from os.path import join, split, abspath
import json
from configuration import Configuration
from island_simulation import GeneticAlgorithmIslandSimulation
from segment_table import SegmentTable
import ga_config
from util import log_hypothesis
from utils.logger import MultiprocessLogger as Logger

logger = Logger.get_logger()

main_dir_path, filename = split(abspath(__file__))
segment_table_dir_path = join(main_dir_path, "tests/fixtures/segment_table")

configurations = Configuration()
configurations.load_configuration_for_simulation(ga_config.CURRENT_SIMULATION)

segment_table_fixture_path = join(segment_table_dir_path, ga_config.CURRENT_SIMULATION.segment_table_file_name)
SegmentTable.load(segment_table_fixture_path)

seed = random.randint(0, 100)
random.seed(seed)
logger.info("Seed: {}".format(seed))
logger.info(str(configurations))
with open('ga_config.py') as f:
    for line in f.readlines():
        logger.info(line)

GRID = [
    ('CXPB', [1.0, 0.8, 0.5, 0.3]),
    ('MUTPB', [0.8, 0.5, 0.4, 0.1]),
    ('VAR_AND', [True, False]),
    ('MIGRATION_INTERVAL', [10, 50, 100]),
    ('ISLAND_POPULATION', [100]), #, 200, 500, 1000]),
    ('MIGRATION_RATIO', [0.1]), #, 0.2, 0.5]),
    ('CROSSOVER_BOTH_HMM_AND_RULES', [True]), #, False]),
    ('MUTATE_BOTH_HMM_AND_RULES', [False]),
    ('MAX_MUTATIONS', [1, 5, 10]),
    ('TOTAL_GENERATIONS', [200]),
    ('NUM_ISLANDS', [7])
]


class GridSearch:
    def __init__(self):
        self.all_combinations = self.get_all_combinations()
        self.total_trials = len(self.all_combinations)
        self.results = []

    def start(self):
        logger.info('GRID SEARCH ')
        for c, combination in enumerate(self.all_combinations):
            current_params = {}
            for i in range(len(combination)):
                param = GRID[i][0]
                val = combination[i]
                setattr(modules['ga_config'], param, val)
                current_params[param] = combination[i]

            logger.info('GRID SEARCH Starting simulation {}/{} with params:\n{}'.format(c+1, len(self.all_combinations), str(current_params)))
            final_hypothesis = self.run_simulation()
            if final_hypothesis:
                self.results.append([current_params, final_hypothesis.get_energy()])
                logger.info('GRID SEARCH Ended simulation with final hypothesis:')
                log_hypothesis(final_hypothesis, logger.info)
            else:
                logger.error('GRID SEARCH failed - simulation failed with current params '
                             '(probably param combination is invalid). Trying next combination on grid...')

        logger.info('GRID SEARCH Final results:\n{}'.format(json.dumps(self.results)))

    def run_simulation(self):
        simulation = GeneticAlgorithmIslandSimulation(ga_config.CURRENT_SIMULATION)
        return simulation.run()

    def get_all_combinations(self):
        return list(itertools.product(*[GRID[k][1] for k in range(len(GRID))]))


if __name__ == '__main__':
    grid_search = GridSearch()
    grid_search.start()
