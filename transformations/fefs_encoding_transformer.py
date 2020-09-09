import logging
from enum import Enum

import pandas as pd
from sklearn.preprocessing import LabelEncoder

from arguments import ArgumentsParser, ArgumentDescriptor
from transformations import EncodingTransformation


class EncodingTransformerArgument(ArgumentDescriptor, Enum):
    FeaturePosition = ArgumentDescriptor("feature_position", 0)


class EncodingTransformer:
    dataset = None
    transformation = None
    arguments = None

    def __init__(self, dataset, transformation, **arguments):
        logging.debug(f"EncodingTransformer.__init__()")
        self.dataset = dataset
        self.transformation = transformation
        self.arguments = arguments

    def execute(self):
        logging.debug(f"EncodingTransformer.execute()")
        try:
            if self.transformation == EncodingTransformation.LabelEncoding:
                return self._label_encoding()
            elif self.transformation == EncodingTransformation.OneHotEncoding:
                return self._one_hot_encoding()
            else:
                message = f"Transformation not supported: {self.transformation}"
                logging.debug(f"{message}")
                raise Exception(message)
        except RuntimeError as error:
            message = f"{str(error)}"
            logging.debug(f"{message}")
            raise Exception(message)

    def _label_encoding(self):
        """
        Translate into numbers any categorical or textual data, from 0 to the
        number of different elements - 1. Choose between features using the
        argument feature_position, a 0-based index. If not present, the
        transformer will try to label-encode the first feature (that is, the
        one with index 0).
        """
        logging.debug(f"EncodingTransformer._label_encoding()")

        arguments_parser = ArgumentsParser(self.arguments)
        feature_position = arguments_parser.get_int(EncodingTransformerArgument.FeaturePosition)

        logging.debug(f"- {EncodingTransformerArgument.FeaturePosition.key}: {feature_position}")

        label_encoder = LabelEncoder()
        dataset = self.dataset
        dataset.iloc[:, feature_position] = label_encoder.fit_transform(dataset.iloc[:, feature_position])

        return dataset

    def _one_hot_encoding(self):
        """
        Translate into numbers any categorical or textual data in a way that no
        hierarchy or order can be inferred from it. A new feature will be
        created for each different value present in the original feature, with
        value 1 where the original value was present, and 0 where it wasn't.
        Choose between features using the argument feature_position, a 0-based
        index. If not present, the transformer will try to one-hot-encode the
        first feature (that is, the one with index 0).
        """
        logging.debug(f"EncodingTransformer._one_hot_encoding()")

        arguments_parser = ArgumentsParser(self.arguments)
        feature_position = arguments_parser.get_int(EncodingTransformerArgument.FeaturePosition)

        logging.debug(f"- {EncodingTransformerArgument.FeaturePosition.key}: {feature_position}")

        dataset = self.dataset
        label = dataset.columns[feature_position]
        dummies = pd.get_dummies(dataset.iloc[:, feature_position], prefix=label)
        dataset_before = dataset.iloc[:, :feature_position]
        dataset_after = dataset.iloc[:, feature_position + 1:]
        transformed_dataset = dummies
        if not dataset_before.empty:
            transformed_dataset = pd.concat([dataset_before, transformed_dataset], axis=1)
        if not dataset_after.empty:
            transformed_dataset = pd.concat([transformed_dataset, dataset_after], axis=1)

        return transformed_dataset
