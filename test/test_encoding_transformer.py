from unittest import TestCase
import pandas as pd
import constants as c

from transformations import EncodingTransformation, Transformer


class TestEncodingTransformer(TestCase):
    def setUp(self) -> None:
        filename = "../" + c.TEST_DATASETS_PATH + "test_encoding.csv"
        self.dataset = pd.read_csv(filename)

    def test_label_encoding(self):
        transformation = EncodingTransformation.LabelEncoding
        transformer = Transformer(self.dataset, transformation)
        dataset_transformed = transformer.execute()
        self.assertIsNotNone(dataset_transformed, "Transformed dataset cannot be None")

    def test_one_hot_encoding(self):
        transformation = EncodingTransformation.OneHotEncoding
        transformer = Transformer(self.dataset, transformation)
        dataset_transformed = transformer.execute()
        self.assertIsNotNone(dataset_transformed, "Transformed dataset cannot be None")
