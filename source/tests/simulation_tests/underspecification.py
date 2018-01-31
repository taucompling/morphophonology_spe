from simulation_test import SimulationTest, SimulationCase
from configuration import Configuration
from rule_set import RuleSet
from rule import Rule
from hmm import HMM

configurations = Configuration()

class TestUnderspecification(SimulationTest):
    def setUp(self):
        configurations["DATA_ENCODING_LENGTH_MULTIPLIER"] = 25
        configurations["MORPHEME_BOUNDARY_FLAG"] = True
        configurations["UNDERSPECIFICATION_FLAG"] = True
        self.initialise_segment_table("underspecification_segment_table.txt")
        self.data = ['dat', 'tat', 'da', 'ta']



        hmm = HMM({'q0': ['q1'],
              'q1': (['q2','qf'], ['dag', 'kat', 'dot', 'kod', 'gas', 'toz', 'kta', 'dgo', 'skoz', 'gdas']),
              'q2': (['qf'], ['zook', 'gos', 'dod', 'sad'])})

        rule = Rule([{"voice": "0"}], [{"voice": "-"}], [], [{"bound": "+"}], True)
        rule.get_transducer()
        print(rule.get_segment_representation())
        rule_set = RuleSet([rule])

        print(rule_set.get_outputs_of_word('daTB'))

        #target = SimulationCase('target', hmm, rule_set)
        #self.get_energy(target)



    def test_(self):
        x =1
        self.assertEqual(x, 1)
