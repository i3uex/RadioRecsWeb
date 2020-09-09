import pandas as pd

from .fefs_encoding_transformer import EncodingTransformer
from .fefs_feature_engineering_transformer import FeatureEngineeringTransformer
from .fefs_feature_selection_transformer import FeatureSelectionTransformer
from .fefs_missing_values_transformer import MissingValuesTransformer
from .fefs_reduce_dimensionality_transformer import ReduceDimensionalityTransformer
from .fefs_scale_normalize_transformer import ScaleNormalizeTransformer
from .fefs_transformation import *


class Transformer:
    """
    Factory class used to encapsulate all Transformer classes.

    Each transformer will have a method called execute(). It will execute a
    different method depending in the transformation passed as an argument when
    creating the instance of the class.

    All these methods called by execute() have the same structure:
    - get the arguments provided, if any.
    - prepare the transformation.
    - transform the dataset.
    - adjust the transformed dataset, if needed.
    - return the transformed dataset.

    Any error that happens will be transferred up in the chain until some piece
    of code takes care of it.
    """
    def __new__(cls, dataset: pd.DataFrame, transformation, **arguments):
        """
        The real type of the class returned will be determined by the
        Transformation instance passed. Its type will be checked and, depending
        on it, the appropriate Transformer instance will be created.

        Parameters:
            dataset (Pandas' DataFrame): data to be transformed
            transformation: the specific transformation to perform with the
            dataset provided
            arguments: variable list of arguments to be applied to the
            transformation selected

        Returns:
            An instance of the appropriate Transformer class, given the
            transformation provided
        """
        logging.debug(f"Transformer.__new__()")
        if isinstance(transformation, FeatureSelectionTransformation):
            return FeatureSelectionTransformer(dataset, transformation, **arguments)
        elif isinstance(transformation, ScaleNormalizeTransformation):
            return ScaleNormalizeTransformer(dataset, transformation, **arguments)
        elif isinstance(transformation, FeatureEngineeringTransformation):
            return FeatureEngineeringTransformer(dataset, transformation, **arguments)
        elif isinstance(transformation, EncodingTransformation):
            return EncodingTransformer(dataset, transformation, **arguments)
        elif isinstance(transformation, MissingValuesTransformation):
            return MissingValuesTransformer(dataset, transformation, **arguments)
        elif isinstance(transformation, ReduceDimensionalityTransformation):
            return ReduceDimensionalityTransformer(dataset, transformation, **arguments)
        else:
            return None
