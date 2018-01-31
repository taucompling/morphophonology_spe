from simulation_test import SimulationTest, SimulationCase
from configuration import Configuration

configurations = Configuration()

class TestNewOpacity(SimulationTest):
    def setUp(self):
        pass

    def test_strage(self):
        self.initialise_segment_table("opacity_segment_table.txt")
        self.data = [u'skazazoka']
        configurations["DATA_ENCODING_LENGTH_MULTIPLIER"] = 25
        hmm = {'q0': ['q1'],
              'q1': (['q2','qf'],  [u'stkaz']),
              'q2': (['qf'], [u'zoka'])}

        target_rule_set = [[[{'coronal': '+'}], [], [{'cons': '+'}], [{'cont': '-'}], True],
                          [[{'voice': '-'}], [], [], [{'voice': '-', 'coronal': '+'}], True],
                          [[], [{'low': '+'}], [{'coronal': '+'}], [{'coronal': '+'}], True],
                          [[{'cons': '+'}], [{'voice': '-'}], [{'voice': '-'}], [], True]]

        target = SimulationCase('target', hmm, target_rule_set)
        self.get_energy(target)



    # def test_(self):
    #     self.initialise_segment_table("opacity_segment_table.txt")
    #     self.data = [u'skazazoka', u'skazasaat', u'skazada', u'skazgo', u'skaz', u'dogzoka', u'dogsaat', u'dogda', u'doggo', u'dog', u'doksoka', u'doksaat', u'dokta', u'dokko', u'dok', u'dootasoka', u'dootasaat', u'dootata', u'dootko', u'doot', u'dkozazoka', u'dkozasaat', u'dkozada', u'dkozgo', u'dkoz', u'taksoka', u'taksaat', u'takta', u'takko', u'tak', u'gkasasoka', u'gkasasaat', u'gkasata', u'gkasko', u'gkas', u'gdaasasoka', u'gdaasasaat', u'gdaasata', u'gdaasko', u'gdaas', u'kodazoka', u'kodasaat', u'kodada', u'kodgo', u'kod', u'katasoka', u'katasaat', u'katata', u'katko', u'kat', u'kaoksoka', u'kaoksaat', u'kaokta', u'kaokko', u'kaok']
    #     configurations["DATA_ENCODING_LENGTH_MULTIPLIER"] = 25
    #     hmm = {'q0': ['q1'],
    #           'q1': (['q2','qf'],  [u'dkoz', u'dog', u'dok', u'doott', u'gdaass', u'gzkass', u'kaok', u'katt', u'kod', u'stkaz', u'tak']),
    #           'q2': (['qf'], [u'da', u'go', u'ksaat', u'zoka'])}
    #
    #     target_rule_set = [[[{'coronal': '+'}], [], [{'cons': '+'}], [{'cont': '-'}], True],
    #                       [[{'voice': '-'}], [], [], [{'voice': '-', 'coronal': '+'}], True],
    #                       [[], [{'low': '+'}], [{'coronal': '+'}], [{'coronal': '+'}], True],
    #                       [[{'cons': '+'}], [{'voice': '-'}], [{'voice': '-'}], [], True]]
    #
    #     target = SimulationCase('target', hmm, target_rule_set)
    #     self.get_energy(target)


    def test_(self):
        self.initialise_segment_table("opacity_segment_table.txt")
        self.data = [u'dootasoka']
        configurations["DATA_ENCODING_LENGTH_MULTIPLIER"] = 25

        hmm = {'q0': ['q1'],
              'q1': (['q3', 'q4' , 'qf'],  [u'doost']),
              'q2': (['qf'], ['a', u'saatt']),
              'q3': (['q2'], [u'd']),
              'q4': (['qf'], [u'go', u'zoka'])
                }

        target_rule_set = [
                          [[{'cons': '+'}], [], [], [{'voice': '-'}], True],
                          [[], [{'low': '+'}], [{'coronal': '+'}], [{'coronal': '+'}], True],
                          [[{'cons': '+'}], [{'voice': '-'}], [{'voice': '-'}], [], True],
                          ]

        target = SimulationCase('target', hmm, target_rule_set)
        self.get_energy(target)



    def test_comapre(self):
        self.initialise_segment_table("opacity_segment_table.txt")
        self.data = [u'takkos', u'taksok', u'taksaad', u'taktoad', u'tak', u'toozazok', u'toozasaad', u'toozadoad', u'toozgos', u'tooz', u'gaoasasok', u'gaoasasaad', u'gaoasatoad', u'gaoaskos', u'gaoas', u'gdaasasok', u'gdaasasaad', u'gdaasatoad', u'gdaaskos', u'gdaas', u'kaokkos', u'kaoksok', u'kaoksaad', u'kaoktoad', u'kaok', u'kodazok', u'kodasaad', u'kodadoad', u'kodgos', u'kod', u'katasok', u'katasaad', u'katatoad', u'katkos', u'kat', u'skozazok', u'skozasaad', u'skozadoad', u'skozgos', u'skoz', u'doggos', u'dogzok', u'dogsaad', u'dogdoad', u'dog', u'dokkos', u'doksok', u'doksaad', u'doktoad', u'dok', u'dootasok', u'dootasaad', u'dootatoad', u'dootkos', u'doot']

        configurations["DATA_ENCODING_LENGTH_MULTIPLIER"] = 25

        hmm = {'q0': ['q1'],
              'q1': (['q2','qf'],  ['tak', 'dog', 'kat', 'doot', 'kod', 'gaoas', 'tooz', 'skoz', 'gdaas', 'dok', 'kaok']),
              'q2': (['qf'], ['zok', 'gos', 'doad', 'saad'])}

        target_rule_set = [[[{"cons": "+"}], [{"voice": "-"}], [{"voice": "-"}], [], True],
                           [[], [{"cons": "-", "low": "+"}], [{"coronal": "+"}], [{"coronal": "+"}], True]]

        target = SimulationCase('target', hmm, target_rule_set)
        self.get_energy(target)



        hmm = {'q0': ['q1'],
              'q1': (['q1', 'qf'], ['a', 'o', 't', 'd', 'k', 'g', 's', 'z'])
                }
        naive = SimulationCase('naive', hmm, [])
        self.get_energy(naive)
        #
        #
        # hmm = {'q0': ['q1'],
        #       'q1': (['q1', 'qf'], ['a', 'o', 't', 'd', 'k', 'g', 's', 'z'])
        #         }
        # from_simulation_extra = SimulationCase('naive_target', hmm, target_rule_set)
        # self.get_energy(from_simulation_extra)




    def test_weird_final_hypothesis(self):
        self.initialise_segment_table("opacity_segment_table.txt")
        self.data = [u'takkos', u'taksok', u'taksaad', u'taktoad', u'tak', u'toozazok', u'toozasaad', u'toozadoad', u'toozgos', u'tooz', u'gaoasasok', u'gaoasasaad', u'gaoasatoad', u'gaoaskos', u'gaoas', u'gdaasasok', u'gdaasasaad', u'gdaasatoad', u'gdaaskos', u'gdaas', u'kaokkos', u'kaoksok', u'kaoksaad', u'kaoktoad', u'kaok', u'kodazok', u'kodasaad', u'kodadoad', u'kodgos', u'kod', u'katasok', u'katasaad', u'katatoad', u'katkos', u'kat', u'skozazok', u'skozasaad', u'skozadoad', u'skozgos', u'skoz', u'doggos', u'dogzok', u'dogsaad', u'dogdoad', u'dog', u'dokkos', u'doksok', u'doksaad', u'doktoad', u'dok', u'dootasok', u'dootasaad', u'dootatoad', u'dootkos', u'doot']

        configurations["DATA_ENCODING_LENGTH_MULTIPLIER"] = 25

        hmm = {'q0': ['q1', 'q2'],
              'q1': (['q2', 'q3', 'q4', 'qf'], ['d', 'g', 'k', 's', 't', 'z']),
              'q2': (['q3'], ['d', 'gda', 'k', 'sk']),
              'q3': (['q1', 'q3'], ['a', 'o']),
              'q4': (['qf'], ['gos', 's', 'saad', 'sok']),
              'q5': ([], [])}

        rule_set = [[[{'voice': '-'}], [{'cont': '-'}], [{'coronal': '+', 'low': '-'}], [{'cons': '+', 'cont': '-'}], True],
                    [[{'cont': '-'}], [{'voice': '-'}], [{'voice': '-'}], [], True],
                    [[{'coronal': '+'}], [{'voice': '+'}], [{'voice': '+'}], [{'cont': '+'}], False],
                    [[], [{'low': '+'}], [{'coronal': '+'}], [{'coronal': '+'}], True]]



        from_simulation_extra = SimulationCase('from_simulation', hmm, rule_set)
        self.get_energy(from_simulation_extra)