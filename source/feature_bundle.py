from segment_table import Feature, SegmentTable
from random import choice, randrange, random
from util import get_weighted_list
from configuration import Configuration

KLEENE_FEATURE_NAME = 'kleene'
WORD_BOUNDARY_FEATURE_NAME = "WB"
MORPHEME_BOUNDARY_FEATURE_NAME = "MB"

configurations = Configuration()


class FeatureBundle:
    def __init__(self, feature_string_dict, role=None):
        """
        :param feature_string_dict: dictionary of form {"cons": "+", "WB": True}
        :param role: "target", "change", "left_context", or "right_context"
        """
        feature_dict = dict()

        self.role = role
        self.kleene = False
        self.word_boundary = False
        self.morpheme_boundary = False

        if WORD_BOUNDARY_FEATURE_NAME in feature_string_dict:
            if feature_string_dict[WORD_BOUNDARY_FEATURE_NAME] and self._is_context_bundle():
                self.word_boundary = True
        elif MORPHEME_BOUNDARY_FEATURE_NAME in feature_string_dict:
            if feature_string_dict[MORPHEME_BOUNDARY_FEATURE_NAME] and self._is_context_bundle():
                self.morpheme_boundary = True
        else:
            for feature_name in feature_string_dict:
                if feature_name == KLEENE_FEATURE_NAME:
                    if self._is_context_bundle() and configurations['CHANGE_KLEENE_VALUE']:
                        self.kleene = feature_string_dict[feature_name]
                else:
                    feature = Feature(feature_name)
                    if not SegmentTable().is_valid_feature(feature):
                        raise ValueError(u"{} not in segment_table".format(feature_name))
                    else:
                        feature_dict[feature] = feature_string_dict[feature_name]

        self.feature_dict = feature_dict

    @classmethod
    def get_random_feature_bundle(cls, role, is_boundary_position=False):
        """
        :param role: 'target', 'change', 'left_context', 'right_context'
        :param is_boundary_position: whether feature bundle is first or last in left or right context, respectively
        :return:
        """
        available_features = list(SegmentTable().features.keys())
        if configurations['WORD_BOUNDARY_FLAG'] and FeatureBundle._is_context_role(role) and is_boundary_position:
            available_features.append(WORD_BOUNDARY_FEATURE_NAME)
        if configurations['MORPHEME_BOUNDARY_FLAG'] and FeatureBundle._is_context_role(role) and is_boundary_position:
            available_features.append(MORPHEME_BOUNDARY_FEATURE_NAME)

        feature_dict = {}
        random_feature = choice(available_features)
        if not isinstance(random_feature, Feature):
            if random_feature == WORD_BOUNDARY_FEATURE_NAME:
                feature_dict[WORD_BOUNDARY_FEATURE_NAME] = True
            elif random_feature == MORPHEME_BOUNDARY_FEATURE_NAME:
                feature_dict[MORPHEME_BOUNDARY_FEATURE_NAME] = True
        else:
            random_value = random_feature.get_random_value()
            feature_dict[random_feature.name] = random_value

        return cls(feature_dict, role)

    def make_mutation(self):
        mutation_weights = [(self._add_feature, configurations["ADD_FEATURE"]),
                            (self._remove_feature, configurations["REMOVE_FEATURE"]),
                            (self._change_feature_value, configurations["CHANGE_FEATURE_VALUE"])
                            ]

        if self.feature_dict and self._is_context_bundle():  # Allow Kleene star mutation only if bundle has any features and in left/right context
            mutation_weights.append((self._toggle_kleene, configurations["CHANGE_KLEENE_VALUE"]))

        weighted_mutation_function_list = get_weighted_list(mutation_weights)
        mutation_result = choice(weighted_mutation_function_list)()
        return mutation_result

    def _add_feature(self):
        if self.morpheme_boundary or self.word_boundary:
            return False  # WB or MB feature must be standalone

        available_feature = SegmentTable().get_random_available_feature(self.feature_dict.keys())
        if available_feature:
            self.feature_dict[available_feature] = available_feature.get_random_value()
            return True
        else:
            return False

    def _remove_feature(self):
        if self.feature_dict:
            random_feature = choice(list(self.feature_dict.keys()))
            self.feature_dict.pop(random_feature)

            if not self.feature_dict:  # Remove Kleene star if no features left after removal
                self.kleene = False

            return True
        else:
            return False

    def _change_feature_value(self):
        available_features = []
        if configurations['WORD_BOUNDARY_FLAG'] and self._is_context_bundle():
            available_features.append(WORD_BOUNDARY_FEATURE_NAME)
        if configurations['MORPHEME_BOUNDARY_FLAG'] and self._is_context_bundle():
            available_features.append(MORPHEME_BOUNDARY_FEATURE_NAME)
        if self.feature_dict:
            available_features += list(self.feature_dict.keys())

        if not available_features:
            return False

        feature_to_change = choice(available_features)

        if type(feature_to_change) is Feature:
            available_feature_values = list(set(feature_to_change.values) - set(self.feature_dict[feature_to_change]))
            if available_feature_values:
                self.feature_dict[feature_to_change] = choice(available_feature_values)
                return True
            else:
                return False

        elif feature_to_change == WORD_BOUNDARY_FEATURE_NAME:
            return self._toggle_word_boundary()

        elif feature_to_change == MORPHEME_BOUNDARY_FEATURE_NAME:
            return self._toggle_morpheme_boundary()

        else:
            return False

    def _toggle_kleene(self):
        if configurations['CHANGE_KLEENE_VALUE'] and self._is_context_bundle() and self._is_context_bundle():
            self.kleene = not self.kleene
            return True
        return False

    def _toggle_morpheme_boundary(self):
        if configurations['MORPHEME_BOUNDARY_FLAG'] and self._is_context_bundle():
            self.morpheme_boundary = not self.morpheme_boundary
            if self.morpheme_boundary:
                # Morpheme boundary can only be standalone feature, reset all features if WB is on
                self._reset_features()

            return True
        return False

    def _toggle_word_boundary(self):
        if configurations['WORD_BOUNDARY_FLAG'] and self._is_context_bundle():
            self.word_boundary = not self.word_boundary
            if self.word_boundary:
                # Word boundary can only be standalone feature, reset all features if WB is on
                self._reset_features()

            return True
        return False

    def _is_context_bundle(self):
        return self._is_context_role(self.role)

    @staticmethod
    def _is_context_role(role):
        return role == 'left_context' or role == 'right_context'

    def _reset_features(self):
        self.feature_dict = dict()

    def get_encoding_length(self, rule_symbol_length):
        feature_bundle_encoding_length = 0
        if self.feature_dict:
            feature_bundle_encoding_length = (len(self.feature_dict) - 1) * rule_symbol_length
            for _ in self.feature_dict:
                feature_bundle_encoding_length += rule_symbol_length * 2  # *2, for feature and sign
        if self.kleene:
            feature_bundle_encoding_length += rule_symbol_length
        if self.word_boundary:
            feature_bundle_encoding_length += rule_symbol_length
        if self.morpheme_boundary:
            feature_bundle_encoding_length += rule_symbol_length
        return feature_bundle_encoding_length

    def __eq__(self, other):
        return self.feature_dict == other.feature_dict

    def __getitem__(self, item):
        return self.feature_dict[item]

    def __str__(self):
        repr_dict = self._get_repr_dict()
        return str(repr_dict)

    def __repr__(self):
        repr_dict = self._get_repr_dict()
        repr_dict_key_to_str = [(key, str(key)) for key in repr_dict]
        sorted_keys = sorted(repr_dict_key_to_str, key=lambda x: x[1])
        sorted_repr_dict = {key[1]: repr_dict[key[0]] for key in sorted_keys}
        return str(sorted_repr_dict)

    def _get_repr_dict(self):
        repr_dict = self.feature_dict.copy()
        if self.kleene:
            repr_dict.update({KLEENE_FEATURE_NAME: True})
        if self.word_boundary:
            repr_dict.update({WORD_BOUNDARY_FEATURE_NAME: True})
        if self.morpheme_boundary:
            repr_dict.update({MORPHEME_BOUNDARY_FEATURE_NAME: True})
        return repr_dict


class FeatureBundleList:
    def __init__(self, feature_bundle_list, is_one_item_list, role=None):
        self.role = role
        if isinstance(feature_bundle_list, list):
            self.is_one_item_list = is_one_item_list
            self.feature_bundle_list = []
            for item in feature_bundle_list:
                if isinstance(item, FeatureBundle):
                    self.feature_bundle_list.append(item)
                else:
                    self.feature_bundle_list.append(FeatureBundle(item, role))
        else:
            self.is_one_item_list = feature_bundle_list.is_one_item_list
            self.feature_bundle_list = feature_bundle_list.feature_bundle_list

    def is_valid(self):
        for feature_bundle in self.feature_bundle_list:
            segments = SegmentTable().get_segments_symbols_by_features(feature_bundle)
            if not segments:  # make sure that the feature_bundle represents any symbol
                return False
        return True

    def get_first_item(self):
        return self.feature_bundle_list[0]

    def get_number_of_features(self):
        return len(self.feature_bundle_list)

    def get_encoding_length(self, rule_symbol_length):
        if self.feature_bundle_list:
            feature_bundle_list_encoding_length = (len(
                self.feature_bundle_list) - 1) * rule_symbol_length  # Encoding length of feature bundle separators (number of bundles - 1)
            for feature_bundle in self.feature_bundle_list:
                feature_bundle_list_encoding_length += feature_bundle.get_encoding_length(rule_symbol_length)
            return feature_bundle_list_encoding_length
        else:
            return 0

    def __len__(self):
        return len(self.feature_bundle_list)

    def __getitem__(self, item):
        return self.feature_bundle_list[item]

    def __str__(self):
        return str(self.feature_bundle_list)

    def __repr__(self):
        return repr(self.feature_bundle_list)

    def make_mutation(self):
        mutation_weights = [(self._add_feature_bundle, configurations["ADD_FEATURE_BUNDLE"]),
                            (self._remove_feature_bundle, configurations["REMOVE_FEATURE_BUNDLE"]),
                            (self._change_existing_feature_bundle, configurations["CHANGE_EXISTING_FEATURE_BUNDLE"])]
        weighted_mutation_function_list = get_weighted_list(mutation_weights)
        mutation_result = choice(weighted_mutation_function_list)()
        return mutation_result

    def _add_feature_bundle(self):
        if self.is_one_item_list and len(self.feature_bundle_list) > 0:
            return False
        elif not self.is_one_item_list and len(self.feature_bundle_list) == configurations["MAX_FEATURE_BUNDLE_IN_CONTEXT"]:
            return False
        else:
            insert_position = randrange(len(self.feature_bundle_list) + 1)
            if (self.role == 'right_context' or self.role == 'left_context') and (insert_position == 0 or insert_position == len(self.feature_bundle_list)):
                is_boundary_position = True
            else:
                is_boundary_position = False

            random_feature_bundle = FeatureBundle.get_random_feature_bundle(role=self.role,
                                                                            is_boundary_position=is_boundary_position)
            self.feature_bundle_list.insert(insert_position, random_feature_bundle)
            return True

    def _remove_feature_bundle(self):
        if len(self):
            position = randrange(len(self.feature_bundle_list))
            self.feature_bundle_list.pop(position)
            return True
        else:
            return False

    def _change_existing_feature_bundle(self):
        if len(self):
            feature_bundle_index = choice(list(range(len(self.feature_bundle_list))))
            feature_bundle = self.feature_bundle_list[feature_bundle_index]

            mutation_result = feature_bundle.make_mutation()
            if mutation_result \
                    and len(feature_bundle.feature_dict) == 0 \
                    and (not feature_bundle.word_boundary) \
                    and (not feature_bundle.morpheme_boundary):
                self.feature_bundle_list.pop(feature_bundle_index)

            return mutation_result
        else:
            return False

    @classmethod
    def get_random_feature_bundle_list(cls, is_one_item_list, role=None):
        is_empty_probab = 1 / len(SegmentTable().features)
        if random() < is_empty_probab:
            is_empty = True
        else:
            is_empty = False

        if is_empty:
            return cls([], is_one_item_list, role)
        else:
            max_bundles = 1 if is_one_item_list else configurations["MAX_FEATURE_BUNDLE_IN_CONTEXT"]
            num_bundles = randrange(1, max_bundles + 1)

            feature_bundles = []
            for i in range(num_bundles):
                if (role == 'left_context' or role=='right_context') and (i == 0 or i == num_bundles-1):
                    is_boundary_position = True
                else:
                    is_boundary_position = False
                feature_bundle = FeatureBundle.get_random_feature_bundle(role=role,
                                                                         is_boundary_position=is_boundary_position)
                feature_bundles.append(feature_bundle)
            return cls(feature_bundles, is_one_item_list, role)
