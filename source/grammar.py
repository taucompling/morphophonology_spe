from random import choice
from automata.parsing_nfa import ParsingNFA
from uniform_encoding import UniformEncoding
from util import get_weighted_list
from rule_set import RuleSet
from segment_table import SegmentTable
from tests.test_util import write_to_dot_file as dot, write_to_dot_file
from configuration import Configuration
import ga_config
from hmm import HMM
from segment_table import MORPHEME_BOUNDARY, WORD_BOUNDARY

configurations = Configuration()
uniform_encoding = UniformEncoding()


class Grammar:
    def __init__(self, hmm, rule_set=None):
        if isinstance(hmm, HMM):
            self.hmm = hmm
        else:
            self.hmm = HMM(hmm)
        segment_table = SegmentTable()
        self.segment_symbol_length = uniform_encoding.log2(len(segment_table) + 1)  # + 1 for the delimiter
        if rule_set:
            self.rule_set = rule_set
        else:
            self.rule_set = RuleSet(noise=False)

        noises = configurations.get("NOISE_RULE_SET", [])
        self.noise_rule_set = RuleSet.load_noise_rules_from_flat_list(noises)

        self._cached_hmm_transducer = None
        self._cached_rule_set_transducer = None
        self._cached_noise_rule_set_transducer = None

    def generate_word(self):
        emission = self.hmm.generate_emission()
        return choice(self.rule_set.get_outputs_of_word(emission))

    def generate_all_words(self):
        # TODO: I think this also generates noised data. This should be fixed.
        words = []
        emissions = self.hmm.generate_all_emissions()
        for emission in emissions:
            words += self.rule_set.get_outputs_of_word(emission)
        return words

    def get_transducer(self, with_noise=True):
        hmm_transducer = self.get_hmm_transducer()

        if "case_name" in configurations.configurations_dict:
            case_name = configurations.configurations_dict["case_name"]
            dot(hmm_transducer, "{}_hmm_transducer".format(case_name))
        rules_set_transducer = self.get_rule_set_transducer()
        if with_noise:
            noise_rules_transducer = self.get_noise_rule_set_transducer()
        else:
            noise_rules_transducer = None

        return self._compose_grammar_transducers(
            hmm_transducer, rules_set_transducer, noise_rules_transducer
        )

    def _compose_grammar_transducers(self, first_transducer, *other_transducers):
        composed_transducer = first_transducer
        for transducer in other_transducers:
            if transducer:
                composed_transducer.arc_sort_input()
                transducer.arc_sort_input()
                composed_transducer = composed_transducer >> transducer
        return composed_transducer

    def get_nfa(self):
        grammar_pyfst_transducer = self.get_transducer()
        # dot(grammar_pyfst_transducer, "grammar_pyfst_transducer")
        # grammar_pyfst_transducer.remove_epsilon()
        return ParsingNFA.get_from_pyfst_transducer(grammar_pyfst_transducer)

    def make_mutation(self):
        mutation_successful = False

        if ga_config.MUTATE_BOTH_HMM_AND_RULES:
            hmm_mutation_successful = False
            rule_set_mutation_successful = False

            if configurations["EVOLVE_HMM"]:
                hmm_mutation_successful = self.hmm.make_mutation()
            if configurations["EVOLVE_RULES"]:
                rule_set_mutation_successful = self.rule_set.make_mutation()

            mutation_successful = mutation_successful or rule_set_mutation_successful or hmm_mutation_successful

            if hmm_mutation_successful:
                self.invalidate_cached_hmm_transducer()
            if rule_set_mutation_successful:
                self.invalidate_cached_rule_set_transducer()

        else:
            rule_set_mutation_weight = 0 if not configurations["EVOLVE_RULES"] else configurations["MUTATE_RULE_SET"]
            hmm_mutation_weight = 0 if not configurations["EVOLVE_HMM"] else configurations["MUTATE_HMM"]

            mutation_weights = [('rule_set', rule_set_mutation_weight),
                                ('hmm', hmm_mutation_weight)]

            weighted_mutatable_object_list = get_weighted_list(mutation_weights)
            object_name_to_mutate = choice(weighted_mutatable_object_list)
            if object_name_to_mutate == 'rule_set':
                object_to_mutate = self.rule_set
            elif object_name_to_mutate == 'hmm':
                object_to_mutate = self.hmm
            mutation_successful = object_to_mutate.make_mutation()

            if mutation_successful:
                if object_name_to_mutate == 'hmm':
                    self.invalidate_cached_hmm_transducer()
                elif object_name_to_mutate == 'rule_set':
                    self.invalidate_cached_rule_set_transducer()

        return mutation_successful

    def get_encoding_length(self):
        if not configurations["UNDERSPECIFICATION_FLAG"]:
            hmm_encoding_length = self.hmm.get_encoding_length(self.segment_symbol_length,
                                                               restrictions_on_alphabet=configurations["RESTRICTIONS_ON_ALPHABET"])
        else:
            hmm_encoding_length = self.hmm.get_underspecified_encoding_length()
        rules_encoding_length = self.rule_set.get_encoding_length()
        return hmm_encoding_length, rules_encoding_length

    def generate_word_list(self, n):
        result = []
        for _ in range(n):
            result.append(self.generate_word())
        return result

    def get_all_outputs(self, with_noise=True):
        transducer = self.get_transducer(with_noise=with_noise)
        if configurations["MINIMIZE_TRANSDUCER"]:
            transducer = self.minimize_transducer(transducer)

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

    def get_hmm_transducer(self):
        if self._cached_hmm_transducer is None:
            self._cached_hmm_transducer = self.hmm.get_transducer()
        return self._cached_hmm_transducer

    def get_rule_set_transducer(self):
        if self._cached_rule_set_transducer is None:  # rule set transducer may be None
            self._cached_rule_set_transducer = self.rule_set.get_transducer()

        return self._cached_rule_set_transducer

    def get_noise_rule_set_transducer(self):
        if self._cached_noise_rule_set_transducer is None:
            self._cached_noise_rule_set_transducer = self.noise_rule_set.get_transducer()
        return self._cached_noise_rule_set_transducer

    def get_log_lines(self):
        return self.hmm.get_log_lines() + self.rule_set.get_log_lines()

    def invalidate_cached_hmm_transducer(self):
        self._cached_hmm_transducer = None

    def invalidate_cached_rule_set_transducer(self):
        self._cached_rule_set_transducer = None

    @staticmethod
    def minimize_transducer(transducer):
        transducer.project_output()
        transducer = transducer.determinize()
        transducer.minimize()
        return transducer

    def __getstate__(self):
        # Don't pickle cached transducers
        state = self.__dict__.copy()
        state['_cached_hmm_transducer'] = None
        state['_cached_rule_set_transducer'] = None
        state['_cached_noise_rule_set_transducer'] = None
        return state
