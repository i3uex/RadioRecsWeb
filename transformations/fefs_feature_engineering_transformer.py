import logging
from enum import Enum

import numpy as np
import pandas as pd
from sklearn.preprocessing import KBinsDiscretizer, FunctionTransformer

from arguments import ArgumentsParser, ArgumentDescriptor
from transformations import FeatureEngineeringTransformation


class FeatureEngineeringTransformerEncode(Enum):
    OneHot = "onehot"
    OneHotDense = "onehot-dense"
    Ordinal = "ordinal"


class FeatureEngineeringTransformerStrategy(Enum):
    Uniform = "uniform"
    Quantile = "quantile"
    KMeans = "kmeans"


class FeatureEngineeringTransformerArgument(ArgumentDescriptor, Enum):
    NumberOfBins = ArgumentDescriptor("n_bins", [5])
    Encode = ArgumentDescriptor("encode", FeatureEngineeringTransformerEncode.OneHot.value)
    Strategy = ArgumentDescriptor("strategy", FeatureEngineeringTransformerStrategy.Quantile.value)


class FeatureEngineeringTransformer:
    dataset = None
    transformation = None
    arguments = None

    def __init__(self, dataset, transformation, **arguments):
        logging.debug(f"FeatureEngineeringTransformer.__init__()")
        self.dataset = dataset
        self.transformation = transformation
        self.arguments = arguments

    def execute(self):
        logging.debug(f"FeatureEngineeringTransformer.execute()")
        try:
            if self.transformation == FeatureEngineeringTransformation.Binning:
                return self._binning()
            elif self.transformation == FeatureEngineeringTransformation.LogTransform:
                return self._log_transform()
            else:
                message = f"Transformation not supported: {self.transformation}"
                logging.debug(f"{message}")
                raise Exception(message)
        except RuntimeError as error:
            message = f"{str(error)}"
            logging.debug(f"{message}")
            raise Exception(message)

    def _binning(self):
        """
        As described by sklearn: "discretizes features into k bins", that is,
        creates a concrete number of bins so the value of each feature can be
        put inside one of those bins. Use argument n_bins to specify how many
        bins to create for each feature. For example, if the dataset has three
        features, use n_bins=[3, 2, 2] to create 3 bins for feature 1, 2 for
        feature 2, and 2 for feature 3. Default value is [5] (it assumes your
        dataset has a single feature). Use parameter encode to choose between
        values onehot (default), onehot-dense, and ordinal. Use argument
        strategy to choose between values uniform, quantile (default), and
        kmeans.
        """
        logging.debug(f"FeatureEngineeringTransformer._binning()")

        arguments_parser = ArgumentsParser(self.arguments)
        n_bins = arguments_parser.get_list_int(FeatureEngineeringTransformerArgument.NumberOfBins)
        encode = arguments_parser.get(FeatureEngineeringTransformerArgument.Encode)
        strategy = arguments_parser.get(FeatureEngineeringTransformerArgument.Strategy)

        logging.debug(f"- {FeatureEngineeringTransformerArgument.NumberOfBins.key}: {n_bins}")
        logging.debug(f"- {FeatureEngineeringTransformerArgument.Encode.key}: {encode}")
        logging.debug(f"- {FeatureEngineeringTransformerArgument.Strategy.key}: {strategy}")

        columns = self.dataset.columns

        k_bins_discretizer = KBinsDiscretizer(n_bins=n_bins, encode=encode, strategy=strategy)
        transformed_dataset = k_bins_discretizer.fit_transform(self.dataset)

        return pd.DataFrame(data=transformed_dataset, columns=columns)

    def _log_transform(self):
        """
        Logarithmic transformation of data to handle skew, adapt magnitude
        order, and decrease the effect of outliers. No arguments needed.
        """
        logging.debug(f"FeatureEngineeringTransformer._log_transform()")

        columns = self.dataset.columns

        function_transformer = FunctionTransformer(np.log1p, validate=True)
        transformed_dataset = function_transformer.transform(self.dataset)

        return pd.DataFrame(data=transformed_dataset, columns=columns)
