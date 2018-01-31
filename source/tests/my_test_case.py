import unittest
from os.path import join, split, abspath
from segment_table import SegmentTable

from rule_set import RuleSet
from tests.test_util import write_to_dot_to_file, get_hypothesis_from_log_string

tests_dir_path, filename = split(abspath(__file__))
fixtures_dir_path = join(tests_dir_path, "fixtures")
dot_files_folder_path = join(tests_dir_path, "dot_files")
segment_table_dir_path = join(fixtures_dir_path, "segment_table")
rule_set_dir_path = join(fixtures_dir_path, "rule_set")
from configuration import Configuration

configurations = Configuration()


class MyTestCase(unittest.TestCase):
    def initialise_simulation(self, simulation):
        configurations = Configuration()
        configurations.load_configuration_for_simulation(simulation)

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

    def write_to_dot_to_file(self, dotable_object, file_name):
        write_to_dot_to_file(dotable_object, file_name)

    def tearDown(self):
        configurations.reset_to_original_configurations()
