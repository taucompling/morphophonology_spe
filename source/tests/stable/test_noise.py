from noise import FinalDevoicingNoise
from tests.stable.test_hypothesis import MyTestCase
from simulations import dam_ka_ilm_final_devoicing


class TestFinalDevoicingNoise(MyTestCase):
    def setUp(self):
        super().setUp()
        self.initialise_segment_table(
            dam_ka_ilm_final_devoicing.segment_table_file_name
        )

    def test_noise_is_applied(self):
        testee = FinalDevoicingNoise(noise_rate=100)
        words = ["dad"]
        testee.apply_noise(words)

        self.assertEqual(words, ["dat"])

    def test_noise_is_applied_at_expected_percent(self):
        testee = FinalDevoicingNoise(noise_rate=67)
        words = ["dad"] * 100
        testee.apply_noise(words)

        self.assertCountEqual(words, ["dad"] * 33 + ["dat"] * 67)

    def test_noise_is_applied_only_for_voiced(self):
        testee = FinalDevoicingNoise(noise_rate=100)
        words = ["tat"]
        testee.apply_noise(words)

        self.assertCountEqual(words, ["tat"])

    def test_noise_is_applied_only_for_obs(self):
        testee = FinalDevoicingNoise(noise_rate=100)
        words = ["dam", "da"]
        testee.apply_noise(words)

        self.assertCountEqual(words, ["dam", "da"])
