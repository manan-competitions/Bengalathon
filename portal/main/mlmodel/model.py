import numpy as np
import pandas as pd
import sklearn
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import pickle
import json
import csv
import os


working_directory = os.path.dirname((os.path.abspath(__file__)))


class ml_model(object):
    def __init__(self):
        try:
            self.models = pickle.load(
                open(os.path.join(working_directory, 'model.pkl'), 'rb'))
        except:
            clf1 = SVC(gamma='auto', probability=True, class_weight='balanced')
            clf2 = RandomForestClassifier(n_estimators=1000, random_state=42)
            clf3 = KNeighborsClassifier(n_neighbors=10)
            clf4 = AdaBoostClassifier()
            self.models = [clf1, clf2, clf3, clf4]

        self.scaler = pickle.load(
            open(os.path.join(working_directory, 'scaler.pkl'), 'rb'))

    def pre_process(self, X):
        """
        pre_process(X)
        Convert user input Data to model compatible data

        Arguments:
            X(dict): X-values for training/prediction
        Returns:
            Numpy Array

        following keys are required in X:
        [ 'KIDSDRIV', 'AGE', 'HOMEKIDS', 'INCOME', 'PARENT1', 'HOME_VAL', 'MSTATUS', 'GENDER', 'TRAVTIME',
        'CAR_USE', 'BLUE_BOOK', 'RED_CAR', 'OLD_CLAIM', 'CLM_FREQ', 'REVOKED', 'CAR_AGE', 'URBAN_CITY',
        'CAR_TYPE', 'OCCUPATION', 'EDUCATION' ]

        Options:
        CAR_TYPE: [Minivan(0), Panel Truck(1), Pickup(2), Sports Car(3), Van(4), SUV(5)]
        OCCUPATION: [Clerical(0), Doctor(1), Home Maker(2), Lawyer(3), Manager(4), Professional(5), Student(6), Blue_Collar(7)]
        EDUCATION: [<High_School(0), High_School(1), Bachelors(2), Masters(3), PhD(4),]

        """

        index = ['KIDSDRIV', 'AGE', 'HOMEKIDS', 'INCOME', 'PARENT1', 'HOME_VAL', 'MSTATUS', 'GENDER', 'TRAVTIME',
                 'CAR_USE', 'BLUE_BOOK', 'RED_CAR', 'OLD_CLAIM', 'CLM_FREQ', 'REVOKED', 'CAR_AGE', 'URBAN_CITY',
                 'CAR_TYPE', 'OCCUPATION', 'EDUCATION']

        X['AGE'] = X['AGE']//10
        X['INCOME'] = np.log(1+X['INCOME'])//1
        X['TRAVTIME'] = X['TRAVTIME']//10
        X['CAR_AGE'] = X['CAR_AGE']//5
        X['HOME_VAL'] = (np.log(2+X['HOME_VAL']//100000))//0.5
        X['BLUE_BOOK'] = (np.log(1+X['BLUE_BOOK']//1000))//1
        X['OLD_CLAIM'] = (np.log(1+X['OLD_CLAIM']//100))//1

        X_new = []
        for col in index:

            if col == 'CAR_TYPE':
                for i in range(6):
                    if i == X[col]:
                        X_new.append(1)
                    else:
                        X_new.append(0)

            elif col == 'OCCUPATION':
                for i in range(8):
                    if i == X[col]:
                        X_new.append(1)
                    else:
                        X_new.append(0)
            else:
                X_new.append(X[col])

        Y = -1
        try:
            Y = X['CLAIM_FLAG']
        except:
            pass

        X_new = np.array(X_new).reshape(1, 32)
        return X_new,Y

    def predict(self, X):
        """
        Arguments:
            X(dict): X-values for Prediction
        Returns:
            prediction(float): 1,0,-1

        following keys are required in X:
        [ 'KIDSDRIV', 'AGE', 'HOMEKIDS', 'INCOME', 'PARENT1', 'HOME_VAL', 'MSTATUS', 'GENDER', 'TRAVTIME',
        'CAR_USE', 'BLUE_BOOK', 'RED_CAR', 'OLD_CLAIM', 'CLM_FREQ', 'REVOKED', 'CAR_AGE', 'URBAN_CITY',
        'CAR_TYPE', 'OCCUPATION', 'EDUCATION' ]
        """
        print(X)
        X_new,Y = self.pre_process(X)
        self.save_data(X_new, Y, os.path.join(working_directory, 'new_data.csv'))
        X_new = self.scaler.transform(X_new)
        Y_pred = np.zeros((np.shape(X_new)[0]))

        vals= []
        for model in self.models:
            Y_pred += model.predict_proba(X_new)[:, 1]
            vals.append(model.predict_proba(X_new)[:, 1][0])

        vals = sorted(vals)
        if Y_pred <= 2.5:
            avg = (vals[0]+vals[1]+vals[2])/3
        elif 4 < Y_pred:
            avg = (vals[-1]+vals[-2]+vals[-3])/3
        else:
            avg = -1
        return round(avg, 2)

    def save_data(self, data, Y, filename='data.csv'):
        print(Y)
        data = list(data.reshape(32,))
        if Y!=-1:
            data.append(Y)
        print(len(data))
        with open(os.path.join(working_directory, filename), 'a') as f:
            csv.writer(f).writerow(data)

    def train(self, data_file='data.csv', model_file='model.pkl'):
        X = pd.read_csv(os.path.join(working_directory, data_file))
        train, test = train_test_split(X, test_size=0.3)

        train_Y = train['CLAIM_FLAG']
        train_X = train.drop(['CLAIM_FLAG'], axis=1)
        train_X = self.scaler.transform(train_X)

        test_Y = test['CLAIM_FLAG']
        test_X = test.drop(['CLAIM_FLAG'], axis=1)
        test_X = self.scaler.transform(test_X)

        clf1 = SVC(gamma='auto', probability=True, class_weight='balanced')
        clf2 = RandomForestClassifier(n_estimators=1000, random_state=42)
        clf3 = KNeighborsClassifier(n_neighbors=10)
        clf4 = AdaBoostClassifier()
        new_models = [clf1, clf2, clf3, clf4]

        for model in new_models:
            model.fit(train_X, train_Y)

        new_models.append(clf1)
        new_models.append(clf1)
        new_models.append(clf2)

        pickle.dump(new_models, open(os.path.join(
            working_directory, model_file), 'wb'))

# model = ml_model()
# model.train()


# Tested:

# data = json.load(
#       open(os.path.join(working_directory, 'sample_data.json'), 'r'))
# model = ml_model()
# result = model.predict(data)
# print(result)
