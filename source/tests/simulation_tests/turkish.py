from simulation_test import SimulationTest, SimulationCase
from configuration import Configuration

configurations = Configuration()

class Turkish(SimulationTest):
    def setUp(self):
        self.initialise_segment_table("turkish_segment_table.txt")
        self.data = [u'gu', u'sukuzu', 'sakuzuzu', 'gydezyzy', 'gudadata', u'gy', 'gudakuzuta', u'ge', 'sekydezyzy', 'sadadata', u'ga', u'sudazu', 'gykydetezy', 'gudadatata', u'gukuta', 'sededezyzy', u'gudazu', u'sakuta', 'gudatazu', u'syde', 'gekykyte', 'gedezyte', 'sededetezy', 'sykykyzyzy', 'guta', u'gydezy', 'sededezy', 'sedetete', u'guda', u'sydete', 'gydedezy', 'sukukuzu', 'sykydetete', u'syky', u'gedete', 'gedeky', 'gazuta', 'gedekytezy', 'sudakuzu', u'sadazu', u'gada', 'gedede', u'guku', 'gykyzyte', 'sadadazu', 'gekyzyte', u'gekyzy', u'gykyte', u'sekyzy', 'sukuda', 'sydedezy', 'gededete', u'gadata', 'gykykyte', 'sukutazu', 'gadatata', 'gakudazu', 'gudatata', 'gudadatazu', 'sukuzuzu', 'gedetezy', u'sykyzy', 'sykytete', 'gedezyzy', 'sekydetete', 'gukudatazu', 'sekytezy', u'gekyte', u'gakuzu', 'gukuda', 'gudakutata', 'gukutata', 'gukudata', 'sekykyzyzy', u'sekyte', 'sykykyzyte', 'sykykytezy', 'guzuzu', u'sydezy', 'gykyde', 'gudadazuzu', 'gykykytezy', 'gukukuzuzu', 'sudakuta', 'sutata', u'sykyte', 'sydekyzyzy', 'sedekyte', 'sukuzuta', 'sudatazu', 'gukukuzu', 'gakutazu', 'gakudazuta', 'sakudazuzu', u'gadazu', 'sutazu', 'gukukutata', 'gazuzu', 'sudadatata', u'saku', 'gakuda', 'gadakuzuta', u'sedete', u'gakuta', 'gakudatata', 'gadakuta', 'gekytezy', 'gadakutazu', u'sukuta', 'sukudazuta', 'sadadatazu', 'sadakuzuta', 'gykykytete', u'gukuzu', u'sudata', u'suda', u'gudata', u'gedezy', u'sakuzu', u'gede', 'gydezyte', u'gyde', 'syzyzy', u'geky', 'gete', u'gydete', u'gaku', 'sadazuta', u'suku', 'sykydetezy', u'sada', u'gyky', u'sede', u'sadata', 'gydekyzy', 'sadaku', u'seky', u'sy', 'sazuzu', u'gykyzy', u'su', u'sedezy', 'gedekyzyte', 'gekykytete', 'sukudazuzu', 'sydedete', u'sa', u'se']
        configurations["DATA_ENCODING_LENGTH_MULTIPLIER"] = 25
        configurations["HMM_ENCODING_LENGTH_MULTIPLIER"] = 5


    def test_(self):
        self.target_energy = None
        hmm = {'q0': ['q1'],
              'q1': (['q3', 'q2', 'qf'], ['ga', 'ge', 'gu', 'gy', 'sa', 'se', 'su', 'sy']),
              'q2': (['q3','q2','qf'], ['da', 'ku']),
              'q3': (['q3', 'qf'], ['ta', 'zu'])
                }

        rule = [[{"back": "+"}], [{"back": "-"}], [{"cons": "-", "back": "-"}, {"cons": "+"}], [], True]
        target = SimulationCase("target", hmm, [rule])
        self.target_energy = self.get_energy(target)


        hmm = {'q0': ['q1'],
              'q1': (['q1', 'qf'], ['a', 'e', 't', 'd', 'k', 'g', 's', 'z','u', 'y'])
                }
        initial = SimulationCase('initial', hmm, [])
        self.get_energy(initial)

        hmm = {'q0': ['q1'],
            'q1': (['qf'], self.data[:]),
              }

        ident = SimulationCase("ident", hmm, [])
        self.get_energy(ident)


        hmm = {'q0': ['q1'],
              'q1': (['q3', 'q2', 'qf'], ['ga', 'ge', 'gu', 'gy', 'sa', 'se', 'su', 'sy']),
              'q2': (['q3','q2','qf'], ['d', 'k']),
              'q3': (['q3', 'qf'], ['t', 'z'])
                }

        rule = [[], [{'cons': '-'}], [{'cons': '+'}], [], True]
        vowel_insertion = SimulationCase("vowel_insertion", hmm, [rule])
        self.get_energy(vowel_insertion)