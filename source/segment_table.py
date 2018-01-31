from math import ceil, log
import codecs
from configuration import Singleton
from copy import deepcopy
from random import choice
import fst
from configuration import Configuration

MORPHEME_BOUNDARY = "B"
LENGTHENING_SYMBOL = "Y"
WORD_BOUNDARY = "W"

LEFT_APPLICATION_BRACKET = "L"
RIGHT_APPLICATION_BRACKET = "R"
LEFT_CENTER_BRACKET = "C"
RIGHT_CENTER_BRACKET = "D"
LEFT_IDENTITY_BRACKET = "I"
RIGHT_IDENTITY_BRACKET = "J"

configurations = Configuration()


class SegmentTable(metaclass=Singleton):
    def __init__(self, segments):

        """
        :type segments: Iterable of Segment
        """
        self.segments = set(segments)
        self.features = deepcopy(segments[0].features)
        self._update_segment_lookup_tables()
        self.transducer_symbol_table = self.get_transducer_symbol_table()
        self.segment_table_file_path = None
        self.number_of_feature_combinations = self.get_number_of_feature_combinations()

    def get_transducer_symbol_table(self):
        transducer_symbol_table = fst.SymbolTable()
        all_segments_string = "".join(self.get_segments_symbols())
        all_segments_string += LEFT_APPLICATION_BRACKET + LEFT_CENTER_BRACKET + LEFT_IDENTITY_BRACKET
        all_segments_string += RIGHT_APPLICATION_BRACKET + RIGHT_CENTER_BRACKET + RIGHT_IDENTITY_BRACKET
        fst.linear_chain(all_segments_string, syms=transducer_symbol_table)
        return transducer_symbol_table

    @classmethod
    def load(cls, segment_table_file_path):
        segments = []
        file = open(segment_table_file_path, "r")
        lines = [x.strip() for x in file.readlines()]
        file.close()
        feature_label_list = lines[0][1:].split(",")  # first line, ignore first comma (,cons, labial..)
        feature_list = [Feature(label) for label in feature_label_list]
        if configurations["UNDERSPECIFICATION_FLAG"]:
            voice_index = feature_label_list.index('voice')
            print(voice_index)
            feature_list[voice_index].values = ('-', '+', '0')

        for line in lines[1:]:
            values_list = line.split(',')
            segment_label = values_list[0]
            values_list = values_list[1:]
            segment_feature_value_dict = dict(zip(feature_list, values_list))
            segment = Segment(segment_label, segment_feature_value_dict)
            segments.append(segment)
        return cls(segments)

    def is_valid(self):
        for segment1 in self.segments:
            for segment2 in self.segments:
                if segment1 != segment2:
                    if segment1.features == segment2.features:
                        return False
        return True

    @property
    def feature_table(self):
        """
        :rtype: set of Feature
        """
        return self._feature_table

    def get_segment_encoding_length(self):
        num_of_bits = 2
        return ceil(log(len(self.features), 2)) * num_of_bits

    def add(self, segment):
        self.segments.add(segment)
        self._update_segment_lookup_tables()

    def remove(self, segment):
        self.segments.remove(segment)
        self._update_segment_lookup_tables()

    def _update_segment_lookup_tables(self):
        lookup_by_feature_table = {}
        lookup_by_symbol_table = {}
        feature_table = set()
        for segment in self.segments:
            lookup_by_symbol_table[segment.symbol] = segment
            for feature_value in segment.features.items():
                if feature_value not in lookup_by_feature_table:
                    lookup_by_feature_table[feature_value] = set()
                lookup_by_feature_table[feature_value].add(segment)
                feature, value = feature_value
                feature_table.add(feature)
        self._lookup_by_feature_table = lookup_by_feature_table
        self._lookup_by_symbol_table = lookup_by_symbol_table
        self._feature_table = feature_table

    def get_segments_by_features(self, features, word_boundary=False, morpheme_boundary=False):
        """
        :type: features: dict
        :rtype: set of Segment
        """
        if word_boundary:
            return [WORD_BOUNDARY]
        elif morpheme_boundary:
            return [MORPHEME_BOUNDARY]

        segments = self.segments.copy()

        # In case no feature mentioned + not boundary feature, this will return all segments
        for feature_value in features.items():
            segments &= self._lookup_by_feature_table[feature_value]
        return segments

    def get_segments_symbols_by_features(self, features):
        """
        Expands features to a list of segments in the matching natural class
        :param features: dict of features
        :return: list of segments that match the input features
        """
        if isinstance(features, dict):
            segments_objects = self.get_segments_by_features(features)
        else:  # feature is FeatureBundle
            segments_objects = self.get_segments_by_features(features.feature_dict,
                                                             word_boundary=features.word_boundary,
                                                             morpheme_boundary=features.morpheme_boundary)
        return [str(segment) for segment in segments_objects]

    def get_segment_symbol_by_features(self, features):
        """features is fully specified"""
        segment_object_list = self.get_segments_by_features(features)
        if segment_object_list:
            return str(segment_object_list.pop())
        else:
            return None

    def get_segment_by_symbol(self, symbol):
        """
        :rtype: Segment
        """
        return self._lookup_by_symbol_table.get(symbol, None)

    def get_segments_symbols(self, include_boundary_symbols=True):
        segments = [segment.symbol for segment in self.segments]
        if include_boundary_symbols:
            if configurations["MORPHEME_BOUNDARY_FLAG"]:
                segments += MORPHEME_BOUNDARY
            if configurations["LENGTHENING_FLAG"]:
                segments += LENGTHENING_SYMBOL
            if configurations["WORD_BOUNDARY_FLAG"]:
                segments += WORD_BOUNDARY
        return segments

    def get_random_segment_symbol(self):
        segment = choice(list(self.segments))
        return str(segment)

    def get_random_available_feature(self, occupied_features):

        available_features = list(set(self.features.keys()) - set(occupied_features))
        if available_features:
            return choice(available_features)
        else:
            return None

    def is_valid_feature(self, feature):
        return feature in self.features

    def get_number_of_feature_combinations(self):
        total = 1
        for feature in self.features:
            total *= len(feature.values)
        return total

    def __str__(self):
        features = list(self.feature_table)
        lines = []
        lines.append(' ' * 4 + ' '.join(map(lambda feature: feature.name.center(8), features)))
        for segment in self.segments:
            line = segment.symbol + ' ' * 3 + ' '.join(
                map(lambda feature: segment.features.get(feature, '?').center(8), features))
            lines.append(line.expandtabs())
        return '\n'.join(lines)

    def __len__(self):
        return len(self.segments)


class Segment(object):
    def __init__(self, symbol, features):
        """
        :type symbol: string
        :type features: dict of (Feature, string)
        """
        self.symbol = symbol
        for feature, value in features.items():
            if value not in feature.values:
                raise TypeError('Invalid value "%s" for feature "%s"' % (value, feature.name))
        self.features = features

    def __repr__(self):
        return self.symbol


class Feature(object):
    def __init__(self, name, values=('-', '+')):
        """
        :type name: string
        :type values: tuple of string
        """
        self.name = name
        self.values = values

    def get_random_value(self):
        return choice(self.values)

    def __repr__(self):
        return "'" + self.name + "'"

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)


NULL_SEGMENT = Segment('', {})
