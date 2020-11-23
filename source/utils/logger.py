from json import dumps, JSONEncoder
from collections import Counter
import shutil
import logging
from logging import handlers
from threading import Thread
from multiprocessing import Queue
from genericpath import exists
from os import makedirs
from os.path import split, abspath, join
import numpy as np
from configuration import Singleton
from utils.environment import get_simulation_id, get_process_number, get_environment_name
from utils.s3 import S3
import ga_config


class MultiprocessLogger(metaclass=Singleton):
    """Platform-agnostic logger, to support single machine multiprocessing or multiple
     machines communicating through cloud storage
     """

    def __init__(self):
        self.simulation_id = get_simulation_id()

    def info(self, s):
        raise NotImplementedError

    def debug(self, s):
        raise NotImplementedError

    def warning(self, s):
        raise NotImplementedError

    def error(self, s):
        raise NotImplementedError

    def exception(self, s):
        raise NotImplementedError

    def log_stats_record(self, record, island_number):
        raise NotImplementedError

    def finalize_log(self, island_num):
        """ Implement in case log file needs to be dealt with when simulation ends (e.g before instance is killed) """
        raise NotImplementedError

    @classmethod
    def get_logger(cls):
        environment_name = get_environment_name()
        if environment_name == 'aws':
            return AWSLogger()
        elif environment_name == 'azure':
            raise NotImplementedError
        else:
            return QueuedFileLogger()


class AWSLogger(MultiprocessLogger):
    def __init__(self):
        super().__init__()
        self.island_num = get_process_number()
        self.file_logger = get_file_logger()
        self.lines_in_buffer = 0
        self.island_name = get_island_name(self.island_num)

        self.s3 = S3()
        self.s3_logs_dir = S3.join_paths(self.simulation_id, '/logs')
        self.island_latest_record = {}
        self.island_records_in_buffer = Counter()
        self.log_s3_location = S3.join_paths(self.simulation_id, '/logs') + '{}.txt'.format(self.island_name)
        self.log_local_location = get_local_log_file_location()

    def info(self, s):
        self.log_and_buffer('info', s)

    def debug(self, s):
        self.log_and_buffer('debug', s)

    def warning(self, s):
        self.log_and_buffer('warning', s)

    def error(self, s):
        self.log_and_buffer('error', s)

    def exception(self, s):
        self.log_and_buffer('exception', s)

    def log_stats_record(self, record, island_number):
        """ Log specific stats record to S3
        :param record: dictionary with nested categories and parameters
                Example: {'fitness': {'avg': 1219870.0, 'std': 482.80430818293246, 'min': 1218000.0, 'max': 1220000.0, 'dist': 1197498.0}}
        :param island_number: int
        """
        self.island_latest_record[island_number] = record
        self.island_records_in_buffer[island_number] += 1
        if self.island_records_in_buffer[island_number] == ga_config.UPLOAD_ISLAND_RECORD_TO_S3_EVERY_N_GENERATIONS:
            self.upload_latest_record_to_s3(island_number)
            self.island_records_in_buffer[island_number] = 0

    def upload_latest_record_to_s3(self, island_num):
        record_json = dumps(self.island_latest_record[island_num], cls=StatsJSONEncoder)
        key = self.s3_logs_dir + '{}_latest.json'.format(get_island_name(island_num))
        try:
            self.s3.upload_string(record_json, key)
        except:
            self.exception("Error sending latest record to S3")

    def finalize_log(self, island_num):
        self.upload_latest_record_to_s3(island_num)
        # self.upload_log_to_s3()

    def log_and_buffer(self, type_, s):
        getattr(self.file_logger, type_)(s)
        self.lines_in_buffer += 1
        if self.lines_in_buffer == ga_config.UPLOAD_LOG_TO_S3_EVERY_N_LINES:
            # self.upload_log_to_s3()
            self.lines_in_buffer = 0

    def upload_log_to_s3(self):
        log_file_name = get_log_file_name()
        copied_log_location = join('/tmp/', log_file_name)
        shutil.copyfile(self.log_local_location, copied_log_location)
        self.s3.upload_file(self.log_s3_location, copied_log_location)


class QueuedFileLogger(MultiprocessLogger):
    """ Spawns a process that receives log records from other
    processes through a queue and writes them to a single log file. """

    def __init__(self):
        super().__init__()
        self.logger_queue = Queue()
        self.queue_logger = self.get_queued_logger(self.logger_queue)
        self.queue_listener_thread = LogListenerThread(self.logger_queue)
        self.queue_listener_thread.daemon = True
        self.queue_listener_thread.start()
        # self.queue_listener_process = Process(target=self.queued_logger_listener_process,
        #                                       kwargs={'queue': self.logger_queue})
        # self.queue_listener_process.daemon = True
        # self.queue_listener_process.start()

    def info(self, s):
        self.queue_logger.info(s)

    def debug(self, s):
        self.queue_logger.debug(s)

    def warning(self, s):
        self.queue_logger.warning(s)

    def error(self, s):
        self.queue_logger.error(s)

    def exception(self, s):
        self.queue_logger.exception(s)

    def log_stats_record(self, record, island_number):
        pass

    def finalize_log(self, island_num):
        # Nothing to do, file log is always written to
        pass

    @staticmethod
    def get_queued_logger(queue):
        """ Logger object that writes messages to multiprocess.Queue """
        logger = logging.getLogger('spe_logger')
        queue_handler = handlers.QueueHandler(queue)
        logger.addHandler(queue_handler)
        logger.setLevel(logging.DEBUG)
        return logger

    @staticmethod
    def queued_logger_listener_process(queue):
        """ Spawn a process that gets messages from a multiprocess queue and logs them to files """
        logger = logging.getLogger('spe_logger_listener')
        log_handlers = get_file_handlers()
        for handler in log_handlers:
            logger.addHandler(handler)

        while True:
            record = queue.get()
            logger.handle(record)


class LogListenerThread(Thread):
    def __init__(self, queue):
        super().__init__()
        self.queue = queue
        logger = logging.getLogger('spe_logger_listener')
        log_handlers = get_file_handlers()
        for handler in log_handlers:
            logger.addHandler(handler)
        self.logger = logger

    def run(self):
        while True:
            record = self.queue.get()
            self.logger.handle(record)


def get_file_logger(process_num=None):
    logger_name = 'spe_logger{}'.format('' if process_num is None else '.{}'.format(process_num))
    logger = logging.getLogger(logger_name)
    for handler in get_file_handlers(process_num):
        logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger


def get_file_handlers(process_num=None):
    file_log_formatter = logging.Formatter('%(asctime)s \t %(message)s', "%y-%m-%d %H:%M:%S")

    log_file_path = get_local_log_file_location(process_num)
    file_log_handler = logging.FileHandler(log_file_path, mode='w', encoding='utf-8')
    file_log_handler.setFormatter(file_log_formatter)
    file_log_handler.setLevel(logging.DEBUG)
    handlers = [file_log_handler]
    return handlers


def get_local_log_file_location(process_num=None):
    logging_folder = "../logs/"
    if not exists(logging_folder):
        makedirs(logging_folder)

    dirname, filename = split(abspath(__file__))
    dirname = join(dirname, '..')  # 'logger.py' is one directory down from 'source'

    log_file_name = get_log_file_name(process_num)

    log_file_path = join(dirname, logging_folder, log_file_name)
    return log_file_path


def get_log_file_name(process_num=None):
    if process_num is None:
        return '{}.txt'.format(ga_config.LOG_NAME_PREFIX)
    else:
        return '{}_{}.txt'.format(ga_config.LOG_NAME_PREFIX, process_num)


def get_island_name(island_num):
    return '{}_{}'.format(ga_config.PROCESS_NAME_PREFIX, island_num)


class StatsJSONEncoder(JSONEncoder):
    """Stats may contain numpy integers and arrays, need to convert them first """

    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(StatsJSONEncoder, self).default(obj)
