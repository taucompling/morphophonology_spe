from tests.my_test_case import MyTestCase
from tests.test_util import get_hypothesis_from_log_string, get_hmm_from_hypothesis_string


class TestHypothesisDebug(MyTestCase):
    def setUp(self):
        pass

    def test_get_message_from_debug_string(self):
        from simulations import catalan_small as simulation
        self.initialise_simulation(simulation)

        hypothesis_string = """Energy: 4063.0
Unparsed words: 0
Fitness: 4063.0
HMM: states ['q1', 'q2', 'q3', 'q4'], transitions {'q1': ['q2', 'q4'], 'q2': ['qf'], 'q0': ['q1'], 'q3': [], 'q4': ['qf']}, emissions {'q1': ['kamp', 'mal', 'blank', 'metal', 'kalent', 'plasa', 'plan', 'silen', 'kap', 'kuzi', 'kasa', 'kuzin', 'sile', 'pla'], 'q2': ['m'], 'q3': [], 'q4': ['a', 'ik', 'et', 's']}
HMM:
q0: ['q1']
q1: ['q2', 'q4'], ['blank', 'kalent', 'kamp', 'kap', 'kasa', 'kuzi', 'kuzin', 'mal', 'metal', 'pla', 'plan', 'plasa', 'sile', 'silen']
q2: ['qf'], ['m']
q3: [], []
q4: ['qf'], ['a', 'et', 'ik', 's']
q0->q1->q4->qf
q0->q1->q2->qf
Rule Set:
transducer_generated:
Rule([{'nasal': '+'}], [], [], [{'WB': True}], True) | ['m', 'n'] --> ε / []__[['W']] obligatory: True
Rule([{'voice': '-'}], [], [{'nasal': '+'}], [{'WB': True}], True) | ['s', 'p', 't', 'k'] --> ε / [['m', 'n']]__[['W']] obligatory: True
not transducer_generated:
Energy: 4,063.0 (data_by_grammar: 3,570.0, hmm: 423, rule_set: 70)
"""

        hypothesis = get_hypothesis_from_log_string(hypothesis_string)
        print(hypothesis.get_energy())
        print(len(hypothesis.grammar.get_transducer()))

    def test_save_hmm_image_from_string(self):
        s = """
        17-12-01 17:45:57 	 HMM:  states ['q1'], transitions {'q1': ['qf'], 'q0': ['q1']}, emissions {'q1': ['adorabl', 'aktif', 'arab', 'arbr', 'brylabl', 'byvabl', 'dyr', 'fiabl', 'fiksabl', 'final', 'finir', 'fumabl', 'fur', 'furyr', 'fylar', 'kadr', 'kafar', 'kalkyl', 'kapabl', 'karaf', 'katr', 'kudr', 'kupl', 'kyrabl', 'lavabl', 'luabl', 'mais', 'marl', 'martir', 'masif', 'mil', 'misil', 'mol', 'montr', 'mordr', 'mutar', 'nap', 'nyl', 'ordr', 'orl', 'parkur', 'parl', 'partir', 'pip', 'polar', 'posibl', 'postyr', 'potabl', 'prut', 'purir', 'pys', 'ridikyl', 'ryptyr', 'saly', 'sibl', 'sidr', 'sifl', 'sirkl', 'sortir', 'stad', 'stryktyr', 'supl', 'tabl', 'titr', 'trubl', 'vivabl', 'yrl', 'nobl']}
17-12-01 17:45:57 	 HMM:

        """
        name = 'french_deletion_new'
        hmm = get_hmm_from_hypothesis_string(s)
        self.write_to_dot_to_file(hmm, name)