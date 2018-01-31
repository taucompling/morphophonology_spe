from tests.my_test_case import MyTestCase
from rule import Rule
from rule_set import RuleSet
from configuration import Configuration
from util import log_rule_set

configurations = Configuration()


class TestRuleSet(MyTestCase):
    def setUp(self):
        pass

    def test_load_from_json(self):
        self.initialise_segment_table("ab_segment_table.txt")
        rule_set = self.get_rule_set("abnese_rule_set.json")
        print(rule_set)

    def test_make_mutation(self):
        self.initialise_segment_table("ab_segment_table.txt")
        rule = Rule([], [{"cons": "-"}], [{"cons": "+"}], [{"cons": "+"}], obligatory=True)
        rule_set = RuleSet([rule])
        rule_set.make_mutation()
        print(rule_set)

    def test_crossover(self):
        self.initialise_segment_table("plural_english_segment_table.txt")
        rule_1 = RuleSet([Rule([{"voice": "+"}], [{"voice": "-"}], [{"velar": "+"}], [{"cons": "+"}], obligatory=True)])
        rule_2 = RuleSet([Rule([{"low": "-"}], [{"low": "+"}], [{"cont": "+"}], [{"voice": "-"}], obligatory=True)])
        offspring_1, offspring_2 = RuleSet.crossover(rule_1, rule_2)
        log_rule_set(rule_1)
        print()
        log_rule_set(rule_2)
        print()
        log_rule_set(offspring_1)
        print()
        log_rule_set(offspring_2)

    def test_unequal_rules_crossover(self):
        self.initialise_segment_table("plural_english_segment_table.txt")
        rule_1 = RuleSet([Rule([{"velar": "+"}], [{"velar": "-"}], [{"cons": "+"}], [{"cons": "+"}], obligatory=True)])

        rule_2 = RuleSet([Rule([{"voice": "+"}], [{"voice": "-"}], [{"velar": "+"}], [{"cons": "+"}], obligatory=True),
                          Rule([{"voice": "-"}], [{"cons": "-"}], [{"cons": "+"}], [{"voice": "+"}], obligatory=False)])

        offspring_1, offspring_2 = RuleSet.crossover(rule_1, rule_2)
        log_rule_set(rule_1)
        print()
        log_rule_set(rule_2)
        print()
        log_rule_set(offspring_1)
        print()
        log_rule_set(offspring_2)

    def test_abnese_insertion(self):
        self.initialise_segment_table("ab_segment_table.txt")
        rule = Rule([], [{"cons": "-"}], [{"cons": "+"}], [{"cons": "+"}], obligatory=True)
        rule_set = RuleSet([rule])
        print(rule_set.get_outputs_of_word("aabb"))

    def test_phi_ro_identity(self):
        self.initialise_segment_table("ab_segment_table.txt")
        rule = Rule([{"cons": "-"}], [{"cons": "-"}], [{"cons": "+"}], [{"cons": "+"}], obligatory=True)
        rule_set = RuleSet([rule])
        print(rule_set.get_outputs_of_word("bb"))  # should be bb , instead []
        print(rule_set.get_outputs_of_word("bab"))  # should be 'bab' instead [u'bab', u'bab']

    def test_assimilation(self):
        self.initialise_segment_table("plural_english_segment_table.txt")
        rule = Rule([{"cons": "+"}], [{"voice": "-"}], [{"voice": "-"}], [], obligatory=True)
        rule_set = RuleSet([rule])
        print(rule_set.get_outputs_of_word("tz"))

    def test_vicky(self):
        self.initialise_segment_table("plural_english_segment_table.txt")
        rule = Rule([], [{"voice": "-"}], [{"voice": "-"}], [], obligatory=True)
        rule_set = RuleSet([rule])
        print(rule_set.get_outputs_of_word("dot"))

    def test_degenerate_assimilation(self):
        self.initialise_segment_table("plural_english_segment_table.txt")
        rule = Rule([{"cons": "+", "low": "+"}], [{"voice": "-"}], [{"voice": "-"}], [], obligatory=False)
        rule_set = RuleSet([rule])
        print(rule_set.get_outputs_of_word("tz"))

    def test_kleene_star(self):
        self.initialise_segment_table("plural_english_segment_table.txt")
        rule = Rule([{"cons": "-"}], [{"low": "+"}], [{"cons": "-"}, {"cons": "+", "kleene": True}], [],
                    obligatory=True)
        rule_set = RuleSet([rule])
        print(rule_set.get_outputs_of_word("ato"))  # -> ata
        print(rule_set.get_outputs_of_word("atttto"))  # -> atttta

    def test_rule_application_direction(self):
        # Test whether rules are applied recursively once the environment changes
        self.initialise_segment_table("turkish_segment_table.txt")
        rule = Rule([{"cons": "-"}], [{"back": "-"}], [{"cons": "-", "back": "-"}], [],
                    obligatory=True)
        rule_set = RuleSet([rule])
        print(rule_set.get_outputs_of_word("i1a"))  # -> iia

    def test_morpheme_boundary(self):
        self.initialise_segment_table("abnese_lengthening_segment_table.txt")
        rule = Rule([], [{"long": "+"}], [], [{"bound": "+"}], obligatory=True)
        rule_set = RuleSet([rule])
        self.assertEqual(rule_set.get_outputs_of_word("ab#"), [u'ab:'])

        rule = Rule([], [{"long": "+"}], [], [{}, {"bound": "+"}], obligatory=True)
        rule_set = RuleSet([rule])
        self.assertEqual(rule_set.get_outputs_of_word("ab#"), [u'a:b'])
        print(rule_set.get_outputs_of_word("b#"))

    def test_insertion_with_left_context_only(self):
        configurations["SINGLE_CONTEXT_TRANSDUCER_FLAG"] = True
        self.initialise_segment_table("ab_segment_table.txt")
        rule = Rule([], [{"cons": "-"}], [{"cons": "+"}], [], obligatory=True)
        rule_set = RuleSet([rule])
        print(rule_set.get_outputs_of_word('bb'))

    def test_insertion_with_left_context_only2(self):
        configurations["SINGLE_CONTEXT_TRANSDUCER_FLAG"] = True
        self.initialise_segment_table("ab_segment_table.txt")
        rule = Rule([], [{"cons": "-"}], [{"cons": "+"}, {"cons": "+"}], [], obligatory=True)
        rule_set = RuleSet([rule])
        print(rule_set.get_outputs_of_word('bbbb'))

    def test_insertion_with_right_context_only(self):
        configurations["SINGLE_CONTEXT_TRANSDUCER_FLAG"] = True
        self.initialise_segment_table("ab_segment_table.txt")
        rule = Rule([], [{"cons": "-"}], [], [{"cons": "+"}], obligatory=True)
        rule_set = RuleSet([rule])
        print(rule_set.get_outputs_of_word('bb'))

    def test_insertion_with_right_context_only_2(self):
        configurations["SINGLE_CONTEXT_TRANSDUCER_FLAG"] = True
        self.initialise_segment_table("ab_segment_table.txt")
        rule = Rule([], [{"cons": "-"}], [], [{"cons": "+"}, {"cons": "+"}], obligatory=True)
        rule_set = RuleSet([rule])
        print(rule_set.get_outputs_of_word('bbbb'))

    def test_insertion_with_right_context_only2(self):
        configurations["SINGLE_CONTEXT_TRANSDUCER_FLAG"] = True
        self.initialise_segment_table("abd_segment_table.txt")
        rule = Rule([], [{"cons": "-"}], [], [{"cons": "+", "labial": "+"}, {"cons": "+", "labial": "-"}],
                    obligatory=True)
        rule_set = RuleSet([rule])
        print(rule_set.get_outputs_of_word('bdbd'))
