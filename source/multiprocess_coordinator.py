import ga_config
import pickle
from multiprocessing import Queue
from queue import Empty, Full
from utils.environment import get_environment_name, get_simulation_id
from utils.s3 import S3


class MigrationCoordinator:
    """ Base class for coordinating migrations while being platform agnostic,
    i.e whether working on single machine, AWS or Azure """

    def __init__(self):
        pass

    @classmethod
    def get_migration_coordinator(cls):
        environment_name = get_environment_name()
        if environment_name == 'aws':
            return S3MigrationCoordinator()
        elif environment_name == 'azure':
            raise NotImplementedError
        else:
            return SingleMachineMigrationCoordinator()

    def get_migrants(self, receiving_island_number):
        raise NotImplementedError

    def send_migrants(self, migrants, sending_island_number, receiving_island_number):
        raise NotImplementedError

    def clear_incoming_migrants(self, target_island_number):
        raise NotImplementedError

    @staticmethod
    def pack_migrants_object(migrants, sending_island_number):
        return {'migrants': migrants, 'sending_island_number': sending_island_number}

    @staticmethod
    def unpack_migration_object(migration_obj):
        return migration_obj['migrants'], migration_obj['sending_island_number']


class S3MigrationCoordinator(MigrationCoordinator):
    def __init__(self):
        super().__init__()
        self.s3 = S3()
        self.simulation_id = get_simulation_id()
        self.migration_location = S3.join_paths(self.simulation_id, '/migrations/')
        # self.clean_previous_simulations()

    def get_migrants(self, receiving_island_number):
        key = self._get_incoming_migrants_key(receiving_island_number)
        try:
            pickled_migrants = self.s3.get_file_to_bytes(key)
            migration_object = pickle.loads(pickled_migrants)
            return self.unpack_migration_object(migration_object)
        except:
            raise Empty

    def send_migrants(self, migrants, sending_island_number, receiving_island_number):
        sent_object = self.pack_migrants_object(migrants, sending_island_number)
        pickled_obj = pickle.dumps(sent_object)
        key = self._get_incoming_migrants_key(receiving_island_number)
        if self.s3.file_exists(key):
            raise Full
        self.s3.upload_object(pickled_obj, key)

    def clear_incoming_migrants(self, target_island_number):
        key = self._get_incoming_migrants_key(target_island_number)
        self.s3.delete_file(key)

    def clean_previous_simulations(self):
        self.s3.delete_file(self.migration_location)

    def _get_incoming_migrants_key(self, island_number):
        return S3.join_paths(self.migration_location, '/island_{}/'.format(island_number)) + 'incoming.obj'


class SingleMachineMigrationCoordinator(MigrationCoordinator):
    def __init__(self):
        super().__init__()

        migration_queues = []
        for _ in range(ga_config.NUM_ISLANDS):
            migration_queues.append(Queue(maxsize=1))
        self.migration_queues = migration_queues

    def send_migrants(self, migrants, sending_island_number, receiving_island_number):
        sent_object = self.pack_migrants_object(migrants, sending_island_number)
        self.migration_queues[receiving_island_number].put(sent_object, block=False)

    def get_migrants(self, receiving_island_number):
        migration_object = self.migration_queues[receiving_island_number].get(block=False)
        return self.unpack_migration_object(migration_object)

    def clear_incoming_migrants(self, target_island_number):
        try:
            self.migration_queues[target_island_number].get(block=False)
        except Empty:
            pass
