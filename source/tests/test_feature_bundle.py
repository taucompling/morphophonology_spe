from tests.my_test_case import MyTestCase
from feature_bundle import FeatureBundle, FeatureBundleList
from segment_table import SegmentTable

class TestFeatureBundle(MyTestCase):
    def setUp(self):
        self.initialise_segment_table("ai_bd_segment_table.txt")

    # feature_bundle
    def test_feature_bundle_add_feature(self):
        feature_bundle = FeatureBundle({'cons': '+'})
        feature_bundle._add_feature()
        print(feature_bundle)

    def test_feature_bundle_remove_feature(self):
        feature_bundle = FeatureBundle({'cons': '+'})
        feature_bundle._remove_feature()
        print(feature_bundle)

    def test_feature_bundle_remove_all_features_with_kleene_on(self):
        feature_bundle = FeatureBundle({'cons': '+', 'kleene': True})
        print(feature_bundle)
        feature_bundle._remove_feature()
        print(feature_bundle)
        feature_bundle._toggle_kleene()
        print(feature_bundle)

    def test_feature_bundle_toggle_kleene_by_role(self):
        left_context = FeatureBundle({'cons': '+', 'kleene': False}, role='left_context')
        left_context._toggle_kleene()
        print(left_context)   # {'cons': '+', 'kleene': True}
        target = FeatureBundle({'cons': '+', 'kleene': True}, role='target')
        print(target)   # {'cons': '+'}
        target_2 = FeatureBundle({'cons': '+'}, role='target')
        target_2._toggle_kleene()
        print(target_2)  # {'cons': '+'}

    def test_feature_bundle_toggle_kleene_when_empty(self):
        feature_bundle = FeatureBundle({'cons': '+', 'kleene': True})
        feature_bundle._toggle_kleene()
        print(feature_bundle)
        feature_bundle._toggle_kleene()
        print(feature_bundle)
        feature_bundle = FeatureBundle({})
        feature_bundle._toggle_kleene()
        print(feature_bundle)

    def test_feature_bundle_change_feature_value(self):
        feature_bundle = FeatureBundle({'cons': '+'})
        feature_bundle._change_feature_value()
        print(feature_bundle)

    # feature_bundle_list

    def test_feature_bundle_list_add_feature_bundle(self):
        feature_bundle_list = FeatureBundleList([], is_one_item_list=False)
        feature_bundle_list._add_feature_bundle()
        print(feature_bundle_list)

    def test_feature_bundle_list_remove_feature_bundle(self):
        feature_bundle_list = FeatureBundleList([{'cons': '+'}], is_one_item_list=True)
        feature_bundle_list._remove_feature_bundle()
        print(feature_bundle_list)

    def test_feature_bundle_list_change_feature_bundle(self):
        feature_bundle_list = FeatureBundleList([{'cons': '+'}], is_one_item_list=True)
        feature_bundle_list._change_existing_feature_bundle()
        print(feature_bundle_list)

    def test_get_random_feature_bundle_list(self):
        print(FeatureBundleList.get_random_feature_bundle_list(True))

    def test_feature_bundle_representation(self):
        feature_bundle = FeatureBundle({'cons': '+', "kleene": True})
        print(repr(feature_bundle))

    def test_feature_bundle_word_boundary(self):
        from simulations import french_deletion_new as simulation
        self.initialise_simulation(simulation)
        feature_bundle = FeatureBundle({"cons": "+", "WB": True}, role='right_context')
        print(feature_bundle)
        print(SegmentTable().get_segments_symbols_by_features(feature_bundle))

    def test_feature_bundle_morpheme_boundary(self):
        from simulations import french_deletion_new as simulation
        self.initialise_simulation(simulation)
        feature_bundle = FeatureBundle({"cons": "+", "MB": True}, role='right_context')
        print(feature_bundle)
        print(SegmentTable().get_segments_symbols_by_features(feature_bundle))