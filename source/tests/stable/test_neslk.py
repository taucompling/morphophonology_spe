from source.simulations import neslk
from source.tests.stable.test_transducer_problem import *


class TestNeslk(TestTransducerProblem):
    def test_neslk(self):
        self.initialise_simulation(neslk)
        target_hypo = self.get_target_hypo()
        target_hypo.get_energy()
        self.fail(target_hypo.energy_signature)