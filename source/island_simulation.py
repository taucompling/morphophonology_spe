import ga_config
from multiprocessing import Process, Queue
from queue import Empty
from util import log_hypothesis
from utils.logger import MultiprocessLogger as Logger
from multiprocess_coordinator import MigrationCoordinator
from genetic_algorithm import GeneticAlgorithm


class GeneticAlgorithmIslandSimulation:
    """ Centralized process to orchestrate multiple-island GA simulations """

    def __init__(self, simulation, total_islands, first_island_idx=0, last_island_idx=None,
                 initial_full_population=None):
        self.logger = Logger.get_logger()
        self.simulation = simulation
        self.simulation_total_islands = total_islands
        self.first_island_idx = first_island_idx
        if last_island_idx is None:
            self.last_island_idx = self.first_island_idx + self.simulation_total_islands - 1
        else:
            self.last_island_idx = last_island_idx
        self.local_simulation_num_islands = self.last_island_idx - self.first_island_idx + 1
        self.initial_full_population = initial_full_population
        self.migration_coordinator = MigrationCoordinator.get_migration_coordinator()
        self.result_queue = self.get_result_queue()
        self.processes = self.init_processes()
        self.best_energy = None
        self.best_hypothesis = None

    def run(self):
        for p in self.processes:
            p.start()
            self.logger.info('Started process {}'.format(p.name))

        self.collect_all_island_results()

        for p in self.processes:
            self.logger.info('Joining process {}'.format(p.name))
            p.join()
            p.terminate()

        return self.best_hypothesis

    def get_result_queue(self):
        return Queue(maxsize=self.local_simulation_num_islands)

    def init_processes(self):
        processes = []
        for island_idx in range(self.first_island_idx, self.first_island_idx + self.local_simulation_num_islands):
            if self.initial_full_population:
                island_population = self.initial_full_population[
                                    island_idx * ga_config.ISLAND_POPULATION: (
                                                                                  island_idx + 1) * ga_config.ISLAND_POPULATION]
            else:
                island_population = None

            p = Process(target=self.run_island,
                        name='{}_{}'.format(ga_config.PROCESS_NAME_PREFIX, island_idx),
                        kwargs={'simulation': self.simulation, 'migration_coordinator': self.migration_coordinator, 'result_queue': self.result_queue,
                                'initial_population': island_population,
                                'island_number': island_idx, 'simulation_total_islands': self.simulation_total_islands})
            p.daemon = True
            processes.append(p)
        return processes

    def collect_all_island_results(self):
        best_energy = float("inf")
        best_hypothesis = None
        for _ in range(self.local_simulation_num_islands):
            island, hypothesis = self.result_queue.get(block=True)
            self.logger.info('{} best hypothesis:'.format(island))
            log_hypothesis(hypothesis, self.logger.info)

            energy = hypothesis.get_energy()
            if energy < best_energy:
                best_energy = energy
                best_hypothesis = hypothesis

        self.best_energy = best_energy
        self.best_hypothesis = best_hypothesis
        if self.best_hypothesis:
            self.logger.info('*Best hypothesis from all islands:*')
            log_hypothesis(self.best_hypothesis, self.logger.info)

    @staticmethod
    def run_island(simulation, migration_coordinator, result_queue, initial_population, island_number, simulation_total_islands):
        genetic_algorithm = GeneticAlgorithm(simulation=simulation,
                                             migration_coordinator=migration_coordinator, result_queue=result_queue,
                                             island_number=island_number,
                                             simulation_total_islands=simulation_total_islands,
                                             initial_population=initial_population)
        try:
            genetic_algorithm.run()
        except Exception as e:
            logger = Logger.get_logger()
            from traceback import format_exc
            logger.error(format_exc())
            logger.error(str(e))
