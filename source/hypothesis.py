import pickle
import random
from deap import base
from math import isinf

from util import DFATooLargeException
from hmm import HMM
from grammar import Grammar
from nfa_parser import nfa_parser_get_most_probable_parse
from configuration import Configuration
from uniform_encoding import UniformEncoding
from rule_set import RuleSet
from copy import deepcopy
import ga_config

configurations = Configuration()
uniform_encoding = UniformEncoding()


class HypothesisFitness(base.Fitness):
    def __init__(self):
        self.weights = (-1.0,)
        super(HypothesisFitness, self).__init__()


class Hypothesis:
    def __init__(self, grammar):
        self.grammar = grammar
        # these three fields have temporal cohesion with get_energy()
        self.energy_signature = None
        self.energy = None
        self.unparsed_words = 0
        self.fitness = HypothesisFitness()

    def get_energy(self):
        if self.energy is None:
            self._calculate_energy()
        return self.energy

    def _calculate_energy(self):
        data_encoding_length_by_grammar = configurations[
                                              "DATA_ENCODING_LENGTH_MULTIPLIER"] * self.get_data_encoding_length_by_grammar()
        hmm_encoding_length, rules_encoding_length = self.grammar.get_encoding_length()
        hmm_encoding_length = configurations["HMM_ENCODING_LENGTH_MULTIPLIER"] * hmm_encoding_length
        rules_encoding_length = configurations["RULES_SET_ENCODING_LENGTH_MULTIPLIER"] * rules_encoding_length
        grammar_encoding_length = hmm_encoding_length + rules_encoding_length
        energy = data_encoding_length_by_grammar + grammar_encoding_length
        self.energy_signature = "Energy: {:,.2f} (data_by_grammar: {:,.2f}, " \
                                "hmm: {:,.2f}, rule_set: {:,.2f})".format(energy, data_encoding_length_by_grammar,
                                                                    hmm_encoding_length, rules_encoding_length)
        self.energy = energy

    def set_energy(self, energy):
        self.energy = energy

    def get_recent_energy_signature(self):
        if not self.energy_signature:
            self._calculate_energy()
        return self.energy_signature

    def get_data_encoding_length_by_grammar(self):
        if ga_config.PARSER_TYPE == 'python':
            return self.get_data_encoding_length_by_grammar_python()
        elif ga_config.PARSER_TYPE == 'openfst':
            return self.get_data_encoding_length_by_grammar_openfst()
        else:
            raise NotImplementedError(ga_config.PARSER_TYPE)

    def get_data_encoding_length_by_grammar_python(self):
        data_by_grammar_length = 0
        unparsed_words = 0
        nfa = self.grammar.get_nfa()
        # self.data_code_length_dict = dict()
        for word in configurations.simulation_data:
            # if configurations["MORPHEME_BOUNDARY_FLAG"]:
            #     word = word #+ "B"
            parse_result = nfa_parser_get_most_probable_parse(nfa, word)
            if parse_result is None:
                unparsed_words += 1
                encoding_length = float("INF")
            else:
                parse_path, output = parse_result
                encoding_length = uniform_encoding.get_encoding_length(nfa, parse_path)
            data_by_grammar_length += encoding_length

        self.unparsed_words = unparsed_words
        return data_by_grammar_length

    def get_data_encoding_length_by_grammar_openfst(self):
        """ Use FST operators on grammar transducer to calculate encoding length """
        data_by_grammar_length = 0
        num_unparsed_words = 0
        total_words = len(configurations.simulation_data)

        transducer_too_large = False
        try:
            transducer = self.grammar.get_transducer()

            num_states_in_transducer = len(transducer)
            if num_states_in_transducer >= configurations["TRANSDUCER_STATES_LIMIT"]:
                transducer_too_large = True

        except DFATooLargeException:
            transducer_too_large = True

        if transducer_too_large:
            num_unparsed_words = total_words
            data_by_grammar_length = float("inf")

        else:
            if configurations["MINIMIZE_TRANSDUCER"]:
                transducer = self.grammar.minimize_transducer(transducer)

            weighted_transducer = transducer
            if configurations["MORPHEME_BOUNDARY_FLAG"]:
                uniform_encoding.replace_morpheme_boundary_with_epsilons(weighted_transducer)

            encoding_length_for_word = {}  # cache in case corpus contains duplicates

            for word in configurations.simulation_data:
                enc_len, parsed = self._get_word_encoding_length(
                    word,
                    encoding_length_for_word,
                    weighted_transducer,
                )
                if not parsed:
                    num_unparsed_words += 1

                data_by_grammar_length += enc_len

        self.unparsed_words = num_unparsed_words
        if self.unparsed_words:
            return float('inf')
        else:
            return data_by_grammar_length

    def _get_word_encoding_length(self,
                                  word,
                                  encoding_length_for_word,
                                  weighted_transducer,
                                  ):
        parsed = True
        if word in encoding_length_for_word:
            enc_len = encoding_length_for_word[word]
        else:
            enc_len = uniform_encoding.get_shortest_encoding_length_fst(weighted_transducer, word)
            encoding_length_for_word[word] = enc_len

        if enc_len == float("inf"):
            parsed = False
            enc_len = 0  # punishment is added in the end
        return enc_len, parsed

    def get_neighbor(self):
        new_hypothesis = self.get_hypothesis_copy()
        mutation_result = new_hypothesis.grammar.make_mutation()
        return mutation_result, new_hypothesis

    def get_hypothesis_copy(self):
        grammar_copy = pickle.loads(pickle.dumps(self.grammar, -1))
        new_hypo = self.__class__(data=self.data)
        new_hypo.grammar = grammar_copy
        return new_hypo

    @classmethod
    def create_initial_hypothesis(cls, data, initial_hmm=None, initial_rule_set=None):
        if not initial_hmm:
            initial_hmm = HMM.get_default_hmm()
        else:
            initial_hmm = HMM(initial_hmm)

        if not initial_rule_set:
            rule_set = RuleSet([])
        else:
            rule_set = initial_rule_set

        grammar = Grammar(initial_hmm, rule_set)
        return Hypothesis(grammar, data)

    @classmethod
    def create_hypothesis(cls, hmm, rules_set):
        grammar = Grammar(hmm, rules_set)
        return Hypothesis(grammar)

    @classmethod
    def get_random_hypothesis(cls, simulation):
        data = configurations.simulation_data
        if hasattr(simulation, 'initial_hmm'):
            initial_hmm = simulation.initial_hmm
        else:
            initial_hmm = None

        if hasattr(simulation, 'initial_rule_set'):
            initial_rules = simulation.initial_rule_set
        else:
            initial_rules = None

        if ga_config.RANDOM_HYPOTHESIS_BY_MUTATIONS:
            random_hypothesis = Hypothesis.get_random_hypothesis_by_mutations(data, initial_hmm, initial_rules)
        else:
            random_hypothesis = Hypothesis.get_random_hypothesis_randomized(simulation, data, initial_hmm, initial_rules)
        return random_hypothesis

    @classmethod
    def get_random_hypothesis_randomized(cls, simulation, data, initial_hmm=None, initial_rules=None):
        if initial_rules:
            rule_set = RuleSet.load_from_flat_list(initial_rules)
        elif not configurations['EVOLVE_RULES']:
            rule_set = RuleSet.load_from_flat_list(deepcopy(simulation.target_tuple[1]))
        else:
            rule_set = RuleSet.get_random_rule_set()

        if initial_hmm:
            hmm = HMM(deepcopy(initial_hmm))
        elif not configurations['EVOLVE_HMM']:
            hmm = HMM(deepcopy(simulation.target_tuple[0]))
        else:
            hmm = HMM.get_random_hmm(data)

        grammar = Grammar(hmm, rule_set)
        return Hypothesis(grammar)

    @classmethod
    def get_random_hypothesis_by_mutations(cls, data, fixed_hmm=None, fixed_rules=None):
        if configurations["EVOLVE_RULES"]:
            initial_rule_set = RuleSet()
        elif fixed_rules:
            initial_rule_set = RuleSet.load_from_flat_list(fixed_rules)
        else:
            initial_rule_set = RuleSet()

        if configurations["EVOLVE_HMM"]:
            initial_hmm = None
        elif fixed_hmm:
            initial_hmm = HMM(deepcopy(fixed_hmm))
        else:
            initial_hmm = None

        hypothesis = Hypothesis.create_initial_hypothesis(data, initial_hmm=initial_hmm,
                                                          initial_rule_set=initial_rule_set)
        for _ in range(ga_config.RANDOM_INIT_WARMUP_STEPS):
            new_hypothesis = deepcopy(hypothesis)
            success = new_hypothesis.grammar.make_mutation()
            current_energy = hypothesis.get_energy()
            new_energy = new_hypothesis.get_energy()
            if success and not isinf(new_energy):
                if new_energy < current_energy or random.random() < ga_config.ACCEPT_WORSE_PROBAB:
                    hypothesis = new_hypothesis

        return hypothesis

    @property
    def grammar(self):
        return self._grammar

    @grammar.setter
    def grammar(self, g):
        self._grammar = g
        self.invalidate_energy()

    def invalidate_energy(self):
        self.energy = None

    def invalidate_fitness(self):
        del self.fitness.values

    def __str__(self):
        return '{} {}'.format(str(self.grammar.hmm), str(self.grammar.rule_set))

    def __repr__(self):
        return '{} {}'.format(repr(self.grammar.hmm), repr(self.grammar.rule_set))
