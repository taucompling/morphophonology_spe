import ga_config
from os import makedirs
import pickle
from multiprocessing import Queue
from queue import Empty, Full
from os.path import join
from genericpath import exists
from utils.environment import get_environment_name, get_simulation_id
from utils.s3 import S3
from utils.cache import Cache
from utils.logger import MultiprocessLogger as Logger

INF = float('inf')


class MigrationCoordinator:
    def __init__(self, total_num_islands):
        self.total_num_islands = total_num_islands
        self.simulation_id = get_simulation_id()
        self.logger = Logger.get_logger()

    @classmethod
    def get_migration_coordinator(cls, *args, **kwargs):
        environment_name = get_environment_name()
        if environment_name == 'aws':
            migration_coordinator_class = AWSMigrationCoordinator
        elif environment_name == 'azure':
            raise NotImplementedError
        else:
            migration_coordinator_class = SingleMachineMigrationCoordinator

        return migration_coordinator_class(*args, **kwargs)

    def get_migrants(self, destination_island_num):
        try:
            migrants, sender_island_num = self._get_migrants(destination_island_num)
            self._set_island_best_incoming_fitness(destination_island_num, INF)
            self.clear_incoming_migrants(destination_island_num)
            return migrants, sender_island_num
        except Empty:
            self.logger.info('{} has no incoming migrants in queue, continuing as-is.'.format(destination_island_num))
            return None, None

    def send_migrants(self, migrants, sending_island_number, destination_island_number):
        best_fitness = min([migrant.fitness.values[0] for migrant in migrants])
        awaiting_best_fitness = self._get_island_best_incoming_fitness(destination_island_number)
        if best_fitness > awaiting_best_fitness:
            self.logger.info('{} tried migrating to island {}, but target has better migrants in queue: {:,.2f} vs {:,.2f}'.format(sending_island_number, destination_island_number, best_fitness, awaiting_best_fitness))
        else:
            self._set_island_best_incoming_fitness(destination_island_number, best_fitness)
            try:
                self._send_migrants(migrants, sending_island_number, destination_island_number)
                self.logger.info('{} sent {} migrants to island {}'.format(sending_island_number,
                                                                           len(migrants),
                                                                           destination_island_number))

            except Full:
                # Override incoming individuals for neighbor
                self.clear_incoming_migrants(destination_island_number)
                try:
                    self._send_migrants(migrants, sending_island_number, destination_island_number)
                except Full:  # Clear+send is not atomic, other island may override migrants in between
                    pass
                self.logger.info('{} sent {} better migrants to island {}: {:,.2f} vs {:,.2f}'.format(sending_island_number,
                                                                                            len(migrants),
                                                                                            destination_island_number,
                                                                                            best_fitness,
                                                                                            awaiting_best_fitness))
            except:
                self.logger.exception("{} failed sending migrants to {}".format(sending_island_number, destination_island_number))

    def clear_incoming_migrants(self, target_island_number):
        raise NotImplementedError

    @staticmethod
    def pack_migrants_object(migrants, sending_island_number):
        return {'migrants': migrants, 'sending_island_number': sending_island_number}

    @staticmethod
    def unpack_migration_object(migration_obj):
        return migration_obj['migrants'], migration_obj['sending_island_number']

    def dump_island(self, genetic_algorithm_instance):
        persisted_object = {
            'island_number': genetic_algorithm_instance.island_number,
            'generation': genetic_algorithm_instance.generation,
            'population': genetic_algorithm_instance.population
        }
        self._dump_island(persisted_object, genetic_algorithm_instance.island_number)

    def _dump_island(self, persisted_object, island_number):
        raise NotImplementedError

    def load_island(self, island_number):
        try:
            island_obj = self._load_island(island_number)
        except:
            self.logger.exception("Can't load island {}".format(island_number))
            island_obj = {'population': None, 'generation': 0}
        return island_obj

    def _load_island(self, island_number):
        raise NotImplementedError

    def _send_migrants(self, migrants, sending_island_number, destination_island_num):
        raise NotImplementedError

    def _get_migrants(self, destination_island_num):
        raise NotImplementedError

    def _get_island_best_incoming_fitness(self, destination_island_num):
        raise NotImplementedError

    def _set_island_best_incoming_fitness(self, destination_island_num, fitness):
        raise NotImplementedError


class AWSMigrationCoordinator(MigrationCoordinator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.migration_location = S3.join_paths(self.simulation_id, '/migrations/')

    @property
    def s3(self):
        return S3()

    def _load_island(self, island_number):
        key = self._get_island_dump_key(island_number)
        return pickle.loads(self.s3.get_file_to_bytes(key))

    def _dump_island(self, persisted_object, island_number):
        key = self._get_island_dump_key(island_number)
        self.s3.upload_object(pickle.dumps(persisted_object), key)

    def _get_migrants(self, destination_island_num):
        key = self._get_incoming_migrants_key(destination_island_num)
        try:
            pickled_migrants = self.s3.get_file_to_bytes(key)
            migration_object = pickle.loads(pickled_migrants)
            return self.unpack_migration_object(migration_object)
        except:
            raise Empty

    def _send_migrants(self, migrants, sending_island_number, destination_island_num):
        sent_object = self.pack_migrants_object(migrants, sending_island_number)
        pickled_obj = pickle.dumps(sent_object)
        key = self._get_incoming_migrants_key(destination_island_num)
        self.s3.upload_object(pickled_obj, key)

    def _get_island_best_incoming_fitness(self, destination_island_num):
        try:
            dict_pickled = self.s3.get_file_to_bytes(self._get_best_incoming_fitness_key(destination_island_num))
            dict_ = pickle.loads(dict_pickled)
            return dict_['best_incoming_fitness']
        except:
            return INF

    def _set_island_best_incoming_fitness(self, destination_island_num, fitness):
        dict_ = {'best_incoming_fitness': fitness}
        pickled_dict = pickle.dumps(dict_)
        key = self._get_best_incoming_fitness_key(destination_island_num)
        self.s3.upload_object(pickled_dict, key)

    def clear_incoming_migrants(self, target_island_number):
        key = self._get_incoming_migrants_key(target_island_number)
        self.s3.delete_file(key)

    def _get_best_incoming_fitness_key(self, island_number):
        return self._get_island_path(island_number) + 'best_incoming.obj'

    def _get_island_dump_key(self, island_number):
        return self._get_island_path(island_number) + 'island_dump.obj'

    def _get_incoming_migrants_key(self, island_number):
        return self._get_island_path(island_number) + 'incoming.obj'

    def _get_island_path(self, island_number):
        return S3.join_paths(self.migration_location, '/island_{}/'.format(island_number))


class SingleMachineMigrationCoordinator(MigrationCoordinator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cache = Cache.get_cache()

        migration_queues = []
        for _ in range(self.total_num_islands):
            migration_queues.append(Queue(maxsize=1))
        self.migration_queues = migration_queues

    def _load_island(self, island_number):
        filename = self._get_simulation_dump_filename(island_number)
        with open(filename, 'rb') as f:
            return pickle.load(f)

    def _dump_island(self, persisted_object, island_number):
        filename = self._get_simulation_dump_filename(island_number)
        with open(filename, 'wb') as f:
            pickle.dump(persisted_object, f)

    def _send_migrants(self, migrants, sending_island_number, destination_island_num):
        sent_object = self.pack_migrants_object(migrants, sending_island_number)
        self.migration_queues[destination_island_num].put(sent_object, block=False)

    def _get_migrants(self, destination_island_num):
        migration_object = self.migration_queues[destination_island_num].get(block=False)
        return self.unpack_migration_object(migration_object)

    def _get_island_best_incoming_fitness(self, destination_island_num):
        fitness = self.cache.get('island_{}_best_incoming_fitness'.format(destination_island_num), prefix=self.simulation_id)
        if fitness is None:
            fitness = INF
        return fitness

    def _set_island_best_incoming_fitness(self, destination_island_num, fitness):
        self.cache.set('island_{}_best_incoming_fitness'.format(destination_island_num), fitness, prefix=self.simulation_id)

    def _get_simulation_dump_filename(self, island_number):
        dumps_dir = './island_dumps/{}/'.format(self.simulation_id)
        if not exists(dumps_dir):
            makedirs(dumps_dir)
        file_location = join(dumps_dir, 'island_{}.pickle'.format(island_number))
        return file_location

    def clear_incoming_migrants(self, target_island_number):
        try:
            self.migration_queues[target_island_number].get(block=False)
        except Empty:
            pass
