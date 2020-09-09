import json
import logging
import os
import shutil
import uuid
from io import StringIO

import cherrypy
import pandas as pd

import constants as c
from arguments import ArgumentsParser
from transformations import *

Transformations = {
    TransformationCategory.FeatureSelection.value: [
        FeatureSelectionTransformation.MutualInformationScore.value,
        FeatureSelectionTransformation.ChiSquaredStatistics.value,
        FeatureSelectionTransformation.RecursiveFeatureElimination.value,
        FeatureSelectionTransformation.SelectFromModel.value,
        FeatureSelectionTransformation.PearsonCorrelation.value
    ],
    TransformationCategory.ScaleNormalize.value: [
        ScaleNormalizeTransformation.MinMaxScaler.value,
        ScaleNormalizeTransformation.StandardScaler.value,
        ScaleNormalizeTransformation.RobustScaler.value,
        ScaleNormalizeTransformation.Normalizer.value
    ],
    TransformationCategory.FeatureEngineering.value: [
        FeatureEngineeringTransformation.Binning.value,
        FeatureEngineeringTransformation.LogTransform.value
    ],
    TransformationCategory.Encoding.value: [
        EncodingTransformation.LabelEncoding.value,
        EncodingTransformation.OneHotEncoding.value
    ],
    TransformationCategory.MissingValues.value: [
        MissingValuesTransformation.DeleteInstanceRow.value,
        MissingValuesTransformation.StatisticsMeanMedianMostFrequent.value,
        MissingValuesTransformation.Constant.value,
        MissingValuesTransformation.NearestNeighbors.value
    ],
    TransformationCategory.ReduceDimensionality.value: [
        ReduceDimensionalityTransformation.LowVarianceFilter.value,
        ReduceDimensionalityTransformation.HighCorrelationFilter.value,
        ReduceDimensionalityTransformation.RandomForest.value,
        ReduceDimensionalityTransformation.PrincipalComponentAnalysis.value,
        ReduceDimensionalityTransformation.SingularValueDecomposition.value
    ]
}
"""
Dictionary with transformation categories and the corresponding transformation,
all in the same place.

Bear in mind that any change in the transformations categories or the 
transformations have to be reflected in the structure above.   
"""


def get_default_datasets():
    """
    Returns the list of default datasets available to the user
    """
    default_datasets = {}
    file_names = os.listdir(c.DEFAULT_DATASETS_PATH)
    for file_name in file_names:
        key = file_name.replace('.csv', '')
        value = c.DEFAULT_DATASETS_PATH + file_name
        default_datasets[key] = value
    return json.dumps(default_datasets)


def get_transformations():
    """
    Returns the list of transformations available to the user
    """
    return Transformations


def execute(
        dataset_name: str,
        dataset_path: str,
        dataset_contents: str,
        transformation_category_value: str,
        transformation_value: str,
        arguments_as_string: str
):
    """
    Perform a transformation on the dataset provided.

    Parameters:
        dataset_name (str): The name of the dataset, used to keep track of the
        transformation.
        dataset_path (str): The path to the dataset. It can be a default one or
        the product of a previously performed transformation.
        dataset_contents (str): The contents of the dataset, if the user chose
        a custom dataset and uploaded it.
        transformation_category_value (str): A string describing the
        category of the transformation to be performed, use to keep track of it
        transformation_value (str): A string describing the transformation to
        be performed
        arguments_as_string (str): A list of arguments in the form of a string.
        Name and value separated with equals sign, couple separated with a coma
    Returns:
        result (JSON): A dictionary with the result of the transformation,
        encoded as a JSON string
    """
    if dataset_contents == "":
        dataset = pd.read_csv(dataset_path)
    else:
        dataset = pd.read_csv(StringIO(dataset_contents))

    try:
        transformation = Transformation(transformation_value)
        arguments = ArgumentsParser.parse(arguments_as_string)
        transformer = Transformer(dataset, transformation, **arguments)
        transformed_dataset = transformer.execute()
    except Exception as exception:
        message = f"{str(exception)}"
        logging.debug(f"{message}")
        raise Exception(message)

    encoded_dataset_name = encode_string(dataset_name)
    encoded_transformation_category_value = encode_string(transformation_category_value)
    encoded_transformation_value = encode_string(transformation_value)
    encoded_transformation = f"{encoded_transformation_category_value}-{encoded_transformation_value}"

    session_id = cherrypy.session["id"]
    transformed_dataset_directory = os.path.join(
        c.TRANSFORMED_DATASETS_PATH,
        session_id
    )
    transformed_dataset_filename = f"{encoded_dataset_name}-{encoded_transformation}.csv"
    transformed_dataset_path = os.path.join(
        transformed_dataset_directory,
        transformed_dataset_filename
    )
    if not os.path.exists(transformed_dataset_directory):
        os.makedirs(transformed_dataset_directory)

    transformed_dataset.to_csv(transformed_dataset_path, index=False)

    transformed_datasets_path = os.path.join(
        c.TRANSFORMED_DATASETS_PATH,
        session_id
    )
    shutil.make_archive(transformed_datasets_path, 'zip', transformed_dataset_directory)

    return json.dumps({
        "dataset_name": dataset_name,
        "transformation_category": transformation_category_value,
        "transformation": transformation_value,
        "arguments": arguments_as_string,
        "url": transformed_dataset_path,
        "zip_url": transformed_datasets_path + ".zip"
    })


def encode_string(string: str) -> str:
    """
    Performs a series of operations in a given string so it can be used as part
    of a file name. Used to set the name of the transformed dataset when saved
    as a CSV file, so the original dataset name, the transformation category,
    and the name of the category can be part of it.

    Work in progress, new substitutions will be added to this method as needed.

    Parameters:
        string (str): The string to be encoded
    Returns:
        encoded_string (str): Encoded string after being transformed
    """
    encoded_string = string
    encoded_string = encoded_string.lower()
    encoded_string = encoded_string.replace(" ", "_")
    encoded_string = encoded_string.replace("(", "")
    encoded_string = encoded_string.replace(")", "")
    return encoded_string
