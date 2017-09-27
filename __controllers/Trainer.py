from Observations import Observations
import numpy as np
import pandas as pd
from sklearn import preprocessing, cross_validation, svm
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.tree import DecisionTreeClassifier

class Trainer:
    def __init__(self):
        self.forecast_col = 'next_open_up'
        # self.clf = DecisionTreeClassifier(max_depth=3)
        # self.clf = MLPClassifier(alpha=10, solver='lbfgs', hidden_layer_sizes=[500], max_iter=2000, activation='relu')
        # self.clf = svm.SVC(gamma=2, C=1)
        self.clf = svm.SVC(kernel="sigmoid", C=0.0001)
        # self.clf = KNeighborsClassifier(n_neighbors=5)

    
    def start(self):
        self.sequence()

    def sequence(self):
        self.getObservations()
        self.setFeatures()
        self.setOutcomes()
        self.fit()
    
    def getObservations(self):
        print 'Fetching observations from db...'
        observations = Observations().fetch()
        self.df = pd.DataFrame(observations.toJSON())
        self.df = self.df[[
            'num_new_highs',
            'num_new_lows',
            'num_highs_abv_avg_vol',
            'num_lows_abv_avg_vol',
            'num_highs_blw_avg_vol',
            'num_lows_blw_avg_vol',
            'num_new_highs_am',
            'num_new_highs_pm',
            'num_new_lows_am',
            'num_new_lows_pm',
            'percent_change',
            'tallest_green_candlestick',
            'tallest_red_candlestick',
            'age_recent_news',
            'next_open_up'
            ]]

    def setFeatures(self):
        self.X = np.array(self.df.drop([self.forecast_col], 1))
        self.X = preprocessing.scale(self.X)
        self.df.dropna(inplace=True)

    def setOutcomes(self):
        self.y = np.array(self.df[self.forecast_col])

    def fit(self):
        X_train, X_test, y_train, y_test = cross_validation.train_test_split(self.X, self.y, test_size=0.3)
        self.clf.fit(X_train, y_train)
        self.accuracy = self.clf.score(X_test, y_test)
        print self.accuracy
        # self.accuracy = cross_val_score(self.clf, self.X, self.y, scoring='r2')
        