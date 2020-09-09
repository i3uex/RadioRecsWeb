# CompareFEFS

A comparator for machine learning feature engineering / feature selection techniques

## Table of contents

- [User Interface](#user-interface)
- [Datasets](#datasets)
- [Transformations](#transformations)
    - [Feature Selection](#feature-selection)
    - [Scale - Normalize](#scale---normalize)
    - [Feature Engineering](#feature-engineering)
    - [Encoding](#encoding)
    - [Missing Values](#missing-values)
    - [Reduce Dimensionality](#reduce-dimensionality)
- [Testing Transformations](#testing-transformations)
    - [Feature Selection](#feature-selection-1)
    - [Scale - Normalize](#scale---normalize-1)
    - [Feature Engineering](#feature-engineering-1)
    - [Encoding](#encoding-1)
    - [Missing Values](#missing-values-1)
    - [Reduce Dimensionality](#reduce-dimensionality-1)

## User Interface

CompareFEFS user interface is designed for ease of use. At first, user is presented with a choice: uploading their own dataset or choosing between a selection of default ones.

![User interface: step 1][user_interface_step_1]

Regardless of the choice made, step 2 will be enabled after selecting a dataset, while step 1 will be disabled. If the user needs to change their selection, they will have to reload the page.

![User interface: step 2][user_interface_step_2]

The dataset selected in step 1 will be the option selected in the list **Dataset**. The user then will have to select a category of transformations from list **Transformation Category**. This will populate the list **Transformation**, so the user can make a choice. If the selected transformation needs arguments, the user will be able to introduce them in the text box **Arguments**. All the arguments available for each transformation are described in [Transformations](#transformations).

When all the required values are selected, the button **Transform Dataset** will enable. When the user presses that button, its contents will change to reflect that an operation is being performed. Also, a tip will be shown above it, asking for patience while the operation finishes.

![User interface: step 2 (processing)][user_interface_step_2_processing]

After the dataset is transformed, step 3 will be enabled, showing a line summarizing the transformation, with its position, the source dataset and the details of the transformation performed.

![User interface: step 3][user_interface_step_3]

Users can view or download the transformed dataset using the corresponding links. CSV content will be formatted as table when **View** link is used. Users can download all the transformed datasets in a ZIP file using the link **Download All**. Besides, the transformed dataset will be available as a source dataset in the corresponding list, already selected.

![User interface: step 2 (new dataset)][user_interface_step_2_new_dataset]

Users can repeat step 2 as many times as needed.

![User interface: step 4][user_interface_step_4]

[user_interface_step_1]: images/user_interface_step_1.png "User interface: step 1"
[user_interface_step_2]: images/user_interface_step_2.png "User interface: step 2"
[user_interface_step_2_processing]: images/user_interface_step_2_processing.png "User interface: step 2 (processing)"
[user_interface_step_3]: images/user_interface_step_3.png "User interface: step 3"
[user_interface_step_2_new_dataset]: images/user_interface_step_2_new_dataset.png "User interface: step 2 (new dataset)"
[user_interface_step_4]: images/user_interface_step_4.png "User interface: step 4"

## Datasets

- **iris**: [The iris dataset][iris_dataset_wikipedia] (more about it on [sklearn documentation][iris_dataset_sklearn]).

- **test_iris_with_noise**: Based on [the iris dataset][iris_dataset_wikipedia] (more about it on [sklearn documentation][iris_dataset_sklearn]). It contains ten extra features with uniform noise, so the feature selection techniques are able to discard them. The noise is added as described in ["Feature selection using Python for classification problems"][iris_dataset_add_noise]. The first five rows of this dataset are:

    ```csv
    sepal_length,sepal_width,petal_length,petal_width,noise_feature_0,noise_feature_1,noise_feature_2,noise_feature_3,noise_feature_4,noise_feature_5,noise_feature_6,noise_feature_7,noise_feature_8,noise_feature_9,species
    5.1,3.5,1.4,0.2,0.5434049417909654,0.27836938509379616,0.4245175907491331,0.8447761323199037,0.004718856190972565,0.12156912078311422,0.6707490847267786,0.8258527551050476,0.13670658968495297,0.57509332942725,setosa
    4.9,3.0,1.4,0.2,0.891321954312264,0.20920212211718958,0.18532821955007506,0.10837689046425514,0.21969749262499216,0.9786237847073697,0.8116831490893233,0.1719410127325942,0.8162247487258399,0.2740737470416992,setosa
    4.7,3.2,1.3,0.2,0.4317041836631217,0.9400298196223746,0.8176493787767274,0.3361119501208987,0.17541045374233666,0.37283204628992317,0.005688507352573424,0.25242635344484043,0.7956625084732873,0.01525497124633901,setosa
    4.6,3.1,1.5,0.2,0.5988433769284929,0.6038045390428536,0.10514768541205632,0.38194344494311006,0.03647605659256892,0.8904115634420757,0.9809208570123115,0.05994198881803725,0.8905459447285041,0.5769014994000329,setosa
    5.0,3.6,1.4,0.2,0.7424796890979773,0.6301839364753761,0.5818421923987779,0.020439132026923157,0.2100265776728606,0.5446848781786475,0.7691151711056516,0.2506952291383959,0.2858956904068647,0.8523950878413064,setosa
    ```

    The script used to alter the original dataset is located in **scratches/create_test_iris_with_noise.py**.

- **test_scale_normalize**: A minimal dataset with the only purpose of testing scale/normalize transformations. It is saved as the file **example_datasets/test_scale_normalize.csv** and its contents are:

    ```csv
    feature_1,feature_2
    -1,2
    -0.5,6
    0,10
    1,18
    ```

    The first row gives name to each feature. Taken from ["sklearn.preprocessing.MinMaxScaler"][min_max_scaler].

- **test_feature_engineering_binning:** A minimal dataset with the only purpose of testing binning feature engineering transformation. It is saved as the file **example_datasets/test_feature_engineering_binning.csv** and its contents are:

    ```csv
    feature_1,feature_2,feature_3
    -3.,5.,15
    0.,6.,14
    6.,3.,11
    ```

    The first row gives name to each feature. Taken from ["K-bins discretization"][k_bins].

- **test_feature_engineering_log_transform:** A minimal dataset with the only purpose of testing log transform feature engineering transformation. It is saved as the file **example_datasets/test_feature_engineering_log_transform.csv** and its contents are:

    ```csv
    feature_1,feature_2
    0,1
    2,3
    ```

    The first row gives name to each feature. Taken from ["Custom transformers"][custom_transformers].

- **test_encoding**: A minimal dataset with the only purpose of testing encoding transformations. It is saved as the file **example_datasets/test_encoding.csv** and its contents are:

    ```csv
    Country,Age,Salary,Purchased
    France,44,72000,No
    Spain,27,48000,Yes
    Germany,30,54000,No
    Spain,38,61000,No
    Germany,40,nan,Yes
    France,35,58000,Yes
    Spain,nan,52000,No
    France,48,79000,Yes
    Germany,50,83000,No
    France,37,67000,Yes
    ```

    The first row gives name to each feature. Use first column (feature **Country**) for testing operations. Taken from ["Label Encoder vs. One Hot Encoder in Machine Learning"][label_v_one_hot].

- **test_missing_values**: A minimal dataset with the only purpose of testing transformations. It is saved as the file **example_datasets/test_missing_values.csv** and its contents are:

    ```csv
    feature_1,feature_2
    nan,2
    6,nan
    7,6
    ```

    The first row gives name to each feature. Missing values are marked with `nan`.

- **test_reduce_dimensionality_low_variance**: A minimal dataset with the only purpose of testing reduce dimensionality low variance transformations. It is saved as the file **example_datasets/test_reduce_dimensionality_low_variance.csv** and its contents are:

    ```csv
    feature_1,feature_2,feature_3,feature_4
    0,2,0,3
    0,1,4,3
    0,1,1,3
    ```

    The first row gives name to each feature. Taken from ["sklearn.feature_selection.VarianceThreshold"][variance_threshold].

- **test_reduce_dimensionality_high_correlation**: A minimal dataset with the only purpose of testing reduce dimensionality high correlation transformations. It is saved as the file **example_datasets/test_reduce_dimensionality_high_correlation.csv** and its contents are:

    ```csv
    feature_1,feature_2,feature_3
    1,1,1
    2,2,0
    3,3,1
    4,4,0
    5,5,1
    6,6,0
    7,7,1
    8,7,0
    9,7,1
    ```

    The first row gives name to each feature. Taken from ["Drop Highly Correlated Features"][drop_high_correlated].

- **test_iris_svd**: [The iris dataset][iris_dataset_wikipedia] (more about it on [sklearn documentation][iris_dataset_sklearn]), with the last column values (species) changed to numeric ones.

[iris_dataset_wikipedia]: https://en.wikipedia.org/wiki/Iris_flower_data_set "Iris flower data set"
[iris_dataset_sklearn]: https://scikit-learn.org/stable/auto_examples/datasets/plot_iris_dataset.html "The Iris Dataset"
[iris_dataset_add_noise]: https://towardsdatascience.com/feature-selection-using-python-for-classification-problem-b5f00a1c7028 "Feature selection using Python for classification problems"
[k_bins]: https://scikit-learn.org/stable/modules/preprocessing.html#k-bins-discretization "K-bins discretization"
[custom_transformers]: https://scikit-learn.org/stable/modules/preprocessing.html#custom-transformers "Custom transformers"
[min_max_scaler]: https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.MinMaxScaler.html "sklearn.preprocessing.MinMaxScaler"
[label_v_one_hot]: https://medium.com/@contactsunny/label-encoder-vs-one-hot-encoder-in-machine-learning-3fc273365621 "Label Encoder vs. One Hot Encoder in Machine Learning"
[variance_threshold]: https://scikit-learn.org/stable/modules/generated/sklearn.feature_selection.VarianceThreshold.html "sklearn.feature_selection.VarianceThreshold"
[drop_high_correlated]: https://chrisalbon.com/machine_learning/feature_selection/drop_highly_correlated_features/ "Drop Highly Correlated Features"

## Transformations

### Feature Selection

- **Mutual Information Score**: As described by sklearn: "select features according to the k highest scores." More specifically: "we compare each feature to the target variable, to see whether there is any statistically significant relationship between them.", as explained in ["Feature selection using Python for classification problems"][feature_selection]. Use argument `features_to_select` to choose the number of top features to select (10 by default). Method used to select features is `mutual_info_classif`.

- **Chi-Squared Statistics**: As described by sklearn: "select features according to the k highest scores." More specifically: "we compare each feature to the target variable, to see whether there is any statistically significant relationship between them.", as explained in ["Feature selection using Python for classification problems"][feature_selection]. Use argument `features_to_select` to choose the number of top features to select (10 by default). Method used to select features is `chi2`.

- **Recursive Feature Elimination**: As described in ["Feature selection using Python for classification problems"][feature_selection]: "recursive feature elimination (RFE) is to select features by recursively considering smaller and smaller sets of features." Use argument `features_to_select` to choose the number of top features to select (10 by default).

- **Select From Model**: As described in ["Feature selection using Python for classification problems"][feature_selection]: "features are considered unimportant and removed if the corresponding `coef` or `feature_importances` values are below the provided threshold parameter." Use argument `features_to_select` to choose the number of top features to select (10 by default).

- **Pearson Correlation**: As described by sklearn: "estimate mutual information for a discrete target variable." Use argument `features_to_select` to choose the number of top features to select (10 by default).

[feature_selection]: https://towardsdatascience.com/feature-selection-using-python-for-classification-problem-b5f00a1c7028 "Feature selection using Python for classification problems"

### Scale - Normalize

- **MinMaxScaler**: As described by sklearn: "transforms features by scaling each feature to a given range". Choose min and max range values using arguments `range_min` (defaults to 0) and `range_max` (defaults to 1).

- **StandardScaler**: As described by sklearn: "standardizes features by removing the mean and scaling to unit variance". Use argument `with_mean` to specify if data should be centered before scaling (defaults to True). Use argument `with_std` to specify if data should be scaled to unit variance (defaults to True).

- **RobustScaler**: As described by sklearn: "scales features using statistics that are robust to outliers. This Scaler removes the median and scales the data according to the quantile range (defaults to IQR: Interquartile Range). The IQR is the range between the 1st quartile (25th quantile) and the 3rd quartile (75th quantile)". Use argument `with_centering` to specify if data should be centered before scaling (defaults to True). Use argument `with_scaling` to specify if data should be scaled to interquartile range (defaults to True). Choose min and max quantile range values using arguments `quantile_range_min` (defaults to 25.0) and `quantile_range_max` (defaults to 75.0).

- **Normalizer**: As described by sklearn: "normalizes samples individually to unit norm", that is, it works on individual rows instead of columns, samples instead of features. Use argument `norm` to specify the norm to use when normalizing each sample. Possible values are `l1`, `l2`, and `max`.

### Feature Engineering

- **Binning**: As described by sklearn: "discretizes features into k bins", that is, creates a concrete number of bins so the value of each feature can be put inside one of those bins. Use argument `n_bins` to specify how many bins to create for each feature. For example, if the dataset has three features, use `n_bins=[3, 2, 2]` to create 3 bins for feature 1, 2 for feature 2, and 2 for feature 3. Default value is `[5]` (it assumes your dataset has a single feature). Use parameter `encode` to choose between values `onehot` (default), `onehot-dense`, and `ordinal`. Use argument `strategy` to choose between values `uniform`, `quantile` (default), and `kmeans`.

- **LogTransform**: Logarithmic transformation of data to handle skew, adapt magnitude order, and decrease the effect of outliers. No arguments needed.

### Encoding

- **Label Encoding**: Translate into numbers any categorical or textual data, from 0 to the number of different elements - 1. Choose between features using the argument `feature_position`, a 0-based index. If not present, the transformer will try to label-encode the first feature (that is, the one with index 0).

- **One-Hot Encoding**: Translate into numbers any categorical or textual data in a way that no hierarchy or order can be inferred from it. A new feature will be created for each different value present in the original feature, with value 1 where the original value was present, and 0 where it wasn't. Choose between features using the argument `feature_position`, a 0-based index. If not present, the transformer will try to one-hot-encode the first feature (that is, the one with index 0).

### Missing Values

- **Delete Instance (Row)**: Delete any row with missing values. sklearn does not offer a transformer to perform this operation, so it has been implemented using pandas, replacing any missing values with NaN and, then, dropping the rows that contain it.

- **Statistics (Mean, Median, Most Frequent)**: Replaces the missing values with the resulting value of performing an statistical operation over the known values (in this case, the mean, the median, or the most repeated value). Choose between them using the argument `strategy`, with values `mean`, `median`, and `most_frequent`. Default strategy is `mean`. More at [sklearn documentation][univariate_feature_imputation].

- **Constant**: Replaces the missing values with the constant provided. Set the constant of your choice using argument `fill_value`. Its default value is 1. Actually, this is another variant of statistical replacement. More at [sklearn documentation][univariate_feature_imputation].

- **Nearest Neighbors**: Use nearest neighbors values to impute the missing values. Use argument `n_neighbors` to select the number of neighbors used for the imputation. Use argument `weights` to choose between `uniform` (default) or `distance`. More at [sklearn documentation][nearest_neighbors_imputation].

[univariate_feature_imputation]: https://scikit-learn.org/stable/modules/impute.html#univariate-feature-imputation "Univariate feature imputation"
[nearest_neighbors_imputation]: https://scikit-learn.org/stable/modules/impute.html#nearest-neighbors-imputation "Nearest neighbors imputation"

### Reduce Dimensionality

- **Low Variance Filter**: As described by sklearn: "Feature selector that removes all low-variance features." Use argument `threshold` to set the variance threshold, defaults to `0`.

- **High Correlation Filter**: Feature selector that removes all high-correlated features. Use argument `threshold` to set the correlation threshold, defaults to `0.95`.

- **Random Forest**: As described in ["Dimensionality Reduction Via Sequential Feature Selection / Assessing Feature Importance Via Random Forests"][bogotobogo]: "As an ensemble learning method for classification and regression, random forests or random decision forests operates by constructing a multitude of decision trees at training time and outputting the class (classification) or mean prediction (regression) of the individual trees." Use argument `features_to_select` to choose the number of top features to select (10 by default).

- **PCA (Principal Component Analysis)**: As described by sklearn: "PCA is used to decompose a multivariate dataset in a set of successive orthogonal components that explain a maximum amount of the variance." Use argument `n_components` to set the number of principal components derived from the original dataset (defaults to 10).

- **SVD (Singular Value Decomposition)**: As described by sklearn: "This transformer performs linear dimensionality reduction by means of truncated singular value decomposition (SVD)." Use argument `n_components` to set the number of principal components derived from the original dataset (defaults to 2).

[bogotobogo]: https://www.bogotobogo.com/python/scikit-learn/scikit_machine_learning_Data_Preprocessing-III-Dimensionality-reduction-via-Sequential-feature-selection-Assessing-feature-importance-via-random-forests.php "SCIKIT-LEARN : DATA PREPROCESSING III - DIMENSIONALITY REDUCTION VIA SEQUENTIAL FEATURE SELECTION / ASSESSING FEATURE IMPORTANCE VIA RANDOM FORESTS"

## Testing Transformations

### Feature Selection

- **Mutual Information Score**: Select dataset **test_iris_with_noise**, mark option **Feature Selection > Mutual Information Score**, pass argument `features_to_select=4`, to see if selected features matches those of the original dataset. Resulting dataset should contain features `sepal_length`, `sepal_width`, `petal_length`, `petal_width`, and target `species`, removing all noise features.

- **Chi-Squared Statistics**: Select dataset **test_iris_with_noise**, mark option **Feature Selection > Chi-Squared Statistics**, pass argument `features_to_select=4`, to see if selected features matches those of the original dataset. Resulting dataset should contain features `sepal_length`, `sepal_width`, `petal_length`, `petal_width`, and target `species`, removing all noise features.

- **Recursive Feature Elimination**: Select dataset **test_iris_with_noise**, mark option **Feature Selection > Recursive Feature Elimination**, pass argument `features_to_select=4`, to see if selected features matches those of the original dataset. Resulting dataset should contain features `sepal_length`, `sepal_width`, `petal_length`, `petal_width`, and target `species`, removing all noise features.

- **Select From Model**: Select dataset **test_iris_with_noise**, mark option **Feature Selection > Select From Model**, pass argument `features_to_select=4`, to see if selected features matches those of the original dataset. Resulting dataset should contain features `sepal_length`, `sepal_width`, `petal_length`, `petal_width`, and target `species`, removing all noise features.

- **Pearson Correlation**: Select dataset **test_iris_with_noise**, mark option **Feature Selection > Pearson Correlation**, pass argument `features_to_select=4`, to see if selected features matches those of the original dataset. Resulting dataset should contain features `sepal_length`, `sepal_width`, `petal_length`, `petal_width`, and target `species`, removing all noise features.

### Scale - Normalize

- **MinMaxScaler**: Select dataset **test_scaler_normalize**, mark option **Scale - Normalize > MinMaxScaler**. Resulting dataset should be:

    ```csv
    feature_1,feature_2
    0.0,0.0
    0.25,0.25
    0.5,0.5
    1.0,1.0
    ```

- **StandardScaler**: Select dataset **test_scaler_normalize**, mark option **Scale - Normalize > StandardScaler**. Resulting dataset should be:

    ```csv
    feature_1,feature_2
    -1.1832159566199232,-1.1832159566199232
    -0.50709255283711,-0.50709255283711
    0.1690308509457033,0.1690308509457033
    1.52127765851133,1.52127765851133
    ```

- **RobustScaler**: Select dataset **test_scaler_normalize**, mark option **Scale - Normalize > RobustScaler**. Resulting dataset should be:

    ```csv
    feature_1,feature_2
    -0.8571428571428571,-0.8571428571428571
    -0.2857142857142857,-0.2857142857142857
    0.2857142857142857,0.2857142857142857
    1.4285714285714286,1.4285714285714286
    ```

- **Normalizer**: Select dataset **test_scaler_normalize**, mark option **Scale - Normalize > Normalizer**. Resulting dataset should be:

    ```csv
    feature_1,feature_2
    -0.4472135954999579,0.8944271909999159
    -0.08304547985373997,0.9965457582448796
    0.0,1.0
    0.05547001962252291,0.9984603532054125
    ```

### Feature Engineering

- **Binning**: Select dataset **test_feature_engineering_binning**, mark option **Feature Engineering > Binning**. Use arguments `n_bins=[3, 2, 2], encode=ordinal`. Resulting dataset should be:

    ```csv
    feature_1,feature_2,feature_3
    0.0,1.0,1.0
    1.0,1.0,1.0
    2.0,0.0,0.0
    ```

- **LogTransform**: Select dataset **test_feature_engineering_log_transform**, mark option **Feature Engineering > LogTransform**. Resulting dataset should be:

    ```csv
    feature_1,feature_2
    0.0,0.6931471805599453
    1.0986122886681098,1.3862943611198906
    ```

### Encoding

- **Label Encoding**: Select dataset **test_encoding**, mark option **Encoding > Label Encoding**. Resulting dataset should be:

    ```csv
    Country,Age,Salary,Purchased
    0,44.0,72000.0,No
    2,27.0,48000.0,Yes
    1,30.0,54000.0,No
    2,38.0,61000.0,No
    1,40.0,,Yes
    0,35.0,58000.0,Yes
    2,,52000.0,No
    0,48.0,79000.0,Yes
    1,50.0,83000.0,No
    0,37.0,67000.0,Yes
    ```

- **One-Hot Encoding**: Select dataset **test_encoding**, mark option **Encoding > One-Hot Encoding**. Resulting dataset should be:

    ```csv
    Country_France,Country_Germany,Country_Spain,Age,Salary,Purchased
    1,0,0,44.0,72000.0,No
    0,0,1,27.0,48000.0,Yes
    0,1,0,30.0,54000.0,No
    0,0,1,38.0,61000.0,No
    0,1,0,40.0,,Yes
    1,0,0,35.0,58000.0,Yes
    0,0,1,,52000.0,No
    1,0,0,48.0,79000.0,Yes
    0,1,0,50.0,83000.0,No
    1,0,0,37.0,67000.0,Yes
    ```

### Missing Values

- **Delete Instance (Row)**: Select dataset **test_missing_values**, mark option **Missing Values > Delete Instance (Row)**. Resulting dataset should be:

    ```csv
    feature_1,feature_2
    7,6
    ```

- **Statistics (Mean, Median, Most Frequent)**: Select dataset **test_missing_values**, mark option **Missing Values > Statistics (Mean, Median, Most Frequent)**. Resulting dataset with mean operation should be:

    ```csv
    feature_1,feature_2
    6.5,2.0
    6.0,4.0
    7.0,6.0
    ```

    Resulting dataset with median operation should be:

    ```csv
    feature_1,feature_2
    6.5,2.0
    6.0,4.0
    7.0,6.0
    ```

    Resulting dataset with most frequent operation should be:

    ```csv
    feature_1,feature_2
    6.0,2.0
    6.0,2.0
    7.0,6.0
    ```

- **Constant**: Select dataset **test_missing_values**, mark option **Missing Values > Constant**. If `fill_value` were 3, resulting dataset should be:

    ```csv
    feature_1,feature_2
    3.0,2.0
    6.0,3.0
    7.0,6.0
    ```

- **Nearest Neighbors**: Select dataset **test_missing_values**, mark option **Missing Values > Nearest Neighbors**. Resulting dataset should be:

    ```csv
    feature_1,feature_2
    6.5,2.0
    6.0,4.0
    7.0,6.0
    ```

### Reduce Dimensionality

- **Low Variance Filter**: Select dataset **test_reduce_dimensionality_low_variance**, mark option **Reduce Dimensionality > Low Variance Filter**. Resulting dataset should be:

    ```csv
    feature_2,feature_3
    2,0
    1,4
    1,1
    ```

- **Low Variance Filter**: Select dataset **test_reduce_dimensionality_high_correlation**, mark option **Reduce Dimensionality > Low Variance Filter**. Resulting dataset should be:

    ```csv
    feature_1,feature_3
    1,1
    2,0
    3,1
    4,0
    5,1
    6,0
    7,1
    8,0
    9,1
    ```

- **Random Forest**: Select dataset **test_iris_with_noise**, mark option **Reduce Dimensionality > Random Forest**, pass argument `features_to_select=4`, to see if selected features matches those of the original dataset. Resulting dataset should contain features `sepal_length`, `sepal_width`, `petal_length`, `petal_width`, and target `species`, removing all noise features.

- **PCA (Principal Component Analysis)**: Select dataset **iris**, mark option **Reduce Dimensionality > PCA (Principal Component Analysis)**, pass argument `n_components=2`. Resulting dataset should contain two features: `principal_component_1` and `principal_component_2`. Its first 5 rows should be:

    ```csv
    principal_component_1,principal_component_2,species
    -2.6842071251039483,0.3266073147643885,setosa
    -2.71539061563413,-0.16955684755602624,setosa
    -2.889819539617916,-0.13734560960502795,setosa
    -2.746437197308734,-0.31112431575199184,setosa
    -2.7285929818313144,0.33392456356845474,setosa
    ```

- **SVD (Singular Value Decomposition)**: Select dataset **test_iris_svd**, mark option **Reduce Dimensionality > SVD (Singular Value Decomposition)**, pass argument `n_components=2`. Resulting dataset should contain two features: `principal_component_1` and `principal_component_2`. Its first 5 rows should be approximately like this:

    ```csv
    principal_component_1,principal_component_2
    5.846721793908344,2.4631425165863856
    5.510740429469278,2.1399791751434263
    5.386211654146823,2.2455666879471825
    5.376300486457194,2.037000549210129
    5.809921203603052,2.484580867908297
    ```
