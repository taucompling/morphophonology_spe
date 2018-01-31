import os
import sys
import re
LOG_FOLDER = "../logging/"


os.chdir(LOG_FOLDER)

simulation_name = "abnese_"

FINAL_STRING = "********** Final Hypothesis **********"
STEP_STRING = "-"*125



class LogSegment:
    def __init__(self, log_name, tail_log_line):
        self.log_name = log_name
        self.distance_from_target_energy = float("inf")
        self.log_lines = []

        for i, line in enumerate(reversed(tail_log_line)):
            if FINAL_STRING in line or STEP_STRING in line:
                break
            else:
                i = 0
        if i:
            self.log_lines = tail_log_line[len(tail_log_line)-i-1:]
            for line in self.log_lines:
                if "Distance from target energy" in line:
                    m = re.search(r'(\): )(.*)', line)
                    self.distance_from_target_energy = float(m.group(2).replace(',',''))
        else:
            self.log_lines = ["no steps made yet"]


    def print_out(self):
        print(self.log_name)
        for line in self.log_lines:
            print(line)

def print_logs():
    find_pattern = 'find * -name "*{}*"'.format(simulation_name)
    log_names = os.popen(find_pattern).read().split()
    log_segments = []
    for log_name in log_names:
        block_lines = os.popen('tail -n 50 {}'.format(log_name)).read().split("\n")
        log_segments.append(LogSegment(log_name, block_lines))

    log_segments = sorted(log_segments, key=lambda x: x.distance_from_target_energy, reverse=True)

    for log_segment in log_segments:
        log_segment.print_out()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        simulation_name = sys.argv[1]
    print_logs()





