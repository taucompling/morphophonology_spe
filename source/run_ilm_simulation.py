#!/usr/bin/env python
import importlib
from copy import deepcopy
from os import environ
from argparse import ArgumentParser
from subprocess import check_call

from configuration import Configuration


def positive_int(i):
    i = int(i)
    if i <= 0:
        raise ValueError("Value must be greater than 0")
    return i


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

parser.add_argument("-i", "--id", required=True, dest="simulation_id", help='Simulation ID')
parser.add_argument("-s", "--simulation", required=True, dest="simulation_name",
                    help='Simulation name, e.g "dag_zook_devoicing"')
parser.add_argument("-e", "--environment", default="local", dest="environment_name",
                    help='Environment to use for migrations: "aws", "azure", or "local". Default: "local"')
parser.add_argument("-n", "--total-islands", type=int, dest="total_islands", required=True,
                    help='Total number of islands in entire simulation (including other machines)"')
parser.add_argument("-r", "--resume", type=int, dest="resume_simulation",
                    help='Resume simulation from given generation')
parser.add_argument("-g", "--generations", type=int, required=True,
                    help='Number of ILM generations to run.')
parser.add_argument(
    '--ilm-bottleneck',
    dest='ilm_bottleneck',
    type=rangeint(1, 100),
    default=100,
    help='%% of words to pass to the next generation. Integer. Default is 100.'
)
parser.add_argument(
    "--noise-rate",
    dest="noise_rate",
    type=rangeint(0, 100),
    default=0,
    help="%% of words to apply noise to in the data passed to the next "
         "generation. Default is 0."
)
machines = parser.add_argument_group("ILM machines")
machines.add_argument("-t", "--total-machines", type=positive_int, default=1, metavar="TOTAL",
                      help="total machines this simulation is running on")
machines.add_argument("-m", "--machine", type=positive_int, metavar="MACHINE", default=1,
                      help="Machine number between 1 and TOTAL (inclusive)")

args = parser.parse_args()

if args.total_machines < args.machine:
    print("MACHINE must be between 1 and TOTAL (inclusive)")
    exit(1)


current_simulation = importlib.import_module(
    'simulations.{}'.format(args.simulation_name)
)
configurations = Configuration()
configurations.load_configuration_for_simulation(current_simulation)
initial_data_len = len(current_simulation.data)


environ["SPE_SIMULATION_ID"] = args.simulation_id
environ["SPE_ENVIRONMENT_NAME"] = args.environment_name.lower()

import random
from time import sleep
from segment_table import SegmentTable, Feature
from os.path import join, split, abspath
from utils.logger import MultiprocessLogger as Logger
import ga_config

logger = Logger.get_logger()


main_dir_path, filename = split(abspath(__file__))
segment_table_dir_path = join(main_dir_path, "tests/fixtures/segment_table")


seed = ga_config.RANDOM_SEED_RANGE_START
random.seed(seed)
logger.info('Initial simulation corpus: {}'.format(args.simulation_name))
logger.info('Simulation id: {}'.format(args.simulation_id))
logger.info('Total number of islands: {}'.format(args.total_islands))

logger.info("Main process seed: {}".format(seed))
logger.info("Simulation configuration:")
logger.info(str(configurations))

logger.info("Genetic algorithm configuration:")
with open('ga_config.py') as f:
    for line in f.readlines():
        logger.info(line.strip())
    sleep(3)  # Ugly hack to let logging queue drain

segment_table_fixture_path = join(segment_table_dir_path, current_simulation.segment_table_file_name)
SegmentTable.load(segment_table_fixture_path)


def noise_data(fname, noise_rate):
    if noise_rate == 0:
        return
    logger.info('Reading words...')
    with open(fname, 'r') as f:
        words = f.read().split()
    for NoiseClass in configurations.get("ILM_NOISES", []):
        noise = NoiseClass(noise_rate)
        logger.info(f"Applying noise: {noise.description}")
        noise.apply_noise(words)
    logger.info('Writing words...')
    with open(fname, 'w') as f:
        f.write(' '.join(words))


def get_first_island():
    per_island = args.total_islands // args.total_machines
    return (args.machine - 1) * per_island


def get_last_island():
    if args.machine == args.total_machines:
        return args.total_islands - 1
    else:
        per_island = args.total_islands // args.total_machines
        return args.machine * per_island - 1


datafile = 'datafile.txt'
start = args.resume_simulation or 0
main_machine = args.machine == 1
for g in range(start, args.generations):
    next_gen_id = f'{args.simulation_id}_gen_{g}'
    simulation_args = ['python', 'run_genetic_algorithm.py',
                       '-i', str(next_gen_id),
                       '-s', args.simulation_name,
                       '--first-island', str(get_first_island()),
                       '--last-island', str(get_last_island()),
                       '-n', str(args.total_islands),
                       '-e', args.environment_name.lower(),
                       '--num-words', str(initial_data_len),
                       '--ilm-bottleneck', str(args.ilm_bottleneck),
                       ]
    if main_machine:
        simulation_args.extend(['--output', datafile])
    if g == args.resume_simulation:
        simulation_args.append('--resume')
    elif g != start:
        if main_machine:
            simulation_args.extend(['--input', datafile])
        else:
            simulation_args.append('--migration-input')

    check_call(simulation_args, shell=False)
    logger.info('Noising data...')
    if main_machine:
        noise_data(datafile, args.noise_rate)
