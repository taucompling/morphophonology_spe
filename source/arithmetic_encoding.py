from gmpy import mpf  # improve precision
from configuration import Configuration
from math import log, ceil, log
from time import clock

point_only = True

configurations = Configuration()

fraction_list = [mpf(2)**(-1*i) for i in range(150)]

# def get_regular_encoding_length(nfa, parse_result):
#     result = 0
#     states_path, outputs_path = parse_result
#     for i, current_state in enumerate(states_path[:-1]):
#         length = len(nfa.probabilities[current_state])
#         result += ceil(log(length, 2))
#     return result


def get_encoding_length(nfa, parse_result):
        minval = mpf(0)
        maxval = mpf(1)
        states_path, outputs_path = parse_result
        for i, current_state in enumerate(states_path[:-1]):
            segment_terminal_state_tuple = (outputs_path[i], states_path[i+1])
            length = len(nfa.probabilities[current_state])
            index = nfa.probabilities[current_state].index(segment_terminal_state_tuple)
            prob_range = (index/length, (index+1)/length)
            delta = maxval - minval
            maxval = minval + prob_range[1] * delta
            minval = minval + prob_range[0] * delta
        return len(get_binary(minval, maxval))

def interval_from_binary_string(binary_string):
    minval = mpf(0)
    maxval = mpf(1)
    for c in binary_string:
        delta = maxval - minval
        n = mpf(c)
        maxval = minval + ((n+1)/2) * delta
        minval = minval + (n/2) * delta
    return Interval(minval, maxval)


def incremental_interval(interval, int_):
    minval = interval._start
    maxval = interval._end
    delta = maxval - minval
    n = mpf(int_)
    maxval = minval + ((n+1)/2) * delta
    minval = minval + (n/2) * delta
    return Interval(minval, maxval)



def get_binary(minval, maxval):
    assert minval != maxval
    interval_to_encode = Interval(minval, maxval)
    binary_string = ""
    binary_interval = Interval(mpf(0), mpf(1))
    while True:
        zero_option = incremental_interval(binary_interval, 0)
        one_option = incremental_interval(binary_interval, 1)

        if interval_to_encode.overlap(zero_option) and interval_to_encode.overlap(one_option):
            interval_to_encode._start = one_option._start

        if interval_to_encode.subset(one_option):
            binary_string += "1"
            binary_interval = one_option
            binary_point = one_option._start
        else:
            binary_string += "0"
            binary_interval = zero_option
            binary_point = zero_option._start

        if point_only:
            if binary_point in interval_to_encode:
                break
        else:
            if binary_interval.subset(interval_to_encode):
                break
    return binary_string


def get_binary_old(minval, maxval):
    assert minval != maxval
    interval_to_encode = Interval(minval, maxval)
    binary_string = ""

    while True:
        zero_option = interval_from_binary_string(binary_string+"0")
        one_option = interval_from_binary_string(binary_string+"1")

        if interval_to_encode.overlap(zero_option) and interval_to_encode.overlap(one_option):
            interval_to_encode._start = one_option._start

        if interval_to_encode.subset(one_option):
            binary_string += "1"
            binary_point = one_option._start
        else:
            binary_string += "0"
            binary_point = zero_option._start

        if binary_point in interval_to_encode:
            break

    return binary_string

def decode(nfa, binary_encoding):
    '''for testing'''
    output_string = ""
    binary_interval = interval_from_binary_string(binary_encoding)
    binary_point = binary_interval._start

    current_state = nfa.initial_state
    current_interval = Interval(0, 1)

    while current_state not in nfa.final_states:
        delta = current_interval._end - current_interval._start
        sorted_tuple_list_by_weight = sorted([value for value, counter in nfa.probabilities[current_state].prob_dict.items() for _ in range(counter)])
        length = len(sorted_tuple_list_by_weight)
        for i, segment_state_tuple in enumerate(sorted_tuple_list_by_weight):
            interval = Interval(current_interval._start + i/length * delta, current_interval._start + (i+1)/length * delta)
            if binary_point in interval:
                current_state = segment_state_tuple[1]
                output_string += segment_state_tuple[0]
                current_interval = interval
                break

    return output_string


def encode_message_over_alphabet(message, alphabet, log_estimate=False):
    '''for testing'''
    if not log_estimate:
        minval = mpf(0)
        maxval = mpf(1)
        length = len(alphabet)
        for char in message:
            delta = maxval - minval
            if char not in alphabet:
                raise ValueError("char in message not in alphabet")
            index = alphabet.index(char)
            prob_range = (index/length, (index+1)/length)
            maxval = minval + prob_range[1] * delta
            minval = minval + prob_range[0] * delta
        return len(get_binary(minval, maxval))
    else:
        return len(message) * -log(2, 1/len(alphabet))


def get_interval_binary_size(minval, maxval):
    delta = maxval - minval
    i = 1
    while True:
        if delta >= fraction_list[i]:
            break
        else:
            i += 1
    return i


class Interval(object):
    """
    Represents an interval.
    Defined as half-open interval [start,end), which includes the start position but not the end.
    Start and end do not have to be numeric types.
    """
    def __init__(self, start, end):
        "Construct, start must be <= end."
        if start > end:
            raise ValueError('Start (%s) must not be greater than end (%s)' % (start, end))
        self._start = mpf(start)
        self._end = mpf(end)


    start = property(fget=lambda self: self._start, doc="The interval's start")
    end = property(fget=lambda self: self._end, doc="The interval's end")


    def __str__(self):
        "As string."
        return '[%s,%s)' % (self.start, self.end)


    def __repr__(self):
        "String representation."
        return '[%s,%s)' % (self.start, self.end)



    def overlap(self, other):
        "@return: True iff self intersects other."
        if self > other:
            other, self = self, other
            #return other.end > self.start
        return self.end > other.start


    def __contains__(self, item):
        "@return: True iff item in self."
        return self.start <= item and item < self.end

    def subset(self, other):
        "@return: True iff self is subset of other."
        return self.start >= other.start and self.end <= other.end



    def __lt__(self, other):
        "Compare."
        if None == other:
            return 1
        start_cmp = self.start < other.start
        if 0 != start_cmp:
            return start_cmp
        else:
            return self.end < other.end
