import codecs
import json
from util import get_transducer_acceptor
from configuration import Configuration
from random import random, choice, randrange, randint
from util import get_weighted_list, get_transducer_outputs, safe_compose, pickle_deepcopy as deepcopy
from segment_table import SegmentTable
from math import ceil, log
from tests.test_util import write_to_dot_to_file as dot
from rule import Rule
from rule import INSERTION, DELETION
import ga_config

configurations = Configuration()

rule_set_transducers = dict()


class RuleSet:
    def __init__(self, rules=[]):
        self.rules = rules
        number_of_features = len(SegmentTable().features)
        self.rule_symbol_length = ceil(log(number_of_features + 6, 2))  # + 6 for 3 delimiters (feature, bundle,
        # rule part), plus sign and minus sign, and Kleene star

    @staticmethod
    def clear_caching():
        global rule_set_transducers
        rule_set_transducers = dict()

    def get_transducer(self):
        rule_set_key = " ".join([str(rule) for rule in self.rules if rule.get_generation_validity()])
        if rule_set_key in rule_set_transducers:
            return rule_set_transducers[rule_set_key]
        else:
            transducer = self.generate_transducer()
            if ga_config.CACHE_RULE_SET_TRANSDUCERS:
                rule_set_transducers[rule_set_key] = transducer
            return transducer

    def generate_transducer(self):
        rule_transducers = [rule.get_transducer() for rule in self.rules]
        rule_transducers = list(filter(None, rule_transducers))
        if not rule_transducers:
            return None
        else:
            transducer = rule_transducers[0]
            for rule_transducer in rule_transducers[1:]:
                rule_transducer.arc_sort_input()
                transducer.arc_sort_input()
                transducer >>= rule_transducer

        return transducer

    @classmethod
    def load(cls, rule_set_file_name):
        rules = []
        with codecs.open(rule_set_file_name, "r") as f:
            rules_list = json.load(f)
            for flat_rule_list in rules_list:
                rules.append(Rule.load(flat_rule_list))
            return cls(rules)

    @classmethod
    def load_form_flat_list(cls, flat_rule_set_list):
        rules = []
        for flat_rule in flat_rule_set_list:
            rules.append(Rule(*flat_rule))
        return cls(rules)

    @classmethod
    def crossover_pivot(cls, rules_set_1, rules_set_2):
        """
        1. Select pivot locus <i> in rule sets A and B
        2. All rules up until <i> remain in original set
        3. Rules A[i] and B[i] in each set is crossed-over:
            a. Its parameters (target, change, left context, right context, optionality) are crossed-over with uniform probability
        4. Rules after <i> are switched between the two sets
        """
        num_rules_1 = len(rules_set_1.rules)
        num_rules_2 = len(rules_set_2.rules)
        max_rules = max(num_rules_1, num_rules_2)

        if max_rules == 0:
            return rules_set_1, rules_set_2

        rules_1 = deepcopy(rules_set_1.rules)
        rules_2 = deepcopy(rules_set_2.rules)

        # pad the rule-set that has fewer rules
        rules_1 += [None] * (max_rules - num_rules_1)
        rules_2 += [None] * (max_rules - num_rules_2)

        locus = randrange(max_rules)

        offspring_1_rules = []
        offspring_2_rules = []
        for i in range(max_rules):
            rule_1 = rules_1[i]
            rule_2 = rules_2[i]

            if i < locus:
                rule_for_offspring_1 = rule_1
                rule_for_offspring_2 = rule_2

            if i == locus:
                rule_for_offspring_1, rule_for_offspring_2 = cls._crossover_rule_pair(rule_1, rule_2)

            if i > locus:
                rule_for_offspring_1 = rule_2
                rule_for_offspring_2 = rule_1

            if rule_for_offspring_1 is not None:
                offspring_1_rules.append(rule_for_offspring_1)
            if rule_for_offspring_2 is not None:
                offspring_2_rules.append(rule_for_offspring_2)

        offspring_1_rules = deepcopy(offspring_1_rules)
        offspring_2_rules = deepcopy(offspring_2_rules)

        return RuleSet(offspring_1_rules), RuleSet(offspring_2_rules)

    @staticmethod
    def _crossover_rule_pair(rule_1, rule_2):
        if rule_1 is not None and rule_2 is not None:
            rule_1_expanded = [rule_1.target_feature_bundle_list, rule_1.change_feature_bundle_list,
                               rule_1.left_context_feature_bundle_list, rule_1.right_context_feature_bundle_list,
                               rule_1.obligatory]

            rule_2_expanded = [rule_2.target_feature_bundle_list, rule_2.change_feature_bundle_list,
                               rule_2.left_context_feature_bundle_list, rule_2.right_context_feature_bundle_list,
                               rule_2.obligatory]

            uniform_crossover_loci = [randint(0, 1) for _ in range(len(rule_1_expanded))]
            # print('rule pair uniform locus', uniform_crossover_loci)

            rules_expanded = [rule_1_expanded, rule_2_expanded]
            offspring_1_expanded = []
            offspring_2_expanded = []
            for i in range(len(uniform_crossover_loci)):
                offspring_1_expanded.append(rules_expanded[uniform_crossover_loci[i]][i])
                offspring_2_expanded.append(rules_expanded[uniform_crossover_loci[i] - 1][i])

            rule_offspring_1 = Rule(*offspring_1_expanded)
            rule_offspring_2 = Rule(*offspring_2_expanded)

        elif rule_1 is not None:
            rule_offspring_1 = None
            rule_offspring_2 = rule_1

        else:
            rule_offspring_2 = None
            rule_offspring_1 = rule_2

        return rule_offspring_1, rule_offspring_2

    @classmethod
    def crossover(cls, rules_set_1, rules_set_2):
        if ga_config.RULE_SET_CROSSOVER == 'uniform':
            offspring_1, offspring_2 = RuleSet.crossover_uniform(rules_set_1, rules_set_2)
        elif ga_config.RULE_SET_CROSSOVER == 'pivot':
            offspring_1, offspring_2 = RuleSet.crossover_pivot(rules_set_1, rules_set_2)
        else:
            raise ValueError("Unknown rule set crossover {}".format(ga_config.RULE_SET_CROSSOVER))
        return offspring_1, offspring_2

    @classmethod
    def crossover_uniform(cls, rules_set_1, rules_set_2):
        """
        For each rule pair r1, r2 in parent rule-sets A, B, select whether to switch between r1, r2.
        If one rule-set has more rules than the other, rules can be moved instead of switching.
        """

        num_rules_1 = len(rules_set_1.rules)
        num_rules_2 = len(rules_set_2.rules)
        max_rules = max(num_rules_1, num_rules_2)

        if max_rules == 0:
            return rules_set_1, rules_set_2

        rules_1 = deepcopy(rules_set_1.rules)
        rules_2 = deepcopy(rules_set_2.rules)

        rule_idx_should_cross_over = [randint(0, 1) for _ in range(max_rules)]

        # pad the rule-set that has fewer rules
        rules_1 += [None] * (max_rules - num_rules_1)
        rules_2 += [None] * (max_rules - num_rules_2)

        rules = [rules_1, rules_2]

        offspring_1_rules = []
        offspring_2_rules = []
        for i in range(max_rules):
            rule_for_offspring_1 = rules[rule_idx_should_cross_over[i]][i]
            rule_for_offspring_2 = rules[rule_idx_should_cross_over[i] - 1][i]

            if rule_for_offspring_1 is not None:
                offspring_1_rules.append(rule_for_offspring_1)
            if rule_for_offspring_2 is not None:
                offspring_2_rules.append(rule_for_offspring_2)

        return RuleSet(offspring_1_rules), RuleSet(offspring_2_rules)

    @classmethod
    def crossover_old(cls, rules_set_1, rules_set_2):
        rules_1 = deepcopy(rules_set_1.rules)
        rules_2 = deepcopy(rules_set_2.rules)

        rule_idx_1, crossover_rule_1, is_null_1 = cls._select_rule_for_crossover(rules_1)
        rule_idx_2, crossover_rule_2, is_null_2 = cls._select_rule_for_crossover(rules_2)

        if is_null_1 or is_null_2:
            offspring_1_rule_set = RuleSet(rules_2)
            offspring_2_rule_set = RuleSet(rules_1)
        else:
            rule_offspring_1 = Rule(target=crossover_rule_1.target_feature_bundle_list,
                                    change=crossover_rule_1.change_feature_bundle_list,
                                    left_context=crossover_rule_2.left_context_feature_bundle_list,
                                    right_context=crossover_rule_2.right_context_feature_bundle_list,
                                    obligatory=crossover_rule_2.obligatory)

            rule_offspring_2 = Rule(target=crossover_rule_2.target_feature_bundle_list,
                                    change=crossover_rule_2.change_feature_bundle_list,
                                    left_context=crossover_rule_1.left_context_feature_bundle_list,
                                    right_context=crossover_rule_1.right_context_feature_bundle_list,
                                    obligatory=crossover_rule_1.obligatory)

            offspring_1_rule_set = RuleSet(rules_1[:rule_idx_1] + [rule_offspring_1] + rules_2[rule_idx_2 + 1:])
            offspring_2_rule_set = RuleSet(rules_2[:rule_idx_2] + [rule_offspring_2] + rules_1[rule_idx_1 + 1:])

        return offspring_1_rule_set, offspring_2_rule_set

    # mutations - all mutations return true or false depending on there success

    @staticmethod
    def _select_rule_for_crossover(rules):
        if rules:
            rule_idx = randint(0, len(rules) - 1)
            rule = rules[rule_idx]
            is_null_rule = False
        else:
            rule_idx = 0
            rule = None
            is_null_rule = True
        return rule_idx, rule, is_null_rule

    def make_mutation(self):
        """
        Randomly select a mutation function based on the probability distribution defined in the configuration.
        """
        mutation_weights = [(self.add_rule, configurations["ADD_RULE"]),
                            (self.remove_rule, configurations["REMOVE_RULE"]),
                            (self.demote_rule, configurations["DEMOTE_RULE"]),
                            (self.change_rule, configurations["CHANGE_RULE"])]

        mutations_list = get_weighted_list(mutation_weights)
        mutation = choice(mutations_list)
        mutation_result = mutation()
        return mutation_result

    def change_rule(self):
        if not self.rules:
            return False
        rule_to_change = choice(self.rules)
        mutation_result = rule_to_change.make_mutation()
        return mutation_result

    def demote_rule(self):
        """
        Mutation, lower rank of one random rule by 1.
        """
        if len(self.rules) > 1:
            index_of_demotion = randrange(len(self.rules) - 1)  # index of a random rule
            i = index_of_demotion  # (which is not the lowest ranked)
            j = index_of_demotion + 1  # index of the rule lower by 1
            self.rules[i], self.rules[j] = self.rules[j], self.rules[i]  # swap places
            return True
        else:
            return False

    def add_rule(self):
        """
        Mutation, add a new random Rule to ruleset.
        """

        if len(self.rules) < configurations["MAX_NUMBER_OF_RULES"]:
            new_rule = Rule.get_random_rule()
            index_of_insertion = randrange(len(self.rules) + 1)
            if new_rule in self.rules:  # newly generated rule is already in rule_set
                return False
            else:
                self.rules.insert(index_of_insertion, new_rule)
                return True
        else:
            return False

    def remove_rule(self):
        """
        Mutation, remove a random rule.
        """

        if not len(self.rules) or len(self.rules) == configurations["MIN_NUMBER_OF_RULES"]:
            return False
        else:
            index = choice(range(len(self.rules)))
            self.rules.pop(index)
            return True

    def get_encoding_length(self):
        if len(self.rules):
            rule_set_encoding_length = (len(self.rules) - 1) * self.rule_symbol_length  # delimiters
            for rule in self.rules:
                rule_set_encoding_length += rule.get_encoding_length(self.rule_symbol_length)
            return rule_set_encoding_length
        else:
            return 0

    def get_outputs_of_word(self, word):
        word_transducer = get_transducer_acceptor(word)
        rule_set_transducer = self.get_transducer()
        if rule_set_transducer:
            dot(word_transducer, "word_transducer")
            dot(rule_set_transducer, "rule_set_transducer")
            word_rule_set_transducer = safe_compose(word_transducer, rule_set_transducer)
            word_rule_set_transducer.remove_epsilon()
            dot(word_rule_set_transducer, "word_rule_set_transducer")
            if len(word_rule_set_transducer):
                try:
                    outputs = get_transducer_outputs(word_rule_set_transducer)
                except:
                    print("get_outputs_of_word failed with word: {}".format(word))

            else:
                outputs = []
        else:
            outputs = get_transducer_outputs(word_transducer)
        return outputs

    def get_log_lines(self):
        log_lines = list()
        log_lines.append("Rule Set:")

        log_lines.append("transducer_generated:")
        for rule in [rule for rule in self.rules if rule.get_generation_validity()]:
            log_lines.append(
                "{} | {}".format(rule.get_construction_representation(), rule.get_segment_representation()))
        log_lines.append("not transducer_generated:")
        for rule in [rule for rule in self.rules if not rule.get_generation_validity()]:
            log_lines.append(
                "{} | {}".format(rule.get_construction_representation(), rule.get_segment_representation()))

        return log_lines

    @classmethod
    def get_random_rule_set(cls):
        num_rules = randint(configurations["MIN_NUMBER_OF_RULES"], configurations["MAX_NUMBER_OF_RULES"])
        rules = []
        for _ in range(num_rules):
            rule = Rule.get_random_rule()
            rules.append(rule)
        return RuleSet(rules)

    def __repr__(self):
        return str(self.rules)

    def is_safe_to_print_parse(self):
        for rule in self.rules:
            if not rule.obligatory:
                if rule.transformation_type == INSERTION:
                    return False
        return True
