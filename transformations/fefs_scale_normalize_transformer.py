import logging
from enum import Enum

import pandas as pd
from sklearn import preprocessing

from arguments import ArgumentsParser, ArgumentDescriptor
from transformations import ScaleNormalizeTransformation


class ScaleNormalizeTransformerNorm(Enum):
    L1 = "l1"
    L2 = "l2"
    Max = "max"


class ScaleNormalizeTransformerArgument(ArgumentDescriptor, Enum):
    RangeMin = ArgumentDescriptor("range_min", 0)
    RangeMax = ArgumentDescriptor("range_max", 1)
    WithMean = ArgumentDescriptor("with_mean", True)
    WithStd = ArgumentDescriptor("with_std", True)
    WithCentering = ArgumentDescriptor("with_centering", True)
    WithScaling = ArgumentDescriptor("with_scaling", True)
    QuantileRangeMin = ArgumentDescriptor("quantile_range_min", 25)
    QuantileRangeMax = ArgumentDescriptor("quantile_range_max", 75)
    Norm = ArgumentDescriptor("norm", ScaleNormalizeTransformerNorm.L2.value)


class ScaleNormalizeTransformer:
    dataset = None
    transformation = None
    arguments = None

    def __init__(self, dataset, transformation, **arguments):
        logging.debug(f"ScaleNormalizeTransformer.__init__()")
        self.dataset = dataset
        self.transformation = transformation
        self.arguments = arguments

    def execute(self):
        logging.debug(f"ScaleNormalizeTransformer.execute()")
        try:
            if self.transformation == ScaleNormalizeTransformation.MinMaxScaler:
                return self._min_max_scaler()
            elif self.transformation == ScaleNormalizeTransformation.StandardScaler:
                return self._standard_scaler()
            elif self.transformation == ScaleNormalizeTransformation.RobustScaler:
                return self._robust_scaler()
            elif self.transformation == ScaleNormalizeTransformation.Normalizer:
                return self._normalizer()
            else:
                message = f"Transformation not supported: {self.transformation}"
                logging.debug(f"{message}")
                raise Exception(message)
        except RuntimeError as error:
            message = f"{str(error)}"
            logging.debug(f"{message}")
            raise Exception(message)

    def _min_max_scaler(self):
        """
        As described by sklearn: "transforms features by scaling each feature
        to a given range". Choose min and max range values using arguments
        range_min (defaults to 0) and range_max (defaults to 1).
        """
        logging.debug(f"ScaleNormalizeTransformer._min_max_scaler()")

        arguments_parser = ArgumentsParser(self.arguments)
        range_min = arguments_parser.get_int(ScaleNormalizeTransformerArgument.RangeMin)
        range_max = arguments_parser.get_int(ScaleNormalizeTransformerArgument.RangeMax)

        logging.debug(f"- {ScaleNormalizeTransformerArgument.RangeMin.key}: {range_min}")
        logging.debug(f"- {ScaleNormalizeTransformerArgument.RangeMax.key}: {range_max}")

        columns = self.dataset.columns

        min_max_scaler = preprocessing.MinMaxScaler(feature_range=(range_min, range_max))
        transformed_dataset = min_max_scaler.fit_transform(self.dataset)

        return pd.DataFrame(data=transformed_dataset, columns=columns)

    def _standard_scaler(self):
        """
        As described by sklearn: "standardizes features by removing the mean
        and scaling to unit variance". Use argument with_mean to specify if
        data should be centered before scaling (defaults to True). Use argument
        with_std to specify if data should be scaled to unit variance (defaults
         to True).
        """
        logging.debug(f"ScaleNormalizeTransformer._standard_scaler()")

        arguments_parser = ArgumentsParser(self.arguments)
        with_mean = arguments_parser.get_bool(ScaleNormalizeTransformerArgument.WithMean)
        with_std = arguments_parser.get_bool(ScaleNormalizeTransformerArgument.WithStd)

        logging.debug(f"- {ScaleNormalizeTransformerArgument.WithMean.key}: {with_mean}")
        logging.debug(f"- {ScaleNormalizeTransformerArgument.WithStd.key}: {with_std}")

        columns = self.dataset.columns

        standard_scaler = preprocessing.StandardScaler(with_mean=with_mean, with_std=with_std)
        transformed_dataset = standard_scaler.fit_transform(self.dataset)

        return pd.DataFrame(data=transformed_dataset, columns=columns)

    def _robust_scaler(self):
        """
        As described by sklearn: "scales features using statistics that are
        robust to outliers. This Scaler removes the median and scales the data
        according to the quantile range (defaults to IQR: Interquartile Range).
        The IQR is the range between the 1st quartile (25th quantile) and the
        3rd quartile (75th quantile)". Use argument with_centering to specify
        if data should be centered before scaling (defaults to True). Use
        argument with_scaling to specify if data should be scaled to
        interquartile range (defaults to True). Choose min and max quantile
        range values using arguments quantile_range_min (defaults to 25.0) and
        quantile_range_max (defaults to 75.0).
        """
        logging.debug(f"ScaleNormalizeTransformer._robust_scaler()")

        arguments_parser = ArgumentsParser(self.arguments)
        with_centering = arguments_parser.get_bool(ScaleNormalizeTransformerArgument.WithCentering)
        with_scaling = arguments_parser.get_bool(ScaleNormalizeTransformerArgument.WithScaling)
        quantile_range_min = arguments_parser.get_float(ScaleNormalizeTransformerArgument.QuantileRangeMin)
        quantile_range_max = arguments_parser.get_float(ScaleNormalizeTransformerArgument.QuantileRangeMax)

        logging.debug(f"- {ScaleNormalizeTransformerArgument.WithCentering.key}: {with_centering}")
        logging.debug(f"- {ScaleNormalizeTransformerArgument.WithScaling.key}: {with_scaling}")
        logging.debug(f"- {ScaleNormalizeTransformerArgument.QuantileRangeMin.key}: {quantile_range_min}")
        logging.debug(f"- {ScaleNormalizeTransformerArgument.QuantileRangeMax.key}: {quantile_range_max}")

        columns = self.dataset.columns

        robust_scaler = preprocessing.RobustScaler(
            with_centering=with_centering,
            with_scaling=with_scaling,
            quantile_range=(quantile_range_min, quantile_range_max)
        )
        transformed_dataset = robust_scaler.fit_transform(self.dataset)

        return pd.DataFrame(data=transformed_dataset, columns=columns)

    def _normalizer(self):
        """
        As described by sklearn: "normalizes samples individually to unit
        norm", that is, it works on individual rows instead of columns, samples
        instead of features. Use argument norm to specify the norm to use when
        normalizing each sample. Possible values are l1, l2, and max.
        """
        logging.debug(f"ScaleNormalizeTransformer._normalizer()")

        arguments_parser = ArgumentsParser(self.arguments)
        norm = arguments_parser.get(ScaleNormalizeTransformerArgument.Norm)

        logging.debug(f"- {ScaleNormalizeTransformerArgument.Norm.key}: {norm}")

        columns = self.dataset.columns

        normalizer = preprocessing.Normalizer(norm=norm)
        transformed_dataset = normalizer.fit_transform(self.dataset)

        return pd.DataFrame(data=transformed_dataset, columns=columns)
