from unittest import TestCase

import pandas as pd

import constants as c
from transformations import FeatureEngineeringTransformation, Transformer


class TestFeatureEngineeringTransformer(TestCase):
    def test_binning(self):
        filename = "../" + c.TEST_DATASETS_PATH + "test_feature_engineering_binning.csv"
        dataset = pd.read_csv(filename)
        transformation = FeatureEngineeringTransformation.Binning
        transformer = Transformer(dataset, transformation, n_bins="[3, 2, 2]", encode="ordinal")
        dataset_transformed = transformer.execute()
        self.assertIsNotNone(dataset_transformed, "Transformed dataset cannot be None")

    def test_log_transform(self):
        filename = "../" + c.TEST_DATASETS_PATH + "test_feature_engineering_log_transform.csv"
        dataset = pd.read_csv(filename)
        transformation = FeatureEngineeringTransformation.LogTransform
        transformer = Transformer(dataset, transformation)
        dataset_transformed = transformer.execute()
        self.assertIsNotNone(dataset_transformed, "Transformed dataset cannot be None")
