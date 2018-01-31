from tests.my_test_case import MyTestCase
from arithmetic_encoding import encode_message_over_alphabet, get_binary, interval_from_binary_string
from gmpy import mpf
from configuration import Configuration
from random import choice
from tests.simulation_tests.simulation_test import SimulationCase, SimulationTest

configurations = Configuration()


class TestArithmeticEncoding(MyTestCase):

    def setUp(self):
        configurations["ARITHMETIC_ENCODING_ESTIMATE"] = True

    def test_(self):
        #for _ in range(1000):
        configurations["ARITHMETIC_ENCODING_ESTIMATE"] = False
        print(encode_message_over_alphabet("abc"*27, ['a', 'b', 'c']))
        #print(encode_message_over_alphabet("c"*64, ['a', 'b', 'c', 'd']))

    def test_log_estimate(self):
        string = ""
        for _ in range(50):
            string += choice(['a', 'b', 'c'])
            print(string)
            print(encode_message_over_alphabet(string, ['a', 'b', 'c']), encode_message_over_alphabet(string, ['a', 'b', 'c'], log_estimate=True))


    def test_m(self):
        fraction_list = [mpf(2)**(-1*i) for i in range(150)]


    def test_im(self):
        fraction_list = [mpf(2)**(-1*i) for i in range(150)]
        print(fraction_list[2])
        delta = mpf(2)**(-100)
        i = 1
        x = mpf(1/2)
        while True:
            x *= mpf(1/2)
            if delta >= x:
                break
            else:
                i += 1


    def test_with_small_hypothesis(self):
        hmm = {'q0': ['q1'],
            'q1': (['qf'], [u'dog', u'cat']),
              }

        simulation = SimulationCase("from_simulation1", hmm, [])
        simulation_test = SimulationTest()
        simulation_test.get_energy(simulation)

    def test_get_binary(self):
        for i in range(10):
            print_get_binary(i/10, i/10+0.1)
        # print(get_binary(0.1, 0.2))
        # print(get_binary(0.2, 0.3))
        # print(get_binary(0.3, 0.4))
        # print(get_binary(0.4, 0.5))
        # print(get_binary(0.5, 0.6))
        # print(get_binary(0.6, 0.7))
        # print(get_binary(0.7, 0.8))
        # print(get_binary(0.8, 0.9))
        # print(get_binary(0.9, 1))

        # print(get_interval_binary_size(0.1, 0.2))
        # print(get_interval_binary_size(0.2, 0.3))
        # print(get_interval_binary_size(0.3, 0.4))
        # print(get_interval_binary_size(0.4, 0.5))
        # print(get_interval_binary_size(0.5, 0.6))
        # print(get_interval_binary_size(0.6, 0.7))
        # print(get_interval_binary_size(0.7, 0.8))
        # print(get_interval_binary_size(0.8, 0.9))
        # print(get_interval_binary_size(0.9, 1))
        #
        #
        # print(get_binary(0.05, 0.1))
        # print(get_interval_binary_size(0.05, 0.10))
        #
        # print(get_binary(0.005, 0.01))
        # print(get_interval_binary_size(0.005, 0.010))
        #
        #
        # print(get_binary(0.0005, 0.001))
        # print(get_interval_binary_size(0.0005, 0.001))


def print_get_binary(minval, maxval):

    binary_string = get_binary(minval, maxval)
    print("[{},{}) {}  {}".format(minval, maxval,interval_from_binary_string(binary_string)._start ,binary_string))