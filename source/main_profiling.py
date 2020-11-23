import random
import importlib
from os import environ
from queue import Queue
from optparse import OptionParser
from os.path import join, split, abspath
from configuration import Configuration
from genetic_algorithm import GeneticAlgorithm
from segment_table import SegmentTable
from utils.logger import MultiprocessLogger as Logger

parser = OptionParser()

parser.add_option("-s", "--simulation", default=None, dest="simulation_name",
                  help='Simulation name, e.g "dag_zook_devoicing"')
(options, args) = parser.parse_args()

if options.simulation_name is None:
    parser.print_help()
    parser.error("Must provide simulation_name")

current_simulation = importlib.import_module('simulations.{}'.format(options.simulation_name))
environ["SPE_SIMULATION_ID"] = "PROFILING_SIMULATION"

logger = Logger.get_logger()

main_dir_path, filename = split(abspath(__file__))
segment_table_dir_path = join(main_dir_path, "tests/fixtures/segment_table")

configurations = Configuration()
configurations.load_configuration_for_simulation(current_simulation)

seed = 100
random.seed(seed)
logger.info('Simulation: {}'.format(options.simulation_name))
logger.info("Seed: {}".format(seed))
logger.info(str(configurations))
with open('ga_config.py') as f:
    for line in f.readlines():
        logger.info(line)

segment_table_fixture_path = join(segment_table_dir_path, current_simulation.segment_table_file_name)
SegmentTable.load(segment_table_fixture_path)
dummy_queue = Queue(maxsize=10)

MAX_GENERATIONS = 10

genetic_algorithm = GeneticAlgorithm(current_simulation, migration_coordinator=None,result_queue=dummy_queue, island_number=1, simulation_total_islands=1, max_generations=MAX_GENERATIONS, simulation_total_generations=100, initial_generation=1)

genetic_algorithm.run()
