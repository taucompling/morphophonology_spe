from simulation_test import SimulationTest, SimulationCase
from configuration import Configuration

configurations = Configuration()

class FrenchDeletion(SimulationTest):
    def setUp(self):
        self.initialise_segment_table("french_deletion_with_h_segment_table.txt")
        self.data = ['tab', 'tabl', 'lib', 'libl', 'tap', 'tapl', 'rid', 'ridl', 'parl', 'birl', 'tpal', 'tbir', 'rdahl', 'tahl']
        configurations["DATA_ENCODING_LENGTH_MULTIPLIER"] = 50
        configurations["HMM_ENCODING_LENGTH_MULTIPLIER"] = 20


    def test_(self):
        self.target_energy = None
        hmm = {'q0': ['q1'],
            'q1': (['qf'], ['tabl', 'libl', 'tapl', 'ridl', 'parl', 'birl', 'tpal', 'tbir', 'rdahl', 'tahl']),
              }

        rule = [[{"liquid": "+"}], [], [{"cons": "+", "son": "-"}], [], False]
        target = SimulationCase("target", hmm, [rule])
        self.target_energy = self.get_energy(target)

        hmm = {'q0': ['q1'],
            'q1': (['qf'], self.data[:]),
              }
        initial = SimulationCase("initial", hmm, [])
        self.get_energy(initial)


        hmm = {'q0': ['q1'],
            'q1': (['qf'], ['tabl', 'libl', 'tapl', 'ridl', 'parl', 'birl', 'tpal', 'tbir', 'rdahl', 'tahl']),
              }
        rule = [[{"liquid": "+"}], [], [{"cons": "+"}], [], False]
        without_son = SimulationCase("without_son", hmm, [rule])
        self.get_energy(without_son)


        hmm = {'q0': ['q1'],
            'q1': (['qf'], ['tabl', 'labl', 'tapl', 'radl', 'parl', 'birl', 'tpal', 'tbar']),
              }
        rule = [[{"liquid": "+"}], [], [{"stop": "+"}], [], False]
        with_stop = SimulationCase("with_stop", hmm, [rule])
        self.get_energy(with_stop)


        hmm = {'q0': ['q1'],
        'q1': (['qf'], ['tbl', 'lbl', 'tpl', 'rdl', 'parl', 'birl', 'tpal', 'tbar']),
          }
        rule = [[{"liquid": "+"}], [], [{"stop": "+"}], [], False]
        a_insertion_rule = [[], [{'high': '-', 'cons': '-'}], [{}], [{'son': '-'}], False]
        a_insertion = SimulationCase("a_insertion", hmm, [rule, a_insertion_rule])
        self.get_energy(a_insertion)