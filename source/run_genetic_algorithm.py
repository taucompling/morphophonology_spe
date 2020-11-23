import importlib
from os import environ
from optparse import OptionParser
from configuration import Configuration

parser = OptionParser()

parser.add_option("-i", "--id", default=None, dest="simulation_id", help='Simulation ID')
parser.add_option("-s", "--simulation", default=None, dest="simulation_name",
                  help='Simulation name, e.g "dag_zook_devoicing"')
parser.add_option("-e", "--environment", default="local", dest="environment_name",
                  help='Environment to use for migrations: "aws", "azure", or "local". Default: "local"')
parser.add_option("-n", "--total-islands", type="int", dest="total_islands",
                  help='Total number of islands in entire simulation (including other machines)')
parser.add_option("-r", "--resume", action="store_true", dest="resume_simulation", default=False,
                  help='Resume simulation from dumped islands')
parser.add_option("--first-island", type="int", default=0, dest="first_island_idx",
                  help='First island index on this machine. Default: 0')
parser.add_option("--last-island", type="int", default=None, dest="last_island_idx",
                  help='Last island index on this machine. Default: number of islands minus 1')
parser.add_option("--sanity-check", action='store_true', default=False, dest="sanity_check",
                  help="Initial hypothesis is final hypothesis. "
                       "Use to check that search algorithm doesn't do crazy stuff"
                       )

(options, args) = parser.parse_args()

if not options.simulation_id:
    parser.print_help()
    parser.error("Must provide simulation ID.")

if not options.simulation_name:
    parser.print_help()
    parser.error("Must provide simulation name.")

if not options.total_islands:
    parser.print_help()
    parser.error("Must provide total number of islands.")


current_simulation = importlib.import_module('simulations.{}'.format(options.simulation_name))
configurations = Configuration()
configurations.load_configuration_for_simulation(current_simulation)


environ["SPE_SIMULATION_ID"] = options.simulation_id
environ["SPE_ENVIRONMENT_NAME"] = options.environment_name.lower()


import random
from time import sleep
from segment_table import SegmentTable
from os.path import join, split, abspath
from island_simulation import GeneticAlgorithmIslandSimulation
from utils.logger import MultiprocessLogger as Logger
import ga_config

logger = Logger.get_logger()


main_dir_path, filename = split(abspath(__file__))
segment_table_dir_path = join(main_dir_path, "tests/fixtures/segment_table")


seed = ga_config.RANDOM_SEED_RANGE_START
random.seed(seed)
logger.info('Simulation corpus: {}'.format(options.simulation_name))
logger.info('Simulation id: {}'.format(options.simulation_id))
logger.info('Total number of islands: {}'.format(options.total_islands))
logger.info('Local simulation island indices: {}-{}'.format(options.first_island_idx,
                                                            options.last_island_idx if options.last_island_idx else (
                                                                        options.total_islands - 1)))
logger.info("Main process seed: {}".format(seed))
logger.info("Simulation configuration:")
logger.info(str(configurations))

logger.info("Genetic algorithm configuration:")
with open('ga_config.py') as f:
    for line in f.readlines():
        logger.info(line.strip())
    sleep(3)  # Ugly hack to let logging queue drain

if options.sanity_check:
    setattr(current_simulation, 'initial_hmm', current_simulation.target_hmm)
    setattr(current_simulation, 'initial_rule_set', current_simulation.rule_set)


segment_table_fixture_path = join(segment_table_dir_path, current_simulation.segment_table_file_name)
SegmentTable.load(segment_table_fixture_path)

genetic_algorithm = GeneticAlgorithmIslandSimulation(current_simulation,
                                                     total_islands=options.total_islands,
                                                     first_island_idx=options.first_island_idx,
                                                     last_island_idx=options.last_island_idx,
                                                     resume=options.resume_simulation)
genetic_algorithm.run()
