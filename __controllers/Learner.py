from Observations import Observations
import numpy as np
import pandas as pd
from sklearn import preprocessing, cross_validation, svm
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.tree import DecisionTreeClassifier
import json
import config
import utils

class Learner:
    def __init__(self, predict=False, test=True):
        self.predict = predict
        self.test = test
        self.forecast_col = 'next_open_up'
        # self.clf = DecisionTreeClassifier(max_depth=3)
        self.clf = MLPClassifier(alpha=10, solver='lbfgs', hidden_layer_sizes=[500], max_iter=2000, activation='relu')
        # self.clf = svm.SVC(gamma=2, C=1)
        # self.clf = svm.SVC(kernel="sigmoid", C=0.0001)
        # self.clf = KNeighborsClassifier(n_neighbors=5)

    
    def start(self):
        if self.predict:
            self.predict = False
            self.sequence()
            self.predict = True
            self.sequence()
        else:
            self.sequence()

    def sequence(self):        
        self.getObservations()
        self.setFeatures()
        if not self.predict:
            self.setOutcomes()
            if self.test:
                self.fittest()
            else:
                self.fit()
        if self.predict:
            self.predictor()
    
    def getObservations(self, from_db=True):
        if not self.predict:
            print 'Fetching observations from db...'
            observations = Observations().fetch()
            predf = pd.DataFrame(observations.toJSON())
            self.df = predf[[
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
        else:
            print 'Parsing predict.json for observations...'
            prediction_file = open('./trading-data/' + config.get('predict.filename'), 'rb')
            prediction_json = prediction_file.read().replace('\n', '')
            self.predictors = utils.filterNoNews(json.loads(prediction_json))
            predf = pd.DataFrame(self.predictors)
            self.df = predf[[
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
                'age_recent_news'
                ]]

    def setFeatures(self):
        if self.predict:
            self.X = np.array(self.df)
        else:
            self.X = np.array(self.df.drop([self.forecast_col], 1))
        self.X = preprocessing.scale(self.X)
        self.df.dropna(inplace=True)

    def setOutcomes(self):
        self.y = np.array(self.df[self.forecast_col])

    def fit(self):
        self.clf.fit(self.X, self.y)
            
    def fittest(self):
        X_train, X_test, y_train, y_test = cross_validation.train_test_split(self.X, self.y, test_size=0.3)
        self.clf.fit(X_train, y_train)
        self.accuracy = self.clf.score(X_test, y_test)
        print self.accuracy

    def predictor(self):
        predictions = self.clf.predict(self.X)
        ret = []
        for key, item in enumerate(predictions):
            insert = {}
            insert['symbol'] = self.predictors[key]['symbol']
            insert['class'] = item
            ret.append(insert)
        print json.dumps(ret)
