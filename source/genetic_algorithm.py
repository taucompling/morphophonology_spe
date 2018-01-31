import random
import numpy as np
from math import isinf, floor
from operator import attrgetter
from deap import base, creator, tools
from hmm import HMM
from grammar import Grammar
from configuration import Configuration
from rule_set import RuleSet
from queue import Empty, Full
from hypothesis import Hypothesis
from util import log_hypothesis, hypothesis_to_string, select_worst_idx, pickle_deepcopy as deepcopy
from utils.logger import MultiprocessLogger as Logger
import ga_config

configurations = Configuration()


class GeneticAlgorithm:
    def __init__(self, simulation, migration_coordinator, result_queue, island_number, simulation_total_islands,
                 initial_population=None):
        self.logger = Logger.get_logger()
        self.island_number = island_number
        self.simulation_total_islands = simulation_total_islands
        self.island_name = '{}_{}'.format(ga_config.PROCESS_NAME_PREFIX, self.island_number)
        self.init_random_seed()

        self.simulation = simulation
        self.migration_coordinator = migration_coordinator
        self.result_queue = result_queue
        if initial_population:
            self.population = initial_population

        self.var_and, self.cxpb, self.mutpb = self.init_crossover_mutation_rates()
        self.init_custom_configuration_for_island()

        self.target_hypothesis, self.target_hypothesis_energy = self.init_target_hypothesis()

        self.generation = 0
        self.migrations_done = 0
        self.new_individuals_in_generation = 0

        self._population = None
        self.elite = None

        self.stats, self.hall_of_fame = self.init_stats()
        self.logbook = self.init_logbook()
        self._non_inf_fitness = None

        self.toolbox = self.init_toolbox()

    def run(self):
        self.evaluate_population()
        self.keep_elite()
        self.hall_of_fame.update(self.population)
        self.debug_generation()

        for _ in range(ga_config.TOTAL_GENERATIONS):
            self.make_generation()
            self.generation += 1
            self.debug_generation()

            self.cxpb *= ga_config.CROSSOVER_COOLING_RATE
            self.mutpb *= ga_config.MUTATION_COOLING_RATE

        best_hypothesis = self.hall_of_fame[0]
        self.logger.info("** {} final best hypothesis: ".format(self.island_name))
        log_hypothesis(best_hypothesis, self.logger.info)
        try:
            if self.result_queue:
                self.result_queue.put((self.island_name, best_hypothesis), block=False)
        except Full:
            self.logger.error('{}: Result queue full'.format(self.island_name))

        self.logger.finalize_log()

    def make_generation(self):
        if self.generation > 0 and self.generation % ga_config.MIGRATION_INTERVAL == 0:
            self.make_migration()
        else:
            self.keep_elite()
            self.make_offspring()
            self.evaluate_population()
            self.make_selection()

    def make_migration(self):
        """
        1. Select the best <M> = <population_size> * <migration_ratio> individuals for migration
        2. Send migrants to the neighbor island
        3. Check if migrants from another island are available
        4. If yes, replace worst <M> individuals with incoming migrants (while protecting elite from being replaced)
        """
        self.logger.info('{} migrating'.format(self.island_name))
        migration_size = floor(len(self.population) * ga_config.MIGRATION_RATIO)
        migrating_individuals = self._select_best_no_repetition(self.population, migration_size)
        destination_island_num = self.get_neighbor_island_number()

        try:
            self.migration_coordinator.send_migrants(migrating_individuals, self.island_number, destination_island_num)
            self.logger.info('{} sent {} migrants to island {}'.format(self.island_name,
                                                                       len(migrating_individuals),
                                                                       destination_island_num))

        except Full:
            # Override incoming individuals for neighbor with newer ones
            self.migration_coordinator.clear_incoming_migrants(destination_island_num)
            try:
                self.migration_coordinator.send_migrants(migrating_individuals, self.island_number, destination_island_num)
            except Full:  # Clear+send is not atomic, other island may override migrants in between
                pass
            self.logger.info('{} sent {} more recent migrants to island {}'.format(self.island_name,
                                                                                   len(migrating_individuals),
                                                                                   destination_island_num))
        except:
            self.logger.exception("{} failed sending migrants".format(self.island_name))

        try:
            replacement_individuals, sender_island_num = self.migration_coordinator.get_migrants(self.island_number)
            self.migration_coordinator.clear_incoming_migrants(self.island_number)
            for individual in replacement_individuals:
                individual.invalidate_fitness()

            replaced_individuals_idxs = select_worst_idx(self.population, len(replacement_individuals))

            for i in range(len(replacement_individuals)):
                self.population[replaced_individuals_idxs[i]] = replacement_individuals[i]
            self.evaluate_population()

            self.logger.info('{} finished migration, got {} migrants from island {}'.format(self.island_name,
                                                                                            len(replacement_individuals),
                                                                                            sender_island_num))

        except Empty:
            self.logger.info('{} has no incoming migrants in queue, continuing as-is.'.format(self.island_name))

        self.migrations_done += 1

    def make_offspring(self):
        if self.var_and:
            for i in range(1, len(self.population), 2):
                if random.random() < self.cxpb:
                    self.population[i - 1], self.population[i] = self.toolbox.mate(self.population[i - 1],
                                                                                   self.population[i])

            for i in range(len(self.population)):
                if random.random() < self.mutpb:
                    self.population[i], = self.toolbox.mutate(self.population[i])
        else:  # VAR_OR
            offspring = self.varOr(self.population, self.toolbox, ga_config.LAMBDA, self.cxpb, self.mutpb)
            self.population = offspring

    def make_selection(self):
        offspring = self.toolbox.select(self.population, ga_config.ISLAND_POPULATION - len(self.elite))
        new_population = self.elite + offspring
        self.population[:] = [self.toolbox.clone(ind) for ind in new_population]

    def keep_elite(self):
        self.elite = [self.toolbox.clone(ind) for ind in
                      self._select_best_no_repetition(self.population, ga_config.ISLAND_ELITE_SIZE)]

    def evaluate_population(self):
        # Evaluate individuals with an invalidated fitness (i.e. new offspring)
        invalid_ind = [ind for ind in self.population if not ind.fitness.valid]
        self.new_individuals_in_generation = len(invalid_ind)
        energy_fitness = [self.toolbox.evaluate(ind) for ind in self.population]
        non_inf = [f[0] for f in energy_fitness if not isinf(f[0])]

        if len(non_inf) == len(self.population):  # All population is parsing all words, no need to penalize
            fitness = energy_fitness
            delta_from_feasible = 0

        else:  # Some/all individuals can't parse the data, need to set a penalty
            all_hypotheses_dont_parse_data = (len(non_inf) == 0)
            if all_hypotheses_dont_parse_data:
                delta_from_feasible = ga_config.UNPARSABLE_HYPOTHESIS_DISTANCE  # All individuals can't parse the data, set penalty very high
            else:
                max_non_inf = np.max(non_inf)  # Some individuals are good, use the worst as penalty threshold
                delta_from_feasible = max_non_inf

            population_penalized_fitness = []
            for hypothesis in self.population:
                penalized_fitness = self.evaluate_with_penalty(hypothesis, delta_from_feasible)
                population_penalized_fitness.append(penalized_fitness)

            fitness = population_penalized_fitness

        assert (len(fitness) == len(self.population))
        for ind, fit in zip(self.population, fitness):
            ind.fitness.values = fit

        return delta_from_feasible

    @staticmethod
    def varOr(population, toolbox, lambda_, cxpb, mutpb):
        """ Same as DEAP's algorithms.varOr, but without cloning each hypothesis
        (clones are made by make_crossover() and make_mutation() methods)
        """
        assert (cxpb + mutpb) <= 1.0, (
            "The sum of the crossover and mutation probabilities must be smaller "
            "or equal to 1.0.")

        offspring = []
        for _ in range(lambda_):
            op_choice = random.random()
            if op_choice < cxpb:  # Apply crossover
                ind1, ind2 = random.sample(population, 2)
                ind1, ind2 = toolbox.mate(ind1, ind2)
                offspring.append(ind1)
            elif op_choice < cxpb + mutpb:  # Apply mutation
                ind = random.choice(population)
                ind, = toolbox.mutate(ind)
                offspring.append(ind)
            else:  # Apply reproduction
                offspring.append(random.choice(population))

        return offspring

    def debug_generation(self):
        self.hall_of_fame.update(self.population)
        record = self.stats.compile(self.population) if self.stats else {}
        self.logbook.record(gen=self.generation, nevals=self.new_individuals_in_generation, **record)
        self.logger.info(self.logbook.stream)

        best_hypothesis_str = hypothesis_to_string(self.hall_of_fame[0])
        record.update({'generation': self.generation, 'best_hypothesis': best_hypothesis_str})
        self.logger.log_stats_record(record, self.island_number)

        if self.generation > 0 and self.generation % ga_config.CLEAR_RULE_SET_CACHE_INTERVAL == 0:
            RuleSet.clear_caching()

        if ga_config.DUMP_ALL_POPULATION_EVERY_N_GENERATIONS > 0 and self.generation % ga_config.DUMP_ALL_POPULATION_EVERY_N_GENERATIONS == 0 and self.generation > 0:
            self.dump_population()

        if self.generation % ga_config.HALL_OF_FAME_DEBUG_INTERVAL == 0:

            self.logger.debug(
                '\n\n**** {} top {} hypothesis:****\n'.format(self.island_name, ga_config.HALL_OF_FAME_HYPOTHESES))
            for i in range(ga_config.HALL_OF_FAME_HYPOTHESES):
                try:
                    hypo = self.hall_of_fame[i]
                    self.logger.debug('** #{} **'.format(i + 1))
                    log_hypothesis(hypo, self.logger.debug)
                    self.logger.debug('\n')
                except IndexError:
                    break

    def dump_population(self):
        self.logger.debug("\n\n**** Population dump: Generation {} ****\n".format(self.generation))
        for h, hypo in enumerate(self.population):
            self.logger.debug('Hypothesis {}\n'.format(h))
            log_hypothesis(hypo, self.logger.debug)
            self.logger.debug('\n')
        self.logger.debug("**** End population dump ****".format(self.generation))

    @property
    def population(self):
        if not self._population:
            self._population = self.generate_population(ga_config.ISLAND_POPULATION)
        return self._population

    @population.setter
    def population(self, val):
        self._population = val

    def generate_population(self, population_size):
        return [Hypothesis.get_random_hypothesis(self.simulation) for _ in range(population_size)]

    @staticmethod
    def evaluate(hypothesis):
        return hypothesis.get_energy(),

    @staticmethod
    def feasible(hypothesis):
        return not isinf(hypothesis.get_energy())

    @staticmethod
    def distance(hypothesis):
        return hypothesis.unparsed_words * ga_config.UNPARSABLE_WORD_PENALTY

    @staticmethod
    def evaluate_with_penalty(hypothesis, delta):
        energy = hypothesis.get_energy()
        if not isinf(energy):
            return energy,

        distance = GeneticAlgorithm.hypothesis_penalty(hypothesis)
        return delta + distance,

    @staticmethod
    def hypothesis_penalty(hypothesis):
        return hypothesis.unparsed_words * ga_config.UNPARSABLE_WORD_PENALTY

    def crossover(self, h1, h2):
        if GeneticAlgorithm._is_incest(h1, h2):
            return h1, h2,

        crossover_rules = False
        crossover_hmm = False
        if ga_config.CROSSOVER_BOTH_HMM_AND_RULES:
            if configurations["EVOLVE_RULES"]:
                crossover_rules = True
            if configurations["EVOLVE_HMM"]:
                crossover_hmm = True

        else:
            loci = []
            if configurations["EVOLVE_RULES"]:
                loci.append('rules')
            if configurations["EVOLVE_HMM"]:
                loci.append('hmm')
            locus = random.choice(loci)

            if locus == 'rules':
                crossover_rules = True
            elif locus == 'hmm':
                crossover_hmm = True

        offspring_1 = deepcopy(h1)
        offspring_2 = deepcopy(h2)

        if crossover_rules:
            offspring_1_rule_set, offspring_2_rule_set = RuleSet.crossover(offspring_1.grammar.rule_set,
                                                                           offspring_2.grammar.rule_set)
        else:
            offspring_1_rule_set, offspring_2_rule_set = offspring_1.grammar.rule_set, offspring_2.grammar.rule_set

        if crossover_hmm:
            offspring_1_hmm, offspring_2_hmm = HMM.crossover(offspring_1.grammar.hmm, offspring_2.grammar.hmm)
        else:
            offspring_1_hmm, offspring_2_hmm = offspring_1.grammar.hmm, offspring_2.grammar.hmm

        offspring_1.grammar = Grammar(offspring_1_hmm, offspring_1_rule_set)
        offspring_2.grammar = Grammar(offspring_2_hmm, offspring_2_rule_set)

        # Invalidate mutated offspring fitness value (i.e. mark for re-evaluation)
        offspring_1.invalidate_fitness()
        offspring_1.invalidate_energy()
        offspring_2.invalidate_fitness()
        offspring_2.invalidate_energy()

        return offspring_1, offspring_2,

    @staticmethod
    def mutate(hypothesis):
        new_hypothesis = deepcopy(hypothesis)
        success = new_hypothesis.grammar.make_mutation()
        if success:
            # Invalidate mutated offspring energy and fitness value (i.e. mark for re-evaluation)
            new_hypothesis.invalidate_energy()
            new_hypothesis.invalidate_fitness()
            return new_hypothesis,
        return hypothesis,

    def init_crossover_mutation_rates(self):
        if self.island_number < len(ga_config.CUSTOM_CXPB_MUTPB_VALUES_PER_ISLAND):
            cxpb, mutpb, var_and = ga_config.CUSTOM_CXPB_MUTPB_VALUES_PER_ISLAND[self.island_number]
        else:
            cxpb, mutpb, var_and = ga_config.DEFAULT_CXPB_MUTPB

        self.logger.info('{} VAR_AND={}, CXPB={}, MUTPB={}'.format(self.island_name, var_and, cxpb, mutpb))
        return var_and, cxpb, mutpb

    def init_custom_configuration_for_island(self):
        if self.island_number in ga_config.CUSTOM_CONFIG_PER_ISLAND:
            configurations.configurations_dict.update(ga_config.CUSTOM_CONFIG_PER_ISLAND[self.island_number])
        self.logger.info('{} Config: {}'.format(self.island_name, configurations.configurations_dict))

    @staticmethod
    def _select_best_no_repetition(individuals, k, fit_attr="fitness"):
        energies = set()
        fitness_getter = attrgetter(fit_attr)
        individuals_no_repetition = []
        for ind in individuals:
            fitness = fitness_getter(ind)
            if fitness not in energies:
                individuals_no_repetition.append(ind)
                energies.add(fitness)
        return sorted(individuals_no_repetition, key=fitness_getter, reverse=True)[:k]

    @staticmethod
    def rank_selection(individuals, k, fit_attr="fitness", selection_pressure=1.1):
        """
        :param individuals:
        :param k:
        :param fit_attr:
        :param selection_pressure: float in range [1.1, 2.0], larger SP => more selection pressure
        """

        population_size = len(individuals)
        sorted_individuals = sorted(individuals, key=attrgetter(fit_attr), reverse=True)  # best to worst, descending
        # scaled ranks in range [population_size, 1], i.e best to worst rank
        scaled_ranks = [2 - selection_pressure + (2 * (selection_pressure - 1) * (rank - 1) / (population_size - 1))
                        for rank in range(population_size, 0, -1)]

        # Roulette selection using scaled ranks
        sum_ranks = sum(scaled_ranks)
        chosen = []
        for i in range(k):
            u = random.random() * sum_ranks
            sum_ = 0
            for ind, scaled_rank in zip(sorted_individuals, scaled_ranks):
                sum_ += scaled_rank
                if sum_ > u:
                    chosen.append(ind)
                    break

        return chosen

    def init_toolbox(self):
        creator.create("EnergyFitness", base.Fitness, weights=(-1.0,))
        toolbox = base.Toolbox()
        toolbox.register("evaluate", self.evaluate)
        toolbox.register("mate", self.crossover)
        toolbox.register("mutate", self.mutate)
        if ga_config.SELECTION_METHOD == 'rank':
            toolbox.register("select", self.rank_selection, selection_pressure=ga_config.RANK_SELECTION_PRESSURE)
        elif ga_config.SELECTION_METHOD == 'tournament':
            toolbox.register("select", tools.selTournament, tournsize=ga_config.TOURNAMENT_SIZE)
        else:
            raise ValueError("Unknown selection method {}".format(ga_config.SELECTION_METHOD))

        def list_map(func, iterable):
            return list(map(func, iterable))

        toolbox.register("map", list_map)
        toolbox.register("clone", deepcopy)

        return toolbox

    def init_stats(self):
        meta_stats = tools.Statistics()
        meta_stats.register("proc", lambda _: self.island_name)

        fitness_stats = tools.Statistics(key=lambda ind: ind.fitness.values)
        fitness_stats.register("avg", np.mean)
        # fitness_stats.register("avg_non_inf", self.avg_non_inf)
        fitness_stats.register("std", np.std)
        # fitness_stats.register("std_non_inf", self.std_non_inf)
        fitness_stats.register("min", np.min)
        # fitness_stats.register("max_non_inf", self.max_non_inf)
        # fitness_stats.register("%_non_inf", self.percent_non_inf)
        fitness_stats.register("max", np.max)
        fitness_stats.register("dist", self.distance_from_target_energy)
        # fitness_stats.register("unique_%", self.unique_percentage_by_fitness)

        hypotheses_stats = tools.Statistics()
        hypotheses_stats.register("rule_avg", self.avg_num_of_rules)
        # hypotheses_stats.register("unique_%_h", self.unique_percentage_by_hypothesis)
        hypotheses_stats.register("rule_max", self.max_num_of_rules)
        hypotheses_stats.register("state_avg", self.avg_num_of_inner_states)
        hypotheses_stats.register("state_max", self.max_num_of_inner_states)
        # hypotheses_stats.register("avg_trns_stts", self.avg_num_states_in_transducer)

        stats = tools.MultiStatistics(a_meta=meta_stats, c_hypotheses=hypotheses_stats, b_fitness=fitness_stats)

        hall_of_fame = tools.HallOfFame(ga_config.HALL_OF_FAME_HYPOTHESES)

        return stats, hall_of_fame

    def init_random_seed(self):
        seed = 10000 + self.island_number
        random.seed(seed)
        np.random.seed(seed)
        self.logger.info('Process {} random seed: {}'.format(self.island_name, seed))

    def init_logbook(self):
        logbook = tools.Logbook()
        logbook.header = ['gen', 'nevals'] + (self.stats.fields if self.stats else [])
        return logbook

    def init_target_hypothesis(self):
        target_tuple = self.simulation.target_tuple
        target_rule_set = RuleSet.load_form_flat_list(target_tuple[1])
        target_hypothesis = Hypothesis.create_hypothesis(HMM(deepcopy(target_tuple[0])), target_rule_set)
        target_energy = target_hypothesis.get_energy()
        self.logger.info('Target hypothesis:')
        log_hypothesis(target_hypothesis, self.logger.info)
        self.logger.info('Target energy: {}'.format(target_energy))
        self.logger.info(
            'Target hypothesis energy signature: {}'.format(target_hypothesis.get_recent_energy_signature()))
        return target_hypothesis, target_energy

    # ##########
    # Statistics
    # ##########

    def distance_from_target_energy(self, fitness):
        min_ = np.min(fitness)
        return min_ - self.target_hypothesis_energy

    @staticmethod
    def unique_percentage_by_fitness(fitness):
        return len(np.unique(fitness)) / len(fitness)

    @staticmethod
    def unique_percentage_by_hypothesis(hypotheses):
        unique = list(set([str(h) for h in hypotheses]))
        return len(unique) / len(hypotheses)

    @staticmethod
    def avg_num_of_rules(hypotheses):
        return np.average([len(h.grammar.rule_set.rules) for h in hypotheses])

    def avg_non_inf(self, fitness):
        return np.average(self.get_non_inf_fitnesses(fitness))

    def max_non_inf(self, fitness):
        return np.max(self.get_non_inf_fitnesses(fitness))

    def std_non_inf(self, fitness):
        return np.std(self.get_non_inf_fitnesses(fitness))

    def percent_non_inf(self, fitness):
        non_inf = self.get_non_inf_fitnesses(fitness)
        if isinf(non_inf[0]):
            return 0
        else:
            r = len(non_inf) / len(fitness)
            return r

    @staticmethod
    def max_num_of_rules(hypotheses):
        return np.max([len(h.grammar.rule_set.rules) for h in hypotheses])

    @staticmethod
    def avg_num_of_inner_states(hypotheses):
        return np.average([len(h.grammar.hmm.inner_states) for h in hypotheses])

    @staticmethod
    def max_num_of_inner_states(hypotheses):
        return np.max([len(h.grammar.hmm.inner_states) for h in hypotheses])

    @staticmethod
    def avg_num_states_in_transducer(hypotheses):
        return np.average([len(h.grammar.get_transducer()) for h in hypotheses])

    def get_non_inf_fitnesses(self, fitness):
        if not self._non_inf_fitness:
            non_inf = [f[0] for f in fitness if not isinf(f[0])]
            if len(non_inf) == 0:
                non_inf = [float("inf")]
            self._non_inf_fitness = non_inf
        return self._non_inf_fitness

    # ################
    # Helper Functions
    # ################

    def get_neighbor_island_number(self):
        if ga_config.MIGRATION_SCHEME == 'fixed':
            return self.get_neighbor_island_number_fixed()
        elif ga_config.MIGRATION_SCHEME == 'round_robin':
            return self.get_neighbor_island_number_round_robin()
        else:
            raise ValueError(ga_config.MIGRATION_SCHEME)

    def get_neighbor_island_number_fixed(self):
        return (self.island_number + 1) % self.simulation_total_islands

    def get_neighbor_island_number_round_robin(self):
        # Advance neighbour with each migration
        n = (self.island_number + self.migrations_done) % self.simulation_total_islands
        if n == self.island_number:  # Don't migrate to self
            n = (n + 1) % self.simulation_total_islands
        return n

    @staticmethod
    def _is_incest(h1, h2):
        if not ga_config.PREVENT_INCEST:
            return False

        h1_energy = h1.get_energy()
        h2_energy = h2.get_energy()

        return abs(h1_energy - h2_energy) <= ga_config.INCEST_THRESHOLD
