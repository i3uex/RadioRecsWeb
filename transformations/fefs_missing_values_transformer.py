import logging
from enum import Enum

import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer, KNNImputer

from arguments import ArgumentsParser, ArgumentDescriptor
from transformations import MissingValuesTransformation


class MissingValuesTransformerStrategy(Enum):
    Mean = "mean"
    Median = "median"
    MostFrequent = "most_frequent"
    Constant = "constant"


class MissingValuesTransformerWeights(Enum):
    Uniform = "uniform"
    Distance = "distance"


class MissingValuesTransformerArgument(ArgumentDescriptor, Enum):
    MissingValues = ArgumentDescriptor("missing_values", np.nan)
    Strategy = ArgumentDescriptor("strategy", MissingValuesTransformerStrategy.Mean.value)
    FillValue = ArgumentDescriptor("fill_value", 1)
    NumberOfNeighbors = ArgumentDescriptor("n_neighbors", 5)
    Weights = ArgumentDescriptor("weights", MissingValuesTransformerWeights.Uniform.value)
    Metric = ArgumentDescriptor("metric", "nan_euclidean")


class MissingValuesTransformer:
    dataset = None
    transformation = None
    arguments = None

    def __init__(self, dataset, transformation, **arguments):
        logging.debug(f"MissingValuesTransformer.__init__()")
        self.dataset = dataset
        self.transformation = transformation
        self.arguments = arguments

    def execute(self):
        logging.debug(f"MissingValuesTransformer.execute()")
        try:
            if self.transformation == MissingValuesTransformation.DeleteInstanceRow:
                return self._delete_instance_row()
            elif self.transformation == MissingValuesTransformation.StatisticsMeanMedianMostFrequent:
                return self._statistics_mean_median_most_frequent()
            elif self.transformation == MissingValuesTransformation.Constant:
                return self._constant()
            elif self.transformation == MissingValuesTransformation.NearestNeighbors:
                return self._nearest_neighbors()
            else:
                message = f"Transformation not supported: {self.transformation}"
                logging.debug(f"{message}")
                raise Exception(message)
        except Exception as exception:
            message = f"{str(exception)}"
            logging.debug(f"{message}")
            raise Exception(message)

    def _delete_instance_row(self):
        """
        Delete any row with missing values. sklearn does not offer a
        transformer to perform this operation, so it has been implemented using
        pandas, replacing any missing values with NaN and, then, dropping the
        rows that contain it.
        """
        logging.debug(f"MissingValuesTransformer._delete_instance_row()")

        arguments_parser = ArgumentsParser(self.arguments)
        missing_values = arguments_parser.get(MissingValuesTransformerArgument.MissingValues)

        logging.debug(f"- {MissingValuesTransformerArgument.MissingValues.key}: {missing_values}")

        dataset = self.dataset
        if missing_values is not np.nan:
            dataset = self.dataset.replace(missing_values, np.nan)
        transformed_dataset = dataset.dropna()

        return transformed_dataset

    def _statistics_mean_median_most_frequent(self):
        """
        Replaces the missing values with the resulting value of performing an
        statistical operation over the known values (in this case, the mean,
        the median, or the most repeated value). Choose between them using the
        argument strategy, with values mean, median, and most_frequent. Default
        strategy is mean. More at sklearn documentation.

        https://scikit-learn.org/stable/modules/impute.html#univariate-feature-imputation
        """
        logging.debug(f"MissingValuesTransformer._statistics_mean_median_most_frequent()")

        arguments_parser = ArgumentsParser(self.arguments)
        missing_values = arguments_parser.get(MissingValuesTransformerArgument.MissingValues)
        strategy = arguments_parser.get(MissingValuesTransformerArgument.Strategy)

        logging.debug(f"- {MissingValuesTransformerArgument.MissingValues.key}: {missing_values}")
        logging.debug(f"- {MissingValuesTransformerArgument.Strategy.key}: {strategy}")

        columns = self.dataset.columns

        imputer = SimpleImputer(
            missing_values=missing_values,
            strategy=strategy
        )
        imputer.fit(self.dataset)
        transformed_dataset = imputer.transform(self.dataset)

        return pd.DataFrame(data=transformed_dataset, columns=columns)

    def _constant(self):
        """
        Replaces the missing values with the constant provided. Set the
        constant of your choice using argument fill_value. Its default value is
        1. Actually, this is another variant of statistical replacement. More
        at sklearn documentation.

        https://scikit-learn.org/stable/modules/impute.html#univariate-feature-imputation
        """
        logging.debug(f"MissingValuesTransformer._constant()")

        arguments_parser = ArgumentsParser(self.arguments)
        missing_values = arguments_parser.get(MissingValuesTransformerArgument.MissingValues)
        strategy = MissingValuesTransformerStrategy.Constant.value
        fill_value = arguments_parser.get_int(MissingValuesTransformerArgument.FillValue)

        logging.debug(f"- {MissingValuesTransformerArgument.MissingValues.key}: {missing_values}")
        logging.debug(f"- {MissingValuesTransformerArgument.Strategy.key}: {strategy}")
        logging.debug(f"- {MissingValuesTransformerArgument.FillValue.key}: {fill_value}")

        columns = self.dataset.columns

        imputer = SimpleImputer(
            missing_values=missing_values,
            strategy=strategy,
            fill_value=fill_value
        )
        imputer.fit(self.dataset)
        transformed_dataset = imputer.transform(self.dataset)

        return pd.DataFrame(data=transformed_dataset, columns=columns)

    def _nearest_neighbors(self):
        """
        Use nearest neighbors values to impute the missing values. Use argument
        n_neighbors to select the number of neighbors used for the imputation.
        Use argument weights to choose between uniform (default) or distance.
        More at sklearn documentation.

        https://scikit-learn.org/stable/modules/impute.html#nearest-neighbors-imputation
        """
        logging.debug(f"MissingValuesTransformer._nearest_neighbors()")

        arguments_parser = ArgumentsParser(self.arguments)
        missing_values = arguments_parser.get(MissingValuesTransformerArgument.MissingValues)
        n_neighbors = arguments_parser.get_int(MissingValuesTransformerArgument.NumberOfNeighbors)
        weights = arguments_parser.get(MissingValuesTransformerArgument.Weights)
        metric = arguments_parser.get(MissingValuesTransformerArgument.Metric)

        logging.debug(f"- {MissingValuesTransformerArgument.MissingValues.key}: {missing_values}")
        logging.debug(f"- {MissingValuesTransformerArgument.NumberOfNeighbors.key}: {n_neighbors}")
        logging.debug(f"- {MissingValuesTransformerArgument.Weights.key}: {weights}")
        logging.debug(f"- {MissingValuesTransformerArgument.Metric.key}: {metric}")

        columns = self.dataset.columns

        imputer = KNNImputer(
            missing_values=missing_values,
            n_neighbors=n_neighbors,
            weights=weights,
            metric=metric
        )
        transformed_dataset = imputer.fit_transform(self.dataset)

        return pd.DataFrame(data=transformed_dataset, columns=columns)
