from grammar import Grammar
from hmm import HMM, INITIAL_STATE, FINAL_STATE
from rule_set import RuleSet

from tests.my_test_case import MyTestCase
from segment_table import SegmentTable
from configuration import Configuration

configurations = Configuration()


class TestGrammar(MyTestCase):
    def setUp(self):
        pass

    def test_plural_english_grammar(self):
         self.initialise_segment_table("plural_english_segment_table.txt")
         rule_set = self.get_rule_set("plural_english_rule_set.json")

         hmm = HMM({INITIAL_STATE: ['q1'],
                     'q1': (['q2', FINAL_STATE], ['dog', 'kat']),
                     'q2': ([FINAL_STATE], ['z'])})


         grammar = Grammar(hmm, rule_set)
         grammar_transducer = grammar.get_transducer()
         # #self.write_to_dot_to_file(grammar_transducer, "plural_english_grammar")
         # self.assertIn('kats', grammar.generate_word_list(30))
         # nfa = grammar.get_nfa()
         # #self.write_to_dot_to_file(nfa, "plural_english_nfa")

    def test_morpheme_boundary(self):
         configurations["MORPHEME_BOUNDARY_FLAG"] = True
         self.initialise_segment_table("plural_english_segment_table.txt")
         hmm = HMM({INITIAL_STATE: ['q1'],
                     'q1': (['q2', FINAL_STATE], ['dog', 'kat']),
                     'q2': ([FINAL_STATE], ['z'])})
         grammar = Grammar(hmm, [])