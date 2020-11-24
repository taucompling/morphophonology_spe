import os

import ga_config
from collections import Counter
from multiprocessing import Process, Queue
from util import log_hypothesis
from utils.cache import Cache
from utils.logger import MultiprocessLogger as Logger
from multiprocess_coordinator import MigrationCoordinator
from genetic_algorithm import GeneticAlgorithm
from configuration import Configuration


configurations = Configuration()


class GeneticAlgorithmIslandSimulation:
    def __init__(self, simulation, total_islands, first_island_idx=0, last_island_idx=None,
                 initial_full_population=None, resume=False):
        self.logger = Logger.get_logger()
        self.simulation = simulation
        self.global_simulation_total_islands = total_islands
        self.first_island_idx = first_island_idx
        if last_island_idx is None:
            self.last_island_idx = self.first_island_idx + self.global_simulation_total_islands - 1
        else:
            self.last_island_idx = last_island_idx
        self.local_simulation_num_islands = self.last_island_idx - self.first_island_idx + 1

        self.total_generations = configurations["TOTAL_GENERATIONS"]
        self.generations_per_process = ga_config.GENERATIONS_PER_PROCESS
        self.generations_completed_per_process = Counter()

        self.initial_full_population = initial_full_population
        self.migration_coordinator = MigrationCoordinator.get_migration_coordinator(total_num_islands=self.global_simulation_total_islands)
        self.result_queue = self.get_result_queue()
        self.final_queue = []
        self.resume = resume

        self.processes = None
        self.best_energy = None
        self.best_hypothesis = None

    def run(self):
        Cache.get_cache().flush()

        if self.resume:
            self.resume_simulation()
        else:
            self.processes = self.init_processes()
            for p in self.processes:
                p.start()
                self.logger.info('Started process {}'.format(p.name))

        self.maintain_island_processes()
        self.collect_all_island_results()

        for p in self.processes:
            self.logger.info('Joining process {}'.format(p.name))
            p.join()
            p.terminate()

        return self.best_hypothesis

    def resume_simulation(self):
        """Resume a stopped simulation"""
        self.processes = []
        self.update_data_from_latest_island()
        for i in range(self.local_simulation_num_islands):
            island_idx = self.first_island_idx + i

            island_dump = self.migration_coordinator.load_island(island_idx)
            population = island_dump['population']
            last_generation = island_dump['generation']
            island_process = self.init_process(island_idx=island_idx, island_population=population,
                                               initial_generation=last_generation)
            self.processes.append(island_process)
            island_process.start()
            self.generations_completed_per_process[i] = last_generation
            self.logger.info("Resumed {} at generation {}, pid: {}".format(island_process.name,
                                                                           last_generation,
                                                                           island_process.pid))

    def update_data_from_latest_island(self):
        """Ensure data used for resumed simulation matches stopped simulation.

        Important for ILM simulations as data is overridden at the beginning of
        each generation.

        In non-ILM simulation this has no actual side effect.
        """
        island_dump = self.migration_coordinator.load_island(0)
        data = island_dump.get('data')
        if data is not None:
            self.logger.info(f'Simulation data overridden by logs, using: {data}')
            self.override_data(data)
            return True
        return False

    def override_data(self, data):
        setattr(self.simulation, 'data', data[:])
        target_hmm = {'q0': ['q1'], 'q1': (['qf'], data[:])}
        setattr(self.simulation, 'target_tuple', (target_hmm, []))
        configurations.load_configuration_for_simulation(self.simulation)

    def get_result_queue(self):
        return Queue(maxsize=self.local_simulation_num_islands)

    def init_processes(self):
        processes = []
        for island_idx in range(self.first_island_idx, self.first_island_idx + self.local_simulation_num_islands):
            if self.initial_full_population:
                island_population_slice_start_idx = island_idx * configurations["ISLAND_POPULATION"]
                island_population_slice_end_idx = (island_idx + 1) * configurations["ISLAND_POPULATION"]
                island_population = self.initial_full_population[island_population_slice_start_idx : island_population_slice_end_idx]
            else:
                island_population = None
            p = self.init_process(island_idx=island_idx, island_population=island_population, initial_generation=0)
            processes.append(p)
        return processes

    def maintain_island_processes(self):
        completed_processes = []
        while len(completed_processes) < self.local_simulation_num_islands:
            for i, process in enumerate(self.processes):
                island_idx = self.first_island_idx + i

                if i in completed_processes:
                    continue

                process.join(timeout=1)
                if self.is_process_finished(process):
                    process.terminate()

                    self.generations_completed_per_process[i] += self.generations_per_process
                    if self.generations_completed_per_process[i] >= self.total_generations:
                        completed_processes.append(i)
                        self.logger.info("Island {} completed all generations".format(island_idx))
                    else:
                        island_dump = self.migration_coordinator.load_island(island_idx)
                        population = island_dump['population']
                        last_generation = island_dump['generation']
                        new_process = self.init_process(island_idx=island_idx, island_population=population,
                                                        initial_generation=last_generation)
                        self.processes[i] = new_process
                        self.processes[i].start()
                        self.logger.info("Restarted {} at generation {}, new pid: {}".format(new_process.name,
                                                                                             last_generation,
                                                                                             new_process.pid))
                self.flush_queue()

    def flush_queue(self):
        while not self.result_queue.empty(): #self.result_queue.qsize():
            self.final_queue.append(self.result_queue.get(block=True))

    def collect_all_island_results(self):
        best_energy = float("inf")
        best_hypothesis = None
        self.flush_queue()
        self.logger.info("Looking at {}/{} results".format(len(self.final_queue),
                                                           self.local_simulation_num_islands))
        all_islands = [f'island_{i}' for i in range(self.first_island_idx, self.last_island_idx + 1)]
        for island, hypothesis in self.final_queue:
            self.logger.info('{} best hypothesis:'.format(island))
            all_islands.remove(island)
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
        if all_islands:
            self.logger.info(f'{len(all_islands)} missing: {all_islands}')

    def init_process(self, island_idx, island_population, initial_generation):
        p = Process(target=self.run_island,
                    name='{}_{}'.format(ga_config.PROCESS_NAME_PREFIX, island_idx),
                    kwargs={'simulation': self.simulation,
                            'migration_coordinator': self.migration_coordinator,
                            'result_queue': self.result_queue,
                            'initial_population': island_population,
                            'simulation_total_generations': self.total_generations,
                            'max_generations': self.generations_per_process,
                            'island_number': island_idx,
                            'initial_generation': initial_generation,
                            'simulation_total_islands': self.global_simulation_total_islands})
        p.daemon = True
        return p

    def is_process_finished(self, process):
        """ checks whether process was successfully joined (ended naturally).
        This method should simply do:
        >>> return process.exitcode is not None
        but for some reason `.exitcode` remains `None` even though process
        finishes. So `sign_of_death()` along with this method do validate
        process finished. This is really ugly, yeah.
        """
        finished_signal = f'{process.name}_finished'
        finished = os.path.exists(finished_signal)
        if finished:
            os.remove(finished_signal)
        return finished

    @staticmethod
    def run_island(simulation, migration_coordinator, result_queue, initial_population, island_number,
                   simulation_total_islands, simulation_total_generations, max_generations, initial_generation):
        genetic_algorithm = GeneticAlgorithm(simulation=simulation,
                                             migration_coordinator=migration_coordinator, result_queue=result_queue,
                                             island_number=island_number,
                                             simulation_total_islands=simulation_total_islands,
                                             max_generations=max_generations,
                                             simulation_total_generations=simulation_total_generations,
                                             initial_generation=initial_generation,
                                             initial_population=initial_population)
        try:
            genetic_algorithm.run()
        except:
            logger = Logger.get_logger()
            logger.exception("Error while running island {}".format(island_number))
        finally:
            # This should be removed. See comment in `is_finished(process)`
            GeneticAlgorithmIslandSimulation.sign_of_death(island_number)

    @staticmethod
    def sign_of_death(island_number):
        with open(f'{ga_config.PROCESS_NAME_PREFIX}_{island_number}_finished', 'w') as f:
            f.write('')
