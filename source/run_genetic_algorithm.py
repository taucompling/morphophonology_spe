import importlib
from os import environ
from argparse import ArgumentParser
from configuration import Configuration
# this probably should be moved somewhere else!
from tests.test_util import get_hypothesis_from_log_string


def rangeint(a, b):
    def _rangeint(i):
        i = int(i)
        if i > b:
            raise ValueError(f"Integer is not in range: {i} > {b}")
        if i < a:
            raise ValueError(f"Integer is not in range: {i} < {a}")
        return i
    return _rangeint


parser = ArgumentParser()

parser.add_argument("-i", "--id", dest="simulation_id", help='Simulation ID', required=True)
parser.add_argument("-s", "--simulation", dest="simulation_name", required=True,
                    help='Simulation name, e.g "dag_zook_devoicing"')
parser.add_argument("-e", "--environment", default="local", dest="environment_name", choices=["aws", "azure", "local"],
                    help="Environment to use for migrations")
parser.add_argument("-n", "--total-islands", type=int, dest="total_islands", required=True,
                    help='Total number of islands in entire simulation (including other machines)')
parser.add_argument("-r", "--resume", action="store_true", dest="resume_simulation",
                    help='Resume simulation from dumped islands')
parser.add_argument("--first-island", type=int, default=0, dest="first_island_idx",
                    help='First island index on this machine. Default: 0')
parser.add_argument("--last-island", type=int, default=None, dest="last_island_idx",
                    help='Last island index on this machine. Default: number of islands minus 1')
parser.add_argument("--sanity-check", action='store_true', dest="sanity_check",
                    help="Initial hypothesis is final hypothesis. "
                         "Use to check that search algorithm doesn't do crazy stuff"
                    )

ilm_group = parser.add_argument_group('Arguments for ILM')
ilm_group.add_argument(
    '--output',
    dest='output',
    help='Output file to write random `num-words` words learned by the learner'
)
ilm_group.add_argument(
    '--num-words',
    dest='num_words',
    type=int,
    default=-1,
    help='Number of words learned to write to `output` file, -1 for no limit '
         '(default).'
)
ilm_group.add_argument(
    '--ilm-bottleneck',
    dest='ilm_bottleneck',
    type=rangeint(1, 100),
    default=100,
    help='% of words to pass to the next generation. Integer. Default is 100.'
)

inputs = ilm_group.add_mutually_exclusive_group()
inputs.add_argument('--input',
                    help="Input to use as data instead of simulation's data. "
                         "Use with caution!")
inputs.add_argument('--migration-input', action="store_true",
                    help="Get input from island number 0. Use with caution!")

args = parser.parse_args()


current_simulation = importlib.import_module('simulations.{}'.format(args.simulation_name))
configurations = Configuration()
configurations.load_configuration_for_simulation(current_simulation)


environ["SPE_SIMULATION_ID"] = args.simulation_id
environ["SPE_ENVIRONMENT_NAME"] = args.environment_name.lower()


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
logger.info('Simulation corpus: {}'.format(args.simulation_name))
logger.info('Simulation id: {}'.format(args.simulation_id))
logger.info('Total number of islands: {}'.format(args.total_islands))
logger.info('Local simulation island indices: {}-{}'.format(args.first_island_idx,
                                                            args.last_island_idx if args.last_island_idx else (args.total_islands - 1)))
logger.info("Main process seed: {}".format(seed))
logger.info("Simulation configuration:")
logger.info(str(configurations))

logger.info("Genetic algorithm configuration:")
with open('ga_config.py') as f:
    for line in f.readlines():
        logger.info(line.strip())
    sleep(3)  # Ugly hack to let logging queue drain

if args.sanity_check:
    setattr(current_simulation, 'initial_hmm', current_simulation.target_hmm)
    setattr(current_simulation, 'initial_rule_set', current_simulation.rule_set)


segment_table_fixture_path = join(segment_table_dir_path, current_simulation.segment_table_file_name)
SegmentTable.load(segment_table_fixture_path)

genetic_algorithm = GeneticAlgorithmIslandSimulation(current_simulation,
                                                     total_islands=args.total_islands,
                                                     first_island_idx=args.first_island_idx,
                                                     last_island_idx=args.last_island_idx,
                                                     resume=args.resume_simulation)

if args.input:
    with open(args.input) as f:
        data = list(filter(None, f.read().split()))
    logger.info(f'Simulation data overridden, using: {data}')
    genetic_algorithm.override_data(data)

elif args.migration_input:
    if args.first_island_idx <= 0:
        print("Island 0 is running on this machine, cannot get data via migration")
        exit(1)
    while not genetic_algorithm.update_data_from_latest_island():
        logger.info("Island 0 is not ready for data migration, sleeping for 1m")
        sleep(60)

final = genetic_algorithm.run()

if args.output:
    logger.info('Generating word list...')
    # TODO: If there is a loop in the HMM this method will probably won't return
    words = list(set(final.grammar.get_all_outputs(with_noise=False)))
    logger.info('Shuffling words...')
    random.shuffle(words)
    logger.info('Applying ILM bottleneck')

    to_next_gen = int(len(words) * args.ilm_bottleneck / 100)
    words = words[:to_next_gen]

    if args.num_words == -1:
        pass
    elif len(words) > args.num_words:
        logger.info(
            f"Too many words: generated %{len(words)}, need {args.num_words}. "
            f"Trimming"
        )
        words = words[:args.num_words]
    elif len(words) < args.num_words:
        logger.info(
            f"Not enough words: generated %{len(words)}, need {args.num_words}."
            f" Repeating"
        )
        words += random.choices(words, k=args.num_words - len(words))
    logger.info(f"Passing {len(words)} words to the next generation")

    logger.info('Shuffling words again...')
    random.shuffle(words)

    with open(args.output, 'w') as f:
        f.write(' '.join(words))
    logger.info('Done writing words!')

exit(0)
