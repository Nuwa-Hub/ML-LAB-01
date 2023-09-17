# -*- coding: utf-8 -*-
"""ml-lab1-label1-190458t.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1t0dCfkqUwvsGZ3vTkP_fEFjrSKXFrMMt

Import necssary libraries and modules
"""

#import libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split

from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC

from sklearn.metrics import accuracy_score, precision_score, recall_score

"""Import training, validation and testing datasets"""

# Load the train dataset
train_data = pd.read_csv('/kaggle/input/lab1-train/train.csv')
# Load the valid dataset
valid_data = pd.read_csv('/kaggle/input/lab1-valid/valid.csv')
# Load the valid dataset
test_data = pd.read_csv('/kaggle/input/lab1-test/test.csv')

"""Visualize original training data"""

train_data.head()

"""Process the data to remove null values for labels and estimate missing values in features

Drop the columns where there are null values for the lables in the training dataset
"""

# Check for null values in train dataset
train_null_counts = train_data.isnull().sum()
print("train null counts : \n {}".format(train_null_counts))

# Drop rows with null values in the final four columns (target labels) for train dataset
train_data = train_data.dropna(subset=train_data.columns[-4:], how='any')

"""Fill the null values in the features with their means in the train, valid and test datasets."""

# Fill null values with mean in train dataset
train_data = train_data.fillna(train_data.mean())

# Fill null values with mean in valid dataset
valid_data = valid_data.fillna(valid_data.mean())

# Fill null values with mean in test dataset
test_data = test_data.fillna(test_data.mean())



"""Visualize processed training data"""

train_data.head()

"""Separate features and labels in the train, valid and test datasets"""

# Separate features and labels in train dataset
train_features = train_data.iloc[:, :-4]
train_labels = train_data.iloc[:, -4:]

# Separate features and labels in valid dataset
valid_features = valid_data.iloc[:, :-4]
valid_labels = valid_data.iloc[:, -4:]

# Separate features and labels in test dataset
test_features = test_data.iloc[:, :-4]
test_labels = test_data.iloc[:, -4:]

"""Extract the first label in the train, valid and test datasets"""

# get the first label of the train dataset
train_label1 = train_labels.iloc[:,0]

# get the first label of the valid dataset
valid_label1 = valid_labels.iloc[:,0]

# get the first label of the test dataset
test_label1 = test_labels.iloc[:,0]

"""# Predicting Label 1 without Feature Engineering

Predict label 1 without feature engineering steps and techniques

Make copies of the features and labels of the datasets to be used in the models without feature engineering
"""

# Make a copy features and labels in train dataset
train_features_copy = train_features.copy()
train_labels_copy = train_labels.copy()

# Make a copy features and labels in valid dataset
valid_features_copy = valid_features.copy()
valid_labels_copy = valid_labels.copy()

# Make a copy features and labels in test dataset
test_features_copy = test_features.copy()
test_labels_copy = test_labels.copy()

"""Make copies of the label 1 of the datasets to be used in the models without feature engineering"""

# Make a copy of the first label of the train dataset
train_label1_copy = train_label1.copy()

# Make a copy of the first label of the valid dataset
valid_label1_copy = valid_label1.copy()

# Make a copy of the first label of the test dataset
test_label1_copy = test_label1.copy()

"""Standardize the features of all datasets"""

# Standardize the features
scaler = StandardScaler()
train_features_copy = scaler.fit_transform(train_features_copy)
valid_features_copy = scaler.transform(valid_features_copy)
test_features_copy = scaler.transform(test_features_copy)

"""Use the raw scaled features to train the best model which is SVM"""

best_model = SVC()

best_model.fit(train_features_copy, train_label1_copy)

"""Used the trained model on all features to predict the valid and test data and get metrics"""

# Predict on the train data
y_pred_base_train = best_model.predict(train_features_copy)

# Calculate metrics for classification evaluation
accuracy = accuracy_score(train_label1_copy, y_pred_base_train)
precision = precision_score(train_label1_copy, y_pred_base_train, average='weighted' , zero_division=1)
recall = recall_score(train_label1_copy, y_pred_base_train, average='weighted')

print(f"Metrics for SVM on train data:")
print(f"Accuracy: {accuracy:.2f}")
print(f"Precision: {precision:.2f}")
print(f"Recall: {recall:.2f}")
print("\n")

# Predict on the validation data
y_pred_base_valid = best_model.predict(valid_features_copy)

# Calculate metrics for classification evaluation on validation data
accuracy = accuracy_score(valid_label1_copy, y_pred_base_valid)
precision = precision_score(valid_label1_copy, y_pred_base_valid, average='weighted', zero_division=1)
recall = recall_score(valid_label1_copy, y_pred_base_valid, average='weighted')

print(f"Metrics for SVM on valid data:")
print(f"Accuracy: {accuracy:.2f}")
print(f"Precision: {precision:.2f}")
print(f"Recall: {recall:.2f}")
print("\n")

# Predict on the test data
y_pred_base_test = best_model.predict(test_features_copy)

# Calculate metrics for classification evaluation on test data
accuracy = accuracy_score(test_label1_copy, y_pred_base_test)
precision = precision_score(test_label1_copy, y_pred_base_test, average='weighted', zero_division=1)
recall = recall_score(test_label1_copy, y_pred_base_test, average='weighted')

print(f"Metrics for SVM on test data:")
print(f"Accuracy: {accuracy:.2f}")
print(f"Precision: {precision:.2f}")
print(f"Recall: {recall:.2f}")
print("\n")

"""# Predicting Label 1 with Feature Engineering

Predict label 1 with feature engineering steps and techniques

## Feature Engineering

Use feature selection based on correlation matrix and feature extraction based on PCA

### Feature Selection

Visualize the distribution of the training label 1
"""

# Plotting the distribution of train_label1
labels, counts = np.unique(train_label1, return_counts=True)

# Create a more readable distribution plot using Seaborn
plt.figure(figsize=(10, 6))
sns.countplot(x=train_label1)
plt.xlabel('Target Label 1')
plt.ylabel('Frequency')
plt.title('Distribution of Target Label 1')
plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
plt.tight_layout()
plt.show()

"""Calculate the correlation matrix of the training data features"""

#Calculate the correlation matrix
correlation_matrix = train_features.corr()

mask = np.triu(np.ones_like(correlation_matrix))

# Create a heatmap of the correlation matrix using seaborn
plt.figure(figsize=(12, 12))
sns.heatmap(correlation_matrix, cmap='coolwarm', center=0, mask=mask)
plt.title("Correlation Matrix")
plt.show()

"""Identify the features that are highly correlated with each other using the traning dataset"""

# Set the threshold for correlation
correlation_threshold = 0.9

highly_correlated = set()

# Find highly correlated features
for i in range(len(correlation_matrix.columns)):
    for j in range(i):
        if abs(correlation_matrix.iloc[i, j]) > correlation_threshold:
            colname = correlation_matrix.columns[i]
            highly_correlated.add(colname)

print(highly_correlated)

"""Remove the previously identified highly correlated features from all the datasets"""

# Remove highly correlated features
train_features = train_features.drop(columns=highly_correlated)
valid_features = valid_features.drop(columns=highly_correlated)
test_features = test_features.drop(columns=highly_correlated)

"""Display the resulting feature shapes of the datasets"""

# Display the filtered train feature count
print("Filtered train features: {}".format(train_features.shape))

# Display the filtered valid feature count
print("Filtered valid features: {}".format(valid_features.shape))

# Display the filtered test feature count
print("Filtered test features: {}".format(test_features.shape))

"""Identify the features that are highly correlated with the label using the traning dataset"""

# Calculate the correlation matrix between features and train_label1
correlation_with_target = train_features.corrwith(train_label1)

# Set the correlation threshold
correlation_threshold = 0.05

# Select features that meet the correlation threshold
highly_correlated_features = correlation_with_target[correlation_with_target.abs() > correlation_threshold]

print(highly_correlated_features)

"""Extract the features that are only highly correlated with the label from all datasets"""

# Drop the features with low correlated in train data
train_features = train_features[highly_correlated_features.index]

# Drop the features with low correlated in valid data
valid_features = valid_features[highly_correlated_features.index]

# Drop the features with low correlated in test data
test_features = test_features[highly_correlated_features.index]

"""Display the resulting feature shapes of the datasets"""

# Display the filtered train feature count
print("Filtered train features: {}".format(train_features.shape))

# Display the filtered valid feature count
print("Filtered valid features: {}".format(valid_features.shape))

# Display the filtered test feature count
print("Filtered test features: {}".format(test_features.shape))

"""Standardize the features of all datasets"""

# Standardize the features
scaler = StandardScaler()
standardized_train_features = scaler.fit_transform(train_features)
standardized_valid_features = scaler.transform(valid_features)
standardized_test_features = scaler.transform(test_features)

"""### Feature Extraction

Extract can combine the features that are highly significant in predicting the label using Principal Componenet Analysis(PCA)

Extract the features that can explain the variance of the label to 99%

Display the resulting explained variances of each principal component
"""

variance_threshold = 0.95

# Apply PCA with the determined number of components
pca = PCA(n_components=variance_threshold, svd_solver='full')

pca_train_result = pca.fit_transform(standardized_train_features)
pca_valid_result = pca.transform(standardized_valid_features)
pca_test_result = pca.transform(standardized_test_features)

# Explained variance ratio after dimensionality reduction
explained_variance_ratio_reduced = pca.explained_variance_ratio_
print("Explained Variance Ratio after Dimensionality Reduction:", explained_variance_ratio_reduced)
# Create a list of colors for each bar
colors = ['blue', 'green', 'orange', 'red', 'purple']
plt.figure(figsize=(18, 10))
# Create the colored bar chart
bars = plt.bar(range(1, len(explained_variance_ratio_reduced) + 1), explained_variance_ratio_reduced, color=colors)
plt.xlabel('Principal Component')
plt.ylabel('Explained Variance Ratio')
plt.title('Explained Variance Ratio per Principal Component (Reduced)')
# Adding a legend for colors
legend_labels = [f'PC{i}' for i in range(1, len(explained_variance_ratio_reduced) + 1)]
plt.legend(bars, legend_labels)
plt.show()

# Display the reduced train feature matrix
print("Reduced Train feature matrix shape: {}".format(pca_train_result.shape))
# Display the reduced valid feature matrix
print("Reduced valid feature matrix shape: {}".format(pca_valid_result.shape))
# Display the reduced test feature matrix
print("Reduced test feature matrix shape: {}".format(pca_test_result.shape))

"""## Model Selection

Select the model that best predicts the valid and test datasets based on accuracy, precision and recall
"""

# Define a list of classification models
classification_models = [
    # ('K Neighbors', KNeighborsClassifier()),
    # ('Decision Tree', DecisionTreeClassifier()),
    # ('Random Forest', RandomForestClassifier()),
    ('SVM', SVC())
]

# The best model is SVM then KNN then Random Forest then Decision Tree

# Number of features used in PCA
num_features = pca_train_result.shape[1]
print(f"Number of features: {num_features}\n")

# Train and evaluate each classification model
for model_name, model in classification_models:
    # Train the model on the training data
    model.fit(pca_train_result, train_label1)

    # Predict on the train data
    y_pred_train = model.predict(pca_train_result)

    # Calculate metrics for classification evaluation
    accuracy = accuracy_score(train_label1, y_pred_train)
    precision = precision_score(train_label1, y_pred_train, average='weighted' , zero_division=1)
    recall = recall_score(train_label1, y_pred_train, average='weighted')

    print(f"Metrics for {model_name} on train data:")
    print(f"Accuracy: {accuracy:.2f}")
    print(f"Precision: {precision:.2f}")
    print(f"Recall: {recall:.2f}")
    print("\n")

    # Predict on the validation data
    y_pred_valid = model.predict(pca_valid_result)

    # Calculate metrics for classification evaluation on validation data
    accuracy = accuracy_score(valid_label1, y_pred_valid)
    precision = precision_score(valid_label1, y_pred_valid, average='weighted', zero_division=1)
    recall = recall_score(valid_label1, y_pred_valid, average='weighted')

    print(f"Metrics for {model_name} on validation data:")
    print(f"Accuracy: {accuracy:.2f}")
    print(f"Precision: {precision:.2f}")
    print(f"Recall: {recall:.2f}")
    print("\n")

    # Predict on the test data
    y_pred_test = model.predict(pca_test_result)

    # Calculate metrics for classification evaluation on test data
    accuracy = accuracy_score(test_label1, y_pred_test)
    precision = precision_score(test_label1, y_pred_test, average='weighted', zero_division=1)
    recall = recall_score(test_label1, y_pred_test, average='weighted')

    print(f"Metrics for {model_name} on test data:")
    print(f"Accuracy: {accuracy:.2f}")
    print(f"Precision: {precision:.2f}")
    print(f"Recall: {recall:.2f}")
    print("\n")

"""# Generate Output CSV

Define method to create the csv file
"""

# define method to create the dataframe and save it as a csv file
def create_csv(features, pred_before_fe, pred_after_fe):
  feature_count = features.shape[1]
  feature_row = np.repeat('new_feature_', feature_count)
  count_row = list(map(str, np.arange(1, feature_count+1)))

  header_row = np.char.add(feature_row, count_row)

  df = pd.DataFrame(features, columns  = header_row)

  df.insert(loc=0, column='Predicted labels before feature engineering', value=pred_before_fe)
  df.insert(loc=1, column='Predicted labels after feature engineering', value=pred_after_fe)
  df.insert(loc=2, column='No of new features', value=np.repeat(feature_count, features.shape[0]))

  df.to_csv('/kaggle/working/190458T_label_1.csv', index=False)

"""Create CSV file"""

# create the csv output file
create_csv(pca_test_result, y_pred_base_test, y_pred_test)

