from random import choice

from fst import EPSILON

from segment_table import SegmentTable, WORD_BOUNDARY, MORPHEME_BOUNDARY
from feature_bundle import FeatureBundleList
from util import get_weighted_list
from utils.cache import Cache
# from util import pickle_deepcopy as deepcopy
from copy import deepcopy
from configuration import Configuration

configurations = Configuration()

NO_CONTEXT = "NO_CONTEXT"
LEFT_CONTEXT_ONLY = "LEFT_CONTEXT_ONLY"
RIGHT_CONTEXT_ONLY = "RIGHT_CONTEXT_ONLY"
BOTH_CONTEXTS = "BOTH_CONTEXTS"

ASSIMILATION = "ASSIMILATION"
DELETION = "DELETION"
INSERTION = "INSERTION"
DEGENERATE = "DEGENERATE"

cache = Cache.get_cache()


class Rule:
    def __init__(self, target, change, left_context, right_context, obligatory):
        """
        :param target: raw FeatureBundleList
        :param change: raw FeatureBundleList
        :param left_context: raw FeatureBundleList
        :param right_context: raw FeatureBundleList
        :param obligatory: boolean
        """
        self.target_feature_bundle_list = FeatureBundleList(target, is_one_item_list=True, role='target')
        self.change_feature_bundle_list = FeatureBundleList(change, is_one_item_list=True, role='change')
        self.left_context_feature_bundle_list = FeatureBundleList(left_context, is_one_item_list=False,
                                                                  role='left_context')
        self.right_context_feature_bundle_list = FeatureBundleList(right_context, is_one_item_list=False,
                                                                   role='right_context')
        self.obligatory = obligatory
        self.transducer_generated = False
        self.repr = None

    def extract_data_from_feature_bundle_lists(self):
        # check rule type
        if not self.target_feature_bundle_list and not self.change_feature_bundle_list:
            self.transformation_type = DEGENERATE
        elif not self.target_feature_bundle_list:
            self.transformation_type = INSERTION
        elif not self.change_feature_bundle_list:
            self.transformation_type = DELETION
        else:
            self.transformation_type = ASSIMILATION

        # check context type
        if not self.left_context_feature_bundle_list and not self.right_context_feature_bundle_list:
            self.context_type = NO_CONTEXT
        elif not self.left_context_feature_bundle_list:
            self.context_type = RIGHT_CONTEXT_ONLY
        elif not self.right_context_feature_bundle_list:
            self.context_type = LEFT_CONTEXT_ONLY
        else:
            self.context_type = BOTH_CONTEXTS

        if self.target_feature_bundle_list:
            self.target_features = self.target_feature_bundle_list.get_first_item()
            self.target_segments = SegmentTable().get_segments_symbols_by_features(self.target_features)

        if self.change_feature_bundle_list:
            self.change_features = self.change_feature_bundle_list.get_first_item()
            self.change_segments = SegmentTable().get_segments_symbols_by_features(self.change_features)

        if self.target_feature_bundle_list or self.change_feature_bundle_list:
            self.target_change_tuples_list = self._get_target_change_tuples_list()

    def _get_target_change_tuples_list(self):
        """
        Creates a list of tuples representing all possible changes that rule
        may generate: [(target_segment, changed_segment), ...]
        """
        rule_repr = repr(self)
        cached = cache.get(rule_repr, 'change')
        if cached is not None:
            return cached

        target_change_tuples_list = list()

        if self.transformation_type == INSERTION:
            for changed_segment in self.change_segments:
                target_change_tuples_list.append((EPSILON, changed_segment))

        elif self.transformation_type == DELETION:
            for target_segment in self.target_segments:
                target_change_tuples_list.append((target_segment, EPSILON))

        elif self.transformation_type == ASSIMILATION:
            for target_segment in self.target_segments:
                changed_segment = self.get_changed_segment(target_segment, self.change_features)
                if target_segment != changed_segment:
                    target_change_tuples_list.append((target_segment, changed_segment))
        cache.set(rule_repr, target_change_tuples_list, 'change')
        return target_change_tuples_list

    @classmethod
    def load(cls, flat_rule_list):
        return cls(*flat_rule_list)

    def get_changed_segment(self, segment_symbol, change_feature_bundle):
        """
        Applies a change of features to a given segment
        :param segment_symbol: Target segment
        :param change_feature_bundle:  Change feature bundle
        :return: String of output segment
        """
        args_repr = repr(segment_symbol) + repr(change_feature_bundle)
        cached = cache.get(args_repr, 'change_segment')
        if cached is not None:
            return cached

        segment = SegmentTable().get_segment_by_symbol(segment_symbol)
        new_segment_features_dict = deepcopy(segment.features)
        new_segment_features_dict.update(change_feature_bundle.feature_dict)

        changed_segment = SegmentTable().get_segment_symbol_by_features(new_segment_features_dict)

        cache.set(args_repr, changed_segment, 'change_segment')
        return changed_segment

    def get_generation_validity(self):
        self.extract_data_from_feature_bundle_lists()

        rule_repr = repr(self)
        cached = cache.get(rule_repr, 'validity')
        if cached is not None:
            return cached

        generation_validity = True

        # check for invalid feature bundle
        if not self.target_feature_bundle_list.is_valid() or not self.change_feature_bundle_list.is_valid() or \
                not self.left_context_feature_bundle_list.is_valid() or not self.right_context_feature_bundle_list.is_valid():
            generation_validity = False

        # check for invalid change
        if self.target_feature_bundle_list:
            if self.change_feature_bundle_list:
                for segment in self.target_segments:
                    if not self.get_changed_segment(segment, self.change_features):
                        generation_validity = False

        if self.transformation_type == DEGENERATE:
            generation_validity = False
        if self.transformation_type == ASSIMILATION and not self.target_change_tuples_list:
            generation_validity = False

        cache.set(rule_repr, generation_validity, 'validity')
        return generation_validity

    def get_transducer(self):
        self.transducer_generated = self.get_generation_validity()

        if not self.transducer_generated:
            transducer = None
        else:
            from bracket_rule_transducer import BracketRuleTransducer
            rule_transducer_factory = BracketRuleTransducer(self)
            transducer = rule_transducer_factory.get_transducer()
        return transducer

    def make_mutation(self):
        mutation_weights = [(self._mutate_target, configurations["MUTATE_TARGET"]),
                            (self._mutate_change, configurations["MUTATE_CHANGE"]),
                            (self._mutate_left_context, configurations["MUTATE_LEFT_CONTEXT"]),
                            (self._mutate_right_context, configurations["MUTATE_RIGHT_CONTEXT"]),
                            (self._mutate_obligatory, configurations["MUTATE_OBLIGATORY"]),
                            (self._switch_target_change, configurations["SWITCH_TARGET_CHANGE"])]
        weighted_mutation_function_list = get_weighted_list(mutation_weights)
        mutation_result = choice(weighted_mutation_function_list)()
        if mutation_result:
            self.repr = None
            self.transducer_generated = False
        return mutation_result

    def _mutate_target(self):
        return self.target_feature_bundle_list.make_mutation()

    def _mutate_change(self):
        return self.change_feature_bundle_list.make_mutation()

    def _mutate_left_context(self):
        return self.left_context_feature_bundle_list.make_mutation()

    def _mutate_right_context(self):
        return self.right_context_feature_bundle_list.make_mutation()

    def _mutate_obligatory(self):
        self.obligatory = not self.obligatory
        return True

    def _switch_target_change(self):
        old_target = deepcopy(self.target_feature_bundle_list)
        old_change = deepcopy(self.change_feature_bundle_list)
        self.change_feature_bundle_list = old_target
        self.target_feature_bundle_list = old_change
        return True

    def get_encoding_length(self, rule_symbol_length):
        rule_encoding_length = 4 * rule_symbol_length  # delimiters
        rule_encoding_length += self.target_feature_bundle_list.get_encoding_length(rule_symbol_length)
        rule_encoding_length += self.change_feature_bundle_list.get_encoding_length(rule_symbol_length)
        rule_encoding_length += self.left_context_feature_bundle_list.get_encoding_length(rule_symbol_length)
        rule_encoding_length += self.right_context_feature_bundle_list.get_encoding_length(rule_symbol_length)
        rule_encoding_length += 1  # obligatory
        return rule_encoding_length

    @classmethod
    def get_random_rule(cls):
        target = FeatureBundleList.get_random_feature_bundle_list(is_one_item_list=True, role='target')
        change = FeatureBundleList.get_random_feature_bundle_list(is_one_item_list=True, role='change')
        left_context = FeatureBundleList.get_random_feature_bundle_list(is_one_item_list=False, role='left_context')
        right_context = FeatureBundleList.get_random_feature_bundle_list(is_one_item_list=False, role='right_context')
        if configurations["MUTATE_OBLIGATORY"]:
            obligatory = choice([True, False])
        else:
            obligatory = True
        random_rule = Rule(target, change, left_context, right_context, obligatory)
        return random_rule

    def __str__(self):
        if not self.repr:
            return u"{} --> {}  /  {}__{} obligatory: {}".format(self.target_feature_bundle_list,
                                                                 self.change_feature_bundle_list,
                                                                 self.left_context_feature_bundle_list,
                                                                 self.right_context_feature_bundle_list,
                                                                 self.obligatory)
        return self.repr

    def __repr__(self):
        if not self.repr:
            self.repr = u"{} --> {}  /  {}__{} obligatory: {}".format(repr(self.target_feature_bundle_list),
                                                                      repr(self.change_feature_bundle_list),
                                                                      repr(self.left_context_feature_bundle_list),
                                                                      repr(self.right_context_feature_bundle_list),
                                                                      self.obligatory)
        return self.repr

    def get_construction_representation(self):
        return u"{} --> {}  /  {}__{} obligatory: {}".format(self.target_feature_bundle_list, self.change_feature_bundle_list,
                                                 self.left_context_feature_bundle_list,
                                                 self.right_context_feature_bundle_list, self.obligatory)

    def get_segment_representation(self):
        if not hasattr(self, "transformation_type"):
            self.extract_data_from_feature_bundle_lists()
        target = EPSILON
        change = EPSILON
        if self.transformation_type == DEGENERATE:
            pass
        elif self.transformation_type == INSERTION:
            change = self.change_segments
        elif self.transformation_type == DELETION:
            target = self.target_segments
        else:
            if self.target_change_tuples_list:
                target, change = zip(*self.target_change_tuples_list)
        left_context = get_context_string_options(
            self.left_context_feature_bundle_list)  # List of list of possible segments for each feature bundle
        right_context = get_context_string_options(
            self.right_context_feature_bundle_list)  # List of list of possible segments for each feature bundle
        return u"{} --> {}  /  {}__{} obligatory: {}".format(target, change, left_context, right_context,
                                                             self.obligatory)


def get_context_string_options(context_features):
    """
    :param context_features: List of feature bundles
    :return: List of lists of segment symbols matching each feature bundle: [[s1, s2, s3], ...]
    """
    context_string_options = []
    for features in context_features:
        context_string_options.append(SegmentTable().get_segments_symbols_by_features(features))
    return context_string_options


def get_context_regex(context_features):
    context_string_options = get_context_string_options(context_features)
    context_regex = ""
    for s, segment_list in enumerate(context_string_options):
        current_feature_bundle_regex = "({piped_segments}){optional_kleene}".format(
            piped_segments="|".join(segment_list),
            optional_kleene="*" if context_features[s].kleene else ""
        )
        context_regex += current_feature_bundle_regex
    return context_regex
