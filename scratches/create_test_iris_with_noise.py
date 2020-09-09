import numpy as np
import pandas as pd
from sklearn.datasets import load_iris

"""
Loads Iris dataset, adds ten new features with uniform noise and saves them
before the target (species). Use the generated dataset with transformations
that can reduce dimensionality searching for features that have no relation
with the target.
"""

iris = load_iris()
X = iris.data
y = iris.target

noise_features = 10
np.random.seed(100)
E = np.random.uniform(0, 1, size=(len(X), noise_features))
X = np.hstack((X, E))
print(X.shape)

noise_columns = []
for index in range(noise_features):
    noise_columns.append(f"noise_feature_{index}")

columns = ["sepal_length", "sepal_width", "petal_length", "petal_width", *noise_columns, "species"]

dataframe_data = pd.DataFrame(data=X)
dataframe_target = pd.DataFrame(data=y)
dataframe = pd.concat([dataframe_data, dataframe_target], axis=1)
dataframe.columns = columns
dataframe.to_csv("iris_with_noise.csv", index=False)
