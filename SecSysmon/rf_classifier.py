from sklearn.feature_selection import SelectKBest, chi2, mutual_info_classif
import pandas as pd
from .config import DROP_LIST
from sklearn.ensemble import RandomForestClassifier
from collections import Counter
import numpy as np

class FeatureSelector():
    """ Select the most important features by computing importance. """
    def __init__(self, train_data, test_data=None):
        """
        Args:
            train_data     (list): a list of dataframes of training data
            test_data (dataFrame): the dataframe format testing data
            select         (bool): select the features by SelectKBest
        """
        self.full_data = pd.concat(train_data, axis=0, ignore_index=True, sort=False)
        self.labels = self.full_data['label']
        self.full_data = self.full_data.drop(columns=['label']+DROP_LIST)
        self.test_data = test_data
        self.train_data = None

    def select(self, select_k=100):
        """
        Select k most important features. Note: only features in the testing data will be selected.
        Args:
            select_k (int): number of selected features, default=500
        Return:
            selected_df (dataframe): a dataframe contains k features
            labels (df): training data labels
        """
        full_columns = self.full_data.columns
        train_columns = []

        if type(self.test_data) == pd.DataFrame:
            test_columns = self.test_data.columns
            for col in test_columns:
                if col in full_columns:
                    train_columns.append(col)
            train_data = self.full_data[train_columns]
        else:
            train_data = self.full_data



        # convert categorical to one-hot encoding
        train_data = pd.get_dummies(train_data)
        if len(train_columns) < select_k:
            select_k = len(train_columns)

        selected_data = SelectKBest(chi2, k=select_k).fit(train_data, self.labels)

        select_cols = selected_data.get_support(indices=True)
        selected_df = train_data.iloc[:,select_cols]

        return (selected_df, self.labels)

    def get_importance(self):
        """
        Return a list of tuple (feature_name, importance) sorted by importance (decending).
        """
        self.full_data = pd.get_dummies(self.full_data)
        selected_data = SelectKBest(chi2).fit(self.full_data, self.labels)
        importance_index = np.argsort(selected_data.scores_)[::-1]
        importance_list = []
        for idx in importance_index:
            importance_list.append((self.full_data.columns[idx], round(selected_data.scores_[idx], 2)))
        return importance_list

class RFClassifier():
    """ Predict the input data by RandomForestClassifier. """
    def __init__(self, train_data, test_data):
        self.selector = FeatureSelector(train_data, test_data)
        self.train_data, self.train_label = self.selector.select()
        self.test_label = test_data['label']
        self.test_data = test_data.drop(columns=['label'])
        self.classifier = None
        self.build_classifier()

    def build_classifier(self):
        self.classifier = RandomForestClassifier(max_depth=100, n_estimators=1000)
        self.classifier.fit(self.train_data, self.train_label)

    def predict(self):
        self.test_data = pd.get_dummies(self.test_data)

        # discard new columns (not exist in training data)
        drop_list = []
        for col in self.test_data.columns:
            if col not in self.train_data.columns:
                drop_list.append(col)
        self.test_data = self.test_data.drop(columns=drop_list)

        # padding lacking columns
        for col in self.train_data.columns:
            if col not in self.test_data.columns:
                self.test_data.insert(0, col, 0) # insert at position 0, value=0

        predicts = self.classifier.predict(self.test_data)

        # find out the label that occurs the most in the prediction
        count = Counter(predicts)
        summary = [(i, count[i] / len(predicts)) for i in count]

        return (summary, predicts)
