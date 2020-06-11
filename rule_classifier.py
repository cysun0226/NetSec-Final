from config import DROP_LIST, IMPORTANCE, OCCUR_WEIGHT
from scipy.spatial.distance import cosine
import pandas as pd

class Analyzer():
    """
    Analyze the feature distribution of each input data
    """
    def __init__(self, readers):
        """
        Args:
            train_readers (list): a list of (label, readers) of training data
        """
        self.train_data = readers
        self.features = None
        self.value_dict = {}
        self.statistics = {}
        self.occurence = {}
        self.classes = [x[0] for x in readers]

        self.collect_features()
        self.analyze()

    def collect_features(self):
        """ Get the union of all dataframe columns """
        self.features = list(set().union(*[data[1].dataframe.columns for data in self.train_data]))
        self.features = [attr for attr in self.features if attr not in DROP_LIST] # drop useless features
        # build value dict of each feature
        for attr in self.features:
            # concat all values of this feature
            self.value_dict[attr] =\
                list(set().union(*[data.df_data[attr] for _, data in self.train_data if attr in data.df_data]))

    def analyze(self):
        """ For each feature, compute the composition of each data """
        for attr in self.features:
            self.statistics[attr] = {}
            self.occurence[attr] = {}
            for label, reader in self.train_data:
                values = {attr: 0 for attr in self.value_dict[attr]}
                occur = 0
                if (attr in reader.df_data):
                    for d in reader.df_data[attr]:
                        values[d] += 1
                        if d != None:
                            occur += 1
                    self.occurence[attr][label] = occur / len(reader.df_data[attr])
                else:
                    self.occurence[attr][label] = 0
                self.statistics[attr][label] = values

class RuleClassifier():
    """
    Classifier that predicts the given data by pre-define rules.
        Return: A dict that contains the similarity score of each class.
    """
    def __init__(self, train_readers, occur_weight=OCCUR_WEIGHT):
        """
        Args:
            train_readers (list): a list of (label, readers) of training data
        """
        self.analyzer = Analyzer(train_readers)
        self.occur_similarity = {}
        self.occur_weight = occur_weight

    def predict(self, test_reader):
        """ Predict the given data """
        self.test_analyzer = Analyzer([('test', test_reader)])
        self.compute_occur()
        self.compute_composition()
        # combine two similarity
        self.total_similarity = {x: 0 for x in self.analyzer.classes}
        for label in self.occur_similarity:
            self.total_similarity[label] =\
            self.occur_weight * self.occur_similarity[label] +\
            (1-self.occur_weight) * self.compose_similarity[label]
            self.total_similarity[label] = round(self.total_similarity[label], 2)
        return self.total_similarity

    def compute_occur(self):
        """ For each feature, find out the class that the occurence is closest to the given data. """
        self.occur_similarity = { x: 0 for x in self.analyzer.classes }
        for attr in self.test_analyzer.features:
            if attr not in self.analyzer.occurence:
                continue

            min_distance = 100
            closest_class = None
            for key, value in self.analyzer.occurence[attr].items():
                distance = abs(value-self.test_analyzer.occurence[attr]['test'])
                if distance < min_distance:
                    min_distance = distance
                    closest_class = key
            if closest_class != None and attr in IMPORTANCE:
                self.occur_similarity[closest_class] += 1 * (IMPORTANCE[attr]*0.1)

    def compute_composition(self):
        """ For each feature, find out the class that the composition is closest to the given data. """
        self.compose_similarity = { x: 0 for x in self.analyzer.classes }

        for attr in self.test_analyzer.features:
            # omit the feature with too may possibile values
            if len(self.analyzer.value_dict[attr]) > 30 or attr not in self.analyzer.features:
                continue

            max_sim = 0
            closest_class = None

            for key, train_values in self.analyzer.statistics[attr].items():
                # padding the lacking columns of the testing data
                test_values = self.test_analyzer.statistics[attr]['test']
                for col in train_values:
                    if col not in test_values:
                        test_values[col] = 0

                # compute the cosine similarity between each class and the given data
                train_s = pd.Series(train_values)
                test_s = pd.Series(test_values)
                sim = 1 - cosine(train_s, test_s)

                if sim > max_sim:
                    max_sim = sim
                    closest_class = key

            if closest_class != None and attr in IMPORTANCE:
                self.compose_similarity[closest_class] += 1 * (IMPORTANCE[attr]*0.1)
