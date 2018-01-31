import re
import os
import json
from os.path import join, split, abspath

tests_dir_path, filename = split(abspath(__file__))
fixtures_dir_path = join(tests_dir_path, "fixtures")
dot_files_folder_path = join(tests_dir_path, "dot_files")


def write_to_dot_to_file(dotable_object, file_name):
    path, file = split(file_name)
    new_path = join(dot_files_folder_path, path)
    if not os.path.exists(new_path):
        os.makedirs(new_path)
    if hasattr(dotable_object, "dotFormat"):
        draw_string = dotable_object.dotFormat()
    else:
        draw_string = dotable_object.draw()
    try:
        open(join(dot_files_folder_path, file_name + ".dot"), "w").write(draw_string)
    except TypeError:
        open(join(dot_files_folder_path, file_name + ".dot"), "wb").write(draw_string)


def get_hypothesis_from_log_string(hypothesis_string):
    from grammar import Grammar
    from hypothesis import Hypothesis

    hmm = get_hmm_from_hypothesis_string(hypothesis_string)
    rule_set = get_rule_set_from_hypothesis_string(hypothesis_string)

    grammar = Grammar(hmm, rule_set)
    return Hypothesis(grammar)


def get_hmm_from_hypothesis_string(s):
    from hmm import HMM

    hmm_regex = re.compile(r'HMM:.+?states.*}', re.MULTILINE)

    match = hmm_regex.search(s)
    hmm_str = match.group()

    transitions = re.compile(r'transitions\s(\{.*?\}),').search(hmm_str).group(1)
    transitions = transitions.replace("'", '"')
    transitions_dict = json.loads(transitions)
    emissions = re.compile(r'emissions\s(\{.*?\})').search(hmm_str).group(1)
    emissions = emissions.replace("'", '"')
    emissions_dict = json.loads(emissions)

    hmm_dict = {}
    for state in transitions_dict:
        if state == 'q0':
            state_mapping = transitions_dict[state]
        else:
            state_mapping = (transitions_dict[state], emissions_dict[state])
        hmm_dict[state] = state_mapping

    return HMM(hmm_dict)


def get_rule_set_from_hypothesis_string(s):
    from rule import Rule
    from rule_set import RuleSet
    rule_regex = re.compile(r'Rule\((\[.*?((True)|(False)))\)')
    rules_matches = rule_regex.findall(s)
    rule_set_list = []

    for match in rules_matches:
        rule_str = match[0]
        rule_str = rule_str.replace("'", '"')
        rule_str = rule_str.replace("True", 'true')
        rule_str = rule_str.replace("False", 'false')
        rule_str = "[{}]".format(rule_str)
        rule_list = json.loads(rule_str)
        rule_obj = Rule(*rule_list)
        rule_set_list.append(rule_obj)

    return RuleSet(rule_set_list)