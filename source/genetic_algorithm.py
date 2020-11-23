import random
import numpy as np
from math import isinf, floor
from operator import attrgetter
from deap import base, creator, tools
from hmm import HMM
from grammar import Grammar
from configuration import Configuration
from rule_set import RuleSet
from hypothesis import Hypothesis
from util import log_hypothesis, hypothesis_to_string, select_worst_idx, pickle_deepcopy as deepcopy, deepcopy_keep_cached_transducers
from utils.logger import MultiprocessLogger as Logger
from utils.cache import Cache
import ga_config

configurations = Configuration()


class GeneticAlgorithm:
    def __init__(self, simulation, migration_coordinator, result_queue, island_number, simulation_total_islands,
                 max_generations, simulation_total_generations, initial_generation=0, initial_population=None):
        self.logger = Logger.get_logger()
        self.island_number = island_number
        self.simulation_total_islands = simulation_total_islands
        self.island_name = '{}_{}'.format(ga_config.PROCESS_NAME_PREFIX, self.island_number)
        self.init_random_seed()
        self.cache = Cache.get_cache()

        self.initial_generation = initial_generation
        self.generation = initial_generation
        self.max_generations = max_generations
        self.simulation_total_generations = simulation_total_generations

        self.simulation = simulation
        self.migration_coordinator = migration_coordinator
        self.result_queue = result_queue

        self._population = None
        if initial_population:
            self.population = initial_population
            self.invalidate_all_population_fitness()

        self.var_and, self.crossover_rate, self.mutation_rate = self.init_crossover_mutation_rates()

        self.target_hypothesis, self.target_hypothesis_energy = self.init_target_hypothesis()

        self.new_individuals_in_generation = 0

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
        if self.generation == 0:
            self.dump_population()

        for _ in range(self.max_generations):
            self.make_generation()
            self.generation += 1
            self.debug_generation()

            self.crossover_rate *= configurations["CROSSOVER_COOLING_RATE"]
            self.mutation_rate *= configurations["MUTATION_COOLING_RATE"]

        self.finalize_simulation()

    def finalize_simulation(self):
        self.dump_population()
        best_hypothesis = self.hall_of_fame[0]
        self.logger.info("{} best hypothesis: ".format(self.island_name))
        log_hypothesis(best_hypothesis, self.logger.info)

        if self.generation >= self.simulation_total_generations:
            if self.result_queue:
                self.result_queue.put((self.island_name, best_hypothesis), block=False)

        self.logger.finalize_log(self.island_number)

    def make_generation(self):
        if self.generation > 0 and self.generation % configurations["MIGRATION_INTERVAL"] == 0:
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
        migration_size = floor(len(self.population) * configurations["MIGRATION_RATIO"])
        migrating_individuals = self._select_best_no_repetition(self.population, migration_size)
        destination_island_num = self.get_neighbor_island_number()

        self.migration_coordinator.send_migrants(migrating_individuals, self.island_number, destination_island_num)

        replacement_individuals, sender_island_num = self.migration_coordinator.get_migrants(self.island_number)
        if replacement_individuals is not None:
            for individual in replacement_individuals:
                individual.invalidate_fitness()

            replaced_individuals_idxs = select_worst_idx(self.population, len(replacement_individuals))

            for i in range(len(replacement_individuals)):
                self.population[replaced_individuals_idxs[i]] = replacement_individuals[i]
            self.evaluate_population()

            self.logger.info('{} finished migration, got {} migrants from island {}'.format(self.island_name,
                                                                                            len(replacement_individuals),
                                                                                            sender_island_num))

    def make_offspring(self):
        if self.var_and:
            for i in range(1, len(self.population), 2):
                if random.random() < self.crossover_rate:
                    self.population[i - 1], self.population[i] = self.toolbox.mate(self.population[i - 1],
                                                                                   self.population[i])

            for i in range(len(self.population)):
                if random.random() < self.mutation_rate:
                    self.population[i], = self.toolbox.mutate(self.population[i])
        else:  # VAR_OR
            new_population_size = floor(len(self.population) / configurations["REPRODUCTION_LAMBDA"])
            offspring = self.varOr(self.population, self.toolbox, new_population_size, self.crossover_rate, self.mutation_rate)
            self.population = offspring

    def make_selection(self):
        offspring = self.toolbox.select(self.population, configurations["ISLAND_POPULATION"] - len(self.elite))
        new_population = self.elite + offspring
        self.population[:] = [deepcopy_keep_cached_transducers(ind) for ind in new_population]

    def keep_elite(self):
        elite_size = floor(configurations["ISLAND_ELITE_RATIO"] * configurations["ISLAND_POPULATION"])
        self.elite = [self.toolbox.clone(ind) for ind in self._select_best_no_repetition(self.population, elite_size)]

    def evaluate_population(self):
        # Evaluate individuals with an invalidated fitness (i.e. new offspring)
        invalid_individuals = [ind for ind in self.population if not ind.fitness.valid]
        self.new_individuals_in_generation = len(invalid_individuals)

        energy_fitness = []
        for hypothesis in self.population:
            hypothesis_repr = repr(hypothesis)
            cached_energy = self.cache.get(hypothesis_repr)
            if cached_energy is not None:
                hypothesis_energy = cached_energy
                hypothesis.set_energy(hypothesis_energy[0])
            else:
                hypothesis_energy = self.toolbox.evaluate(hypothesis)
                self.cache.set(hypothesis_repr, hypothesis_energy)
            energy_fitness.append(hypothesis_energy)
        non_inf_fitness = [f[0] for f in energy_fitness if not isinf(f[0])]

        if len(non_inf_fitness) == len(self.population):  # All population is parsing all words, no need to penalize
            final_fitness = energy_fitness
            delta_from_feasible = 0

        else:  # Some/all individuals can't parse the data, need to set a penalty
            all_population_cant_parse_data = (len(non_inf_fitness) == 0)
            if all_population_cant_parse_data:
                delta_from_feasible = ga_config.UNPARSABLE_HYPOTHESIS_DISTANCE  # All individuals can't parse the data, set penalty very high
            else:
                max_non_inf = np.max(non_inf_fitness)  # Some individuals are good, use the worst as penalty threshold
                delta_from_feasible = max_non_inf

            population_penalized_fitness = []
            for hypothesis in self.population:
                penalized_fitness = self.evaluate_with_penalty(hypothesis, delta_from_feasible)
                population_penalized_fitness.append(penalized_fitness)

            final_fitness = population_penalized_fitness

        for ind, fit in zip(self.population, final_fitness):
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

        if self.generation != self.initial_generation and self.generation % ga_config.DUMP_POPULATION_INTERVAL == 0:
            self.dump_population()

        if self.generation > 0 and self.generation % ga_config.CLEAR_KEY_VALUE_CACHE_INTERVAL == 0:
            self.cache.flush()

        if self.generation > 0 and self.generation % ga_config.CLEAR_TRANSDUCERS_CACHE_INTERVAL == 0:
            from bracket_rule_transducer import BracketRuleTransducer
            self.logger.info("Clearing rule set cache...")
            RuleSet.clear_caching()
            self.logger.info("Clearing bracket rule transducers cache...")
            BracketRuleTransducer.clear_caching()

        if ga_config.LOG_POPULATION_INTERVAL > 0 and self.generation % ga_config.LOG_POPULATION_INTERVAL == 0 and self.generation > 0:
            self.log_all_population()

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

    def log_all_population(self):
        self.logger.debug("\n\n**** Population dump: Generation {} ****\n".format(self.generation))
        for h, hypo in enumerate(self.population):
            self.logger.debug('Hypothesis {}\n'.format(h))
            log_hypothesis(hypo, self.logger.debug)
            self.logger.debug('\n')
        self.logger.debug("**** End population dump ****".format(self.generation))

    def dump_population(self):
        if self.migration_coordinator:
            self.logger.info("Dumping {} to disk...".format(self.island_name))
            self.migration_coordinator.dump_island(self)
            self.logger.info("Finished dumping {} to disk.".format(self.island_name))

    @property
    def population(self):
        if not self._population:
            self._population = self.generate_population(configurations["ISLAND_POPULATION"])
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
        new_hypothesis = deepcopy_keep_cached_transducers(hypothesis)
        mutataion_successful = new_hypothesis.grammar.make_mutation()
        if mutataion_successful:
            # Invalidate mutated offspring energy and fitness value (i.e. mark for re-evaluation)
            new_hypothesis.invalidate_energy()
            new_hypothesis.invalidate_fitness()
            return new_hypothesis,
        return hypothesis,

    def init_crossover_mutation_rates(self):
        crossover_rate = configurations["CROSSOVER_RATE"]
        mutation_rate = configurations["MUTATION_RATE"]
        var_and = configurations["VAR_AND"]

        self.logger.info('{} VAR_AND={}, CXPB={}, MUTPB={}'.format(self.island_name, var_and, crossover_rate, mutation_rate))
        return var_and, crossover_rate, mutation_rate

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
        :param selection_pressure: float in range [1.1, 2.0], larger value => higher selection pressure
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

    def invalidate_all_population_fitness(self):
        for hypothesis in self.population:
            hypothesis.invalidate_fitness()
            hypothesis.invalidate_energy()

    def init_toolbox(self):
        creator.create("EnergyFitness", base.Fitness, weights=(-1.0,))
        toolbox = base.Toolbox()
        toolbox.register("evaluate", self.evaluate)
        toolbox.register("mate", self.crossover)
        toolbox.register("mutate", self.mutate)
        toolbox.register("clone", deepcopy)

        if configurations["SELECTION_METHOD"] == 'rank':
            toolbox.register("select", self.rank_selection, selection_pressure=configurations["RANK_SELECTION_PRESSURE"])
        elif configurations["SELECTION_METHOD"] == 'tournament':
            toolbox.register("select", tools.selTournament, tournsize=configurations["TOURNAMENT_SIZE"])
        else:
            raise ValueError("Unknown selection method {}".format(configurations["SELECTION_METHOD"]))

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
        # hypotheses_stats.register("avg_hyp_sz", self.avg_hypothesis_size_bytes)

        stats = tools.MultiStatistics(a_meta=meta_stats, c_hypotheses=hypotheses_stats, b_fitness=fitness_stats)

        hall_of_fame = tools.HallOfFame(ga_config.HALL_OF_FAME_HYPOTHESES)

        return stats, hall_of_fame

    def init_random_seed(self):
        seed = ga_config.RANDOM_SEED_RANGE_START + self.island_number
        random.seed(seed)
        np.random.seed(seed)
        self.logger.info('Process {} random seed: {}'.format(self.island_name, seed))

    def init_logbook(self):
        logbook = tools.Logbook()
        logbook.header = ['gen', 'nevals'] + (self.stats.fields if self.stats else [])
        return logbook

    def init_target_hypothesis(self):
        target_tuple = self.simulation.target_tuple
        target_rule_set = RuleSet.load_from_flat_list(target_tuple[1])
        target_hypothesis = Hypothesis.create_hypothesis(HMM(deepcopy(target_tuple[0])), target_rule_set)
        target_energy = target_hypothesis.get_energy()
        if self.generation == 0:
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
        unique = list(set([repr(h) for h in hypotheses]))
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

    @staticmethod
    def avg_hypothesis_size_bytes(hypotheses):
        from sys import getsizeof
        return np.average([getsizeof(h) for h in hypotheses])

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
        if configurations["MIGRATION_SCHEME"] == 'fixed':
            return self.get_neighbor_island_number_fixed()
        elif configurations["MIGRATION_SCHEME"] == 'round_robin':
            return self.get_neighbor_island_number_round_robin()
        else:
            raise ValueError(f"Unknown migration scheme: {configurations['MIGRATION_SCHEME']}")

    def get_neighbor_island_number_fixed(self):
        return (self.island_number + 1) % self.simulation_total_islands

    def get_neighbor_island_number_round_robin(self):
        num_migrations_done = self.generation // configurations["MIGRATION_INTERVAL"]
        destination = (self.island_number + num_migrations_done) % self.simulation_total_islands
        if destination == self.island_number:
            destination = (destination + 1) % self.simulation_total_islands
        return destination