from copy import deepcopy

from fst._fst import EPSILON

from grammar import Grammar
from hmm import HMM
from hypothesis import Hypothesis
from rule import Rule
from rule_set import RuleSet
from segment_table import SegmentTable, Feature
from tests.stable.test_hypothesis import TestHypothesisBase
from simulations import dag_zook_opacity, dag_zook_opacity_large, \
    french_two_rules, french_deletion_new, french_deletion_new_no_sab, \
    turkish_vowel_harmony_new_weights, tk_aspiration, finnish_two_rules, \
    dag_zook_noise, tag_soo_ilm_final_devoicing
from tests.test_util import get_hypothesis_from_log_string


class TestTransducerProblem(TestHypothesisBase):
    def test_original_problem(self):
        self.initialise_simulation(dag_zook_opacity_large)
        hmm_str = '''
q0: ['q1']
q1: ['q2', 'q3'], ['ag', 'agtod', 'daot', 'daota', 'dkaz', 'dkaza', 'dog', 'gdaas', 'gkas', 'gkasa', 'good', 'gooda', 'kaos', 'kaosa', 'kat', 'kata', 'koad', 'koada', 'ksoag', 'oktado', 'osko', 'ozka', 'saas', 'saasa', 'sak', 'skod', 'skoda', 'tok', 'toot', 'toota', 'tso', 'zook']
q2: ['qf'], ['gat', 'go', 'kts', 'ook']
q3: ['qf'], ['dot', 'gozka', 'oad', 'saat', 'tsk', 'zoka', 'ε']
q4: [], []
'''
        rules_str = '''
[{'low': '+'}] --> [] / [{'coronal': '+'}]__[{'coronal': '+'}] obligatory: False | ['a'] --> ε / [['z', 'd', 't', 's']]__[['z', 'd', 't', 's']] obligatory: False
[{'cons': '+'}] --> [{'voice': '-'}] / [{'voice': '-'}]__[] obligatory: True | ('z', 'g', 'd') --> ('s', 'k', 't') / [['t', 'k', 's']]__[] obligatory: True
[] --> [{'low': '+'}] / [{'coronal': '+'}]__[{'coronal': '+'}] obligatory: True | ε --> ['a'] / [['z', 'd', 't', 's']]__[['z', 'd', 't', 's']] obligatory: True
'''
        final_hypo = self.hypo_from_strings(hmm_str, rules_str)
        target_hypo = self.get_target_hypo()
        self.assert_less_no_infs(target_hypo.get_energy(), final_hypo.get_energy())

    def test_original_problem__mini(self):
        self.initialise_simulation(dag_zook_opacity_large)
        self.configurations.simulation_data = ['agktas', 'oktado']
        hmm_str = '''
q0: ['q1']
q1: ['qf'], ['agkts', 'oktado']
'''
        rules_str = '''
[{'low': '+'}] --> [] / [{'coronal': '+'}]__[{'coronal': '+'}] obligatory: False | ['a'] --> ε / [['z', 'd', 't', 's']]__[['z', 'd', 't', 's']] obligatory: False
[{'cons': '+'}] --> [{'voice': '-'}] / [{'voice': '-'}]__[] obligatory: True | ('z', 'g', 'd') --> ('s', 'k', 't') / [['t', 'k', 's']]__[] obligatory: True
[] --> [{'low': '+'}] / [{'coronal': '+'}]__[{'coronal': '+'}] obligatory: True | ε --> ['a'] / [['z', 'd', 't', 's']]__[['z', 'd', 't', 's']] obligatory: True
'''
        final_hypo = self.hypo_from_strings(hmm_str, rules_str)
        self.assertLess(final_hypo.get_energy(), float("inf"))

    def test_dag_zook_opacity(self):
        self.initialise_simulation(dag_zook_opacity)
        hmm_str = '''
q0: ['q3']
q3: ['q3', 'qf'], ['a', 'ado', 'agk', 'ao', 'asa', 'azk', 'd', 'dko', 'do', 'dog', 'gda', 'gka', 'k', 'kao', 'kat', 'kk', 'o', 'sk', 'ta']
'''
        rules_str = '''
transducer_generated:
[] --> [{'low': '-'}] / []__[] obligatory: False |
[] --> [{'low': '-'}] / []__[] obligatory: False |
not transducer_generated:
[{'cont': '+'}] --> [{'cont': '-'}] / [{'low': '+'}]__[{'low': '+'}] obligatory: True | 
'''
        target_hypo = self.get_target_hypo()
        final_hypo = self.hypo_from_strings(hmm_str, rules_str)
        self.assert_less_no_infs(target_hypo.get_energy(), final_hypo.get_energy())

    def test_dag_zook_opacity_b(self):
        self.initialise_simulation(dag_zook_opacity)
        hmm_str = '''
q0: ['q3']
q1: ['qf'], ['kazka', 'ε']
q2: ['qf'], ['asaat', 'atask', 'go', 'ko', 'task']
q3: ['q1', 'q2', 'q4'], ['daot', 'dkoz', 'dog', 'dok', 'gdaas', 'gkas', 'kaos', 'kat', 'kood', 'ksoag', 'ogtad', 'oktado', 'skaz', 'tak', 'taso']
q4: ['qf'], ['ada', 'asoka', 'ata', 'azoka', 'da', 'saat', 'soka', 'ta', 'zoka']
        '''
        final_hypo = self.hypo_from_strings(hmm_str, '')
        target_hypo = self.get_target_hypo()

        self.assert_less_no_infs(target_hypo.get_energy(),
                        final_hypo.get_energy())

    def test_dag_zook_opacity_large(self):
        self.initialise_simulation(dag_zook_opacity_large)
        hmm_str = '''
q0: ['q1']
q1: ['q1', 'qf'], ['gaka']
'''
        rules_str = '''
[] --> [{'low': '-'}] / []__[] obligatory: True | ε --> ['d', 'k', 'g', 't', 'z', 's', 'o'] / []__[] obligatory: True
[] --> [{'voice': '+'}] / []__[{'coronal': '+'}] obligatory: True | ε --> ['d', 'g', 'z', 'a', 'o'] / []__[['t', 'd', 'z', 's']] obligatory: True
[{'coronal': '-'}] --> [] / []__[{'coronal': '-'}] obligatory: True | ['k', 'a', 'g', 'o'] --> ε / []__[['k', 'a', 'g', 'o']] obligatory: True
[{'cont': '-', 'voice': '+'}] --> [] / []__[] obligatory: True | ['d', 'g'] --> ε / []__[] obligatory: True
'''
        final_hypo = self.hypo_from_strings(hmm_str, rules_str)
        target_hypo = self.get_target_hypo()

        self.assert_less_no_infs(target_hypo.get_energy(),
                        final_hypo.get_energy())

    def test_dag_zook_opacity_large2(self):
            self.initialise_simulation(dag_zook_opacity_large)
            hmm_str = '''
q0: ['q1']
q1: ['q2'], ['ag', 'agtod', 'daot', 'dkaz', 'dog', 'gdaas', 'gkas', 'good', 'kaos', 'kat', 'koad', 'ksoag', 'o', 'oktado', 'osko', 'ozka', 's', 'saas', 'sak', 'skod', 'tok', 'toot', 'tso', 'zook']
q2: ['qf'], ['d', 'dot', 'gat', 'go', 'gozka', 'ktas', 'oad', 'ook', 'saat', 'task', 'zoka', 'ε']
    '''
            rules_str = '''
[{'cons': '+'}] --> [{'voice': '-'}] / [{'voice': '-'}]__[] obligatory: True | ('d', 'g', 'z') --> ('t', 'k', 's') / [['t', 'k', 's']]__[] obligatory: True
[] --> [{'low': '+'}] / [{'coronal': '+'}]__[{'coronal': '+'}] obligatory: True | ε --> ['a'] / [['t', 'd', 'z', 's']]__[['t', 'd', 'z', 's']] obligatory: True
    '''
            final_hypo = self.hypo_from_strings(hmm_str, rules_str)
            target_hypo = self.get_target_hypo()

            # self.fail(final_hypo.get_energy() - target_hypo.get_energy())
            self.assert_less_no_infs(target_hypo.get_energy(),
                            final_hypo.get_energy())

    def test_french_two_rules_2(self):
        more_data = ['b' * i for i in range(1, 1)]
        more_datal = [f'{b}l' for b in more_data]
        # more_data = ['b' * i for i in range(1, 4)]
        # more_datal = [f'{d}l' for d in more_data] + ['k' * i for i in range(1, 2)]
        french_two_rules.data += more_data + more_datal
        french_two_rules.target_hmm['q1'][1].extend(more_datal)

        self.initialise_simulation(french_two_rules)
        hmm_final = f'''
        q0: ['q1']
q1: ['q2'], ['amur', 'arb', 'arbr', 'batir', 'tyrk', 'tyrke', 'byl', 'dart', 'dartr', 'film', 'filt', 'filtr', 'furyr', 'kapt', 'karaf', 'klad', 'klop', 'krab', 'kup', 'kupl', 'kurb', 'kuverk', 'kuverkl', 'kylt', 'mord', 'mordr', 'odor', 'parl', 'provok', 'prut', 'purp', 'purpr', 'romp', 'rompr', 'tab', 'tabl', 'yrl', 'bibl', 'ofr', 'vitr', 'bib', 'of', 'vit'] + {more_data} + {more_datal}
q2: ['qf'], ['abil', 'byf', 'byfl', 'byvab', 'byvabl', 'dub', 'dubl', 'fad', 'fut', 'futr', 'iv', 'ivr', 'kif', 'mal', 'puri', 'timid', 'formidabl', 'probabl', 'formidab', 'probab', 'ε']
        '''
        rule_str = '''[] --> [{'center': '+'}] / [{'cons': '+'}, {'back': '-'}]__[{'MB': True}, {'cons': '+'}] obligatory: False | ε --> ['e'] / [['r', 'm', 'f', 'b', 'p', 'v', 'd', 't', 'k', 'l'], ['r', 'm', 'y', 'f', 'b', 'p', 'v', 'd', 't', 'l', 'i']]__[['B'], ['r', 'm', 'f', 'b', 'p', 'v', 'd', 't', 'k', 'l']] obligatory: False'''
        final_hypo1 = self.hypo_from_strings(hmm_final, rule_str)

        better_hmm_str = f'''
        q0: ['q1']
q1: ['q2'], ['amur', 'arbr', 'batir', 'tyrk', 'tyrke', 'byl', 'dartr', 'film', 'filtr', 'furyr', 'kapt', 'karaf', 'klad', 'klop', 'krab', 'kupl', 'kurb', 'kuverkl', 'kylt', 'mordr', 'odor', 'parl', 'provok', 'prut', 'purpr', 'rompr', 'tabl', 'yrl', 'bibl', 'ofr', 'vitr'] + {more_data} + {more_datal}
q2: ['qf'], ['abil', 'byfl', 'byvabl', 'dubl', 'fad', 'futr', 'ivr', 'kif', 'mal', 'puri', 'timid', 'formidabl', 'probabl', 'ε']
'''
        better_rule_str = '''
[] --> [{'center': '+'}] / [{'cons': '+'}, {'back': '-'}]__[{'MB': True}, {'cons': '+'}] obligatory: False | ε --> ['e'] / [['r', 'm', 'f', 'b', 'p', 'v', 'd', 't', 'k', 'l'], ['r', 'm', 'y', 'f', 'b', 'p', 'v', 'd', 't', 'l', 'i']]__[['B'], ['r', 'm', 'f', 'b', 'p', 'v', 'd', 't', 'k', 'l']] obligatory: False
[{'liquid': '+'}] --> [] / [{'son': '-'}]__[] obligatory: False | ['r', 'l'] --> ε / [['s', 'b', 'f', 'p', 'd', 'v', 't', 'k']]__[] obligatory: False
        '''

        target_hypo = self.hypo_from_strings(better_hmm_str, better_rule_str)
        # self.assert_less_no_infs(target_hypo.get_energy(), final_hypo1.get_energy())

        real_target = self.get_target_hypo()
        self.assert_less_no_infs(real_target.get_energy(), final_hypo1.get_energy())

        hmm_no_del = '''
q0: ['q1']
q1: ['q2'], ['amur', 'arb', 'arbr', 'bib', 'batir', 'bibl', 'byl', 'dart', 'dartr', 'film', 'filt', 'filtr', 'furyr', 'kapt', 'karaf', 'klad', 'klop', 'krab', 'kup', 'kupl', 'kurb', 'kuverk', 'kuverkl', 'kylt', 'mord', 'mordr', 'odor', 'of', 'ofr', 'parl', 'provok', 'prut', 'purp', 'purpr','romp', 'rompr', 'tab', 'tabl', 'tyrk', 'vit', 'vitr', 'yrl']
q2: ['qf'], ['abil', 'byf', 'byfl', 'byvab', 'byvabl', 'dub', 'dubl', 'fad', 'formidab', 'formidabl', 'fut', 'futr', 'iv', 'ivr', 'kif', 'mal', 'probab', 'probabl', 'puri', 'timid', 'ε']
'''
        rules_no_del = '''
[] --> [{'center': '+'}] / [{'cons': '+'}, {'cons': '+'}]__[{'MB': True}, {'cons': '+'}] obligatory: False | ε --> ['e'] / [['r', 'm', 'f', 'b', 'p', 'v', 'd', 't', 'k', 'l'], ['r', 'm', 'y', 'f', 'b', 'p', 'v', 'd', 't', 'l', 'i']]__[['B'], ['r', 'm', 'f', 'b', 'p', 'v', 'd', 't', 'k', 'l']] obligatory: False
        '''

        no_del_hypo = self.hypo_from_strings(hmm_no_del, rules_no_del)
        self.assert_less_no_infs(real_target.get_energy(), no_del_hypo.get_energy())

    def test_french_deletion_new_things(self):
        self.initialise_simulation(french_deletion_new)
        h = self.get_target_hypo()
        h.get_energy()
        # self.fail(h.energy_signature)

        hmm_str = '''
q0: ['q1']
q1: ['qf'], ['adorab', 'adorabl', 'aktif', 'arab', 'arbr', 'brylab', 'brylabl', 'byvab', 'byvabl', 'dyr', 'fiab', 'fiabl', 'fiksab', 'fiksabl', 'final', 'finir', 'fumab', 'fumabl', 'fur', 'furyr', 'fylar', 'kadr', 'kafar', 'kalkyl', 'kapab', 'kapabl', 'karaf', 'katr', 'kudr', 'kup', 'kupl', 'kyrab', 'kyrabl', 'lavab', 'lavabl', 'luab', 'luabl', 'mais', 'mutar', 'nyl', 'ordr', 'orl', 'parkur', 'parl', 'partir', 'pip', 'polar', 'posib', 'posibl', 'postyr', 'potab', 'potabl', 'prut', 'purir', 'pys', 'ridikyl', 'ryptyr', 'saly', 'sib', 'sibl', 'sidr', 'sif', 'sifl', 'sirk', 'sirkl', 'sortir', 'stad', 'stryktyr', 'sup', 'supl', 'tab', 'tabl', 'titr', 'trub', 'trubl', 'vivab', 'vivabl', 'yrl']'''

        rule_str = '''
[{'lateral': '-', 'liquid': '+'}] --> [] / [{'cons': '+'}]__[] obligatory: False | ['r'] --> ε / [['l', 'r', 'n', 'm', 's', 'b', 'f', 'p', 'v', 'd', 't', 'k']]__[] obligatory: False
'''
        final_hypo = self.hypo_from_strings(hmm_str, rule_str)

        self.assertGreater(final_hypo.get_energy(),
                           self.get_target_hypo().get_energy())

    # def test_many_sable(self):
    #     self.initialise_simulation(french_deletion_new_many_sabl)
    #     # th = self.get_target_hypo()
    #     # th.get_energy()
    #     # self.fail(th.energy_signature)
    #     hmm = {
    #         'q0': ['q1'],
    #         'q1': (['qf'],
    #            ['adorabl', 'aktif', 'arab', 'arbr', 'brylabl', 'byvabl', 'dyr', 'stad', 'fiabl', 'fiksabl',
    #             'finir', 'fumabl', 'fur', 'furyr', 'fylar', 'kadr', 'kafar', 'kalkyl', 'kapabl', 'karaf', 'katr',
    #             'kudr', 'kupl', 'kyrabl', 'lavabl', 'luabl', 'mais', 'nyl', 'ordr', 'orl', 'final', 'parkur',
    #             'parl', 'partir', 'pip', 'polar', 'posibl', 'postyr', 'potabl', 'prut', 'purir', 'pys', 'ridikyl',      'ryptyr', 'saly', 'sibl', 'sidr', 'sifl', 'sirkl', 'sortir', 'stryktyr', 'supl', 'tabl', 'mutar',
    #             'titr', 'trubl', 'vivabl', 'yrl', 'sabml']),
    #           }
    #     rule_set = self.rule_set_from_rules([
    #         [[{"liquid": "+"}], [], [{"son": "-"}], [], False],
    #         [[{"cons": "+"}], [], [{"son": "-"}], [{"lateral": '+'}], True],
    #     ])
    #
    #     h = Hypothesis(Grammar(hmm, rule_set))
    #     h.get_energy()
    #     self.fail(h.energy_signature)

    def test_french_from_sabl(self):
        self.initialise_simulation(french_deletion_new)
        # this is a weird final hypothesis from french_deletion_new_many_sabl
        # simulation. I removed the 'sabl' from the HMM to test it vs. french_deletion_new.
        hmm_str = '''
q0: ['q1']
q1: ['qf'], ['adorabsl', 'aktif', 'arab', 'arbr', 'brylabtl', 'byvabsl', 'dyr', 'fiabsl', 'fiksabsl', 'final', 'finir', 'fumabsl', 'fur', 'furyr', 'fylar', 'kadr', 'kafar', 'kalkyl', 'kapabtl', 'karaf', 'katr', 'kudr', 'kupsl', 'kyrabsl', 'lavabsl', 'luabsl', 'mais', 'mutar', 'nyl', 'ordr', 'orl', 'parkur', 'parl', 'partir', 'pip', 'polar', 'posibsl', 'postyr', 'potabsl', 'prut', 'purir', 'pys', 'ridikyl', 'ryptyr', 'saly', 'sibsl', 'sidr', 'sif', 'sifl', 'sirkl', 'sortir', 'stad', 'stryktyr', 'supdl', 'tabtl', 'titr', 'trubsl', 'vivabtl', 'yrl']
'''
        rule_str = '''
[{'liquid': '+'}] --> [] / [{'labial': '-', 'son': '-'}]__[] obligatory: False | ['r', 'l'] --> ε / [['k', 'd', 's', 't']]__[] obligatory: False
[{'back': '-', 'high': '-', 'lateral': '-'}] --> [] / [{'cons': '+', 'labial': '+'}]__[] obligatory: False | ['r', 'n', 'm', 's', 'b', 'f', 'p', 'd', 'v', 't'] --> ε / [['m', 'b', 'f', 'p', 'v']]__[] obligatory: False
'''
        final = self.hypo_from_strings(hmm_str, rule_str)
        target = self.get_target_hypo()
        self.assert_less_no_infs(target.get_energy(),
                        final.get_energy())

    def test_french_deletion_no_sabl_from_many_sabl(self):
        # see previous test's comment. Here I left the `sabl` in the HMM.
        self.initialise_simulation(french_deletion_new_no_sab)
        hmm_str = '''
q0: ['q1']
q1: ['qf'], ['adorabsl', 'aktif', 'arab', 'arbr', 'brylabtl', 'byvabsl', 'dyr', 'fiabsl', 'fiksabsl', 'final', 'finir', 'fumabsl', 'fur', 'furyr', 'fylar', 'kadr', 'kafar', 'kalkyl', 'kapabtl', 'karaf', 'katr', 'kudr', 'kupsl', 'kyrabsl', 'lavabsl', 'luabsl', 'mais', 'mutar', 'nyl', 'ordr', 'orl', 'parkur', 'parl', 'partir', 'pip', 'polar', 'posibsl', 'postyr', 'potabsl', 'prut', 'purir', 'pys', 'ridikyl', 'ryptyr', 'saly', 'sibsl', 'sidr', 'sif', 'sifl', 'sirkl', 'sortir', 'stad', 'stryktyr', 'supdl', 'tabtl', 'titr', 'trubsl', 'vivabtl', 'yrl', 'sabl']
'''
        rule_str = '''
[{'liquid': '+'}] --> [] / [{'labial': '-', 'son': '-'}]__[] obligatory: False | ['r', 'l'] --> ε / [['k', 'd', 's', 't']]__[] obligatory: False
[{'back': '-', 'high': '-', 'lateral': '-'}] --> [] / [{'cons': '+', 'labial': '+'}]__[] obligatory: False | ['r', 'n', 'm', 's', 'b', 'f', 'p', 'd', 'v', 't'] --> ε / [['m', 'b', 'f', 'p', 'v']]__[] obligatory: False
'''
        final = self.hypo_from_strings(hmm_str, rule_str)
        target = self.get_target_hypo()
        self.assert_less_no_infs(target.get_energy(),
                        final.get_energy())

    # def test_english_devoicing(self):
    #     self.initialise_simulation(english_devoicing)
    #     hmm = deepcopy(self.simulation.target_hmm)
    #     hmm['q2'][1].append('s')
    #     h = Hypothesis(Grammar(hmm))
    #     h.get_energy()
    #     self.fail(h.energy_signature)
    #
#     def test_french_deletion_success(self):
#         self.initialise_simulation(french_two_rules)
#         hmm_str = '''
# q0: ['q1']
# q1: ['q2'], ['amur', 'arb', 'arbr', 'batir', 'burk', 'burke', 'byl', 'dart', 'dartr', 'film', 'filt', 'filtr', 'furyr', 'kapt', 'kapte', 'karaf', 'klad', 'klop', 'krab', 'kup', 'kupl', 'kurb', 'kurbe', 'kuverk', 'kuverkl', 'kylt', 'kylte', 'mord', 'mordr', 'odor', 'parl', 'provok', 'prut', 'purp', 'purpr', 'romp', 'rompr', 'tab', 'tabl', 'yrl']
# q2: ['qf'], ['abil', 'byf', 'byfl', 'byvab', 'byvabl', 'dub', 'dubl', 'fad', 'fut', 'futr', 'iv', 'ivr', 'kif', 'mal', 'puri', 'timid', 'ε']
# '''
#         rule_str = '''
# [] --> [{'center': '+'}] / [{'cons': '+'}, {'back': '-', 'son': '+'}, {'MB': True}]__[{'cons': '+'}] obligatory: False | ε --> ['e'] / [['t', 'k', 'l', 'r', 'm', 'f', 'b', 'v', 'p', 'd'], ['i', 'l', 'r', 'm', 'y'], ['B']]__[['t', 'k', 'l', 'r', 'm', 'f', 'b', 'v', 'p', 'd']] obligatory: False
# '''
#         hmm_str2 = '''
# q0: ['q1']
# q1: ['q2'], ['amur', 'arbr', 'batir', 'burk', 'burke', 'byl', 'dartr', 'film', 'filtr', 'furyr', 'kapt', 'kapte', 'karaf', 'klad', 'klop', 'krab', 'kupl', 'kurb', 'kurbe', 'kuverkl', 'kylt', 'kylte', 'mordr', 'odor', 'parl', 'provok', 'prut', 'purp', 'purpr', 'rompr', 'tabl', 'yrl']
# q2: ['qf'], ['abil', 'byfl', 'byvabl', 'dubl', 'fad', 'fut', 'futr', 'ivr', 'kif', 'mal', 'puri', 'timid', 'ε']
# '''
#
#         rule_str2 = '''
# [] --> [{'center': '+'}] / [{'cons': '+'}, {'back': '-', 'son': '+'}, {'MB': True}]__[{'cons': '+'}] obligatory: False | ε --> ['e'] / [['t', 'k', 'l', 'r', 'm', 'f', 'b', 'v', 'p', 'd'], ['i', 'l', 'r', 'm', 'y'], ['B']]__[['t', 'k', 'l', 'r', 'm', 'f', 'b', 'v', 'p', 'd']] obligatory: False
# [{"liquid": "+"}] -->  [] / [{"cons": "+", "son": "-"}]__[{"MB": True}] obligatory: False | ...
# '''
#
#         final = self.hypo_from_strings(hmm_str, rule_str)
#
#         final2 = self.hypo_from_strings(hmm_str2, rule_str2)
#
#
#         self.fail(f'FINAL : {final.get_energy()}\nFINAL2: {final2.get_energy()}')




#     def test(self):
#         self.initialise_simulation(dag_zook_opacity_large)
#         hmm_str = '''
#         q0: ['q1']
#         q1: ['q1', 'qf'], ['gaka']
#         '''
#         rules_str =  '''
# # [] --> [{'coronal': '-', 'cons': '+'}] / [{'coronal': '-', 'cons': '+'}]__[{'coronal': '-', 'cons': '+'}] obligatory: True | ε --> ['g', 'k'] / ['g', 'k']__['g', 'k'] obligatory: False
# [{'coronal': '+','voice': '-', 'cont': '-'}] --> [{'voice': '+'}] / []__[] obligatory: False |
#         '''
#         final_hypo = self.hypo_from_strings(hmm_str, rules_str)
#         final_hypo.get_energy()

    def devoice(self, words):
        for i, word in enumerate(words):
            # if random.randint(1, 5) != 5:
            #     continue  # chance of 5 to 1 of changing
            c = word[-1]
            segment = SegmentTable().get_segment_by_symbol(c)
            new_features = deepcopy(segment.features)
            new_features[Feature('voice', ('+', '-'))] = '-'
            new_c = SegmentTable().get_segment_symbol_by_features(new_features)
            if new_c:
                words[i] = word[:-1] + new_c

    def test_finnish_two_rules(self):
        self.initialise_simulation(finnish_two_rules)
        final_hmm = """
q0: ['q1']
q1: ['q2'], ['abs', 'essi', 'imes', 'imet', 'mea', 'mens', 'ment', 'pans', 'piis', 'piit', 'pitaa', 'sam', 'siad', 'sippa', 'sippi', 'tei', 'tiad']
q2: ['qf'], ['i', 'ias', 'impa', 'iss', 'issi', 'ist', 'isti', 'itten', 'mainen', 'n', 'ns', 'nsi', 'nt', 'nti', 'ssa', 'ε']
"""
        final_rules = '''
[] --> [{'coronal': '+', 'voice': '-'}] / [{'coronal': '-', 'voice': '-'}, {'coronal': '-'}, {'low': '+'}]__[] obligatory: True | ε --> ['t', 's'] / [['p'], ['b', 'm', 'a', 'e', 'i', 'p'], ['a']]__[] obligatory: True
'''
        self.assert_greater_than_target(final_hmm, final_rules, fail=False)

    def test_finnish_two_rules__(self):
        self.initialise_simulation(finnish_two_rules)
        final_hmm = """
q0: ['q1']
q1: ['q2'], ['abs', 'essi', 'imes', 'imet', 'mea', 'mens', 'ment', 'pans', 'piis', 'piit', 'pitaa', 'sam', 'siad', 'sippas', 'sippat', 'sippi', 'tei', 'tiad']
q2: ['qf'], ['i', 'ias', 'impa', 'iss', 'issi', 'ist', 'isti', 'itten', 'mainen', 'n', 'ns', 'nsi', 'nt', 'nti', 'ssa', 'ε']    """
        final_rules = ''
        self.assert_greater_than_target(final_hmm, final_rules, fail=False)

    def test_finnish_(self):
        self.initialise_simulation(finnish_two_rules)
        fhmm = """
q0: ['q1']
q1: ['q1', 'qf'], ['spi', 'stati']
"""
        frules = '''
[{'nasal': '-'}] --> [] / []__[] obligatory: True | ['b', 't', 's', 'd', 'a', 'e', 'i', 'p'] --> ε / []__[] obligatory: True
[] --> [{'high': '-'}] / [{'cons': '+'}]__[{'voice': '-'}] obligatory: True | ε --> ['b', 't', 's', 'd', 'm', 'n', 'a', 'e', 'p'] / [['b', 't', 's', 'd', 'm', 'n', 'p']]__[['t', 'p', 's']] obligatory: True
[{'nasal': '-'}] --> [] / []__[] obligatory: True | ['b', 't', 's', 'd', 'a', 'e', 'i', 'p'] --> ε / []__[] obligatory: True
'''
        self.assert_greater_than_target(fhmm, frules, fail=False)

    def test_tk_asp(self):
        self.initialise_simulation(tk_aspiration)
        final_hmm = '''
q0: ['q1']
q1: ['qf'], ['ikak', 'itik', 'katiit', 'kiki', 'kiktak', 'tatka', 'tattat', 'tikiit']        
'''
        rule_str = '''
[{'cons': '-'}] --> [{'high': '-'}] / [{'velar': '-'}]__[] obligatory: False | ('i',) --> ('a',) / [['h', 'i', 't', 'a']]__[] obligatory: False
[] --> [{'asp': '+'}] / [{'stop': '+'}]__[{'cons': '-'}] obligatory: True | ε --> ['h'] / [['t', 'k']]__[['i', 'a']] obligatory: True
        '''
        self.assert_greater_than_target(final_hmm, rule_str)

    def test_tk_asp_weird(self):
        self.initialise_simulation(tk_aspiration)
        final_hmm = '''
q0: ['q1']
q1: ['qf'], ['ithak', 'ithik', 'khathiit', 'khikhi', 'khikthak', 'thakhiit', 'thatthat', 'thikhiat']
'''
        rule_str = '''
[] --> [{'velar': '+'}] / []__[] obligatory: False | ε --> ['k'] / []__[] obligatory: False
[{'asp': '-'}] --> [] / [{'stop': '-'}]__[] obligatory: True | ['i', 't', 'a', 'k'] --> ε / [['i', 'a', 'h']]__[] obligatory: True
        '''
        self.assert_greater_than_target(final_hmm, rule_str)

    def test_turkish(self):
        self.initialise_simulation(turkish_vowel_harmony_new_weights)
        final_hmm = '''
q0: ['q3']
q1: ['qf'], ['e']
q2: ['q1', 'q3', 'qf'], ['ε']
q3: ['q2', 'q4', 'q5'], ['arp', 'aj', 'dal', 'ek', 'el', 'et', 'g0z', 'gyn', 'ip', 'j1l', 'josun', 'k0j', 'k0k', 'k1z', 'kedi', 'kent', 'kirpi', 'kurt', 'len', 'renk', 's1rt', 'sokak', 'son', 'tuz']
q4: ['qf'], ['in', 'ler', 'sel', 'ten']
q5: ['qf'], ['i', 'li', 'lik', 'siz']
'''
        final_rules = '''
[{'syll': '+'}] --> [{'back': '+'}] / [{'back': '+', 'cont': '+'}, {'kleene': True, 'syll': '-'}]__[] obligatory: True | ('i', 'y', '0', 'e') --> ('1', 'u', 'o', 'a') / [['a', 'o', 'u', '1'], ['z', 'a', 'j', 'l', 'i', 's', '1', 'r', 'n', 'k', 'g', 't', 'd', 'e']]__[] obligatory: True
        '''
        better_hmm = '''
q0: ['q1']
q1: ['q2'], ['arp', 'aj', 'dal', 'ek', 'el', 'et', 'g0z', 'gyn', 'ip', 'j1l', 'josun', 'k0j', 'k0k', 'k1z', 'kedi', 'kent', 'kirpi', 'kurt', 'renk', 's1rtlan', 'sokak', 'son', 'tuz']
q2: ['qf'], ['in', 'ler', 'sel', 'ten', 'i', 'li', 'lik', 'siz', 'ε', 'e']
'''

        final_hypo = self.hypo_from_strings(final_hmm, final_rules)
        better_hypo = self.hypo_from_strings(better_hmm, final_rules)
        better_hypo.get_energy()
        final_hypo.get_energy()

        self.assert_less_no_infs(better_hypo.energy, final_hypo.energy)

        self.assert_equal_no_infs(self.get_target_hypo().get_energy(), better_hypo.energy)

    def test_turkish_playground(self):
        self.initialise_simulation(turkish_vowel_harmony_new_weights)
        final_hmm = '''
q0: ['q3']
q1: ['qf'], ['e']
q2: ['q1', 'q3', 'qf'], ['ε']
q3: ['q2', 'q4', 'q5'], ['arp', 'aj', 'dal', 'ek', 'el', 'et', 'g0z', 'gyn', 'ip', 'j1l', 'josun', 'k0j', 'k0k', 'k1z', 'kedi', 'kent', 'kirpi', 'kurt', 'len', 'renk', 's1rt', 'sokak', 'son', 'tuz']
q4: ['qf'], ['in', 'ler', 'sel', 'ten']
q5: ['qf'], ['i', 'li', 'lik', 'siz']
'''
        final_rules = '''
[{'syll': '+'}] --> [{'back': '+'}] / [{'back': '+', 'cont': '+'}, {'kleene': True, 'syll': '-'}]__[] obligatory: True | 
        '''
        dfinal_hmm = '''
q0: ['q3']
q1: ['qf'], ['e']
q2: ['q1', 'q3', 'qf'], ['ε']
q3: ['q2', 'q4', 'q5'], ['arp', 'aj', 'dal', 'ek', 'el', 'et', 'g0z', 'gyn', 'ip', 'j1l', 'josun', 'k0j', 'k0k', 'k1z', 'kedi', 'kent', 'kirpi', 'kurt', 'renk', 's1rtlen', 'sokak', 'son', 'tuz']
q4: ['qf'], ['in', 'ler', 'sel', 'ten']
q5: ['qf'], ['i', 'li', 'lik', 'siz']
        '''

        final_hypo = self.hypo_from_strings(final_hmm, final_rules)
        dfinal_hypo = self.hypo_from_strings(dfinal_hmm, final_rules)

        self.assert_less_no_infs(
            dfinal_hypo.get_energy(),
            final_hypo.get_energy()
        )

    def devoicer(self, words):
        for i, word in enumerate(words):
            c = word[-1]
            segment = SegmentTable().get_segment_by_symbol(c)
            new_features = deepcopy(segment.features)
            new_features[Feature('voice', ('+', '-'))] = '-'
            new_c = SegmentTable().get_segment_symbol_by_features(new_features)
            if new_c:
                words[i] = word[:-1] + new_c

    def test_my_thigwsgs(self):
        self.initialise_simulation(tk_aspiration)
        hypo = self.get_target_hypo()

        rule_str = '\n'.join([str(rule) for rule in hypo.grammar.rule_set.rules])
        hypo2 = get_hypothesis_from_log_string(f'HMM: {hypo.grammar.hmm}\n{rule_str}')
        self.assert_equal_no_infs(hypo2.get_energy(), hypo.get_energy())

    def test_turkish_VH(self):
        self.initialise_simulation(turkish_vowel_harmony_new_weights)
        final_hmm = '''
q0: ['q1']
q1: ['q2', 'q4', 'q5'], ['aj', 'dal', 'ek', 'el', 'et', 'g0z', 'gyn', 'ip', 'j1l', 'josun', 'k0j', 'k0k', 'k1z', 'kedi', 'kent', 'kirpi', 'kurt', 'lan', 'renk', 's1rt', 'sokak', 'son', 'tuz']
q2: ['qf'], ['ler', 'li', 'lik', 'sel']
q3: ['qf'], ['e']
q4: ['qf'], ['i', 'in', 'siz', 'ten']
q5: ['q1', 'q3', 'qf'], ['ε']
'''
        final_rules = '''
[{'syll': '+'}] --> [{'back': '+'}] / [{'back': '+', 'syll': '+'}, {'high': '-', 'kleene': True}]__[] obligatory: True | ('y', '0', 'e', 'i') --> ('u', 'o', 'a', '1') / [['a', 'o', 'u', '1'], ['n', 'k', 'g', '0', 'l', 'o', 't', 'd', 'e', 'a', 'z', 'p', 's', 'r']]__[] obligatory: True
'''
        hfinal = self.hypo_from_strings(final_hmm, final_rules)

        # with new morphem `aj` and VH of `->+back`, `aj1` cannot be generated
        self.assertEqual(hfinal.get_energy(), float("inf"))

    def test_turkish_blah(self):
        self.initialise_simulation(turkish_vowel_harmony_new_weights)
        Q2s = ['in', 'ler', 'siz', 'i', 'ten', 'sel', 'lik',
                              'li', 'e', EPSILON]
        hmm_dict = {'q0': ['q1'],
              'q1': (['q2'], ['el', 'j1l', 'ek', 'ip', 'renk', 'son', 'et',
                              'josun', 'kedi', 'kent', 'k0j', 'k0k', 'sokak',
                              'tuz', 'dal', 'gyn', 'kirpi', 'k1z', 's1rtlan',
                              'g0z', 'kurt', 'aj', 'arp']),
              'q2': (['qf'], Q2s),
              }
        some_hmm = HMM(deepcopy(hmm_dict))
        some_rules = RuleSet([Rule([{"syll": "+"}], [{"back": "+"}], [{"cont": "+", "back": "+"}, {"syll": "-", "kleene": True}], [], True)])

        some_hypo = Hypothesis(Grammar(some_hmm, some_rules))

        #
        self.assert_equal_no_infs(self.get_target_hypo().get_energy(),
                                  some_hypo.get_energy())

    def test_noise(self):
        self.initialise_simulation(dag_zook_opacity)
        self.configurations.simulation_data = ['dag', 'zook']
        self.configurations['NOISE_RULE_SET'] = []
        hmm_str = "q0: ['q1']\nq1: ['qf'], ['dag', 'zoog']"
        hypo = self.hypo_from_strings(hmm_str, "")
        self.assertEqual(hypo.get_energy(), float('inf'))

        self.configurations['NOISE_RULE_SET'] = [[[{"cons": "+"}], [{"voice": "-"}], [], [], True]]
        self.configurations['NOISE_WEIGHT'] = 100
        hypo2 = self.hypo_from_strings(hmm_str, "")
        self.assertLess(hypo2.get_energy(), float('inf'))

    def test_turkish__only_syll_is_the_correct_context(self):
        self.initialise_simulation(turkish_vowel_harmony_new_weights)

        # +syll --> +back
        hmm_dict = {'q0': ['q1'],
              'q1': (['q2'], ['el', 'j1l', 'ek', 'ip', 'renk', 'son', 'et',
                              'josun', 'kedi', 'kent', 'k0j', 'k0k', 'sokak',
                              'tuz', 'dal', 'gyn', 'kirpi', 'k1z', 's1rtlan',
                              'g0z', 'kurt', 'aj', 'arp']),
              'q2': (['qf'], ['in', 'ler', 'siz', 'i', 'ten', 'sel', 'lik', 'li', 'e', EPSILON]),
              }
        rule_change = ([{"syll": "+"}], [{"back": "+"}])


        # +syll --> -back
        hmm_dict2 = {'q0': ['q1'],
                    'q1': (
                    ['q2'], ['el', 'j1l', 'ek', 'ip', 'renk', 'son', 'et',
                             'josun', 'kedi', 'kent', 'k0j', 'k0k', 'sokak',
                             'tuz', 'dal', 'gyn', 'kirpi', 'k1z', 's1rtlan',
                             'g0z', 'kurt', 'aj', 'arp']),
                    'q2': (['qf'], ['1n', 'lar', 's1z', '1', 'tan', 'sal', 'l1k', 'l1', 'a', EPSILON]),
                    }
        rule_change2 = ([{"syll": "+"}], [{"back": "-"}])

        target_energy = self.get_target_hypo().get_energy()
        unexpexted_context = []
        for feat in 'syll,back,round,high,voice,cont,lateral,son'.split(','):
            for val in ['+', '-']:
                if (feat, val) == ('syll', '-'):
                    continue
                for r, change in enumerate([rule_change, rule_change2], start=1):
                    for h, hmm in enumerate([hmm_dict, hmm_dict2], start=1):
                        some_hmm = HMM(deepcopy(hmm))
                        rule = change + ([{"syll": "+", "back": change[1][0]['back']}, {feat: val, "kleene": True}], [], True)
                        some_rules = RuleSet([Rule(*rule)])
                        some_hypo = Hypothesis(Grammar(some_hmm, some_rules))
                        if some_hypo.get_energy() <= target_energy:
                            unexpexted_context.append({f"hmm{h} rule {r}": {feat: val}})

        assert unexpexted_context == [], f"Unexpected kleene context for rule: {unexpexted_context}"

    def test_dag_zook_hmm(self):
        self.initialise_simulation(dag_zook_noise)
        self.assert_greater_than_target(
            final_hmm_str='''
q0: ['q1']
q1: ['q2', 'q3', 'qf'], ['dag', 'kad', 'dod', 'kod', 'gas', 'toz', 'ata', 'aso', 'daod', 'sog', 'saog', 'tad', 'taz', 'kaod', 'kaz', 'kak']
q2: ['qf'], ['gos']
q3: ['qf'], ['dos', 'zook']
            ''',
            final_rule_str="[{'cons': '+'}] --> [{'voice': '-'}] / []__[{'WB': True}] obligatory: True | blah",
        )

