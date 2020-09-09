from unittest import TestCase

import pandas as pd

import constants as c
from transformations import MissingValuesTransformation, Transformer


class TestMissingValuesTransformer(TestCase):
    def setUp(self) -> None:
        filename = "../" + c.TEST_DATASETS_PATH + "test_missing_values.csv"
        self.dataset = pd.read_csv(filename)

    def test_delete_instance_row(self):
        transformation = MissingValuesTransformation.DeleteInstanceRow
        transformer = Transformer(self.dataset, transformation)
        dataset_transformed = transformer.execute()
        self.assertIsNotNone(dataset_transformed, "Transformed dataset cannot be None")

    def test_statistics_mean(self):
        transformation = MissingValuesTransformation.StatisticsMeanMedianMostFrequent
        transformer = Transformer(self.dataset, transformation, strategy="mean")
        dataset_transformed = transformer.execute()
        self.assertIsNotNone(dataset_transformed, "Transformed dataset cannot be None")

    def test_statistics_median(self):
        transformation = MissingValuesTransformation.StatisticsMeanMedianMostFrequent
        transformer = Transformer(self.dataset, transformation, strategy="median")
        dataset_transformed = transformer.execute()
        self.assertIsNotNone(dataset_transformed, "Transformed dataset cannot be None")

    def test_statistics_most_frequent(self):
        transformation = MissingValuesTransformation.StatisticsMeanMedianMostFrequent
        transformer = Transformer(self.dataset, transformation, strategy="most_frequent")
        dataset_transformed = transformer.execute()
        self.assertIsNotNone(dataset_transformed, "Transformed dataset cannot be None")

    def test_constant(self):
        transformation = MissingValuesTransformation.Constant
        transformer = Transformer(self.dataset, transformation, fill_value=5)
        dataset_transformed = transformer.execute()
        self.assertIsNotNone(dataset_transformed, "Transformed dataset cannot be None")

    def test_nearest_neighbors(self):
        transformation = MissingValuesTransformation.NearestNeighbors
        transformer = Transformer(self.dataset, transformation)
        dataset_transformed = transformer.execute()
        self.assertIsNotNone(dataset_transformed, "Transformed dataset cannot be None")
