"""
Written by Manan Soni
github: MananSoni42
"""

import numpy as np
import pandas as pd
import sklearn
from sklearn.neural_network import MLPClassifier
import pickle
import csv
import os

class ml_model(object):
    """
    Class ml_model

    Attributes:
        nn: Neural Network used for prediction

    Methods:
        train(X,Y)                 : returns None
        eval(X,Y)                  : returns {"accuracy":  , "f-score": }
        predict(X,save=False)      : returns [predictions]
        save(filename='model.pkl') : returns None
        load(filename='model.pkl') : returns None
    """
    def __init__(self, layers=(512,128,32), lrate=0.001, alpha=0.03, max_iter=5000):
        """
        __init__(layers=(512,128,32), lrate=0.001, alpha=0.03, max_iter=5000)
        Initializes the Neural Network

        Arguements:
            layers (tuple): number of units in each hidden layer
            lrate(int)    : learning rate
            alpha(int)    : alpha (regularization constant)
            max_iter(int) : maximum number of iterations for training
        Returns:
            None
        """
        self.nn = MLPClassifier(hidden_layer_sizes = layers, activation = 'logistic', learning_rate_init = lrate, alpha = alpha, max_iter = max_iter)

    def train(self, X, Y):
        """
        train(X,Y)
        Train the Neural Network

        Arguements:
            X(array): X-values for training. Shape=(n,44) n is number of rows
            Y(array): Y-values for training. Shape=(n,1) n is number of
        Returns:
            None
        """
        self.nn.fit(X,Y)

    def eval(self, X ,Y):
        """
        eval(X,Y)
        Evaluate the perfomance of the Neural Network

        Arguements:
            X(array): X-values for evaluation. Shape=(n,44) n is number of rows
            Y(array): Y-values for evaluation. Shape=(n,1) n is number of
        Returns:
            Dictionary with keys "accuracy" and  "f-score"
            {"accuracy": float, "f-score": float}
        """
        Y_pred = self.nn.predict(X)
        acc = sklearn.metrics.accuracy_score(np.array(Y_pred), np.array(Y))
        f = sklearn.metrics.f1_score(np.array(Y),np.array(Y_pred))
        return {"accuracy": acc, "f-score": f}

    def predict(self, X, save=False):
        """
        predict(X, save=False)
        Predict Y values from given X values

        Arguements:
            X(array)     : X-values for prediction. Shape=(n,44) n is number of rows
            save(Boolean): if True save values to new_data.csv
        Returns:
            list of predictions of length n
            [float, float, ...]
        """
        filename='new_data.csv'
        if save:
            with open(filename,'a') as f:
                for row in np.array(X):
                    csv.writer(f).writerow(row)

        return [pred[0] for pred in self.nn.predict_proba(X)]

    def save(self, filename='model.pkl'):
        """
        save(filename)
        Save the model to filename

        Arguements:
            filename(string): Name of file to store the model
        Returns:
            None
        """
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
        pickle.dump(self.nn, open(file_path, 'wb'))

    def load(self, filename='model.pkl'):
        """
        load(filename)
        Load the model from filename

        Arguements:
            filename(string): Name of file to load the model
        Returns:
            None
        """
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
        self.nn = pickle.load(open(file_path, 'rb'))

valid_csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'valid.csv')
valid_X = pd.read_csv(valid_csv_path, index_col='ID')
valid_Y = valid_X['CLAIM_FLAG']
valid_X = valid_X.drop(['CLAIM_FLAG'], axis=1)

model = ml_model()

#model.load()
model.save()

print(model.eval(valid_X,valid_Y))

X = valid_X.sample(n=5)
print(model.predict(X,save=True))
