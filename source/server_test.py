from os.path import join, split, abspath
from segment_table import SegmentTable
from collections import namedtuple
from hmm import HMM
from grammar import Grammar
from rule import Rule
from rule_set import RuleSet
from hypothesis import Hypothesis

SimulationCase = namedtuple('SimulationHypothesis', ['case_name', 'hmm_dict', 'flat_rule_set_list'])

tests_dir_path, filename = split(abspath(__file__))
fixtures_dir_path = join(tests_dir_path, "fixtures")
dot_files_folder_path = join(tests_dir_path, "dot_files")
segment_table_dir_path = join(fixtures_dir_path, "segment_table")
rule_set_dir_path = join(fixtures_dir_path, "rule_set")
from configuration import Configuration

configurations = Configuration()
def initialise_segment_table(segment_table_file_name):
    segment_table_fixture_path = join(segment_table_dir_path, segment_table_file_name)
    SegmentTable.load(segment_table_fixture_path)

def get_energy(self, simulation_case):
    case_name = simulation_case.case_name
    if isinstance(simulation_case.hmm_dict, HMM):
        hmm = simulation_case.hmm_dict
    else:
        hmm = HMM(simulation_case.hmm_dict)
    if isinstance(simulation_case.flat_rule_set_list, RuleSet):
        rule_set = simulation_case.flat_rule_set_list
    else:
        rule_set_list = []
        for flat_rule in simulation_case.flat_rule_set_list:
            rule_set_list.append(Rule(*flat_rule))
        rule_set = RuleSet(rule_set_list)
    grammar = Grammar(hmm, rule_set)
    self.write_to_dot_file(hmm, "hmm")
    self.write_to_dot_file(grammar.get_nfa(), "grammar_nfa_" + case_name)
    hypothesis = Hypothesis(grammar, self.data)
    energy = hypothesis.get_energy()
    print("{}: {}".format(case_name, hypothesis.get_recent_energy_signature()))
    return energy

initialise_segment_table("cons_optionality_segment_table.txt")
data = [u'katoragod', u'katorad', u'katoroto', u'katoko', u'katoagod', u'katoad', u'katooto', u'kato', u'akdko', u'akdagod', u'akdad', u'akdoto', u'akd', u'odaragod', u'odarad', u'odaroto', u'odako', u'odaagod', u'odaad', u'odaoto', u'oda', u'dtoragod', u'dtorad', u'dtoroto', u'dtoko', u'dtoagod', u'dtoad', u'dtooto', u'dto', u'dagko', u'dagagod', u'dagad', u'dagoto', u'dag', u'dogaragod', u'dogarad', u'dogaroto', u'dogako', u'dogaagod', u'dogaad', u'dogaoto', u'doga', u'takaragod', u'takarad', u'takaroto', u'takako', u'takaagod', u'takaad', u'takaoto', u'taka', u'gtaragod', u'gtarad', u'gtaroto', u'gtako', u'gtaagod', u'gtaad', u'gtaoto', u'gta']
configurations["DATA_ENCODING_LENGTH_MULTIPLIER"] = 10
configurations["HMM_ENCODING_LENGTH_MULTIPLIER"] = 10


hmm = {'q0': ['q1'],
      'q1': (['q2', 'qf'], ['taka', 'doga', 'kato', 'dto', 'oda', 'gta', 'akd', 'dag']),
      'q2': (['qf'], ['agod', 'oto', 'ko', 'ad'])}

epenthesis_rule = [[], [{"rhotic": "+"}], [{"cons": "-"}], [{"cons": "-"}], False]
target = SimulationCase("target", hmm, [epenthesis_rule])
get_energy(target)


hmm = {'q0': ['q1'],
    'q1': (['q1', 'qf'], list("aotdkgr")),
      }


initial = SimulationCase("initial", hmm, [])
get_energy(initial)


hmm = {'q0': ['q1'],
      'q1': (['q2', 'qf'], ['taka', 'doga', 'kato', 'dto', 'oda', 'gta', 'akd', 'dag']),
      'q2': (['qf'], ['agod', 'oto', 'ko', 'ad', 'ragod', 'roto', 'rad'])}

no_rule = SimulationCase("no_rule", hmm, [])
get_energy(no_rule)

hmm = {'q0': ['q1'],
      'q1': (['q2', 'q3',  'qf'], ['taka', 'doga', 'kato', 'dto', 'oda', 'gta', 'akd', 'dag']),
      'q2': (['qf'], ['agod', 'oto', 'ko', 'ad']),
      'q3': (['q2'], ['r'])}

r_morpheme = SimulationCase("r_morpheme", hmm, [])
get_energy(r_morpheme)


