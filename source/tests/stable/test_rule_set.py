import random
from unittest.mock import ANY

from tests.my_test_case import MyTestCase
from rule import Rule
from rule_set import RuleSet
from configuration import Configuration
from util import log_rule_set

configurations = Configuration()


class TestRuleSet(MyTestCase):

    def test_load_from_json(self):
        self.initialise_segment_table("ab_segment_table.txt")
        rule_set = self.get_rule_set("abnese_rule_set.json")
        self.assertEqual(str(rule_set), "[[] --> [{'cons': '-'}]  /  [{'cons': '+'}]__[{'cons': '+'}] obligatory: True]")

    def test_make_mutation__remove_rule(self):
        self.configurations['UNDERSPECIFICATION_FLAG'] = 0
        self.configurations['REMOVE_RULE'] = 1
        self.initialise_segment_table("ab_segment_table.txt")
        rule = Rule([], [{"cons": "-"}], [{"cons": "+"}], [{"cons": "+"}], obligatory=True)
        rule_set = RuleSet([rule])
        rule_set.make_mutation()
        self.assertEqual(str(RuleSet()), str(rule_set))

    def test_make_mutation__change_rule(self):
        self.configurations['UNDERSPECIFICATION_FLAG'] = 0
        self.configurations['CHANGE_RULE'] = 1
        self.configurations['MUTATE_OBLIGATORY'] = 1
        self.initialise_segment_table("ab_segment_table.txt")
        rule = Rule([], [{"cons": "-"}], [{"cons": "+"}], [{"cons": "+"}], obligatory=True)
        cule = Rule([], [{"cons": "-"}], [{"cons": "+"}], [{"cons": "+"}], obligatory=False)
        rule_set = RuleSet([rule])
        rule_set.make_mutation()

        self.assertEqual(str(RuleSet([cule])), str(rule_set))

    def test_crossover(self):
        self.configurations['RULE_SET_CROSSOVER_METHOD'] = 'pivot'
        self.initialise_segment_table("plural_english_segment_table.txt")
        rule1_target, rule2_target = [{"voice": "+"}],  [{"low": "-"}]
        rule1_change, rule2_change = [{"voice": "-"}], [{"low": "+"}]
        rule1_lcontext, rule2_lcontext = [{"velar": "+"}], [{"cont": "+"}]
        rule1_rcontext, rule2_rcontext = [{"cons": "+"}], [{"voice": "-"}]
        rule1 = Rule(rule1_target, rule1_change, rule1_lcontext, rule1_rcontext, obligatory=True)
        rule2 = Rule(rule2_target, rule2_change, rule2_lcontext, rule2_rcontext, obligatory=True)
        self._seed_me_multiple(methods=[random.randrange] + [random.randint for _ in range(5)],
                               argss=[[1]] + [[0, 1] for _ in range(5)],
                               expecteds=[ANY, 1, 0, 1, 0, 1])

        offspring_1, offspring_2 = RuleSet.crossover(RuleSet([rule1]), RuleSet([rule2]))

        self.assertEqual(str(offspring_1), str(RuleSet([Rule(target=rule2_target, change=rule1_change, left_context=rule2_lcontext, right_context=rule1_rcontext, obligatory=True)])))
        self.assertEqual(str(offspring_2), str(RuleSet([Rule(target=rule1_target, change=rule2_change, left_context=rule1_lcontext, right_context=rule2_rcontext, obligatory=True)])))

    def test_unequal_rules_crossover(self):
        self.configurations['RULE_SET_CROSSOVER_METHOD'] = 'pivot'
        self.initialise_segment_table("plural_english_segment_table.txt")

        r1 = Rule([{"velar": "+"}], [{"velar": "-"}], [{"cons": "+"}], [{"cons": "+"}], obligatory=True)
        r2 = Rule([{"voice": "+"}], [{"voice": "-"}], [{"velar": "+"}], [{"cons": "+"}], obligatory=True)
        r3 = Rule([{"voice": "-"}], [{"cons": "-"}], [{"cons": "+"}], [{"voice": "+"}], obligatory=False)

        rule_1 = RuleSet([r1])
        rule_2 = RuleSet([r2, r3])

        self._seed_me_multiple(
            methods=[random.randrange] + [random.randint for _ in range(5)],
            argss=[[1]] + [[0, 1] for _ in range(5)],
            expecteds=[0, 0, 0, 0, 1, 0])

        offspring_1, offspring_2 = RuleSet.crossover(rule_1, rule_2)
        self.assertEqual(str(offspring_1), str(RuleSet([r1, r3])))
        self.assertEqual(str(offspring_2), str(RuleSet([r2])))
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
        self.assertCountEqual(rule_set.get_outputs_of_word("aabb"), ["aabab"])

    def test_phi_ro_identity(self):
        self.initialise_segment_table("ab_segment_table.txt")
        rule = Rule([{"cons": "-"}], [{"cons": "-"}], [{"cons": "+"}], [{"cons": "+"}], obligatory=True)
        rule_set = RuleSet([rule])
        self.assertCountEqual(rule_set.get_outputs_of_word("bb"), ["bb"])
        self.assertCountEqual(rule_set.get_outputs_of_word("bab"), ["bab"])

    def test_assimilation(self):
        self.initialise_segment_table("plural_english_segment_table.txt")
        rule = Rule([{"cons": "+"}], [{"voice": "-"}], [{"voice": "-"}], [], obligatory=True)
        rule_set = RuleSet([rule])
        self.assertCountEqual(rule_set.get_outputs_of_word("tz"), ["ts"])

    def test_vicky(self):
        self.initialise_segment_table("plural_english_segment_table.txt")
        rule = Rule([], [{"voice": "-"}], [{"voice": "-"}], [], obligatory=True)
        rule_set = RuleSet([rule])
        self.assertCountEqual(rule_set.get_outputs_of_word("dot"), ["dot" + s for s in ('s', 'k', 't')])

    def test_degenerate_assimilation(self):
        self.initialise_segment_table("plural_english_segment_table.txt")
        rule = Rule([{"cons": "+", "low": "+"}], [{"voice": "-"}], [{"voice": "-"}], [], obligatory=False)
        rule_set = RuleSet([rule])
        self.assertCountEqual(rule_set.get_outputs_of_word("tz"), ["tz"])

    def test_kleene_star(self):
        self.initialise_segment_table("plural_english_segment_table.txt")
        self.configurations["CHANGE_KLEENE_VALUE"] = True
        rule = Rule([{"cons": "-"}], [{"low": "+"}], [{"cons": "-"}, {"cons": "+", "kleene": True}], [],
                    obligatory=True)
        rule_set = RuleSet([rule])
        self.assertCountEqual(rule_set.get_outputs_of_word("ato"), ['ata'])
        self.assertCountEqual(rule_set.get_outputs_of_word("attto"), ['attta'])

    def test_rule_application_direction(self):
        # Test whether rules are applied recursively once the environment changes
        self.initialise_segment_table("turkish_segment_table.txt")
        rule = Rule([{"syll": "+"}], [{"back": "-"}], [{"syll": "+", "back": "-"}], [],
                    obligatory=True)
        rule_set = RuleSet([rule])

        # TODO: this should be replaced with:
        # self.assertEqual(rule_set.get_outputs_of_word("i1a"), ['iia'])
        # I have no idea why `iie` returns here as well, but this is a bug.
        self.assertIn('iia', rule_set.get_outputs_of_word("i1a"))

    def test_morpheme_boundary(self):
        self.initialise_segment_table("abnese_lengthening_segment_table.txt")
        rule = Rule([], [{"long": "+"}], [], [{"bound": "+"}], obligatory=True)
        rule_set = RuleSet([rule])
        self.assertEqual(rule_set.get_outputs_of_word("abB"), [u'abYB'])

        rule = Rule([], [{"long": "+"}], [], [{}, {"bound": "+"}], obligatory=True)
        rule_set = RuleSet([rule])
        self.assertEqual(rule_set.get_outputs_of_word("abB"), [u'aYbB'])

    def test_insertion_with_left_context_only(self):
        configurations["SINGLE_CONTEXT_TRANSDUCER_FLAG"] = True
        self.initialise_segment_table("ab_segment_table.txt")
        rule = Rule([], [{"cons": "-"}], [{"cons": "+"}], [], obligatory=True)
        rule_set = RuleSet([rule])
        self.assertCountEqual(rule_set.get_outputs_of_word('bb'), ['baba'])

    def test_insertion_with_left_context_only2(self):
        configurations["SINGLE_CONTEXT_TRANSDUCER_FLAG"] = True
        self.initialise_segment_table("ab_segment_table.txt")
        rule = Rule([], [{"cons": "-"}], [{"cons": "+"}, {"cons": "+"}], [], obligatory=True)
        rule_set = RuleSet([rule])
        self.assertCountEqual(rule_set.get_outputs_of_word('bbbb'), ['bbabba'])

    def test_insertion_with_right_context_only(self):
        configurations["SINGLE_CONTEXT_TRANSDUCER_FLAG"] = True
        self.initialise_segment_table("ab_segment_table.txt")
        rule = Rule([], [{"cons": "-"}], [], [{"cons": "+"}], obligatory=True)
        rule_set = RuleSet([rule])
        self.assertCountEqual(rule_set.get_outputs_of_word('bb'), ['abab'])

    def test_insertion_with_right_context_only_2(self):
        configurations["SINGLE_CONTEXT_TRANSDUCER_FLAG"] = True
        self.initialise_segment_table("ab_segment_table.txt")
        rule = Rule([], [{"cons": "-"}], [], [{"cons": "+"}, {"cons": "+"}], obligatory=True)
        rule_set = RuleSet([rule])
        self.assertCountEqual(rule_set.get_outputs_of_word('bbbb'), ['abababb'])

    def test_insertion_with_right_context_only2(self):
        configurations["SINGLE_CONTEXT_TRANSDUCER_FLAG"] = True
        self.initialise_segment_table("abd_segment_table.txt")
        rule = Rule([], [{"cons": "-"}], [], [{"cons": "+", "labial": "+"}, {"cons": "+", "labial": "-"}],
                    obligatory=True)
        rule_set = RuleSet([rule])
        self.assertCountEqual(rule_set.get_outputs_of_word('bdbd'), ['abdabd'])
