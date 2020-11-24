from collections import defaultdict

from fst import TropicalWeight, linear_chain, EPSILON
from math import ceil, log

from configuration import Singleton
from rule import INSERTION
from segment_table import MORPHEME_BOUNDARY, WORD_BOUNDARY
from configuration import Configuration


CEIL_LOG2 = False
configurations = Configuration()


class UniformEncoding(metaclass=Singleton):
    def __init__(self):
        self._word_acceptors_cache = {}
        self.logarithms_cache = {x: self._log2(x) if x > 0 else 0 for x in range(100)}

    def clear(self):
        self._word_acceptors_cache.clear()

    def get_acceptor_for_word(self, word, syms):
        try:
            return self._word_acceptors_cache[word]
        except KeyError:
            acceptor = linear_chain(word, syms=syms)
            self._word_acceptors_cache[word] = acceptor
            return acceptor

    def _log2(self, n):
        log_n = log(n, 2)
        if CEIL_LOG2:
            return ceil(log_n)
        else:
            return log_n

    def log2(self, n):
        if n not in self.logarithms_cache:
            self.logarithms_cache[n] = self._log2(n)
        return self.logarithms_cache[n]

    def get_weighted_transducer(self, transducer):
        for state in transducer:
            # TODO (@itamar): we might want to consider using:
            # `num_neighbours = len(set(arc.nextstate for arc in state.arcs))`
            num_neighbours = len(list(state.arcs))
            num_bits = self.log2(num_neighbours)
            for arc in state:
                arc.weight = TropicalWeight(num_bits)
        return transducer

    def get_weighted_replace_transducer(self, transducer, rule):
        return self._get_weighted_transducer(transducer,
                                             count_epsilons=False,
                                             noise=rule.noise)

    def get_weighted_rule_transducer(self, transducer, rule):
        is_optional_insertion = not rule.obligatory and rule.transformation_type == INSERTION
        return self._get_weighted_transducer(transducer,
                                             count_epsilons=is_optional_insertion,
                                             noise=rule.noise)

    def _get_weighted_transducer(self, transducer, count_epsilons, noise=False):
        epsilon_ilabel = transducer.isyms[EPSILON]
        for state in transducer:
            arcs = defaultdict(int)
            epsilon_transitions = 0
            for arc in state:
                # count the number of transitions with same input
                arcs[arc.ilabel] += 1

                # an epsilon transition in an optional-insertion-rule should
                # cost as one binary choice
                if count_epsilons and arc.ilabel == epsilon_ilabel:
                    epsilon_transitions += 1
            for arc in state:
                total_inputs = arcs[arc.ilabel]
                if count_epsilons:
                    if arc.ilabel == epsilon_ilabel:
                        # epsilon transition is always considered as one binary
                        # choice (if it is an optional insertion rule)
                        total_inputs += 1
                    else:
                        total_inputs += epsilon_transitions

                if total_inputs not in self.logarithms_cache:
                    self.logarithms_cache[total_inputs] = self.log2(total_inputs)
                # transitions with the same input are a non-deterministic choice
                # the number of choices is reflected in the weight
                if not noise:
                    arc.weight = TropicalWeight(self.log2(total_inputs))
                # for noise rules: weight is applied only to arcs that represent
                # noise application
                elif arc.ilabel != arc.olabel:
                    arc.weight = TropicalWeight(configurations["NOISE_WEIGHT"])
        return transducer

    def replace_morpheme_boundary_with_epsilons(self, transducer):
        transducer.relabel(
            imap={MORPHEME_BOUNDARY: EPSILON}, omap={MORPHEME_BOUNDARY: EPSILON}
        )

    def get_shortest_encoding_length_fst(self, weighted_transducer, word):
        if configurations.get("WORD_BOUNDARY_FLAG", False):
            word += WORD_BOUNDARY

        if word == 'kat':
            print(word)
        acceptor = self.get_acceptor_for_word(word, syms=weighted_transducer.isyms)
        # composition result is: acceptor(weighted_transducer())
        composed = weighted_transducer.compose(acceptor)
        # word can't be parsed by transducer
        if len(composed) == 0:
            return float("INF")

        shortest_distances = composed.shortest_distance(reverse=True)
        if shortest_distances:
            return float(shortest_distances[0])
        return float("INF")

    def get_encoding_length(self, nfa, parse_path):
        total_bits = 0
        for state in parse_path[:-1]:
            bits_for_transition = self.log2(len(nfa.probabilities[state]))
            total_bits += bits_for_transition
        return total_bits

    def get_shortest_encoding_length(self, nfa, parse_paths):
        paths_encoding_lengths = [
            self.get_encoding_length(nfa, path) for path in parse_paths
        ]
        return min(paths_encoding_lengths)
