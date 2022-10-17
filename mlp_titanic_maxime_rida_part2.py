# -*- coding: utf-8 -*-
"""MLP_Titanic_Maxime_Rida_Part2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1XmsGKyBLZc3-0Fgdpn4aBCE6-zOSzgbv
"""

from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import Perceptron

from sklearn.metrics import classification_report, accuracy_score, log_loss

from sklearn.decomposition import PCA

import pandas as pd
import numpy as np
import time
import seaborn as sns
import matplotlib.pyplot as plt

from google.colab import drive
drive.mount('/content/drive')

# Commented out IPython magic to ensure Python compatibility.
# %cd /content/drive/'My Drive'/'DL'/'Titanic'

train =  pd.read_csv('train.csv', sep=",")
train_edit = train.copy()

train_edit['Title'] = train_edit.Name.str.extract(' ([A-Za-z]+)\.', expand=False)
train_edit['Title'] = train_edit['Title'].replace(['Lady', 'Countess','Capt', 'Col','Don', 'Dr','Major', 'Rev', 'Sir', 'Jonkheer', 'Dona'], 'Speciaux')
train_edit['Title'] = train_edit['Title'].replace('Mlle', 'Miss')
train_edit['Title'] = train_edit['Title'].replace('Ms', 'Miss')
train_edit['Title'] = train_edit['Title'].replace('Mme', 'Mrs')

train_edit['Title'] = train_edit['Title'].replace(['Mr'],1)
train_edit['Title'] = train_edit['Title'].replace(['Mrs'],2)
train_edit['Title'] = train_edit['Title'].replace(['Miss'],3)
train_edit['Title'] = train_edit['Title'].replace(['Master'],4)
train_edit['Title'] = train_edit['Title'].replace(['Speciaux'],5)

train.head()

sns.set()
sns.pairplot(train, hue="Survived", height=5)

#Suppresion des lignes si non présences de données (NaN)
change_train = train.drop(['PassengerId', 'Name', 'Ticket', 'Cabin'], axis=1)
change_train = change_train.dropna(axis=0)

change_train_edit = train_edit.drop(['PassengerId', 'Name', 'Ticket', 'Cabin'], axis=1)
change_train_edit = change_train_edit.dropna(axis=0)

change_train['Sex'] = change_train['Sex'].replace(['male'], 1)
change_train['Sex'] = change_train['Sex'].replace(['female'], 2)
change_train['Embarked'] = change_train['Embarked'].replace(['S'], 1)
change_train['Embarked'] = change_train['Embarked'].replace(['C'], 2)
change_train['Embarked'] = change_train['Embarked'].replace(['Q'], 3)

change_train_edit['Sex'] = change_train_edit['Sex'].replace(['male'], 1)
change_train_edit['Sex'] = change_train_edit['Sex'].replace(['female'], 2)
change_train_edit['Embarked'] = change_train_edit['Embarked'].replace(['S'], 1)
change_train_edit['Embarked'] = change_train_edit['Embarked'].replace(['C'], 2)
change_train_edit['Embarked'] = change_train_edit['Embarked'].replace(['Q'], 3)

x = change_train.drop(['Survived'], axis=1)
y = change_train['Survived']

xedit = change_train_edit.drop(['Survived'], axis=1)
yedit = change_train_edit['Survived']

x.head()

xtrain, xtest, ytrain, ytest = train_test_split(x, y, test_size = 0.2, random_state = 0)
xtrain_edit, xtest_edit, ytrain_edit, ytest_edit = train_test_split(xedit, yedit, test_size = 0.2, random_state = 0)

"""Meilleur score StandardScaler actuel"""

start_time = time.time()
mlp = Pipeline([('minmax', StandardScaler()),
                ('mlp', MLPClassifier(solver='adam', activation='relu', max_iter=300,
                                      alpha=1, hidden_layer_sizes=(10), tol=0.001,
                                      random_state=0))])
mlp.fit(xtrain, ytrain)
end_time = time.time()
print(f"Temps entraînement = {end_time - start_time}s")
y_pred = mlp.predict(xtest)

accuracy_score(ytest, y_pred)

"""TEST"""

start_time = time.time()
mlp = Pipeline([('std', StandardScaler()),
                ('mlp', MLPClassifier(solver='adam', activation='relu',
                                      hidden_layer_sizes=(10),
                                      random_state=0))])
mlp.fit(xtrain, ytrain)
end_time = time.time()
print(f"Temps entraînement = {end_time - start_time}s")
y_pred = mlp.predict(xtest)

accuracy_score(ytest, y_pred)

start_time = time.time()
mlp = MLPClassifier(solver='adam', activation='identity',
                    hidden_layer_sizes=(41, 8),
                    random_state=0)
mlp.fit(xtrain_edit, ytrain_edit)
end_time = time.time()
print(f"Temps entraînement = {end_time - start_time}s")
y_pred = mlp.predict(xtest_edit)
print(accuracy_score(ytest_edit, y_pred))

start_time = time.time()
mlp = Pipeline([('stdscaler', MinMaxScaler()),
                ('mlp', MLPClassifier(solver='adam',
                                      hidden_layer_sizes=(10,7,5,3),
                                      random_state=0))])
mlp.fit(xtrain, ytrain)
end_time = time.time()
print(f"Temps entraînement = {end_time - start_time}s")
y_pred = mlp.predict(xtest)

accuracy_score(ytest, y_pred)

mlp[1].n_iter_

"""Meilleur score sans pre-processing"""

start_time = time.time()
mlp = MLPClassifier(solver='adam', activation='relu', 
                    alpha=1e-3, hidden_layer_sizes=(50, 50), random_state=0)
mlp.fit(xtrain, ytrain)
end_time = time.time()
print(f"Temps entraînement = {end_time - start_time}s")
y_pred = mlp.predict(xtest)

accuracy_score(ytest, y_pred)

mlp.n_iter_

start_time = time.time()

mlp = MLPClassifier(solver='adam', hidden_layer_sizes=(10, 7, 5), random_state=0)
mlp.fit(xtrain, ytrain)
end_time = time.time()
print(f"Temps entraînement = {end_time - start_time}s")
y_pred = mlp.predict(xtest)

accuracy_score(ytest, y_pred)

from keras import Sequential, losses, metrics
from keras.layers import Dense, Activation
from sklearn.metrics import confusion_matrix

std = StandardScaler()
std.fit(xtrain)
std_xtrain = std.transform(xtrain)
std_xtest = std.transform(xtest)

fc_model = Sequential()
fc_model.add(Dense(10, input_shape=(std_xtrain.shape[1],)))
fc_model.add(Activation('relu'))
fc_model.add(Dense(1))
fc_model.add(Activation('sigmoid'))
fc_model.summary()

fc_model.compile(loss=losses.BinaryCrossentropy(),
                 optimizer='adam',
                 metrics=metrics.BinaryAccuracy())

history = fc_model.fit(
              std_xtrain, 
              ytrain,
              validation_data=(std_xtest, ytest),
              batch_size=20, 
              epochs=30,
              verbose=1
              )

score = fc_model.evaluate(std_xtest, ytest)
print('Test accuracy:', score[1])

