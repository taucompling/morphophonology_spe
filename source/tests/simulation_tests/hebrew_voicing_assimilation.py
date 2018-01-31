from simulation_test import SimulationTest, SimulationCase
from rule import Rule
from rule_set import RuleSet
class HebrewVoicingAssimilation(SimulationTest):
    def setUp(self):
        self.initialise_segment_table("hebrew_voicing_assimilation_segment_table.txt")

    def test_2(self):
        rule1 = [[], [{"ATR": "+"}], [{"coronal": "+"}], [{"coronal": "+"}], True]
        rule2 = [[{"voice": "+"}], [{"voice": "-"}], [{"voice": "-"}], [], True]
        rule_set = RuleSet([Rule(*rule1), Rule(*rule2)])
        result = rule_set.get_outputs_of_word('daadt')
        print(result)

    def test_(self):
        self.data = ['katav', 'daag', 'rakad', 'takaf', 'kataft', 'daakt', 'rakadet', 'takaft']
        hmm = {'q0': ['q1'],
            'q1': (['q2', 'qf'], ['katav', 'daag', 'rakad', 'takaf']),
            'q2': (['qf'], ['t'])
              }
        rule1 = [[], [{"ATR": "+"}], [{"coronal": "+"}], [{"coronal": "+"}], True]
        rule2 = [[{"voice": "+"}], [{"voice": "-"}], [], [{"voice": "-"}], True]
        target = SimulationCase("taget", hmm, [rule1, rule2])
        return self.get_energy(target)

        # target = SimulationCase("target", )


