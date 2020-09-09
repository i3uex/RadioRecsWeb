from unittest import TestCase

import pandas as pd

import constants as c
from transformations import ScaleNormalizeTransformation, Transformer


class TestScaleNormalizeTransformer(TestCase):
    def setUp(self) -> None:
        filename = "../" + c.TEST_DATASETS_PATH + "test_scale_normalize.csv"
        self.dataset = pd.read_csv(filename)

    def test_min_max_scaler(self):
        transformation = ScaleNormalizeTransformation.MinMaxScaler
        transformer = Transformer(self.dataset, transformation)
        dataset_transformed = transformer.execute()
        self.assertIsNotNone(dataset_transformed, "Transformed dataset cannot be None")

    def test_standard_scaler(self):
        transformation = ScaleNormalizeTransformation.StandardScaler
        transformer = Transformer(self.dataset, transformation)
        dataset_transformed = transformer.execute()
        self.assertIsNotNone(dataset_transformed, "Transformed dataset cannot be None")

    def test_robust_scaler(self):
        transformation = ScaleNormalizeTransformation.RobustScaler
        transformer = Transformer(self.dataset, transformation)
        dataset_transformed = transformer.execute()
        self.assertIsNotNone(dataset_transformed, "Transformed dataset cannot be None")

    def test_normalizer(self):
        transformation = ScaleNormalizeTransformation.Normalizer
        transformer = Transformer(self.dataset, transformation)
        dataset_transformed = transformer.execute()
        self.assertIsNotNone(dataset_transformed, "Transformed dataset cannot be None")
