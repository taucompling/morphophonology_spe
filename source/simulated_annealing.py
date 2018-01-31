from math import exp, isinf
import random
import logging
from datetime import timedelta
import time
import re
from collections import deque
import platform
from configuration import Configuration

from rule_set import RuleSet


logger = logging.getLogger(__name__)
configurations = Configuration()



class SimulatedAnnealing(object):

    def __init__(self, hypothesis, target_energy):
        self.current_hypothesis = hypothesis
        self.step = 0
        self.current_temperature = configurations["INITIAL_TEMPERATURE"]
        self.current_hypothesis_energy = None
        self.neighbor_hypothesis = None
        self.neighbor_hypothesis_energy = None
        self.target_energy = target_energy
        self.interval_hypothesis_energies = None
        self.threshold = configurations["THRESHOLD"]
        self.steps_limitation = configurations["STEPS_LIMITATION"]
        self.linear_decay = configurations["LINEAR_DECAY"]
        self.cooling_rate = configurations["COOLING_RATE"]
        self.debug_logging_interval = configurations["DEBUG_LOGGING_INTERVAL"]
        self.clear_modules_caching_interval = configurations["CLEAR_MODULES_CACHING_INTERVAL"]
        if self.linear_decay:
            self.linear_cooling_rate = self._calculate_linear_decay()

    def run(self):
        self.current_hypothesis_energy = self.current_hypothesis.get_energy()
        self.before_loop()

        while (self.current_temperature > self.threshold) and \
              (self.step != self.steps_limitation):
                self.make_step()

        self._after_loop()

    def make_step(self):
        self.step += 1
        if not self.linear_decay:
            self.current_temperature *= self.cooling_rate
        else:
            self.current_temperature -= self.linear_cooling_rate

        self._check_for_intervals()

        mutation_result, neighbor_hypothesis = self.current_hypothesis.get_neighbor()
        if not mutation_result:
            return  # mutation failed - the neighbor hypothesis is the same as current hypothesis

        self.neighbor_hypothesis = neighbor_hypothesis
        self.neighbor_hypothesis_energy = self.neighbor_hypothesis.get_energy()
        delta = self.neighbor_hypothesis_energy - self.current_hypothesis_energy

        if isinf(self.neighbor_hypothesis_energy):
            return  # the neighbor hypothesis does not describe the data

        if delta < 0:
            p = 1
        else:
            p = exp(-delta / self.current_temperature)

        if random.random() < p:
            self.current_hypothesis = self.neighbor_hypothesis
            self.current_hypothesis_energy = self.neighbor_hypothesis_energy
        else:
            pass

    def _check_for_intervals(self):
        if not self.step % self.debug_logging_interval:
            self._debug_interval()
            self._check_for_stalemate()
        if not self.step % self.clear_modules_caching_interval:
            self._clear_modules_caching()


    def _clear_modules_caching(self):
        from bracket_rule_transducer import BracketRuleTransducer
        BracketRuleTransducer.clear_caching()
        RuleSet.clear_caching()


    def _check_for_stalemate(self):
        if not configurations["CHECK_STALEMATE"]:
            return

        #10% percent of the simulation
        if not self.interval_hypothesis_energies:
            self.maxlen = int(int(self.number_of_expected_steps * 0.1)/self.debug_logging_interval)
            self.interval_hypothesis_energies = deque(maxlen=self.maxlen)
            self.interval_hypothesis_energies.append("dummy_value")  # in order to prevent ==1 in first iteration
        else:
            self.interval_hypothesis_energies.append(self.current_hypothesis_energy)
            if len(set(self.interval_hypothesis_energies)) == 1:
                logger.info("same energy for 10% of simulation ({} steps), stopping it".format(self.maxlen*self.debug_logging_interval))
                self.current_temperature = self.threshold

    def before_loop(self):
        self.start_time = time.time()
        self.previous_interval_time = self.start_time
        logger.info(configurations)
        if self.steps_limitation != float("inf"):
            self.number_of_expected_steps = self.steps_limitation
        else:
            self.number_of_expected_steps = self._calculate_num_of_steps()

        logger.info("Number of expected steps is: {:,}".format(self.number_of_expected_steps))
        self.current_hypothesis_energy = self.current_hypothesis.get_energy()
        if isinf(self.current_hypothesis_energy):
            raise ValueError("first hypothesis energy can not be INF")
        logger.info("data: {}".format(self.current_hypothesis.data))
        if self.target_energy:
            logger.info("Target energy: {:,}".format(self.target_energy))
        self._log_hypothesis_state()

        self.previous_interval_energy = self.current_hypothesis_energy

    def _after_loop(self):
        current_time = time.time()
        logger.info("*"*10 +" Final Hypothesis " + "*"*10)
        self._log_hypothesis_state()
        msg = "simulated annealing runtime was: {}".format(_pretty_runtime_str(current_time - self.start_time))
        logger.info(msg)


    def _debug_interval(self):
            current_time = time.time()
            logger.info("\n"+"-"*125)
            percentage_completed = 100 * float(self.step)/float(self.number_of_expected_steps)
            logger.info("Step {0:,} of {1:,} ({2:.2f}%)".format(self.step, self.number_of_expected_steps,
                                                                percentage_completed))
            logger.info("-" * 80)
            elapsed_time = current_time - self.start_time
            logger.info("Time from simulation start: {}".format(_pretty_runtime_str(elapsed_time)))
            crude_expected_time = elapsed_time * (100/percentage_completed)
            logger.info("Expected simulation time: {} ".format(_pretty_runtime_str(crude_expected_time)))
            logger.info("Current temperature: {}".format(self.current_temperature))
            self._log_hypothesis_state()
            logger.info("Energy difference from last interval: {}".format(self.current_hypothesis_energy - self.previous_interval_energy))
            self.previous_interval_energy = self.current_hypothesis_energy
            time_from_last_interval = current_time - self.previous_interval_time
            logger.info("Time from last interval: {}".format(_pretty_runtime_str(time_from_last_interval)))
            logger.info("Time to finish based on current interval: {}".format(self.estimate_by_interval_time(time_from_last_interval)))
            self.previous_interval_time = current_time

    def estimate_by_interval_time(self, time_from_last_interval):
        number_of_remaining_steps = self.number_of_expected_steps - self.step
        number_of_remaining_intervals = int(number_of_remaining_steps/self.debug_logging_interval)
        expected_time = number_of_remaining_intervals * time_from_last_interval
        return _pretty_runtime_str(expected_time)

    def _log_hypothesis_state(self):
        logger.info("HMM:  {}".format(self.current_hypothesis.grammar.hmm))
        for line in self.current_hypothesis.grammar.hmm.get_log_lines():
            logger.info(line)
        #logger.info("Rule Set: {}".format(self.current_hypothesis.grammar.rule_set))
        for line in self.current_hypothesis.grammar.rule_set.get_log_lines():
            logger.info(line)
        logger.info(self.current_hypothesis.get_recent_energy_signature())
        # if configurations["PRINT_PARSE"]:
        #     logger.info("Parse: {}".format(self._get_parsing_results()))
        if self.target_energy:
            energy_delta = self.current_hypothesis.energy - self.target_energy
            logger.info("Distance from target energy({:,}): {:,}".format(self.target_energy, energy_delta))

    def _get_parsing_results(self):
        rule_set = self.current_hypothesis.grammar.rule_set
        if not rule_set.is_safe_to_print_parse():
            return "Parse too complicated to print"
        parsing_results = []
        hmm = self.current_hypothesis.grammar.hmm
        data = self.current_hypothesis.data
        for emission in sorted(hmm.get_all_emissions()):
            outpus_in_data = []
            other_outputs = []
            if configurations["MORPHEME_BOUNDARY_FLAG"]:
                outputs = rule_set.get_outputs_of_word(emission + "B")
            else:
                outputs = rule_set.get_outputs_of_word(emission)
            for output in outputs:
                if configurations["MORPHEME_BOUNDARY_FLAG"]:
                    output = output[:-1]  # remove last "#"
                if output in data:
                    outpus_in_data.append(output)
                else:
                    other_outputs.append(output)
            if outpus_in_data == [emission] and not other_outputs:
                continue
            else:
                if other_outputs:
                    parsing_result = "{}->{} ({})".format(emission, outpus_in_data, other_outputs)
                else:
                    parsing_result = "{}->{}".format(emission, outpus_in_data)
            parsing_results.append(parsing_result)
        return ", ".join(parsing_results)

    @staticmethod
    def _calculate_num_of_steps():
        cooling_rate = configurations["COOLING_RATE"]
        threshold = configurations["THRESHOLD"]
        num_of_steps = 0
        temp = configurations["INITIAL_TEMPERATURE"]
        while temp > threshold:
            num_of_steps += 1
            temp *= cooling_rate
        return num_of_steps

    @staticmethod
    def _calculate_linear_decay():
        num_of_steps = SimulatedAnnealing._calculate_num_of_steps()
        return (configurations["INITIAL_TEMPERATURE"]-configurations["THRESHOLD"])/num_of_steps

def _pretty_runtime_str(run_time_in_seconds):
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
