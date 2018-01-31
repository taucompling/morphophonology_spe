from simulation_test import SimulationTest, SimulationCase
from configuration import Configuration

configurations = Configuration()

class TkAspiration(SimulationTest):
    def setUp(self):
        self.initialise_segment_table("tk_aspiration_segment_table.txt")
        self.data = ['ithik', 'thatkha', 'thatthat', 'ikhak', 'khikthak', 'khathiit', 'ithak', 'thikhiat', 'thakhiit', 'khikhi']
        configurations["DATA_ENCODING_LENGTH_MULTIPLIER"] = 1000
        configurations["HMM_ENCODING_LENGTH_MULTIPLIER"] = 50
        configurations["RESTRICTIONS_ON_ALPHABET"] = True


    def test_(self):
        self.target_energy = None
        hmm = {'q0': ['q1'],
            'q1': (['qf'], [word.replace("h","") for word in self.data[:]]),
              }

        rule = [[], [{"asp": "+"}], [{"stop": "+"}], [{"cons": "-"}], True]
        target = SimulationCase("target", hmm, [rule])
        self.target_energy = self.get_energy(target)

        hmm = {'q0': ['q1'],
            'q1': (['qf'], self.data[:]),
              }


        initial = SimulationCase("initial", hmm, [])
        self.get_energy(initial)

        hmm = {'q0': ['q1'],
            'q1': (['qf'], [u'hahiit', u'hattat', u'ihak', u'itik', u'kihi', u'kikhak', u'tatka', u'tikiat']),
              }

        rule1 = [[], [{'high': '-', 'asp': '-', 'stop': '+'}], [], [{'asp': '+'}], True]
        rule2 = [[], [{'velar': '-', 'asp': '+', 'stop': '-'}], [{'high': '-', 'stop': '+'}], [{'asp': '-', 'stop': '-'}], True]
        from_simulation1 = SimulationCase("from_simulation1", hmm, [rule1, rule2])
        self.get_energy(from_simulation1)