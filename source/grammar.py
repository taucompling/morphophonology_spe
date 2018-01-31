from math import ceil, log
from random import choice, randint
from automata.parsing_nfa import ParsingNFA
from util import get_weighted_list
from rule_set import RuleSet
from segment_table import SegmentTable
from tests.test_util import write_to_dot_to_file as dot
from configuration import Configuration
import ga_config
from hmm import HMM
from segment_table import MORPHEME_BOUNDARY, WORD_BOUNDARY

configurations = Configuration()


class Grammar:
    def __init__(self, hmm, rule_set=None):
        if isinstance(hmm, HMM):
            self.hmm = hmm
        else:
            self.hmm = HMM(hmm)
        segment_table = SegmentTable()
        self.segment_symbol_length = ceil(log(len(segment_table) + 1, 2))  # + 1 for the delimiter
        if rule_set:
            self.rule_set = rule_set
        else:
            self.rule_set = RuleSet()

    def generate_word(self):
        emission = self.hmm.generate_emission()
        return choice(self.rule_set.get_outputs_of_word(emission))

    def get_transducer(self):
        hmm_transducer = self.hmm.get_transducer()
        if "case_name" in configurations.configurations_dict:
            case_name = configurations.configurations_dict["case_name"]
            dot(hmm_transducer, "{}_hmm_transducer".format(case_name))
        rules_set_transducer = self.rule_set.get_transducer()
        if rules_set_transducer:
            hmm_transducer.arc_sort_input()
            rules_set_transducer.arc_sort_input()
            composed_hmm_rules_transducer = hmm_transducer >> rules_set_transducer
        else:
            composed_hmm_rules_transducer = hmm_transducer
        return composed_hmm_rules_transducer

    def get_nfa(self):
        grammar_pyfst_transducer = self.get_transducer()
        # dot(grammar_pyfst_transducer, "grammar_pyfst_transducer")
        # grammar_pyfst_transducer.remove_epsilon()
        return ParsingNFA.get_from_pyfst_transducer(grammar_pyfst_transducer)

    def make_mutation(self):
        num_mutations = randint(1, ga_config.MAX_MUTATIONS)
        mutation_result = False

        for _ in range(num_mutations):
            if ga_config.MUTATE_BOTH_HMM_AND_RULES:
                rule_set_success = False
                hmm_success = False
                if configurations["EVOLVE_RULES"]:
                    rule_set_success = self.rule_set.make_mutation()
                if configurations["EVOLVE_HMM"]:
                    hmm_success = self.hmm.make_mutation()
                mutation_result = mutation_result or rule_set_success or hmm_success

            else:
                rule_set_mutation_weight = 0 if not configurations["EVOLVE_RULES"] else configurations[
                    "MUTATE_RULE_SET"]
                hmm_mutation_weight = 0 if not configurations["EVOLVE_HMM"] else configurations["MUTATE_HMM"]

                mutation_weights = [(self.rule_set, rule_set_mutation_weight),
                                    (self.hmm, hmm_mutation_weight)]

                weighted_mutatable_object_list = get_weighted_list(mutation_weights)
                object_to_mutate = choice(weighted_mutatable_object_list)
                mutation_result = object_to_mutate.make_mutation()

        return mutation_result

    def get_encoding_length(self):
        if not configurations["UNDERSPECIFICATION_FLAG"]:
            hmm_encoding_length = self.hmm.get_encoding_length(self.segment_symbol_length,
                                                               restrictions_on_alphabet=
                                                               configurations["RESTRICTIONS_ON_ALPHABET"])
        else:
            hmm_encoding_length = self.hmm.get_underspecified_encoding_length()
        rules_encoding_length = self.rule_set.get_encoding_length()
        return hmm_encoding_length, rules_encoding_length

    def generate_word_list(self, n):
        result = []
        for _ in range(n):
            result.append(self.generate_word())
        return result

    def get_all_outputs(self):
        transducer = self.get_transducer()
        transducer_symbol_table = SegmentTable().transducer_symbol_table
        outputs = list()
        for path in transducer.paths():
            output = ""
            for i in path:
                symbol = transducer_symbol_table.find(i.olabel)
                if symbol != u"\u03b5" and symbol != MORPHEME_BOUNDARY and symbol != WORD_BOUNDARY:
                    output += symbol
            outputs.append(output)
        return outputs

