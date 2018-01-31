from math import ceil, log
from fst import TropicalWeight, linear_chain, EPSILON
from configuration import Singleton
from segment_table import MORPHEME_BOUNDARY, WORD_BOUNDARY
from configuration import Configuration

configurations = Configuration()


class UniformEncoding(metaclass=Singleton):
    def __init__(self):
        self._word_acceptors_cache = {}
        self.logarithms_cache = {x: ceil(log(x, 2)) if x > 0 else 0 for x in range(100)}

    def get_acceptor_for_word(self, word, syms):
        try:
            return self._word_acceptors_cache[word]
        except KeyError:
            acceptor = linear_chain(word, syms=syms)
            self._word_acceptors_cache[word] = acceptor
            return acceptor

    def get_weighted_transducer(self, transducer):
        for state in transducer:
            num_neighbours = len(list(state.arcs))
            try:
                num_bits = self.logarithms_cache[num_neighbours]
            except KeyError:
                num_bits = ceil(log(num_neighbours, 2))
            for arc in state:
                arc.weight = TropicalWeight(num_bits)
        return transducer

    def replace_morpheme_boundary_with_epsilons(self, transducer):
        transducer.relabel(imap={MORPHEME_BOUNDARY: EPSILON}, omap={MORPHEME_BOUNDARY: EPSILON})

    def get_shortest_encoding_length_fst(self, weighted_transducer, word):
        if configurations["WORD_BOUNDARY_FLAG"]:
            word += WORD_BOUNDARY

        acceptor = self.get_acceptor_for_word(word, syms=weighted_transducer.isyms)
        composed = weighted_transducer.compose(acceptor)  # composition result is: acceptor(weighted_transducer())
        if len(composed) == 0:  # word can't be parsed by transducer
            return float("INF")

        shortest_distances = composed.shortest_distance(reverse=True)
        if shortest_distances:
            return float(shortest_distances[0])
        return float("INF")

    @staticmethod
    def get_encoding_length(nfa, parse_path):
        total_bits = 0
        for state in parse_path[:-1]:
            bits_for_transition = ceil(log(len(nfa.probabilities[state]), 2))
            total_bits += bits_for_transition
        return total_bits

    @staticmethod
    def get_shortest_encoding_length(nfa, parse_paths):
        paths_encoding_lengths = [UniformEncoding.get_encoding_length(nfa, path) for path in parse_paths]
        return min(paths_encoding_lengths)
