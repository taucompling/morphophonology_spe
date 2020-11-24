from copy import deepcopy
from math import ceil

from hypothesis import Hypothesis
from hmm import HMM, INITIAL_STATE, FINAL_STATE
from grammar import Grammar
from tests.my_test_case import MyTestCase
from rule import Rule
from rule_set import RuleSet
from util import log_hypothesis
from fst import EPSILON


class TestHypothesisBase(MyTestCase):

    def get_target_hypo(self):
        target_hmm = deepcopy(self.simulation.target_hmm)
        target_rule_set = RuleSet.load_from_flat_list(self.simulation.target_tuple[1])
        return Hypothesis(Grammar(target_hmm, target_rule_set))

    def hypo_from_strings(self, hmm_str, rules_str):
        final_hmm = self.parse_hmm(hmm_str)
        final_rule_set = self.parse_rules(rules_str)
        return Hypothesis(Grammar(final_hmm, final_rule_set))

    def parse_hmm(self, hmm_str):
        hmm = {}
        for line in hmm_str.split('\n'):
            striped = line.strip()
            if not striped:
                continue
            key, value = striped.split(': ')
            trans_emis = eval(value)
            if not isinstance(trans_emis[0], list):
                pass
            else:
                trans_emis = tuple(trans_emis)
            hmm[key] = trans_emis
        return hmm

    def parse_rules(self, rules_str):
        """Parse Hypos"""
        rules = []
        for line in rules_str.split('\n'):
            if not line.startswith('['):
                continue
            r = line[:line.find('|')]
            arrow = r.find('-->')
            slash = r.find('/')
            context = r.find('__')
            obligatoric = r.find('obligatory')
            noisec = r.find('noise')

            target = eval(r[:arrow])
            change = eval(r[arrow + 3: slash])
            left_context = eval(r[slash + 1: context])
            right_context = eval(r[context + 2: obligatoric])
            obligatory = eval(r[obligatoric + len('obligatory:'):noisec])

            rules.append([target, change, left_context, right_context, obligatory])
        return self.rule_set_from_rules(rules)

    def assert_less_no_infs(self, a, b, msg=None):
        self.assertLess(a, float('inf'), msg="Unexpected inf (first arg)")
        self.assertLess(b, float('inf'), msg="Unexpected inf (second arg)")
        self.assertLess(a, b, msg)

    def assert_equal_no_infs(self, first, second, msg=None):
        self.assertLess(first, float('inf'), msg="Unexpected inf (first arg)")
        self.assertLess(second, float('inf'), msg="Unexpected inf (second arg)")
        self.assertEqual(first, second, msg)

    def assert_greater_than_target(self, final_hmm_str, final_rule_str, fail=False):
        final_hypo = self.hypo_from_strings(final_hmm_str, final_rule_str)
        target_hypo = self.get_target_hypo()
        if fail:
            target_hypo.get_energy()
            final_hypo.get_energy()
            self.fail(
                f'\n'
                f'TARGET: {target_hypo.energy_signature}\n'
                f'FINAL : {final_hypo.energy_signature}\n'
                f'DIFF: {target_hypo.energy - final_hypo.energy}\n'
                f'WHICH IS {100 * abs(target_hypo.energy - final_hypo.energy) / final_hypo.energy:.2f}% OF FINAL'
            )

        target_energy = target_hypo.get_energy()
        final_energy = final_hypo.get_energy()

        self.assert_less_no_infs(target_energy, final_energy)

    def rule_set_from_rules(self, rules):
        return RuleSet([Rule(*r) for r in rules])



class TestHypothesis(MyTestCase):
    def setUp(self):
        super(TestHypothesis, self).setUp()
        self.configurations["DATA_ENCODING_LENGTH_MULTIPLIER"] = 1
        self.configurations["HMM_ENCODING_LENGTH_MULTIPLIER"] = 1
        self.configurations["RULES_SET_ENCODING_LENGTH_MULTIPLIER"] = 1

    def test_hypothesis_unique_representation(self):
        from simulations import french_two_rules as simulation
        self.initialise_simulation(simulation)

        hmm_1 = HMM({'q0': ['q1'],
                     'q1': (['q2'],
                            ['klop', 'kylt', 'provok']),
                     'q2': (['qf'], ['kif', 'timid', 'fad', 'mal', 'byvabl', EPSILON])
                     })

        rule_1 = Rule.load([[], [{"center": "+"}], [{"cons": "+", "son": "+"}, {"son": "+", "cons": "+"}], [{"MB": True}, {"cons": "+"}], False])
        rule_set_1 = RuleSet([rule_1])

        grammar_1 = Grammar(hmm_1, rule_set_1)
        hypothesis_1 = Hypothesis(grammar_1)

        repr_1 = repr(hypothesis_1)

        hmm_2 = HMM({'q0': ['q1'],
                     'q2': (['qf'], ['kif', 'timid', 'mal', 'fad', 'byvabl', EPSILON]),
                     'q1': (['q2'],
                            ['provok', 'kylt', 'klop'])
                     })

        rule_2 = Rule.load([[], [{"center": "+"}], [{"son": "+", "cons": "+"}, {"cons": "+", "son": "+"}], [{"MB": True}, {"cons": "+"}], False])
        rule_set_2 = RuleSet([rule_2])

        grammar_2 = Grammar(hmm_2, rule_set_2)
        hypothesis_2 = Hypothesis(grammar_2)

        repr_2 = repr(hypothesis_2)

        print(repr_1)
        print(repr_2)

        assert repr_1 == repr_2

    def test_plural_english_hypothesis(self):
        self.initialise_segment_table("plural_english_segment_table.txt")
        self.rule_set = self.get_rule_set("plural_english_rule_set.json")
        plural_english_data = 1 * ['kats', 'dogz', 'kat', 'dog']
        hmm = HMM({INITIAL_STATE: ['q1'],
                 'q1': (['q2', FINAL_STATE], ['dog', 'kat']),
                 'q2': ([FINAL_STATE], ['z'])})

        grammar = Grammar(hmm, self.rule_set)
        self.write_to_dot_file(self.rule_set.rules[0].get_transducer(), "plural_english_rule")
        self.write_to_dot_file(grammar.get_nfa(), "grammar_nfa")
        self.configurations.simulation_data = plural_english_data
        hypothesis = Hypothesis(grammar)
        self.assertEqual(int(hypothesis.get_energy()), 117)

    def test_crossover(self):
        from simulations import dag_zook_opacity as simulation
        self.initialise_simulation(simulation)
        from copy import deepcopy


        rule_1 = Rule.load([[{'cont': '+'}], [{'coronal': '-'}], [{'coronal': '-'}], [], True])
        rule_2 = Rule.load([[{'cons': '+', 'low': '-'}], [{'voice': '-'}], [{'voice': '-'}], [], True])

        crossover_rule_1 = deepcopy(rule_1)
        crossover_rule_2 = deepcopy(rule_2)
        crossover_rule_1.left_context_feature_bundle_list = rule_2.left_context_feature_bundle_list
        crossover_rule_1.right_context_feature_bundle_list = rule_2.right_context_feature_bundle_list
        crossover_rule_1.change_feature_bundle_list = rule_2.change_feature_bundle_list

        crossover_rule_2.left_context_feature_bundle_list = rule_1.left_context_feature_bundle_list
        crossover_rule_2.right_context_feature_bundle_list = rule_1.right_context_feature_bundle_list
        crossover_rule_2.change_feature_bundle_list = rule_1.change_feature_bundle_list

        rule_set_1 = RuleSet([crossover_rule_1])
        rule_set_2 = RuleSet([crossover_rule_2])
        print(rule_set_1)
        print(rule_set_2)

        hmm = HMM({'q0': ['q1'],
              'q1': (['q2', 'qf'], ['dag', 'kat', 'dot', 'kod']),
              'q2': (['qf'], ['zo', 'go', 'do'])
               })
        grammar_1 = Grammar(hmm, rule_set_1)
        grammar_2 = Grammar(hmm, rule_set_2)

        data = ['kat', 'dot',     'dag', 'kod'] + \
               ['katso', 'dotso', 'dagzo', 'kodzo'] + \
               ['katko', 'dotko', 'daggo', 'kodgo'] + \
               ['katto', 'dotto', 'dagdo', 'koddo']

        self.configurations.simulation_data = data
        hypothesis_1 = Hypothesis(grammar_1)
        hypothesis_2 = Hypothesis(grammar_2)

        print(hypothesis_1.get_energy())
        print(hypothesis_2.get_energy())

    def test_get_random_hypothesis(self):
        self.configurations["EVOLVE_HMM"] = True
        self.configurations["EVOLVE_RULES"] = True
        self.initialise_segment_table("plural_english_segment_table.txt")
        data = ['kats', 'dogz', 'kat', 'dog']
        rand_hypothesis = Hypothesis.get_random_hypothesis(data)
        log_hypothesis(rand_hypothesis)

    def test_assimilation2(self):
        self.initialise_segment_table("plural_english_segment_table.txt")
        self.rule_set = self.get_rule_set("plural_english_rule_set.json")
        data = ['kat', 'dot',     'dag', 'kod'] + \
               ['katso', 'dotso', 'dagzo', 'kodzo'] + \
               ['katko', 'dotko', 'daggo', 'kodgo'] + \
               ['katto', 'dotto', 'dagdo', 'koddo']

        hmm = HMM({'q0': ['q1'],
              'q1': (['q2', 'qf'], ['dag', 'kat', 'dot', 'kod']),
              'q2': (['qf'], ['zo', 'go', 'do'])
               })

        grammar = Grammar(hmm, self.rule_set)
        self.configurations.simulation_data = data
        hypothesis = Hypothesis(grammar)
        for _ in range(10):  #1.4
            energy = hypothesis.get_energy()
        #self.assertEqual(energy, 269)

    def test_opacity_two_hypotheses(self):
        from simulations import dag_zook_opacity as simulation
        self.initialise_simulation(simulation)
        hmm = HMM({'q0': ['q1'],
              'q1': (['q2', 'q3'], ['daot', 'dkoz', 'dog', 'dok', 'gdaas', 'gkas', 'kaos', 'kat', 'kood', 'ksoag', 'ogtd', 'oktdo', 'skaz', 'tak', 'tso']),
              'q2': (['qf'], ['go', 'kazka', 'soka', 'ta', EPSILON]),
              'q3': (['qf'], ['da', 'saat', 'tsk', 'zoka'])
               })

        epenthesis_rule = Rule([], [{'low': '+'}], [{'coronal': '+'}], [{'coronal': '+'}], True)
        assimilation_rule = Rule([{'cons': '+'}], [{'voice': '-'}], [{'voice': '-'}], [], True)

        rule_set = RuleSet([assimilation_rule, epenthesis_rule])
        grammar = Grammar(hmm, rule_set)
        hypothesis = Hypothesis(grammar)
        print(hypothesis.get_energy())


    def test_assimilation_no_rule(self):
        self.initialise_segment_table("plural_english_segment_table.txt")
        data = ['kat', 'dot',     'dag', 'kod'] + \
               ['katso', 'dotso', 'dagzo', 'kodzo'] + \
               ['katko', 'dotko', 'daggo', 'kodgo'] + \
               ['katto', 'dotto', 'dagdo', 'koddo']

        hmm = HMM({'q0': ['q1'],
              'q1': (['q2', 'qf'], ['dag', 'kat', 'dot', 'kod']),
              'q2': (['qf'], ['zo', 'go', 'do', 'to', 'so', 'ko'])
               })

        grammar = Grammar(hmm, [])

        hypothesis = Hypothesis(grammar)
        self.configurations.simulation_data = data
        self.assertEqual(int(hypothesis.get_energy()), 230)

    def test_katso_two_rule(self):
        #configurations["DATA_ENCODING_LENGTH_MULTIPLIER"] = 25
        self.initialise_segment_table("plural_english_segment_table.txt")
        data = ['kat', 'dot',     'dag', 'kod',     'gas', 'toz'] + \
               ['katso', 'dotso', 'dagzo', 'kodzo', 'gasazo', 'tozazo'] + \
               ['katko', 'dotko', 'daggo', 'kodgo', 'gasko', 'tozgo'] + \
               ['katto', 'dotto', 'dagdo', 'koddo', 'gasto', 'tozdo']

        hmm = {'q0': ['q1'],
              'q1': (['q2', 'qf'], ['dag', 'kat', 'dot', 'kod', 'gas', 'toz']),
              'q2': (['qf'], ['zo', 'go', 'do'])}

        epenthesis_rule = Rule.load([[], [{"cons": "-", "low": "+"}], [{"cons": "+", "cont": "+"}], [{"cons": "+", "cont": "+"}], True])
        assimilation_rule = Rule.load([[{"cons": "+"}], [{"voice": "-"}], [{"voice": "-"}], [], True])
        rule_set = RuleSet([epenthesis_rule, assimilation_rule])
        hmm = HMM(hmm)
        grammar = Grammar(hmm, rule_set)
        self.write_to_dot_file(grammar.get_nfa(), "grammar_nfa")
        self.configurations.simulation_data = data
        hypothesis = Hypothesis(grammar)
        self.assertEqual(int(hypothesis.get_energy()), 364)

    def test_abadnese(self):
        self.initialise_segment_table("abd_segment_table.txt")
        data = ['bbabbba', 'baabbba', 'babbbba', 'bbabadba', 'baabadba', 'babbadba', 'bbabbad', 'baabbad',
        'babbbad', 'bbabadad', 'baabadad', 'babbadad', 'bbabbab', 'baabbab', 'babbbab', 'bbabadab',
        'baabadab', 'babbadab']

        hmm = HMM({'q0': ['q1'],
              'q1': (['q2'], ['bbab', 'baab', 'babb', 'bbaba', 'baaba', 'babba']),
              'q2': (['qf'], ['dba', 'dad', 'dab'])})
        rule = Rule.load([[{"cons": "+"}], [{"labial": "+"}], [{"labial": "+"}], [], True])
        rule_set = RuleSet([rule])

        grammar = Grammar(hmm, rule_set)
        self.configurations.simulation_data = data
        hypothesis = Hypothesis(grammar)
        hypothesis.get_energy()
        self.assertEqual(ceil(hypothesis.get_energy()), 231)

    def test_abadnese_no_rule(self):
        self.initialise_segment_table("abd_segment_table.txt")
        data = ['bbabbba', 'baabbba', 'babbbba', 'bbabadba', 'baabadba', 'babbadba', 'bbabbad', 'baabbad',
        'babbbad', 'bbabadad', 'baabadad', 'babbadad', 'bbabbab', 'baabbab', 'babbbab', 'bbabadab',
        'baabadab', 'babbadab']

        hmm = HMM({'q0': ['q1'],
              'q1': (['q2'], ['bbab', 'baab', 'babb', 'bbaba', 'baaba', 'babba']),
              'q2': (['qf'], ['dba', 'dad', 'dab', 'bba', 'bad', 'bab'])})

        grammar = Grammar(hmm, [])
        self.configurations.simulation_data = data
        hypothesis = Hypothesis(grammar)
        self.assertEqual(int(hypothesis.get_energy()), 243)

    def test_morphology_only(self):
        self.initialise_segment_table("plural_english_segment_table.txt")
        data = [u'tozat', u'tozgoat', u'tozgo', u'tozdoat', u'tozdo', u'tozzoat', u'tozzo', u'toz', u'dagat', u'daggoat', u'daggo', u'dagdoat', u'dagdo', u'dagzoat', u'dagzo', u'dag', u'gasat', u'gasgoat', u'gasgo', u'gasdoat', u'gasdo', u'gaszoat', u'gaszo', u'gas', u'kodat', u'kodgoat', u'kodgo', u'koddoat', u'koddo', u'kodzoat', u'kodzo', u'kod', u'katat', u'katgoat', u'katgo', u'katdoat', u'katdo', u'katzoat', u'katzo', u'kat', u'dotat', u'dotgoat', u'dotgo', u'dotdoat', u'dotdo', u'dotzoat', u'dotzo', u'dot']

        #target
        hmm = {'q0': ['q1'],
              'q1': (['q2', 'q3', 'qf'], ['dag', 'kat', 'dot', 'kod', 'gas', 'toz']),
              'q2': (['q3','qf'], ['zo', 'go', 'do']),
              'q3': (['qf'], ['at'])}
        self.configurations.simulation_data = data
        self.assertLess(Hypothesis(Grammar(hmm, [])).get_energy(), 5190)

        #single_sate
        hmm = HMM({'q0': ['q1'],
              'q1': (['q1', 'qf'], ['dag', 'kat', 'dot', 'kod', 'gas', 'toz'] + ['zo', 'go', 'do'] + ['at'])
                })
        self.assertLess(Hypothesis(Grammar(hmm, [])).get_energy(), 6430)


        #two state
        hmm = {'q0': ['q1'],
              'q1': (['q1', 'q2', 'qf'], ['dag', 'kat', 'dot', 'kod', 'gas', 'toz'] + ['zo', 'go', 'do']),
              'q2': (['qf'], ['at'])
                }
        self.assertLess(Hypothesis(Grammar(hmm, [])).get_energy(), 6010)

        #from simualation
        hmm = HMM({'q0': ['q1'],
      'q1': (['q1', 'qf'], ['toz', 'do', 'zo', 'gas', 'kod', 'dag', 'at', 'zoat', 'kat', 'go', 'dot'])
        })


    def test_morphology_only2(self):
        self.initialise_segment_table("plural_english_segment_table.txt")
        self.configurations["DATA_ENCODING_LENGTH_MULTIPLIER"] = 25
        data = [u'tozata', u'tozaso', u'tozakt', u'tozzookata', u'tozzookaso', u'tozzookakt', u'tozzook', u'tozdodata', u'tozdodaso', u'tozdodakt', u'tozdod', u'tozgosata', u'tozgosaso', u'tozgosakt', u'tozgos', u'toz', u'dagata', u'dagaso', u'dagakt', u'dagzookata', u'dagzookaso', u'dagzookakt', u'dagzook', u'dagdodata', u'dagdodaso', u'dagdodakt', u'dagdod', u'daggosata', u'daggosaso', u'daggosakt', u'daggos', u'dag', u'gasata', u'gasaso', u'gasakt', u'gaszookata', u'gaszookaso', u'gaszookakt', u'gaszook', u'gasdodata', u'gasdodaso', u'gasdodakt', u'gasdod', u'gasgosata', u'gasgosaso', u'gasgosakt', u'gasgos', u'gas', u'kodata', u'kodaso', u'kodakt', u'kodzookata', u'kodzookaso', u'kodzookakt', u'kodzook', u'koddodata', u'koddodaso', u'koddodakt', u'koddod', u'kodgosata', u'kodgosaso', u'kodgosakt', u'kodgos', u'kod', u'katata', u'kataso', u'katakt', u'katzookata', u'katzookaso', u'katzookakt', u'katzook', u'katdodata', u'katdodaso', u'katdodakt', u'katdod', u'katgosata', u'katgosaso', u'katgosakt', u'katgos', u'kat', u'dotata', u'dotaso', u'dotakt', u'dotzookata', u'dotzookaso', u'dotzookakt', u'dotzook', u'dotdodata', u'dotdodaso', u'dotdodakt', u'dotdod', u'dotgosata', u'dotgosaso', u'dotgosakt', u'dotgos', u'dot']
        hmm = HMM({'q0': [u'q1'],
        'q1': ([u'q2', u'q3', u'qf'], ['toz', 'dag', 'kat', 'dot', 'kod', 'gas']),
        'q2': ([u'q3',u'qf'], ['zook', 'gos', 'dod']),
        'q3': ([u'qf'], ['aso', 'akt', 'ata'])})

        self.configurations.simulation_data = data
        hypothesis = Hypothesis(Grammar(hmm, []))
        # no assertion ?

    def test_abnese(self):
        self.initialise_segment_table("ab_segment_table.txt")
        self.configurations["BRACKET_TRANSDUCER"] = True
        data = ['bab', 'aabab']

        hmm = HMM( {'q0': ['q1'],
              'q1': (['qf'], ['bb', 'aabb'])
              })
        rule = Rule([], [{"cons": "-"}], [{"cons": "+"}], [{"cons": "+"}], False)  # e->a / b_b
        rule_set = RuleSet([rule])

        print(rule_set.get_outputs_of_word("bb"))

        grammar = Grammar(hmm, rule_set)
        self.write_to_dot_file(grammar.get_nfa(), "grammar_nfa")
        self.configurations.simulation_data = data
        hypothesis = Hypothesis(grammar)

        print(hypothesis.get_energy())
        print(hypothesis.get_recent_energy_signature())
