import pickle
import re
import time
from datetime import timedelta
from operator import attrgetter
from random import randint

import fst

from segment_table import SegmentTable


def get_weighted_list(weighted_choices):
    """
    weighted_choices is a list of tuples
    """
    return [value for value, counter in weighted_choices for i in range(counter)]


def get_transducer_acceptor(string_):
    transducer_symbol_table = SegmentTable().transducer_symbol_table
    transducer = fst.Transducer(isyms=transducer_symbol_table, osyms=transducer_symbol_table)
    for i, char in enumerate(string_):
        transducer.add_arc(i, i + 1, char, char)
    transducer[i + 1].final = True
    return transducer


def safe_compose(transducer1, transducer2):
    transducer1.arc_sort_input()
    transducer2.arc_sort_input()
    compose_result = transducer1 >> transducer2
    compose_result.remove_epsilon()
    return compose_result


def chain_safe_compose(*transducers):
    compose_result = transducers[0]
    for transducer in transducers[1:]:
        compose_result = safe_compose(compose_result, transducer)
    return compose_result


def get_transducer_outputs(transducer, limit=float("inf")):
    transducer_symbol_table = SegmentTable().transducer_symbol_table
    outputs = list()
    counter = 0
    for path in transducer.paths():
        output = ""
        for arc in path:
            symbol = transducer_symbol_table.find(arc.olabel)
            if symbol != u"\u03b5":
                output += symbol
        outputs.append(output)
        counter += 1
        if counter > limit:
            break
    return outputs


def longer_time_string(run_time_in_seconds):
    time_delta = timedelta(seconds=run_time_in_seconds)
    timedelta_string = str(time_delta)

    m = re.search('(\d* (days|day), )?(\d*):(\d*):(\d*)', timedelta_string)
    days_string = m.group(1)
    hours = int(m.group(3))
    minutes = int(m.group(4))
    seconds = int(m.group(5))

    if days_string:
        days_string = days_string[:-2]
        return "{}, {} hours, {} minutes, {} seconds".format(days_string, hours, minutes, seconds)
    elif hours:
        return "{} hours, {} minutes, {} seconds".format(hours, minutes, seconds)
    elif minutes:
        return "{} minutes, {} seconds".format(minutes, seconds)
    else:
        return "{} seconds".format(seconds)


def get_time_string(time):
    if time > 1:
        time_string = "{0:.1f} seconds".format(time)
        if time > 60:
            time_string = longer_time_string(time)
    else:
        time *= 1000
        if time > 1:
            time_string = "{0:.0f} milliseconds".format(time)
        else:
            time *= 1000
            time_string = "{0:.0f} microseconds".format(time)

    return time_string


def select_worst_idx(population, k, fit_attr="fitness"):
    """ Same as DEAP.selection.selWorst() but returns selected indices  """
    zipped = list(zip(population, list(range(len(population)))))
    worst = sorted(zipped, key=lambda tup: attrgetter(fit_attr)(tup[0]))[:k]
    return [tup[1] for tup in worst]


def tournament_selection_with_idx(individuals, k, tournsize, avoid_first=0, fit_attr="fitness"):
    """ Same as DEAP.selection.selTournament() but returns selected indices as well

    :return: list of <k> tuples: (individual, individual_idx)
    """

    chosen = []
    for i in range(k):
        aspirants_idx = [randint(avoid_first, len(individuals) - 1) for _ in range(tournsize)]
        aspirants = [individuals[i] for i in aspirants_idx]
        zipped = zip(aspirants, aspirants_idx)
        chosen.append(max(zipped, key=lambda tup: attrgetter(fit_attr)(tup[0])))
    return chosen


def timeit_best_of_N(method):
    loop_iterations = 100
    trials = 3

    def timed(*args, **kw):
        loop_times = []

        for t in range(1, trials + 1):
            print("Starting loop #{}...".format(t))

            ts = time.time()
            for i in range(1, loop_iterations + 1):
                if i % 10 == 0:
                    print("Iteration #{}...".format(i))

                result = method(*args, **kw)

            te = time.time()
            time_ = (te - ts) / loop_iterations
            loop_times.append(time_)

            print("Finished loop #{} in time {}".format(t, get_time_string(time_)))

        best_time = min(loop_times)
        print("{} loops: best of {}: {}".format(loop_iterations, trials, get_time_string(best_time)))

        return result

    return timed


def pickle_deepcopy(obj):
    return pickle.loads(pickle.dumps(obj))


def hypothesis_to_string(hypothesis):
    log_lines = []

    def log_multiline(line):
        log_lines.append(line)

    log_lines.append("Energy:  {}".format(hypothesis.get_energy()))
    log_lines.append("Unparsed words: {}".format(hypothesis.unparsed_words))
    log_lines.append("Fitness:  {}".format(hypothesis.fitness.values[0]))
    log_lines.append("HMM:  {}".format(hypothesis.grammar.hmm))
    log_hmm(hypothesis.grammar.hmm, log_multiline)
    log_rule_set(hypothesis.grammar.rule_set, log_multiline)
    log_lines.append(hypothesis.get_recent_energy_signature())

    log_str = '\n'.join(log_lines)
    return log_str


def log_hypothesis(hypothesis, logger_func=print):
    log_lines = []

    def log_multiline(line):
        log_lines.append(line)

    log_lines.append("Energy: {}".format(hypothesis.get_energy()))
    log_lines.append("Unrepresented words: {}".format(hypothesis.unparsed_words))
    try:  # Hypothesis might not have a fitness value outside of GA context
        log_lines.append("Fitness:  {}".format(hypothesis.fitness.values[0]))
    except IndexError:
        pass
    log_lines.append("HMM: {}".format(hypothesis.grammar.hmm))
    log_hmm(hypothesis.grammar.hmm, log_multiline)
    log_rule_set(hypothesis.grammar.rule_set, log_multiline)
    log_lines.append(hypothesis.get_recent_energy_signature())

    log_str = '\n'.join(log_lines)
    logger_func(log_str)


def log_hmm(hmm, logger_func=print):
    for line in hmm.get_log_lines():
        logger_func(line)


def log_rule_set(rule_set, logger_func=print):
    for line in rule_set.get_log_lines():
        logger_func(line)
