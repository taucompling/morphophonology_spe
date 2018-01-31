from simulation_test import SimulationTest, SimulationCase
from configuration import Configuration

configurations = Configuration()

class IcelandicUmlaut(SimulationTest):
    def setUp(self):
        self.initialise_segment_table("icelandic_umlaut_segment_table.txt")
        self.data = [u'parmAtum', u'parmAtumda', u'parmatur', u'parmaturamt', u'parmat', u'paum', u'paumda', u'par', u'paramt', u'pa', u'puduretur', u'pudureturamt', u'puduret', u'puduretum', u'puduretumda', u'petaum', u'petaumda', u'petar', u'petaramt', u'peta', u'epuraum', u'epuraumda', u'epurar', u'epuraramt', u'epura', u'dAmum', u'dAmumda', u'damur', u'damuramt', u'dam', u'durpAmum', u'durpAmumda', u'durpamur', u'durpamuramt', u'durpam', u'murtaum', u'murtaumda', u'murtar', u'murtaramt', u'murta', u'mudAtum', u'mudAtumda', u'mudatur', u'mudaturamt', u'mudat', u'rAtum', u'rAtumda', u'ratur', u'raturamt', u'rat', u'rempur', u'rempuramt', u'remp', u'rempum', u'rempumda']
        configurations["DATA_ENCODING_LENGTH_MULTIPLIER"] = 25
        configurations["HMM_ENCODING_LENGTH_MULTIPLIER"] = 1


    def test_(self):
        self.target_energy = None

        hmm = {'q0': ['q1'],
              'q1': (['q2','qf'], ['dam', 'mudat', 'durpam', 'rat', 'epura', 'parmat', 'puduret', 'pa', 'remp', 'murta', 'peta']),
              'q2': (['qf'], ['r', 'um', 'ramt', 'umda'])}

        umlaut_rule = [[{"low": "+"}], [{"round": "+"}],  [],  [{"cons": "+"}, {"round": "+"}], True]
        epenthesis_rule = [[], [{"low": "-", "round": "+"}], [{"cons": "+"}], [{"rhotic": "+"}], True]
        target = SimulationCase("target", hmm, [umlaut_rule, epenthesis_rule])
        self.target_energy = self.get_energy(target)

        hmm = {'q0': ['q1'],
            'q1': (['q1', 'qf'], list("ptdmraAue")),
              }

        initial = SimulationCase("initial", hmm, [])
        self.get_energy(initial)