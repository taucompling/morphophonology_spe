from tests.my_test_case import MyTestCase
from rule import Rule
from rule_set import RuleSet

from configuration import Configuration

configurations = Configuration()

plus = "+"
minus = "-"
cons = "cons"
low = "low"
voice = "voice"
cont = "cont"
velar = "velar"

d = {cons: plus, voice: plus, velar: minus}
t = {cons: plus, voice: minus, velar: minus}
a = {cons: minus, low: plus}
g = {"cons": "+", "voice": "+", "velar": "+"}


class TesAllRuleTypes(MyTestCase):
    def setUp(self):
        self.initialise_segment_table("plural_english_segment_table.txt")

    def test_insertion_both_contexts(self):
        rule = Rule([], [{"cons": "-", "low": "+"}], [{"cons": "+"}], [{"cons": "+"}], True)
        self.assertEqual(print_rule_word_outputs(rule, 'ttt'), [u'tatat'])

        rule = Rule([], [a], [{cons: "+", voice: "+"}], [{cons: "+"}], True)
        self.assertEqual(print_rule_word_outputs(rule, 'ddodd'), [u'dadodad'])

        rule = Rule([], [{"cons": "+", "voice": "+"}], [{"cons": "+", "voice": "-"}], [{"cons": "+", "voice": "-"}], False)
        self.assertEqual(set(print_rule_word_outputs(rule, 'tt')), set([u'tt', u'tdt', u'tzt', u'tgt']))

        rule = Rule([], [{"cons": "+", "voice": "-"}], [{"cons": "+", "voice": "-"}], [{"cons": "+", "voice": "-"}], True)
        self.assertEqual(set(print_rule_word_outputs(rule, 'tt')), set([u'ttt', u'tkt', u'tst']))

    def test_insertion_left_context_only(self):
        rule = Rule([], [{"cons": "-", "low": "+"}], [{"cons": "+"}], [], False)
        self.assertEqual(set(print_rule_word_outputs(rule, 'gg')),set( [u'gg', u'gga', u'gag', u'gaga']))
        rule = Rule([], [{"cons": "-", "low": "+"}], [g], [], True)
        self.assertEqual(print_rule_word_outputs(rule,'g'), [u'ga'])
        rule = Rule([], [{"cons": "-", "low": "+"}], [{"cons": "-", "low": "+"}], [], False)
        self.assertEqual(set(print_rule_word_outputs(rule,'aa')), set([u'aa', u'aaa', u'aaa', u'aaaa']))
        rule = Rule([], [g], [g], [], True)
        self.assertEqual(print_rule_word_outputs(rule,'g'), [u'gg'])

    def test_insertion_with_right_context_only(self):
        rule = Rule([], [{"cons": "-", "low": "+"}], [], [{"cons": "+"}], False)
        self.assertEqual(set(print_rule_word_outputs(rule,'t')), set([u't', u'at']))
        rule = Rule([], [{"cons": "-", "low": "+"}], [], [{"cons": "+"}], True)
        self.assertEqual(print_rule_word_outputs(rule,'t'), [u'at'])
        rule = Rule([], [{"cons": "+", "voice": "+"}], [], [{"cons": "+"}], True)
        self.assertEqual(set(print_rule_word_outputs(rule,'t')), set([u'dt', u'gt', u'zt']))
        rule = Rule([], [g], [], [{"cons": "+", "voice": "+"}], False)
        self.assertEqual(set(print_rule_word_outputs(rule,'dd')), set([u'dd', u'dgd', u'gdd', u'gdgd']))

    def test_insertion_no_context(self):
        rule = Rule([], [g], [], [], False)
        self.assertEqual(set(print_rule_word_outputs(rule, 'd')), set([u'd', u'dg', u'gd', u'gdg']))

    def test_deletion_both_contexts(self):
        rule = Rule([{"velar": "+"}], [], [{"velar": "+"}], [{"velar": "+"}], True)
        self.assertEqual(print_rule_word_outputs(rule, "ggg"), ['gg'])
        rule = Rule([{"cons": "-"}], [], [d], [t], True)
        self.assertEqual(print_rule_word_outputs(rule,'dat'), [u'dt'])

    def test_deletion_left_context_only(self):
        rule = Rule([{"velar": "+"}], [], [{"velar": "+"}], [], True)
        self.assertEqual(print_rule_word_outputs(rule, "gg"), ['g'])

        rule = Rule([{"cons": "+"}], [], [{"cons": "+"}], [], True)
        self.assertEqual(print_rule_word_outputs(rule, "gg"), ['g'])

        rule = Rule([{"cons": "-"}], [], [{"cons": "+"}], [], True)
        self.assertEqual(print_rule_word_outputs(rule, 'da'), [u'd'])  #fail  "[u'd', u'd']"   - solved

    def test_deletion_right_context_only(self):
        rule = Rule([{"velar": "+"}], [], [{"velar": "+"}], [], True)
        self.assertEqual(print_rule_word_outputs(rule, "gg"), ['g'])

        rule = Rule([{"cons": "-"}], [], [], [{"cons": "+"}], True)
        self.assertEqual(print_rule_word_outputs(rule, 'aad'), [u'ad'])

    def test_deletion_no_context(self):
        rule = Rule([{"cons": "-"}], [], [], [], True)
        self.assertEqual(print_rule_word_outputs(rule,'dad'), [u'dd'])

    def test_deletion_no_context_zero(self):
        rule = Rule([{"cons": "-"}], [], [], [], True)
        self.assertEqual(print_rule_word_outputs(rule, 'daa'), [u'da'])



    def test_assimilation_both_contexts(self):
        rule = Rule([{"cons": "+"}], [{"voice": "-"}], [{"voice": "-"}], [{"voice": "-"}], True)
        self.assertEqual(print_rule_word_outputs(rule,'tzt'), [u'tst'])   #fail  "[u'tst', u'tst']" - solved

    def test_assimilation_left_context_only(self):
        rule = Rule([{"cons": "+"}], [{"voice": "-"}], [{"voice": "-"}], [], True)
        self.assertEqual(print_rule_word_outputs(rule,'tz'), [u'ts'])

    def test_assimilation_right_context_only(self):
        rule = Rule([{"cons": "+"}], [{"voice": "-"}], [], [{"voice": "-"}], True)
        self.assertEqual(print_rule_word_outputs(rule,'zt'), [u'st']) #fail  "[u'st', u'st']  - solved

    def test_assimilation_no_context(self):
        rule = Rule([{"cons": "+"}], [{"voice": "-"}], [], [], True)
        self.assertEqual(print_rule_word_outputs(rule,'zt'), [u'st'])



def print_rule_word_outputs(rule, word):
        rule_set = RuleSet([rule])
        result = rule_set.get_outputs_of_word(word)
        #print("{} -> {}    {}".format(word, rule_set.get_outputs_of_word(word), rule))
        return result