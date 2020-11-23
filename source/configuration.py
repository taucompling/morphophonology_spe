from io import StringIO
from copy import deepcopy


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if not args and not kwargs:  # empty call
            if cls not in cls._instances:
                cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        else:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

    def clear(cls):
        try:
            del cls._instances[cls]
        except KeyError:
            pass


class ConfigurationError(Exception):
    pass


_DEFAULT_VALUE = object()


class Configuration(metaclass=Singleton):
    def __init__(self):
        self.initial_configurations_dict = dict()
        self.configurations_dict = dict()
        self.simulation_data = list()
        self.simulation_number = None

    def reset_to_original_configurations(self):
        self.configurations_dict = deepcopy(self.initial_configurations_dict)

    def __getitem__(self, key):
        # import inspect
        # print (inspect.getframeinfo(inspect.currentframe().f_back)[2])
        if key in self.configurations_dict:
            return self.configurations_dict[key]
        else:
            raise ConfigurationError("{} not found".format(key))

    def __setitem__(self, key, value):
        self.configurations_dict[key] = value

    def get(self, key, default=_DEFAULT_VALUE):
        try:
            return self.configurations_dict[key]
        except KeyError:
            if default is _DEFAULT_VALUE:
                raise
            else:
                return default

    def load_configuration_for_simulation(self, simulation):
        self.simulation_data = sorted(simulation.data)
        self.load_configurations_from_dict(simulation.configurations_dict)

    def load_configurations_from_dict(self, configurations_dict):
        self.configurations_dict = configurations_dict
        self.initial_configurations_dict = deepcopy(self.configurations_dict)

    def __str__(self):
        values_str_io = StringIO()
        print("Configurations:", end="\n", file=values_str_io)
        for (key, value) in sorted(self.configurations_dict.items()):
            value_string = ""
            if type(value) is dict:
                for (secondary_key, secondary_value) in self.configurations_dict[key].items():
                    value_string += (len(key) + 2) * " " + "{}: {}\n".format(secondary_key,
                                                                             secondary_value)  # manual justification
                value_string = value_string.strip()
            else:
                value_string = str(value)
            print("{}: {}".format(key, value_string), end="\n", file=values_str_io)

        return values_str_io.getvalue().strip()

    def clear(self):
        self.__init__()
