from tests.stable.test_hypothesis import TestHypothesisBase
from simulations import dag_zook_noise


class TestNoiseRules(TestHypothesisBase):
    def initialise_simulation_and_add_noise(self, simulation, noise):
        self.initialise_simulation(simulation)
        self.configurations.simulation_data.extend(noise)

    def test_noise_rules(self):
        self.initialise_simulation_and_add_noise(dag_zook_noise, ['dag'])
        hypo = self.get_target_hypo()
        self.assertLess(hypo.get_energy(), float('inf'))

    def test_no_noise_fixing__energy_is_inf(self):
        self.initialise_simulation_and_add_noise(dag_zook_noise, ['dag'])
        self.configurations["NOISE_RULE_SET"] = []
        hypo = self.get_target_hypo()
        self.assertEqual(hypo.get_energy(), float('inf'))

    def test_no_noise_fixing__but_rule_is_optional(self):
        self.initialise_simulation_and_add_noise(dag_zook_noise, ['dag'])
        self.configurations["NOISE_RULE_SET"] = []
        hypo = self.get_target_hypo()
        hypo.grammar.rule_set.rules[0].obligatory = False
        self.assertLess(hypo.get_energy(), float('inf'))

    def test_dealing_with_noise_is_better_than_optional_rule(self):
        self.initialise_simulation_and_add_noise(dag_zook_noise, ['dag'] * 2)
        hypo = self.get_target_hypo()
        optional_hypo = self.get_target_hypo()
        optional_hypo.grammar.rule_set.rules[0].obligatory = False
        self.assert_less_no_infs(hypo.get_energy(), optional_hypo.get_energy())

    def test_dealing_with_noise_is_better_than_optional_rule__up_to_certain_noise_rate(self):
        self.initialise_simulation_and_add_noise(dag_zook_noise, ['dag'] * 3)
        hypo = self.get_target_hypo()
        optional_hypo = self.get_target_hypo()
        optional_hypo.grammar.rule_set.rules[0].obligatory = False
        self.assert_less_no_infs(optional_hypo.get_energy(), hypo.get_energy())

    def test_dealing_with_noise_is_better_than_adding_an_optional_rule(self):
        self.initialise_simulation_and_add_noise(dag_zook_noise, ['dag'])
        self.assert_greater_than_target(
            final_hmm_str='''
q0: ['q1']
q1: ['q5'], ['dag', 'kad', 'dod', 'kod', 'gas', 'toz', 'ata', 'aso', 'daod', 'sog', 'saog', 'tad', 'taz', 'kaod', 'kaz', 'kak']
q5: ['qf'], ['dos', 'gos', 'zook', 'ε']
''',
            final_rule_str="[{'cons': '+'}] --> [{'voice': '-'}] / []__[{'WB': True}] obligatory: False noise: False | dd"
        )

