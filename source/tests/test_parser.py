import unittest
from grammar import Grammar
from hypothesis import Hypothesis
from hmm import HMM, INITIAL_STATE, FINAL_STATE
from tests.my_test_case import MyTestCase
from segment_table import SegmentTable
from parser import nfa_parser_get_all_parses
from parser import nfa_parser_get_most_probable_parse as nfa_parser
from uniform_encoding import get_shortest_encoding_length, get_encoding_length, get_weighted_transducer, get_shortest_encoding_length_fst
from rule_set import RuleSet
from rule import Rule


class TestParser(MyTestCase):
    def setUp(self):
        self.table = "plural_english_segment_table"
        self.initialise_segment_table("%s.txt" % self.table)
        self.plural_english_segments = SegmentTable().get_segments_symbols()
        assimilation_rule = Rule([{"cons": "+"}], [{"voice": "-"}], [{"voice": "-"}], [], True)
        self.plural_english_rule_set = RuleSet([assimilation_rule])

    def test_parser(self):
        hmm_multiple_paths = HMM({INITIAL_STATE: ['q1', 'q3'],
                                  'q1': (['q2', FINAL_STATE], ['dog', 'kat', 'kats', 'dogz']),
                                  'q2': ([FINAL_STATE], ['z']),
                                  'q3': (['q3', FINAL_STATE], self.plural_english_segments)})

        grammar = Grammar(hmm_multiple_paths, self.plural_english_rule_set)
        hypothesis = Hypothesis(grammar, ['dogz'])
        nfa = grammar.get_nfa()
        parses, outputs = nfa_parser(nfa, 'dogz')
        print(parses)
        print(outputs)

        nfa = grammar.get_nfa()

        self.write_to_dot_file(nfa, "test_parser_nfa")

    def test_uniform_encoding_length(self):
        hmm_multiple_paths = HMM({INITIAL_STATE: ['q1', 'q3'],
                                  'q1': (['q2', FINAL_STATE], ['dog', 'kat', 'kats', 'dogz']),
                                  'q2': ([FINAL_STATE], ['z']),
                                  'q3': (['q3', FINAL_STATE], self.plural_english_segments)})

        grammar = Grammar(hmm_multiple_paths, None)
        nfa = grammar.get_nfa()
        parse_path, output = nfa_parser(nfa, 'dogz')
        print(parse_path)
        print(output)

        nfa = grammar.get_nfa()
        self.write_to_dot_file(nfa, "test_parser_nfa")
        encoding_length = get_encoding_length(nfa, parse_path)
        print(encoding_length)
        assert(encoding_length == 4.0)

    def test_encoding_length_by_fst(self):
        hmm_multiple_paths = HMM({INITIAL_STATE: ['q1', 'q3'],
                                  'q1': (['q2', FINAL_STATE], ['dog', 'kat', 'kats', 'dogz']),
                                  'q2': ([FINAL_STATE], ['z']),
                                  'q3': (['q3', FINAL_STATE], self.plural_english_segments)})

        grammar = Grammar(hmm_multiple_paths, None)
        transducer = grammar.get_transducer()
        weighted_transducer = get_weighted_transducer(transducer)
        dogz_encoding_length = get_shortest_encoding_length_fst(weighted_transducer, 'dogz')
        print('shortest encoding_length', dogz_encoding_length)
        assert(dogz_encoding_length == 4.0)

        unparsable_encoding_length = get_shortest_encoding_length_fst(weighted_transducer, 'dox')
        print('unparsable_encoding_length', unparsable_encoding_length)
        assert(unparsable_encoding_length == float("INF"))


    def test_parse_uniform_encoding(self):
        hmm_multiple_paths = HMM({INITIAL_STATE: ['q1', 'q3'],
                                  'q1': (['q1','q2', 'q3', FINAL_STATE], ['d', 'k', 'a', 'o', 'g']),
                                  'q2': ([FINAL_STATE], ['z']),
                                  'q3': (['q3', FINAL_STATE], ['z'])})

        grammar = Grammar(hmm_multiple_paths, None)
        # hypothesis = Hypothesis(grammar, ['kats'])
        nfa = grammar.get_nfa()
        transducer = grammar.get_transducer()
        self.write_to_dot_file(nfa, "test_parser_nfa_uniform_encoding")
        parse_paths = nfa_parser_get_all_parses(nfa, 'dogz')
        print(parse_paths)
        #print(parse_paths[2], get_encoding_length(nfa, parse_paths[2]))
        print(get_shortest_encoding_length(nfa, parse_paths))

        assert(len(parse_paths) == 3)


    def test_parser_kleene(self):
        hmm = HMM({INITIAL_STATE: ['q1'],
                   'q1': (['q2', FINAL_STATE], ['at', 'attstktttt', 'st']),
                   'q2': ([FINAL_STATE], ['o'])})

        hmm_transducer = hmm.get_transducer()
        self.write_to_dot_file(hmm_transducer, "test_hmm_transducer_kleene")

        assimilation_rule_with_kleene = Rule([{"cons": "-"}], [{"low": "+"}],
                                             [{"cons": "-"}, {"cons": "+", "kleene": True}], [],
                                             obligatory=True)

        rule_set_with_kleene = RuleSet([assimilation_rule_with_kleene])
        grammar = Grammar(hmm, rule_set_with_kleene)

        nfa = grammar.get_nfa()
        self.write_to_dot_file(nfa, "test_parser_nfa_kleene")

    def test_parser2(self):
        hmm = HMM({INITIAL_STATE: ['q1'],
                   'q1': (['q2', FINAL_STATE], ['dog', 'kat']),
                   'q2': ([FINAL_STATE], ['z'])})
        grammar = Grammar(hmm, self.plural_english_rule_set)
        nfa = grammar.get_nfa()
