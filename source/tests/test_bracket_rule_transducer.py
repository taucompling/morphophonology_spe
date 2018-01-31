from tests.my_test_case import MyTestCase
from segment_table import SegmentTable
from configuration import Configuration
from automata.pyfst_fado_interface import pyfst_from_dfa
from feature_bundle import FeatureBundle, FeatureBundleList
from rule import get_context_regex
from FAdo.reex import str2regexp

from rule import Rule
from util import get_transducer_acceptor, safe_compose, get_transducer_outputs, chain_safe_compose

configurations = Configuration()

a = {"cons": "-", "low": "+"}
i = {"cons": "-", "low": "-"}
b = {"cons": "+", "labial": "+"}
d = {"cons": "+", "labial": "-"}


class TestBracketRuleTransducer(MyTestCase):
    def test_bracket_markings(self):
        self.initialise_segment_table("plural_english_segment_table.txt")
        from bracket_rule_transducer import get_prologue_inverse_transducer
        from bracket_rule_transducer import BracketRuleTransducer
        from bracket_rule_transducer import LEFT_IDENTITY_BRACKET, RIGHT_BRACKETS, LEFT_BRACKETS, \
            RIGHT_IDENTITY_BRACKET, RIGHT_APPLICATION_BRACKET, LEFT_APPLICATION_BRACKET
        rule = Rule([{"cons": "+"}], [{"voice": "-"}], [], [{"voice": "-"}], False)
        word = 'zt'

        prologued_word_transducer = get_prologued_word(word)

        rule.extract_data_from_feature_bundle_lists()
        bracket_rule_transducer_factory = BracketRuleTransducer(rule)
        if rule.obligatory:
            obligatory_dfa = bracket_rule_transducer_factory._get_obligatory_dfa([LEFT_IDENTITY_BRACKET],
                                                                                 RIGHT_BRACKETS)
            obligatory_transducer = pyfst_from_dfa(obligatory_dfa)
            self.write_to_dot_to_file(obligatory_transducer, "obligatory_transducer")
            prologued_obligatory = safe_compose(prologued_word_transducer, obligatory_transducer)
            self.write_to_dot_to_file(prologued_obligatory, "prologued_obligatory")

            custom_obligatory_transducer = pyfst_from_dfa(
                bracket_rule_transducer_factory._get_obligatory_dfa([RIGHT_IDENTITY_BRACKET], LEFT_BRACKETS))
            prologued_obligatory = safe_compose(prologued_obligatory, custom_obligatory_transducer)
            self.write_to_dot_to_file(prologued_obligatory, "prologued_obligatory2")

        else:
            prologued_obligatory = prologued_word_transducer

        right_context_transducer = pyfst_from_dfa(bracket_rule_transducer_factory._get_right_context_dfa())
        prologued_obligatory_right = safe_compose(prologued_obligatory, right_context_transducer)
        self.write_to_dot_to_file(prologued_obligatory_right, "prologued_obligatory_right")

        left_context_transducer = pyfst_from_dfa(bracket_rule_transducer_factory._get_left_context_dfa())
        prologued_obligatory_right_left = safe_compose(prologued_obligatory_right, left_context_transducer)
        self.write_to_dot_to_file(prologued_obligatory_right_left, "prologued_obligatory_right_left")
        print(get_transducer_outputs(prologued_obligatory_right_left, limit=10))

        replace_transducer = bracket_rule_transducer_factory.get_replace_transducer()
        prologued_obligatory_right_left_replace = safe_compose(prologued_obligatory_right_left, replace_transducer)
        self.write_to_dot_to_file(prologued_obligatory_right_left_replace, "prologued_obligatory_right_left_replace")
        print(get_transducer_outputs(prologued_obligatory_right_left_replace, limit=10))

    def setUp(self):
        self.initialise_segment_table("plural_english_segment_table.txt")

    # insertion

    def test_insertion_both_contexts_true(self):
        rule = Rule([], [{"cons": "-", "low": "+"}], [{"cons": "+"}], [{"cons": "+"}], True)
        word = 'tt'
        self.assertEqualsSets(self._rule_construction_helper(rule, word), ["tat"])

    def test_insertion_both_contexts_false(self):
        rule = Rule([], [{"cons": "-", "low": "+"}], [{"cons": "+"}], [{"cons": "+"}], False)
        word = 'tt'
        self.assertEqualsSets(self._rule_construction_helper(rule, word), ["tt", "tat"])

    def test_insertion_right_context_only_true(self):
        rule = Rule([], [{"cons": "-", "low": "+"}], [], [{"cons": "+"}], True)
        word = 't'

    def test_insertion_right_context_only_false(self):
        rule = Rule([], [{"cons": "-", "low": "+"}], [], [{"cons": "+"}], False)
        word = 't'

    def test_insertion_left_context_only_true(self):
        rule = Rule([], [{"cons": "-", "low": "+"}], [{"cons": "+"}], [], True)
        word = 't'
        self.assertEqualsSets(self._rule_construction_helper(rule, word), ["ta"])

    def test_insertion_left_context_only_false(self):
        rule = Rule([], [{"cons": "-", "low": "+"}], [{"cons": "+"}], [], False)
        word = 't'
        self.assertEqualsSets(self._rule_construction_helper(rule, word), ["t", "ta"])

    def test_insertion_no_context_true(self):
        rule = Rule([], [{"cons": "-", "low": "+"}], [], [], True)
        word = 'g'

    def test_insertion_no_context_false(self):
        rule = Rule([], [{"cons": "-", "low": "+"}], [], [], False)
        word = 'g'

    # assimilation


    def test_assimilation_both_contexts_true(self):
        rule = Rule([{"cons": "+"}], [{"voice": "-"}], [{"voice": "-", "velar": "+"}], [{"voice": "-", "velar": "+"}],
                    True)
        word = 'kzk'

    def test_assimilation_both_contexts_false(self):
        rule = Rule([{"cons": "+"}], [{"voice": "-"}], [{"voice": "-", "velar": "+"}], [{"voice": "-", "velar": "+"}],
                    True)
        word = 'kzk'

    def test_assimilation_right_context_only_true(self):
        rule = Rule([{"cons": "+"}], [{"voice": "-"}], [], [{"voice": "-", "velar": "+"}], True)
        word = 'zk'

    def test_assimilation_right_context_only_false(self):
        rule = Rule([{"cons": "+"}], [{"voice": "-"}], [], [{"voice": "-", "velar": "+"}], True)
        word = 'zk'

    def test_assimilationn_left_context_only_true(self):
        rule = Rule([{"cons": "+"}], [{"voice": "-"}], [{"voice": "-"}], [], True)
        word = 'tz'

    def test_assimilationn_left_context_only_false(self):
        rule = Rule([{"cons": "+"}], [{"voice": "-"}], [{"voice": "-"}], [], False)
        word = 'tz'

    def test_assimilation_no_context_true(self):
        rule = Rule([{"cons": "+"}], [{"voice": "-"}], [], [], True)
        word = 'zt'

    def test_assimilation_no_context_false(self):
        rule = Rule([{"cons": "+"}], [{"voice": "-"}], [], [], False)
        word = 'zt'

    # deletion

    def test_deletion_both_contexts_true(self):
        rule = Rule([{"cons": "-"}], [], [{"cons": "+"}], [{"cons": "+"}], True)
        word = 'dat'

    def test_deletion_both_contexts_false(self):
        rule = Rule([{"cons": "-"}], [], [{"cons": "+"}], [{"cons": "+"}], False)
        word = 'dat'

    def test_deletion_right_context_only_true(self):
        pass

    def test_deletion_right_context_only_false(self):
        pass

    def test_deletion_left_context_only_true(self):
        rule = Rule([{"cons": "-"}], [], [{"cons": "+"}], [], True)
        word = "ta"

    def test_deletion_left_context_only_false(self):
        rule = Rule([{"cons": "-"}], [], [{"cons": "+"}], [], False)
        word = "ta"

    # # #deletion_left_context_only -
    # # rule = Rule([{"velar": "+"}], [], [{"velar": "+"}], [], True)
    # # word = "gg"
    #
    #
    # # #deletion_left_context_only -2
    # rule = Rule([{"cons": "-"}], [], [{"velar": "+"}], [], True)
    # word = "gaaa"

    def test_deletion_no_context_true(self):
        pass

    def test_deletion_no_context_false(self):
        pass

    # #deletion_right_context_only
    # rule = Rule([{"cons": "-"}], [], [], [{"cons": "+"}], True)
    # word = "ag"
    # #
    # #deletion_no_context  #JL
    # rule = Rule([{"cons": "-"}], [], [], [], True)
    # word = "da"
    #
    #
    # #deletion_no_context  - special
    # rule = Rule([{"cons": "-"}], [], [], [], True)
    # word = 'daa'
    #


    def assertEqualsSets(self, first, second):
        self.assertEquals(set(first), set(second))

    def _rule_construction_helper(self, rule, word):

        from bracket_rule_transducer import get_prologue_inverse_transducer
        from bracket_rule_transducer import BracketRuleTransducer
        from bracket_rule_transducer import LEFT_IDENTITY_BRACKET, RIGHT_BRACKETS, LEFT_BRACKETS, \
            RIGHT_IDENTITY_BRACKET, RIGHT_APPLICATION_BRACKET, LEFT_APPLICATION_BRACKET
        remove_multiple_paths = False
        second_obligatory = True

        prologued_word_transducer = get_prologued_word(word)

        rule.extract_data_from_feature_bundle_lists()
        bracket_rule_transducer_factory = BracketRuleTransducer(rule)
        if rule.obligatory:
            obligatory_dfa = bracket_rule_transducer_factory._get_obligatory_dfa([LEFT_IDENTITY_BRACKET],
                                                                                 [RIGHT_IDENTITY_BRACKET])
            obligatory_transducer = pyfst_from_dfa(obligatory_dfa)
            self.write_to_dot_to_file(obligatory_transducer, "obligatory_transducer")
            prologued_obligatory = safe_compose(prologued_word_transducer, obligatory_transducer)
            self.write_to_dot_to_file(prologued_obligatory, "prologued_obligatory")

            if second_obligatory:
                custom_obligatory_transducer = pyfst_from_dfa(
                    bracket_rule_transducer_factory._get_obligatory_dfa([RIGHT_IDENTITY_BRACKET],
                                                                        [LEFT_IDENTITY_BRACKET]))
                prologued_obligatory = safe_compose(prologued_obligatory, custom_obligatory_transducer)
                self.write_to_dot_to_file(prologued_obligatory, "prologued_obligatory2")

        else:
            prologued_obligatory = prologued_word_transducer

        right_context_transducer = pyfst_from_dfa(bracket_rule_transducer_factory._get_right_context_dfa())
        self.write_to_dot_to_file(right_context_transducer, "right_context_transducer")
        prologued_obligatory_right = safe_compose(prologued_obligatory, right_context_transducer)
        self.write_to_dot_to_file(prologued_obligatory_right, "prologued_obligatory_right")

        replace_transducer = bracket_rule_transducer_factory.get_replace_transducer()
        self.write_to_dot_to_file(replace_transducer, "replace_transducer")
        prologued_obligatory_right_replace = safe_compose(prologued_obligatory_right, replace_transducer)
        self.write_to_dot_to_file(prologued_obligatory_right_replace, "prologued_obligatory_right_replace")

        left_context_transducer = pyfst_from_dfa(bracket_rule_transducer_factory._get_left_context_dfa())
        self.write_to_dot_to_file(left_context_transducer, "left_context_transducer")
        prologued_obligatory_right_replace_left = safe_compose(prologued_obligatory_right_replace,
                                                               left_context_transducer)
        self.write_to_dot_to_file(prologued_obligatory_right_replace_left, "prologued_obligatory_right_replace_left")
        print(get_transducer_outputs(prologued_obligatory_right_replace_left, limit=10))

        # remove_multiple_paths
        if remove_multiple_paths:
            custom_obligatory_transducer = pyfst_from_dfa(
                bracket_rule_transducer_factory._get_custom_obligatory_dfa([RIGHT_APPLICATION_BRACKET],
                                                                           [LEFT_IDENTITY_BRACKET]))
            prologued_obligatory_right_replace_left = safe_compose(prologued_obligatory_right_replace_left,
                                                                   custom_obligatory_transducer)

            custom_obligatory_transducer = pyfst_from_dfa(
                bracket_rule_transducer_factory._get_custom_obligatory_dfa([RIGHT_IDENTITY_BRACKET],
                                                                           [LEFT_APPLICATION_BRACKET]))
            prologued_obligatory_right_replace_left = safe_compose(prologued_obligatory_right_replace_left,
                                                                   custom_obligatory_transducer)

        self.write_to_dot_to_file(prologued_obligatory_right_replace_left,
                                  "prologued_obligatory_right_replace_left_remove_multiple_paths")
        print(get_transducer_outputs(prologued_obligatory_right_replace_left, limit=10))

        prologue_inverse_transducer = get_prologue_inverse_transducer()
        self.write_to_dot_to_file(prologue_inverse_transducer, "prologue_inverse_transducer")
        prologued_obligatory_right_replace_left_inverse = safe_compose(prologued_obligatory_right_replace_left,
                                                                       prologue_inverse_transducer)
        prologued_obligatory_right_replace_left_inverse.remove_epsilon()
        self.write_to_dot_to_file(prologued_obligatory_right_replace_left_inverse,
                                  "prologued_obligatory_right_replace_left_inverse")
        transducer_outputs = get_transducer_outputs(prologued_obligatory_right_replace_left_inverse, limit=10)
        print(transducer_outputs)

        return transducer_outputs

    # FAdo regexes

    def test_get_context_regex(self):
        feature_bundle_list = FeatureBundleList([{'cons': '+'}], is_one_item_list=True)
        regex_str = get_context_regex(feature_bundle_list)
        print(regex_str)
        regex = str2regexp(regex_str)
        eval_word = regex.evalWordP("t")
        print(eval_word)
        assert eval_word

        eval_word = regex.evalWordP("a")
        print(eval_word)
        assert not eval_word

        eval_word = regex.evalWordP("tt")
        print(eval_word)
        assert not eval_word

        regex1_str = "(a|b|c)"
        regex2_str = "a+b+c"

        regex_1 = str2regexp(regex1_str)
        regex_2 = str2regexp(regex2_str)

        comp = regex_1.compare(regex_2)
        assert comp


def get_prologued_word(word):
    from bracket_rule_transducer import get_prologue_transducer
    word_transducer = get_transducer_acceptor(word)
    prologue_transducer = get_prologue_transducer()
    prologued_word_transducer = safe_compose(word_transducer, prologue_transducer)
    prologued_word_transducer.remove_epsilon()
    return prologued_word_transducer
