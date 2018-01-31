from simulation_test import SimulationTest, SimulationCase
from configuration import Configuration

configurations = Configuration()

class GermanOpacity(SimulationTest):
    def setUp(self):
        self.initialise_segment_table("german_opacity_segment_table.txt")
        configurations["DATA_ENCODING_LENGTH_MULTIPLIER"] = 25
        self.data = [u'cicun', u'ciin', u'ci', u'ciacun', u'cia', u'cirin', u'craxun', u'crain', u'cra', u'axtuxun', u'axtuin', u'axtu', u'icnaxun', u'icnain', u'icna', u'naxun', u'nain', u'na', u'truxun', u'truin', u'tru', u'taacun', u'taa', u'tarin', u'tuacun', u'tua', u'turin', u'taniacun', u'tania', u'tanirin', u'tranicun', u'traniin', u'trani']
        configurations["HMM_ENCODING_LENGTH_MULTIPLIER"] = 1
        configurations["RESTRICTIONS_ON_ALPHABET"] = False
        configurations["MORPHEME_BOUNDARY_FLAG"] = False
        configurations["WORD_BOUNDARY_FLAG"] = True

    def test_(self):
        self.target_energy = None

        hmm = {'q0': ['q1'],
              'q1': (['q2', 'qf'], ['ci','na','tur','cir','tar','tru','cra','axtu','icna','tanir','trani']),
              'q2': (['qf'], ['in', 'cun'])}

        backing_rule = [[{"velar": "+"}], [{"back": "+"}], [{"back":"+", "cons":"-"}], [], True]
        vocalization_rule = [[{"low": "+"}], [{"cons":"-", "coronal":"-"}], [], [{"cons":"+"}], True]
        target = SimulationCase("target", hmm, [backing_rule, vocalization_rule])
        self.target_energy = self.get_energy(target)


        hmm = {'q0': ['q1'],
            'q1': (['q1', 'qf'], list("ntxcraui")),
              }

        initial = SimulationCase("initial", hmm, [])
        self.get_energy(initial)

    def test_only_vocalization(self):
        self.target_energy = None
        self.data = [u'cicun', u'ciin', u'ci', u'ciacun', u'cia', u'cirin', u'cracun', u'crain', u'cra', u'axtucun', u'axtuin', u'axtu', u'icnacun', u'icnain', u'icna', u'nacun', u'nain', u'na', u'trucun', u'truin', u'tru', u'taacun', u'taa', u'tarin', u'tuacun', u'tua', u'turin', u'taniacun', u'tania', u'tanirin', u'tranicun', u'traniin', u'trani']
        hmm = {'q0': ['q1'],
              'q1': (['q2', 'qf'], ['ci','na','tur','cir','tar','tru','cra','axtu','icna','tanir','trani']),
              'q2': (['qf'], ['in', 'cun'])}

        vocalization_rule = [[{"low": "+"}], [{"cons":"-", "coronal":"-"}], [], [{"cons":"+"}], True]
        target = SimulationCase("target", hmm, [vocalization_rule])
        self.target_energy = self.get_energy(target)

        hmm = {'q0': ['q1'],
         'q1': (['q1', 'qf'], list("ntxcraui")),
             }

        initial = SimulationCase("initial", hmm, [])
        self.get_energy(initial)


    def test_mini_german(self):
        self.target_energy = None

        self.data = ['turin', 'tuacun', 'tua']

        hmm = {'q0': ['q1'],
              'q1': (['q2', 'qf'], ['tur']),
              'q2': (['qf'], ['in', 'cun'])}


        backing_rule = [[{"velar": "+"}], [{"back": "+"}], [{"back":"+", "cons":"-"}], [], True]
        vocalization_rule = [[{"low": "+"}], [{"cons":"-", "coronal":"-"}], [], [{"cons":"+"}], True]
        print(backing_rule)
        target = SimulationCase("target", hmm, [backing_rule, vocalization_rule])
        self.target_energy = self.get_energy(target)


        hmm = {'q0': ['q1'],
            'q1': (['q1', 'qf'], list("ntxcraui")),
              }

        initial = SimulationCase("initial", hmm, [])
        self.get_energy(initial)