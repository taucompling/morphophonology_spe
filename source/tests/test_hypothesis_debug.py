from util import log_hypothesis, log_hmm, log_rule_set
from tests.my_test_case import MyTestCase
from tests.test_util import get_hypothesis_from_log_string, get_hmm_from_hypothesis_string


class TestHypothesisDebug(MyTestCase):
    def setUp(self):
        pass

    def test_get_hypothesis_from_debug_string(self):
        from simulations import french_two_rules as simulation
        self.initialise_simulation(simulation)

        hypothesis_string = """
        HMM: states ['q1', 'q2'], transitions {'q1': ['q2'], 'q2': ['qf'], 'q0': ['q1']}, emissions {'q1': ['arb', 'tab', 'kup', 'yrl', 'purp', 'filt', 'romp', 'byl', 'dart', 'mord', 'kuverk', 'prut', 'kylt', 'amur', 'klop', 'film', 'kurb', 'kapt', 'tabl', 'krab', 'karaf', 'parl', 'provok', 'filtr', 'klad', 'kuverkl', 'purpr', 'odor', 'arbr', 'furyr', 'burk', 'kupl', 'batir', 'rompr', 'mordr', 'dartr'], 'q2': ['mal', 'iv', 'ε', 'fad', 'puri', 'byvab', 'kif', 'timid', 'abil']}
HMM:
q0: ['q1']
q1: ['q2'], ['amur', 'arb', 'arbr', 'batir', 'burk', 'byl', 'dart', 'dartr', 'film', 'filt', 'filtr', 'furyr', 'kapt', 'karaf', 'klad', 'klop', 'krab', 'kup', 'kupl', 'kurb', 'kuverk', 'kuverkl', 'kylt', 'mord', 'mordr', 'odor', 'parl', 'provok', 'prut', 'purp', 'purpr', 'romp', 'rompr', 'tab', 'tabl', 'yrl']
q2: ['qf'], ['abil', 'byvab', 'fad', 'iv', 'kif', 'mal', 'puri', 'timid', 'ε']
q0->q1->q2->qf
Rule Set:
transducer_generated:
[] --> [{'back': '+', 'center': '+', 'high': '-', 'low': '-'}] / [{'cons': '+'}, {'strident': '-'}, {'MB': True}]__[{'cons': '+'}] obligatory: False | ε --> ['e'] / [['p', 'd', 'v', 't', 'k', 'l', 'r', 'm', 'f', 'b'], ['p', 'm', 'd', 'e', 't', 'k', 'a', 'i', 'l', 'r', 'u', 'o', 'y', 'b'], ['B']]__[['p', 'd', 'v', 't', 'k', 'l', 'r', 'm', 'f', 'b']] obligatory: False
[] --> [{'back': '-', 'liquid': '+', 'strident': '-', 'voice': '+'}] / [{'cons': '-', 'lateral': '-'}, {'back': '-', 'center': '-', 'liquid': '-', 'voice': '+'}, {'MB': True}]__[] obligatory: False | ε --> ['l', 'r'] / [['e', 'a', 'i', 'u', 'o', 'y'], ['d', 'b', 'i', 'm', 'y', 'v'], ['B']]__[] obligatory: False
[] --> [{'lateral': '+'}] / [{'MB': True}]__[{'MB': True}, {'lateral': '-', 'voice': '+'}, {'voice': '+'}] obligatory: False | ε --> ['l'] / [['B']]__[['B'], ['o', 'd', 'b', 'e', 'a', 'i', 'r', 'u', 'm', 'y', 'v'], ['m', 'd', 'v', 'e', 'a', 'i', 'l', 'r', 'u', 'o', 'y', 'b']] obligatory: False
not transducer_generated:
Energy: 250,819.10989435515 (data_by_grammar: 230,883.2703113556, hmm: 19,624.83958299955, rule_set: 311.0)
        
        """

        hypothesis = get_hypothesis_from_log_string(hypothesis_string)
        log_hypothesis(hypothesis)
        print(hypothesis.get_energy())
        print(hypothesis.get_recent_energy_signature())
        # print(len(hypothesis.grammar.get_transducer()))

    def test_save_hmm_image_from_string(self):
        s = """
        17-12-01 17:45:57 	 HMM:  states ['q1'], transitions {'q1': ['qf'], 'q0': ['q1']}, emissions {'q1': ['adorabl', 'aktif', 'arab', 'arbr', 'brylabl', 'byvabl', 'dyr', 'fiabl', 'fiksabl', 'final', 'finir', 'fumabl', 'fur', 'furyr', 'fylar', 'kadr', 'kafar', 'kalkyl', 'kapabl', 'karaf', 'katr', 'kudr', 'kupl', 'kyrabl', 'lavabl', 'luabl', 'mais', 'marl', 'martir', 'masif', 'mil', 'misil', 'mol', 'montr', 'mordr', 'mutar', 'nap', 'nyl', 'ordr', 'orl', 'parkur', 'parl', 'partir', 'pip', 'polar', 'posibl', 'postyr', 'potabl', 'prut', 'purir', 'pys', 'ridikyl', 'ryptyr', 'saly', 'sibl', 'sidr', 'sifl', 'sirkl', 'sortir', 'stad', 'stryktyr', 'supl', 'tabl', 'titr', 'trubl', 'vivabl', 'yrl', 'nobl']}
17-12-01 17:45:57 	 HMM:

        """
        name = 'french_deletion_new'
        hmm = get_hmm_from_hypothesis_string(s)
        self.write_to_dot_to_file(hmm, name)