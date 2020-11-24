from abc import abstractmethod
from copy import deepcopy

from segment_table import SegmentTable, Feature


class BaseNoise:
    def __init__(self, noise_rate):
        self.noise_rate = noise_rate

    @property
    @abstractmethod
    def description(self):
        raise NotImplementedError()

    @abstractmethod
    def apply_noise(self, words):
        """Applies noise to a list of words"""
        raise NotImplementedError()


class FinalDevoicingNoise(BaseNoise):

    @property
    def description(self):
        return f"""devoicing the final obstruent of {self.noise_rate}% of the 
words. If the final segment of a words is not a voiced obstruent, does nothing.
"""

    def apply_noise(self, words):
        total_to_noise = int(len(words) * self.noise_rate / 100)
        segment_table = SegmentTable()
        for i, word in enumerate(words[:total_to_noise]):
            c = word[-1]
            segment = segment_table.get_segment_by_symbol(c)
            if not self._is_voiced_obstruent(segment):
                continue
            new_features = deepcopy(segment.features)
            new_features[Feature('voice', ('+', '-'))] = '-'
            new_c = segment_table.get_segment_symbol_by_features(new_features)
            if new_c:
                words[i] = word[:-1] + new_c

    def _is_voiced_obstruent(self, segment):
        is_voiced = segment.features[Feature('voice', ('+', '-'))] == '+'
        is_obstruent = segment.features[Feature('cont', ('+', '-'))] == '-'
        return is_voiced and is_obstruent
