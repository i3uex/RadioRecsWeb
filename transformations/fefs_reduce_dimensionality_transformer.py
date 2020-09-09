import logging
from enum import Enum

import numpy as np
import pandas as pd
from sklearn.decomposition import PCA, TruncatedSVD
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import VarianceThreshold

from arguments import ArgumentDescriptor, ArgumentsParser
from transformations import ReduceDimensionalityTransformation


class ReduceDimensionalityTransformerArgument(ArgumentDescriptor, Enum):
    VarianceThreshold = ArgumentDescriptor("threshold", 0.0)
    CorrelationThreshold = ArgumentDescriptor("threshold", 0.95)
    FeaturesToSelect = ArgumentDescriptor("features_to_select", 10)
    PCAComponents = ArgumentDescriptor("n_components", 10)
    SVDComponents = ArgumentDescriptor("n_components", 2)


class ReduceDimensionalityTransformer:
    dataset = None
    transformation = None
    arguments = None

    def __init__(self, dataset, transformation, **arguments):
        logging.debug(f"ReduceDimensionalityTransformer.__init__()")
        self.dataset = dataset
        self.transformation = transformation
        self.arguments = arguments

    def execute(self):
        logging.debug(f"ReduceDimensionalityTransformer.execute()")
        try:
            if self.transformation == ReduceDimensionalityTransformation.LowVarianceFilter:
                return self._low_variance_filter()
            elif self.transformation == ReduceDimensionalityTransformation.HighCorrelationFilter:
                return self._high_correlation_filter()
            elif self.transformation == ReduceDimensionalityTransformation.RandomForest:
                return self._random_forest()
            elif self.transformation == ReduceDimensionalityTransformation.PrincipalComponentAnalysis:
                return self._principal_component_analysis()
            elif self.transformation == ReduceDimensionalityTransformation.SingularValueDecomposition:
                return self._singular_value_decomposition()
            else:
                message = f"Transformation not supported: {self.transformation}"
                logging.debug(f"{message}")
                raise Exception(message)
        except RuntimeError as error:
            message = f"{str(error)}"
            logging.debug(f"{message}")
            raise Exception(message)

    def _low_variance_filter(self):
        """
        As described by sklearn: "Feature selector that removes all
        low-variance features." Use argument threshold to set the variance
        threshold, defaults to 0.
        """
        logging.debug(f"ReduceDimensionalityTransformer._low_variance_filter()")

        arguments_parser = ArgumentsParser(self.arguments)
        threshold = arguments_parser.get_float(ReduceDimensionalityTransformerArgument.VarianceThreshold)

        logging.debug(f"- {ReduceDimensionalityTransformerArgument.VarianceThreshold.key}: {threshold}")

        columns = self.dataset.columns

        selector = VarianceThreshold(
            threshold=threshold
        )
        selected_features = selector.fit_transform(self.dataset)
        transformed_dataset = pd.DataFrame(data=selected_features)

        selected_columns = []
        support = selector.get_support()
        for index, selected in enumerate(support):
            if selected:
                selected_columns.append(columns[index])

        transformed_dataset.columns = selected_columns
        return transformed_dataset

    def _high_correlation_filter(self):
        """
        Feature selector that removes all high-correlated features. Use
        argument threshold to set the correlation threshold, defaults to 0.95.
        """
        logging.debug(f"ReduceDimensionalityTransformer._high_correlation_filter()")

        arguments_parser = ArgumentsParser(self.arguments)
        threshold = arguments_parser.get_float(ReduceDimensionalityTransformerArgument.CorrelationThreshold)

        logging.debug(f"- {ReduceDimensionalityTransformerArgument.CorrelationThreshold.key}: {threshold}")

        correlation_matrix = self.dataset.corr().abs()
        upper_triangle = correlation_matrix.where(np.triu(np.ones(correlation_matrix.shape), k=1).astype(np.bool))
        features_to_drop = [column for column in upper_triangle.columns if any(upper_triangle[column] > threshold)]
        transformed_dataset = self.dataset.drop(self.dataset[features_to_drop], axis=1)

        return transformed_dataset

    def _random_forest(self):
        """
        As described in "Dimensionality Reduction Via Sequential Feature
        Selection / Assessing Feature Importance Via Random Forests": "As an
        ensemble learning method for classification and regression, random
        forests or random decision forests operates by constructing a multitude
        of decision trees at training time and outputting the class
        (classification) or mean prediction (regression) of the individual
        trees." Use argument features_to_select to choose the number of top
        features to select (10 by default).

        https://www.bogotobogo.com/python/scikit-learn/scikit_machine_learning_Data_Preprocessing-III-Dimensionality-reduction-via-Sequential-feature-selection-Assessing-feature-importance-via-random-forests.php
        """
        logging.debug(f"ReduceDimensionalityTransformer._random_forest()")

        arguments_parser = ArgumentsParser(self.arguments)
        features_to_select = arguments_parser.get(ReduceDimensionalityTransformerArgument.FeaturesToSelect)

        logging.debug(f"- {ReduceDimensionalityTransformerArgument.FeaturesToSelect.key}: {features_to_select}")

        data = self.dataset.iloc[:, :-1]
        target = self.dataset.iloc[:, -1]

        random_forest_classifier = RandomForestClassifier(n_estimators=1000, random_state=0, n_jobs=-1)
        random_forest_classifier.fit(data, target)
        importances = random_forest_classifier.feature_importances_
        indices = np.argsort(importances)[::-1]

        transformed_dataset = None
        if len(indices) > 0:
            transformed_dataset = data[data.columns[0]]
            for index in range(1, len(indices)):
                if index == features_to_select:
                    break
                transformed_dataset = pd.concat([transformed_dataset, data[data.columns[index]]], axis=1)
            transformed_dataset = pd.concat([transformed_dataset, target], axis=1)

        return transformed_dataset

    def _principal_component_analysis(self):
        """
        As described by sklearn: "PCA is used to decompose a multivariate
        dataset in a set of successive orthogonal components that explain a
        maximum amount of the variance." Use argument n_components to set the
        number of principal components derived from the original dataset
        (defaults to 10).
        """
        logging.debug(f"ReduceDimensionalityTransformer._principal_component_analysis()")

        arguments_parser = ArgumentsParser(self.arguments)
        n_components = arguments_parser.get_int(ReduceDimensionalityTransformerArgument.PCAComponents)

        logging.debug(f"- {ReduceDimensionalityTransformerArgument.PCAComponents.key}: {n_components}")

        data = self.dataset.iloc[:, :-1]
        target = self.dataset.iloc[:, -1]

        pca = PCA(n_components=n_components)
        principal_components = pca.fit_transform(data)

        transformed_columns = []
        for index in range(n_components):
            transformed_columns.append(f"principal_component_{index + 1}")
        transformed_dataset = pd.DataFrame(data=principal_components, columns=transformed_columns)
        transformed_dataset = pd.concat([transformed_dataset, target], axis=1)

        return transformed_dataset

    def _singular_value_decomposition(self):
        """
        As described by sklearn: "This transformer performs linear
        dimensionality reduction by means of truncated singular value
        decomposition (SVD)." Use argument n_components to set the number of
        principal components derived from the original dataset (defaults to 2).
        """
        logging.debug(f"ReduceDimensionalityTransformer._singular_value_decomposition()")

        arguments_parser = ArgumentsParser(self.arguments)
        n_components = arguments_parser.get_int(ReduceDimensionalityTransformerArgument.SVDComponents)

        logging.debug(f"- {ReduceDimensionalityTransformerArgument.SVDComponents.key}: {n_components}")

        svd = TruncatedSVD(n_components=n_components)
        principal_components = svd.fit_transform(self.dataset)

        transformed_columns = []
        for index in range(n_components):
            transformed_columns.append(f"principal_component_{index + 1}")

        return pd.DataFrame(data=principal_components, columns=transformed_columns)
