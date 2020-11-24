import random
import unittest
import uuid
from copy import deepcopy
from os.path import join, split, abspath

from bracket_rule_transducer import clear_module
from segment_table import SegmentTable
from rule_set import RuleSet
from uniform_encoding import UniformEncoding
from utils.cache import Cache
from tests.test_util import write_to_dot_file, get_hypothesis_from_log_string

tests_dir_path, filename = split(abspath(__file__))
fixtures_dir_path = join(tests_dir_path, "fixtures")
dot_files_folder_path = join(tests_dir_path, "dot_files")
segment_table_dir_path = join(fixtures_dir_path, "segment_table")
rule_set_dir_path = join(fixtures_dir_path, "rule_set")
from configuration import Configuration

configurations = Configuration()


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.config_default = False
        # configurations.configurations_dict = deepcopy(configurations.configurations_dict)
        configurations.configurations_dict.setdefault("TRANSDUCER_STATES_LIMIT", 5000)
        configurations.configurations_dict.setdefault("DFAS_STATES_LIMIT", 1000)
        configurations.configurations_dict.setdefault("HMM_MAX_CROSSOVERS", 1)
        configurations.configurations_dict.setdefault("HMM_CROSSOVER_METHOD", "emissions")
        configurations.configurations_dict.setdefault("RANDOM_HMM_METHOD", "simple")
        configurations.configurations_dict.setdefault("DATA_ENCODING_LENGTH_MULTIPLIER", 1)
        configurations.configurations_dict.setdefault("HMM_ENCODING_LENGTH_MULTIPLIER", 1)
        configurations.configurations_dict.setdefault("RULES_SET_ENCODING_LENGTH_MULTIPLIER", 1)
        self.configurations = configurations
        self.p_configurations_get_item = Configuration.__getitem__
        self.patch_configurations()

    def tearDown(self):
        self.tear_down_configurations()
        SegmentTable.clear()
        UniformEncoding().clear()
        clear_module()

    def initialise_simulation(self, simulation):
        self.simulation = simulation
        Cache.get_cache().flush()
        self.configurations.load_configuration_for_simulation(simulation)
        self.configurations.configurations_dict = deepcopy(self.configurations.configurations_dict)

        segment_table_fixture_path = join(segment_table_dir_path, simulation.segment_table_file_name)
        SegmentTable.load(segment_table_fixture_path)

    def initialise_segment_table(self, segment_table_file_name):
        segment_table_fixture_path = join(segment_table_dir_path, segment_table_file_name)
        SegmentTable.load(segment_table_fixture_path)

    def get_hypothesis_from_string(self, s):
        return get_hypothesis_from_log_string(s)

    def get_rule_set(self, rule_set_file_name):
        rule_set_file_name = join(rule_set_dir_path, rule_set_file_name)
        rule_set = RuleSet.load(rule_set_file_name)
        return rule_set

    def write_to_dot_file(self, dotable_object, file_name):
        return
        write_to_dot_file(dotable_object, file_name)

    def patch_configurations(self):
        Configuration.__getitem__ = lambda zelf, x: Configuration.get(
            zelf, x, self.config_default
        )

    def tear_down_configurations(self):
        configurations.reset_to_original_configurations()
        configurations.clear()
        if hasattr(self, 'p_configurations_get_item'):
            Configuration.__getitem__ = self.p_configurations_get_item
        self.config_default = False

    def _seed_me_multiple(self, methods, argss, expecteds):
        seed = -1
        while True:
            seed += 1
            random.seed(seed)
            for method, args, expected in zip(methods, argss, expecteds):
                if method(*args) != expected:
                    break
            else:
                break
        print(f"SEEDING: {seed}")
        random.seed(seed)

    def _seed_me(self, method, args, expected):
        return self._seed_me_multiple([method], [args], [expected])

    def unique(self, prefix):
        return prefix + uuid.uuid4().hex[:7]
