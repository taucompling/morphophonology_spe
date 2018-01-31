from tests.my_test_case import MyTestCase
from segment_table import SegmentTable

class TestFeatureBundle(MyTestCase):
    def setUp(self):
        pass

    def test_segment_table_is_valid(self):
        self.initialise_segment_table("invalid_segment_table.txt")
        segment_table = SegmentTable()
        print(segment_table.is_valid())


