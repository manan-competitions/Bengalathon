import pandas as pd
import lightgbm as lgb
import numpy as np
import sklearn
import json
from pprint import pprint
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
pd.set_option('display.max_columns', 500)

train_X = pd.read_csv('train.csv', index_col='ID')
valid_X = pd.read_csv('valid.csv', index_col='ID')
test_X = pd.read_csv('test.csv', index_col='ID')
X=train_X.append(valid_X.append(test_X))

X=train_X

import pickle
import os

models = pickle.load(open(os.path.join(".", 'model.pkl'), 'rb'))

index = ['KIDSDRIV', 'AGE', 'HOMEKIDS', 'INCOME', 'PARENT1', 'HOME_VAL', 'MSTATUS', 'GENDER', 'TRAVTIME',
         'CAR_USE', 'BLUE_BOOK', 'RED_CAR', 'OLD_CLAIM', 'CLM_FREQ', 'REVOKED', 'CAR_AGE', 'URBAN_CITY',
          'CAR_TYPE_Minivan', 'CAR_TYPE_Panel Truck', 'CAR_TYPE_Pickup', 'CAR_TYPE_Sports Car', 'CAR_TYPE_Van',
 'CAR_TYPE_z_SUV', 'OCCUPATION_Clerical', 'OCCUPATION_Doctor', 'OCCUPATION_Home Maker',
 'OCCUPATION_Lawyer', 'OCCUPATION_Manager', 'OCCUPATION_Professional', 'OCCUPATION_Student', 'OCCUPATION_z_Blue Collar', 'EDUCATION']
X['EDUCATION']=X['EDUCATION_z_High School']+2*X['EDUCATION_Bachelors']+3*X['EDUCATION_Masters']+4*X['EDUCATION_PhD']
X['AGE'] = X['AGE']//10
X['INCOME'] = np.log(1+X['INCOME'])//1
X['TRAVTIME'] = X['TRAVTIME']//10
X['CAR_AGE'] = X['CAR_AGE']//5
X['HOME_VAL'] = (np.log(2+X['HOME_VAL']//100000))//0.5
X['BLUE_BOOK'] = (np.log(1+X['BLUE_BOOK']//1000))//1
X['OLD_CLAIM'] = (np.log(1+X['OLD_CLAIM']//100))//1

X_new = []


Y = -1
try:
    Y = X['CLAIM_FLAG']
except:
    pass

scaler = pickle.load(open(os.path.join(".", 'scaler.pkl'), 'rb'))

X_new = scaler.transform([X.iloc[4][index]])
Y_pred = np.zeros((np.shape(X_new)[0]))

vals= []
for model in models:
    Y_pred += model.predict_proba(X_new)[:, 1]
    vals.append(model.predict_proba(X_new)[:, 1][0])

vals = sorted(vals)
if Y_pred <= 2.5:
    avg = (vals[0]+vals[1]+vals[2])/3
elif 4 < Y_pred:
    avg = (vals[-1]+vals[-2]+vals[-3])/3
else:
    avg = -1

print(avg)
