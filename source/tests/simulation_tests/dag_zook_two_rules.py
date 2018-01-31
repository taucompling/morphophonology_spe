from simulation_test import SimulationTest, SimulationCase
from configuration import Configuration

configurations = Configuration()

class TestDakZookTwoRules(SimulationTest):
    def setUp(self):
        self.target_energy = None
        self.initialise_segment_table("plural_english_segment_table.txt")
        self.data = [u'dagdod', u'daggos', u'dagzook', u'dagsad', u'dag', u'dgodod', u'dgogos', u'dgozook', u'dgosad', u'dgo', u'dottod', u'dotkos', u'dotsook', u'dotsad', u'dot', u'tozazook', u'tozasad', u'tozdod', u'tozgos', u'toz', u'gasazook', u'gasasad', u'gastod', u'gaskos', u'gas', u'gdasazook', u'gdasasad', u'gdastod', u'gdaskos', u'gdas', u'koddod', u'kodgos', u'kodzook', u'kodsad', u'kod', u'ktadod', u'ktagos', u'ktazook', u'ktasad', u'kta', u'kattod', u'katkos', u'katsook', u'katsad', u'kat', u'skozazook', u'skozasad', u'skozdod', u'skozgos', u'skoz']

        configurations["DATA_ENCODING_LENGTH_MULTIPLIER"] = 25

        hmm = {'q0': ['q1'],
              'q1': (['q2','qf'], ['dag', 'kat', 'dot', 'kod', 'gas', 'toz', 'kta', 'dgo', 'skoz', 'gdas']),
              'q2': (['qf'], ['zook', 'gos', 'dod', 'sad'])}

        target_rule_set = [[[], [{"cons": "-", "low": "+"}], [{"cons": "+", "cont": "+"}], [{"cons": "+", "cont": "+"}], True],
                           [[{"cons": "+"}], [{"voice": "-"}], [{"voice": "-"}], [], True]]

        target = SimulationCase('target', hmm, target_rule_set)
        self.target_energy = self.get_energy(target)

        hmm = {'q0': ['q1'],
              'q1': (['q1', 'qf'], ['a', 'o', 't', 'd', 'k', 'g', 's', 'z'])
                }
        from_simulation_extra = SimulationCase('naive', hmm, [])
        self.get_energy(from_simulation_extra)


        hmm = {'q0': ['q1'],
              'q1': (['q1', 'qf'], ['a', 'o', 't', 'd', 'k', 'g', 's', 'z'])
                }
        from_simulation_extra = SimulationCase('naive_target', hmm, target_rule_set)
        self.get_energy(from_simulation_extra)



    def test_(self):
        x =1
        self.assertEqual(x, 1)
