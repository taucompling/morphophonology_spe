from simulation_test import SimulationTest, SimulationCase
from configuration import Configuration

configurations = Configuration()

class FrenchDeletionExtraVowel(SimulationTest):
    def setUp(self):
        self.initialise_segment_table("french_deletion_with_h_extra_vowel_segment_table.txt")
        self.data = ['tab', 'tabl', 'lib', 'libl', 'tap', 'tapl', 'rud', 'rudl', 'parl', 'birl', 'tpul', 'tbir', 'rdahl', 'tuhl', 'tid', 'ruap', 'dail', 'rlid', 'puard']
        configurations["DATA_ENCODING_LENGTH_MULTIPLIER"] = 200
        configurations["HMM_ENCODING_LENGTH_MULTIPLIER"] = 10


    def test_(self):

        #target
        target_words = ['tabl', 'libl', 'tapl', 'rudl', 'parl', 'birl', 'tpul', 'tbir', 'rdahl', 'tuhl', 'tid', 'ruap', 'dail', 'rlid', 'puard']

        self.target_energy = None
        hmm = {'q0': ['q1'],
            'q1': (['qf'], target_words),
              }

        rule = [[{"liquid": "+"}], [], [{"cons": "+", "son": "-"}], [], False]
        target = SimulationCase("target", hmm, [rule])
        self.target_energy = self.get_energy(target)


        #initial
        hmm = {'q0': ['q1'],
            'q1': (['qf'], self.data[:]),
              }
        initial = SimulationCase("initial", hmm, [])
        self.get_energy(initial)


        #iu_insertion
        hmm_emissions = ['birl', 'dail', u'lb', u'lbl', 'parl', u'puard', 'rdahl', u'rld', 'ruap', 'rud', 'rudl', u'tab', 'tabl', 'tap', 'tapl', 'tbir', 'tid', 'tpul', 'tuhl']
        hmm = {'q0': ['q1'],
            'q1': (['qf'], hmm_emissions),
              }
        iu_insertion_rule = [[], [{'high': '+'}], [{'liquid': '+'}], [{}], True]
        iu_insertion = SimulationCase("iu_insertion", hmm, [iu_insertion_rule])
        self.get_energy(iu_insertion)


