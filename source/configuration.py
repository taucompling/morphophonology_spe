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


class ConfigurationError(Exception):
    pass


class Configuration(metaclass=Singleton):
    def __init__(self):
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


class PrefixDict:
    def __init__(self, words):
        words_by_prefix = {}  # {prefix: [words with this prefix]}
        prefixes_by_word = {}  # {word: longest prefix in `words`}

        for w_1 in range(len(words)):
            for w_2 in range(len(words)):
                if w_1 == w_2:
                    continue
                word_1 = words[w_1]
                word_2 = words[w_2]
                if word_2.startswith(word_1):
                    words_by_prefix.setdefault(word_1, []).append(word_2)
                    curr_prefix = prefixes_by_word.setdefault(word_2, word_1)
                    if len(curr_prefix) < len(word_1):
                        prefixes_by_word[word_2] = word_1

        self.words_by_prefix = words_by_prefix
        self.prefixes_by_word = prefixes_by_word

    def get_prefix_for_word(self, word):
        return self.prefixes_by_word.get(word, None)

    def get_words_for_prefix(self, prefix):
        return self.words_by_prefix.get(prefix, list())
