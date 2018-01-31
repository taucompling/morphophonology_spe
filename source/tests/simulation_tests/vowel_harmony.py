from simulation_test import SimulationTest, SimulationCase
from configuration import Configuration

configurations = Configuration()

class VowelHarmony(SimulationTest):
    def setUp(self):
        self.initialise_segment_table("vowel_harmony_segment_table.txt")
        self.data = ['sadadatata', 'gekezeze', u'ge', u'ga', 'sekekeze', 'gadatata', 'gakakaza', u'gakaza', 'sata', 'sededeteze', 'sekeketete', 'sakada', 'sakakazaza', 'sededezete', u'sakata', 'sedetete', 'sekedeze', 'sadadazaza', 'gakadazaza', 'gekekezete', 'sakatata', 'sakakataza', u'gedete', 'sekedezeze', u'gada', 'gedede', 'gekekete', 'gadataza', u'sadaza', 'gedeketeze', 'gezeze', 'gekedezete', u'gadata', 'gadakatata', 'gadadatata', 'sazaza', 'seteze', 'geketeze', 'gakadatata', u'gakata', 'gadadazaza', 'gedeteze', 'sekekete', 'sadadazata', 'gadadaza', 'sakakatata', u'gekeze', 'gadakazaza', 'gadakazata', 'gadadataza', 'sadakazaza', 'gakakata', u'gedeze', 'gedekeze', 'gadakata', 'sakazata', 'sakakaza', 'gededeteze', u'sadata', 'gezete', 'gekede', 'sekekezete', 'gedetete', 'sedeke', u'gadaza', 'sekeke', u'saka', 'sedekezete', 'sedede', 'sedezete', 'sazata', u'sedete', 'gekeke', u'sakaza', 'gazaza', 'sadakata', 'gadadazata', u'sekeze', u'gekete', 'sekezeze', 'gekedetete', 'gedeke', u'gede', u'gaka', 'sedezeze', 'sakadata', 'gete', 'gedezete', u'geke', 'sakadazata', 'gakadata', u'sekete', 'gadazaza', u'sada', 'gekekeze', 'sededetete', 'sekede', 'sekedete', 'sadaka', 'sedekete', u'sede', 'seketeze', 'gekeketeze', u'sa', 'sete', 'gekedeteze', 'sadazaza', u'sedeze', 'setete', 'gekedeze', u'seke', 'sakadataza', u'se']
        configurations["DATA_ENCODING_LENGTH_MULTIPLIER"] = 25
        configurations["HMM_ENCODING_LENGTH_MULTIPLIER"] = 5


    def test_(self):
        self.target_energy = None
        hmm = {'q0': ['q1'],
              'q1': (['q3', 'q2', 'qf'], ['ga', 'ge', 'sa', 'se']),
              'q2': (['q3','q2','qf'], ['da', 'ka']),
              'q3': (['q3', 'qf'], ['ta', 'za'])
                }

        rule = [[{"back": "+"}], [{"back": "-"}], [{"cons": "-", "back": "-"}, {"cons": "+"}], [], True]
        target = SimulationCase("target", hmm, [rule])
        self.target_energy = self.get_energy(target)


        hmm = {'q0': ['q1'],
              'q1': (['q1', 'qf'], ['a', 'e', 't', 'd', 'k', 'g', 's', 'z'])
                }
        initial = SimulationCase('initial', hmm, [])
        self.get_energy(initial)

        hmm = {'q0': ['q1'],
            'q1': (['qf'], self.data[:]),
              }

        ident = SimulationCase("ident", hmm, [])
        self.get_energy(ident)


        hmm = {'q0': ['q1'],
              'q1': (['q3', 'q2', 'qf'], ['ga', 'ge', 'sa', 'se']),
              'q2': (['q3','q2','qf'], ['d', 'k']),
              'q3': (['q3', 'qf'], ['t', 'z'])
                }

        rule = [[], [{'cons': '-'}], [{'cons': '+'}], [], True]
        vowel_insertion = SimulationCase("vowel_insertion", hmm, [rule])
        self.get_energy(vowel_insertion)