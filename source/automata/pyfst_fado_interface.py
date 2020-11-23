
import fst
from segment_table import SegmentTable
from tests.test_util import write_to_dot_file as dot
import FAdo
import re
from FAdo.fa import NFA


def pyfst_from_dfa(dfa):
    transducer_symbol_table = SegmentTable().transducer_symbol_table
    transducer = fst.Transducer(isyms=transducer_symbol_table, osyms=transducer_symbol_table)

    dfa_state_transducer_state_dict = {i: i for i, dfa_state in enumerate(dfa.States)}
    for dfa_state1 in dfa.delta:
        for segment in dfa.delta[dfa_state1]:
            dfa_state2 = dfa.delta[dfa_state1][segment]
            transducer_state1 = dfa_state_transducer_state_dict[dfa_state1]
            transducer_state2 = dfa_state_transducer_state_dict[dfa_state2]
            transducer.add_arc(transducer_state1, transducer_state2, segment, segment)


    for dfa_final_state in dfa.Final:
        transducer_final_state = dfa_state_transducer_state_dict[dfa_final_state]
        transducer[transducer_final_state].final = True

    transducer_initial_state = dfa_state_transducer_state_dict[dfa.Initial]
    transducer[transducer_initial_state].initial = True
    return transducer


def pyfst_to_dfa(transducer, alphabet):
    transducer_symbol_table = SegmentTable().transducer_symbol_table
    nfa = NFA()
    nfa.Sigma = alphabet
    delta = dict()
    States = list()
    nfa.Initial = set()
    for state in transducer:
        m = re.match(r".*#(\w*).*", str(state))  # get sate number from the string: "<StdState #x with y arcs>"
        nfa_state1_name = m.group(1)
        States.append(nfa_state1_name)
        nfa_state1 = States.index(nfa_state1_name)
        if state.initial:
            nfa.Initial.add(nfa_state1)
        if state.final:
            nfa.Final.add(nfa_state1)

    for state in transducer:
        m = re.match(r".*#(\w*).*", str(state))
        nfa_state1_name = m.group(1)
        nfa_state1 = States.index(nfa_state1_name)
        for arc in state:
            nfa_state2 = States.index(str(arc.nextstate))
            output_symbol = transducer_symbol_table.find(arc.olabel)
            if output_symbol == u"\u03b5":
                output_symbol = FAdo.common.Epsilon
            if nfa_state1 not in delta:
                delta[nfa_state1] = dict()
            if output_symbol not in delta[nfa_state1]:
                delta[nfa_state1][output_symbol] = set()
            delta[nfa_state1][output_symbol].add(nfa_state2)


    nfa.delta = delta
    nfa.States = States

    dfa = nfa.toDFA()

    return dfa
