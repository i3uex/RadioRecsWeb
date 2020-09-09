from enum import Enum
import logging


class Transformation:
    """
    Factory class used to encapsulate all Transformation enums.
    """
    def __new__(cls, value: str):
        """
        Create a new instance of this class providing a string that should be
        the value of one the enums created below. A new instance of the Enum
        containing said string value will be returned.

        Bear in mind that no repetition in value is allowed. The software won't
        crash; instead, the first declaration of that value will always be
        returned, rendering unused the rest of declarations with the same value.

        Update the if stair with the appropriate enums you create, so all of them
        are taken into account.
        """
        logging.debug(f"Transformation.__new__(\"{value}\")")
        if FeatureSelectionTransformation.contains(value):
            return FeatureSelectionTransformation(value)
        elif ScaleNormalizeTransformation.contains(value):
            return ScaleNormalizeTransformation(value)
        elif FeatureEngineeringTransformation.contains(value):
            return FeatureEngineeringTransformation(value)
        elif EncodingTransformation.contains(value):
            return EncodingTransformation(value)
        elif MissingValuesTransformation.contains(value):
            return MissingValuesTransformation(value)
        elif ReduceDimensionalityTransformation.contains(value):
            return ReduceDimensionalityTransformation(value)
        else:
            return None


class TransformationEnum(Enum):
    @classmethod
    def contains(cls, value: str) -> bool:
        """
        Returns True if the Enum class provided in the first parameter has any
        item with the value string provided in the second.

        In other words, the idea behind this subclass is being able to check if
        a given string is the value of one of the items in an Enum class.

        Create Enum subclasses of this type so they have the method contains
        and you can check if a given string, passed from the calling software,
        is the value of any of the items in said subclass without having to
        explicitly check for every value.

        Parameters:
            value (str): Value string searched for in the enum class provided

        Returns:
            bool: True if the enum class provided contains the value provided,
            False otherwise
        """
        logging.debug(f"TransformationEnum.contains(\"{value}\")")
        return any(x for x in cls if x.value == value)


class TransformationCategory(TransformationEnum):
    """
    List of transformation categories. Each category must have a corresponding
    enum class withe the transformations belonging to them. This relationship
    must be maintained by the programmer.
    """
    FeatureSelection = "Feature Selection"
    ScaleNormalize = "Scale - Normalize"
    FeatureEngineering = "Feature Engineering"
    Encoding = "Encoding"
    MissingValues = "Missing Values"
    ReduceDimensionality = "Reduce Dimensionality"


class FeatureSelectionTransformation(TransformationEnum):
    """
    List of transformations in the feature selection category.
    """
    MutualInformationScore = "Mutual Information Score"
    ChiSquaredStatistics = "Chi-Squared Statistics"
    RecursiveFeatureElimination = "Recursive Feature Elimination"
    SelectFromModel = "Select From Model"
    PearsonCorrelation = "Pearson Correlation"


class ScaleNormalizeTransformation(TransformationEnum):
    """
    List of transformations in the scale/normalization category
    """
    MinMaxScaler = "MinMaxScaler"
    StandardScaler = "StandardScaler"
    RobustScaler = "RobustScaler"
    Normalizer = "Normalizer"


class FeatureEngineeringTransformation(TransformationEnum):
    """
    List of transformations in the feature engineering category
    """
    Binning = "Binning"
    LogTransform = "LogTransform"


class EncodingTransformation(TransformationEnum):
    """
    List of transformations in the encoding category
    """
    LabelEncoding = "Label Encoding"
    OneHotEncoding = "One-Hot Encoding"


class MissingValuesTransformation(TransformationEnum):
    """
    List of transformations in the missing values category
    """
    DeleteInstanceRow = "Delete Instance (Row)"
    StatisticsMeanMedianMostFrequent = "Statistics (Mean, Median, Most Frequent)"
    Constant = "Constant"
    NearestNeighbors = "Nearest Neighbors"


class ReduceDimensionalityTransformation(TransformationEnum):
    """
    List of transformations in the reduce dimensionality category
    """
    LowVarianceFilter = "Low Variance Filter"
    HighCorrelationFilter = "High Correlation Filter"
    RandomForest = "Random Forest"
    PrincipalComponentAnalysis = "PCA (Principal Component Analysis)"
    SingularValueDecomposition = "SVD (Singular Value Decomposition)"
