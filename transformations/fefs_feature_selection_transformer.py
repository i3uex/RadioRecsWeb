import logging
from enum import Enum

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SelectKBest, mutual_info_classif, chi2, RFE, SelectFromModel, f_classif
from sklearn.linear_model import LogisticRegression

from arguments import ArgumentDescriptor, ArgumentsParser
from transformations import FeatureSelectionTransformation


class FeatureSelectionTransformerSelector(Enum):
    MutualInformationClassifier = "MutualInformationClassifier"
    ChiSquared = "ChiSquared"
    RandomForestClassifier = "RandomForestClassifier"
    LogisticRegressionClassifier = "LogisticRegressionClassifier"
    RegressionClassifier = "RegressionClassifier"


class FeatureSelectionTransformerArgument(ArgumentDescriptor, Enum):
    FeaturesToSelect = ArgumentDescriptor("features_to_select", 10)


class FeatureSelectionTransformer:
    dataset = None
    transformation = None
    arguments = None

    def __init__(self, dataset, transformation, **arguments):
        logging.debug(f"FeatureSelectionTransformer.__init__()")
        self.dataset = dataset
        self.transformation = transformation
        self.arguments = arguments

    def execute(self):
        logging.debug(f"FeatureSelectionTransformer.execute()")
        try:
            if self.transformation == FeatureSelectionTransformation.MutualInformationScore:
                return self._mutual_information_score()
            elif self.transformation == FeatureSelectionTransformation.ChiSquaredStatistics:
                return self._chi_squared_statistics()
            elif self.transformation == FeatureSelectionTransformation.RecursiveFeatureElimination:
                return self._recursive_feature_elimination()
            elif self.transformation == FeatureSelectionTransformation.SelectFromModel:
                return self._select_from_model()
            elif self.transformation == FeatureSelectionTransformation.PearsonCorrelation:
                return self._pearson_correlation()
            else:
                message = f"Transformation not supported: {self.transformation}"
                logging.debug(f"{message}")
                raise Exception(message)
        except RuntimeError as error:
            message = f"{str(error)}"
            logging.debug(f"{message}")
            raise Exception(message)

    def _mutual_information_score(self):
        """
        As described by sklearn: "select features according to the k highest
        scores." More specifically: "we compare each feature to the target
        variable, to see whether there is any statistically significant
        relationship between them.", as explained in "Feature selection using
        Python for classification problems". Use argument features_to_select to
        choose the number of top features to select (10 by default). Method
        used to select features is mutual_info_classif().

        https://towardsdatascience.com/feature-selection-using-python-for-classification-problem-b5f00a1c7028
        """
        logging.debug(f"FeatureSelectionTransformer._mutual_information_score()")
        return self._select_features(FeatureSelectionTransformerSelector.MutualInformationClassifier)

    def _chi_squared_statistics(self):
        """
        As described by sklearn: "select features according to the k highest
        scores." More specifically: "we compare each feature to the target
        variable, to see whether there is any statistically significant
        relationship between them.", as explained in "Feature selection using
        Python for classification problems". Use argument features_to_select to
        choose the number of top features to select (10 by default). Method
        used to select features is chi2.

        https://towardsdatascience.com/feature-selection-using-python-for-classification-problem-b5f00a1c7028
        """
        logging.debug(f"FeatureSelectionTransformer._chi_squared_statistics()")
        return self._select_features(FeatureSelectionTransformerSelector.ChiSquared)

    def _recursive_feature_elimination(self):
        """
        As described in "Feature selection using Python for classification
        problems": "recursive feature elimination (RFE) is to select features
        by recursively considering smaller and smaller sets of features." Use
        argument features_to_select to choose the number of top features to
        select (10 by default).

        https://towardsdatascience.com/feature-selection-using-python-for-classification-problem-b5f00a1c7028
        """
        logging.debug(f"FeatureSelectionTransformation._recursive_feature_elimination()")
        return self._select_features(FeatureSelectionTransformerSelector.RandomForestClassifier)

    def _select_from_model(self):
        """
        As described in "Feature selection using Python for classification
        problems": "features are considered unimportant and removed if the
        corresponding coef or feature_importances values are below the provided
        threshold parameter." Use argument features_to_select to choose the
        number of top features to select (10 by default).

        https://towardsdatascience.com/feature-selection-using-python-for-classification-problem-b5f00a1c7028
        """
        logging.debug(f"FeatureSelectionTransformation._select_from_model()")
        return self._select_features(FeatureSelectionTransformerSelector.LogisticRegressionClassifier)

    def _pearson_correlation(self):
        """
        As described by sklearn: "estimate mutual information for a discrete
        target variable." Use argument features_to_select to choose the number
        of top features to select (10 by default).
        """
        logging.debug(f"FeatureSelectionTransformation._pearson_correlation()")
        return self._select_features(FeatureSelectionTransformerSelector.RegressionClassifier)

    def _select_features(self, selector_name):
        logging.debug(f"FeatureSelectionTransformer._select_k_best(\"{selector_name}\")")

        arguments_parser = ArgumentsParser(self.arguments)
        features_to_select = arguments_parser.get_int(FeatureSelectionTransformerArgument.FeaturesToSelect)

        logging.debug(f"- {FeatureSelectionTransformerArgument.FeaturesToSelect.key}: {features_to_select}")

        columns = self.dataset.columns

        data = self.dataset.iloc[:, :-1]
        target = self.dataset.iloc[:, -1]
        selector = FeatureSelectionTransformer._get_selector(
            selector_name=selector_name,
            features_to_select=features_to_select
        )
        selected_features = selector.fit_transform(data, target)

        transformed_dataset_features = pd.DataFrame(data=selected_features)
        transformed_dataframe_target = pd.DataFrame(data=target)
        transformed_dataset = pd.concat([transformed_dataset_features, transformed_dataframe_target], axis=1)

        selected_columns = []
        support = selector.get_support()
        for index, selected in enumerate(support):
            if selected:
                selected_columns.append(columns[index])
        selected_columns.append(columns[-1])

        transformed_dataset.columns = selected_columns
        return transformed_dataset

    @staticmethod
    def _get_selector(selector_name, features_to_select):
        if selector_name == FeatureSelectionTransformerSelector.MutualInformationClassifier:
            return SelectKBest(mutual_info_classif, k=features_to_select)
        elif selector_name == FeatureSelectionTransformerSelector.ChiSquared:
            return SelectKBest(chi2, k=features_to_select)
        elif selector_name == FeatureSelectionTransformerSelector.RandomForestClassifier:
            random_forest_classifier = RandomForestClassifier(random_state=100, n_estimators=50)
            return RFE(estimator=random_forest_classifier, n_features_to_select=features_to_select, step=1)
        elif selector_name == FeatureSelectionTransformerSelector.LogisticRegressionClassifier:
            model_logistic = LogisticRegression(solver='saga', multi_class='multinomial', max_iter=10000, penalty='l1')
            return SelectFromModel(estimator=model_logistic, max_features=features_to_select)
        elif selector_name == FeatureSelectionTransformerSelector.RegressionClassifier:
            return SelectKBest(f_classif, k=features_to_select)
