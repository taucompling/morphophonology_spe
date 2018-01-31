from os import getenv
from multiprocessing import current_process


def get_simulation_name():
    return get_mandatory_envar('SPE_SIMULATION_NAME')


def get_simulation_id():
    return get_mandatory_envar('SPE_SIMULATION_ID')


def get_mandatory_envar(var_name):
    val = getenv(var_name, None)
    if val is None:
        raise ValueError('Must set "{}" environment variable'.format(var_name))
    return val


def get_environment_name():
    return getenv("SPE_ENVIRONMENT_NAME", '').lower()


def get_process_number():
    process_name = current_process().name
    process_name_split = process_name.split('_')
    process_number = int(process_name_split[1] if len(process_name_split) > 1 else '0')
    return process_number
