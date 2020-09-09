from unittest import TestCase

import pandas as pd

import constants as c
from transformations import FeatureSelectionTransformation, Transformer


class TestFeatureSelectionTransformer(TestCase):
    def setUp(self) -> None:
        filename = "../" + c.TEST_DATASETS_PATH + "test_iris_with_noise.csv"
        self.dataset = pd.read_csv(filename)

    def test_mutual_information_score(self):
        transformation = FeatureSelectionTransformation.MutualInformationScore
        transformer = Transformer(self.dataset, transformation, features_to_select=4)
        dataset_transformed = transformer.execute()
        self.assertIsNotNone(dataset_transformed, "Transformed dataset cannot be None")

    def test_chi_squared_statistics(self):
        transformation = FeatureSelectionTransformation.ChiSquaredStatistics
        transformer = Transformer(self.dataset, transformation, features_to_select=4)
        dataset_transformed = transformer.execute()
        self.assertIsNotNone(dataset_transformed, "Transformed dataset cannot be None")

    def test_recursive_feature_elimination(self):
        transformation = FeatureSelectionTransformation.RecursiveFeatureElimination
        transformer = Transformer(self.dataset, transformation, features_to_select=4)
        dataset_transformed = transformer.execute()
        self.assertIsNotNone(dataset_transformed, "Transformed dataset cannot be None")

    def test_select_from_model(self):
        transformation = FeatureSelectionTransformation.SelectFromModel
        transformer = Transformer(self.dataset, transformation, features_to_select=4)
        dataset_transformed = transformer.execute()
        self.assertIsNotNone(dataset_transformed, "Transformed dataset cannot be None")

    def test_pearson_correlation(self):
        transformation = FeatureSelectionTransformation.PearsonCorrelation
        transformer = Transformer(self.dataset, transformation, features_to_select=4)
        dataset_transformed = transformer.execute()
        self.assertIsNotNone(dataset_transformed, "Transformed dataset cannot be None")
