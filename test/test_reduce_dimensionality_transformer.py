from unittest import TestCase

import pandas as pd

import constants as c
from transformations import ReduceDimensionalityTransformation, Transformer


class TestReduceDimensionalityTransformer(TestCase):
    def test_low_variance_filter(self):
        filename = "../" + c.TEST_DATASETS_PATH + "test_reduce_dimensionality_low_variance.csv"
        dataset = pd.read_csv(filename)
        transformation = ReduceDimensionalityTransformation.LowVarianceFilter
        transformer = Transformer(dataset, transformation)
        dataset_transformed = transformer.execute()
        self.assertIsNotNone(dataset_transformed, "Transformed dataset cannot be None")

    def test_high_correlation_filter(self):
        filename = "../" + c.TEST_DATASETS_PATH + "test_reduce_dimensionality_high_correlation.csv"
        dataset = pd.read_csv(filename)
        transformation = ReduceDimensionalityTransformation.HighCorrelationFilter
        transformer = Transformer(dataset, transformation, strategy="mean")
        dataset_transformed = transformer.execute()
        self.assertIsNotNone(dataset_transformed, "Transformed dataset cannot be None")

    def test_random_forest(self):
        filename = "../" + c.TEST_DATASETS_PATH + "test_iris_with_noise.csv"
        dataset = pd.read_csv(filename)
        transformation = ReduceDimensionalityTransformation.RandomForest
        transformer = Transformer(dataset, transformation, features_to_select=4)
        dataset_transformed = transformer.execute()
        self.assertIsNotNone(dataset_transformed, "Transformed dataset cannot be None")

    def test_principal_component_analysis(self):
        filename = "../" + c.TEST_DATASETS_PATH + "iris.csv"
        dataset = pd.read_csv(filename)
        transformation = ReduceDimensionalityTransformation.PrincipalComponentAnalysis
        transformer = Transformer(dataset, transformation, n_components=2)
        dataset_transformed = transformer.execute()
        self.assertIsNotNone(dataset_transformed, "Transformed dataset cannot be None")

    def test_singular_value_decomposition(self):
        filename = "../" + c.TEST_DATASETS_PATH + "test_iris_svd.csv"
        dataset = pd.read_csv(filename)
        transformation = ReduceDimensionalityTransformation.SingularValueDecomposition
        transformer = Transformer(dataset, transformation, n_components=2)
        dataset_transformed = transformer.execute()
        self.assertIsNotNone(dataset_transformed, "Transformed dataset cannot be None")
