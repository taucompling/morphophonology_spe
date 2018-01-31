from simulation_test import SimulationTest, SimulationCase
from configuration import Configuration

configurations = Configuration()

class ConsOptionality(SimulationTest):
    def setUp(self):
        self.initialise_segment_table("cons_optionality_segment_table.txt")
        self.data = [u'katoragod', u'katorad', u'katoroto', u'katoko', u'katoagod', u'katoad', u'katooto', u'kato', u'akdko', u'akdagod', u'akdad', u'akdoto', u'akd', u'odaragod', u'odarad', u'odaroto', u'odako', u'odaagod', u'odaad', u'odaoto', u'oda', u'dtoragod', u'dtorad', u'dtoroto', u'dtoko', u'dtoagod', u'dtoad', u'dtooto', u'dto', u'dagko', u'dagagod', u'dagad', u'dagoto', u'dag', u'dogaragod', u'dogarad', u'dogaroto', u'dogako', u'dogaagod', u'dogaad', u'dogaoto', u'doga', u'takaragod', u'takarad', u'takaroto', u'takako', u'takaagod', u'takaad', u'takaoto', u'taka', u'gtaragod', u'gtarad', u'gtaroto', u'gtako', u'gtaagod', u'gtaad', u'gtaoto', u'gta']
        configurations["DATA_ENCODING_LENGTH_MULTIPLIER"] = 10
        configurations["HMM_ENCODING_LENGTH_MULTIPLIER"] = 10


    def test_(self):
        self.target_energy = None

        hmm = {'q0': ['q1'],
              'q1': (['q2', 'qf'], ['akd', 'dag', 'doga', 'dto', 'gta', 'kato', 'oda', 'taka']),
              'q2': (['qf'], ['ad', 'agod', 'ko', 'oto'])}

        epenthesis_rule = [[], [{"rhotic": "+"}], [{"cons": "-"}], [{"cons": "-"}], False]
        target = SimulationCase("target", hmm, [epenthesis_rule])
        self.target_energy = self.get_energy(target)


        hmm = {'q0': ['q1'],
            'q1': (['q1', 'qf'], list("aotdkgr")),
              }


        initial = SimulationCase("initial", hmm, [])
        self.get_energy(initial)



        hmm = {'q0': ['q1'],
              'q1': (['q2', 'qf'], ['akd', 'dag', 'doga', 'dto', 'gta', 'kato', 'oda', 'taka']),
              'q2': (['qf'], ['ad', 'agod', 'ko', 'oto'] + ['ragod', 'roto', 'rad'])}

        no_rule = SimulationCase("no_rule", hmm, [])
        self.get_energy(no_rule)

        hmm = {'q0': ['q1'],
              'q1': (['q2', 'q3',  'qf'], ['akd', 'dag', 'doga', 'dto', 'gta', 'kato', 'oda', 'taka']),
              'q2': (['qf'], ['ad', 'agod', 'ko', 'oto']),
              'q3': (['q2'], ['r'])}

        r_morpheme = SimulationCase("r_morpheme", hmm, [])
        self.get_energy(r_morpheme)

        hmm = {'q0': ['q1'],
              'q1': (['q2', 'qf'], ['akd', 'dag', 'doga', 'dto', 'gta', 'kato', 'oda', 'taka']),
              'q2': (['qf'], ['ko'] + ['ragod', 'roto', 'rad']),
              }

        rule = [[{'rhotic': '+'}], [], [], [], False]
        r_deletion = SimulationCase("r_deletion", hmm, [rule])
        self.get_energy(r_deletion)


        hmm = {'q0': ['q1'],
              'q1': (['q2', 'qf'], ['akd', u'dag', u'doga', 'dto', u'gta', 'kato', u'oda', u'taka']),
              'q2': (['qf'], ['ko', 'r', 'rad', u'ragod', u'roto']),
              }

        rule = [[{'rhotic': '+'}], [], [], [], False]
        from_simulation1 = SimulationCase("from_simulation1", hmm, [rule])
        self.get_energy(from_simulation1)

        hmm = {'q0': ['q1'],
       'q1': (['q2', 'qf'], [u'akd', u'dag', u'doga', u'dto', u'gta', u'kato', 'oda', u'taka']),
       'q2': (['qf'], [u'ad', 'agod', u'ko', u'oto'])}

        rule = [[], [{'rhotic': '+', 'low': '-'}], [{'cons': '-'}], [{'cons': '-'}], False]
        from_simulation2 = SimulationCase("from_simulation2", hmm, [rule])
        self.get_energy(from_simulation2)