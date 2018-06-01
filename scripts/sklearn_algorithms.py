#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from os import getcwd, chdir, path
import matplotlib.pyplot as plt
import pandas as pd
from pandas.tools.plotting import scatter_matrix
import numpy as np
from sklearn import svm
from sklearn.preprocessing import LabelEncoder
import random
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
from sklearn.metrics import roc_curve, auc
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.feature_selection import RFE


datafile = join(dirname(__file__), '/COMPANY_SCORES_TOP_HALF.csv')


df = pd.read_csv(datafile)
criterion = ['JUST_100']
drivers = ['PAY', 'TREAT', 'SUPPLY', 'COMM',
           'JOBS', 'PROD', 'CUST', 'LEAD', 'ENV', 'INVEST']
components = ['PAY.LIVING', 'PAY.PTO', 'PAY.HEALTH', 'PAY.FAIR', 'PAY.RETIRE', 'PAY.DISC', 'PAY.CEO', 'TREAT.SAFE', 'TREAT.WLB', 'TREAT.EDU', 'TREAT.DISC', 'TREAT.LAYOFF', 'TREAT.RESPECT', 'SUPPLY.ABUSE', 'SUPPLY.CONFLICT', 'SUPPLY.REPRESS', 'COMM.RELS', 'COMM.CHARITY',
              'JOBS.US', 'PROD.BEN', 'PROD.QUAL', 'CUST.FAIR', 'CUST.RELS', 'CUST.DISC', 'CUST.PRIV', 'LEAD.LAWS', 'LEAD.INTEGRITY', 'LEAD.TRUTH', 'LEAD.TAX', 'LEAD.POLITICS', 'ENV.POLLUTION', 'ENV.MGMT', 'ENV.EFFICIENT', 'INVEST.ACCURATE', 'INVEST.PROFIT', 'INVEST.RETURN']
other = ['JUST_IND', 'WGT_SCORE']
df['target'] = 1 * (df[criterion] == 'Yes')
X = df[components]
y = df['target']
X_train, X_test, y_train, y_test = train_test_split(X, y)

# Extra Trees model to the data
extratrees = ExtraTreesClassifier()
extratrees.fit(X, y)
# display the relative importance of each attribute
# print(extratrees.feature_importances_)
importances = extratrees.feature_importances_
std = np.std(
    [tree.feature_importances_ for tree in extratrees.estimators_], axis=0)
indices = np.argsort(importances)[::-1]
ordcomp = list()
print("Feature ranking:")
for f in range(X.shape[1]):
    print("%d. %s (%f)" %
          (f + 1, components[indices[f]], importances[indices[f]]))
    ordcomp.append(components[indices[f]])


# Plot the feature importances of the forest
nfeature = 10
featureidx = indices[0:nfeature]
plt.figure()
plt.title("Feature importances")
plt.barh(range(nfeature), importances[featureidx],
         color="r", xerr=std[featureidx], align="center")
plt.yticks(range(nfeature), ordcomp[1:nfeature], rotation=0)
plt.ylim([-1, nfeature])
plt.xlabel('Feature Importance')
plt.show()

# KNeighborsClassifier
from sklearn.neighbors import KNeighborsClassifier
knn = KNeighborsClassifier()
knn.fit(X_train, y_train)
knn.predict(X_test)
knnscore = cross_val_score(knn, X, y, cv=50)

# Decision Tree
from sklearn.tree import DecisionTreeClassifier
tree_model = DecisionTreeClassifier()
tree_model.fit(X_train, y_train)
tree_model.predict(X_test)
treescore = cross_val_score(tree_model, X, y, cv=50)

# Visualize the Tree - 'dot -Tpng tree.dot > output.png' to convert
from sklearn import tree
tree.export_graphviz(tree_model, out_file='tree.dot')

# Naive Bayes
from sklearn.naive_bayes import GaussianNB
naive_model = GaussianNB()
naive_model.fit(X_train, y_train)
naive_model.predict(X_test)
nbscore = cross_val_score(naive_model, X, y, cv=50)
print(np.mean(nbscore))

# Random Forest
rf = RandomForestClassifier()
rf.fit(X_train, y_train)
rfscore = cross_val_score(rf, X, y, cv=50)

# SVM
svm_model = svm.SVC()
svm_model.fit(X_train, y_train)
svmscore = cross_val_score(svm_model, X, y, cv=50)

# BOX PLOT
model_list = ['KNeighbors', 'Decision Tree',
              'Naive Bayes', 'Random Forest', 'SVM']
scores = np.transpose(
    np.array([knnscore, treescore, nbscore, rfscore, svmscore]))
fig = plt.figure()
# scores.plot(kind = 'box', subplots = True)
boxplot(scores)
xticks(range(1, 6), model_list, rotation=15)
xlabel('Algorithm')
ylabel('Mean Accuracy')
title('Classifier Performance')


# ROC CURVE
predicted = rf.predict_proba(X_test)
fpr, tpr, _ = roc_curve(y_test, predicted[:, 1])
roc_auc = auc(fpr, tpr)
print(roc_auc)
plt.figure()
lw = 2
plt.plot(fpr, tpr, color='darkorange',
         lw=lw, label='ROC curve (area = %0.2f)' % roc_auc)
plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver operating characteristic example')
plt.legend(loc="lower right")
plt.show()


# df.plot(kind = 'box'',' subplots = True)

#fig = plt.figure()
# scatter_matrix(df)
# plt.show()

# plot correlation matrix

# fig = plt.figure()
# ax = fig.add_subplot(111)
# correlations = X.corr()
# cax = ax.matshow(correlations, vmin=-1, vmax=1)
# fig.colorbar(cax)
# ticks = np.arange(0,9,1)
# ax.set_xticks(ticks)
# ax.set_yticks(ticks)
# ax.set_xticklabels(names)
# ax.set_yticklabels(names)

# Box and Whisker Plots
#import matplotlib.pyplot as plt
#import pandas
#url = "https://archive.ics.uci.edu/ml/machine-learning-databases/pima-indians-diabetes/pima-indians-diabetes.data"
#names = ['preg', 'plas', 'pres', 'skin', 'test', 'mass', 'pedi', 'age', 'class']
#data = pandas.read_csv(url, names=names)
#data.plot(kind='box', subplots=True, layout=(3,3), sharex=False, sharey=False)
# plt.show()

# Univariate Density Plots
#import matplotlib.pyplot as plt
#import pandas
#url = "https://archive.ics.uci.edu/ml/machine-learning-databases/pima-indians-diabetes/pima-indians-diabetes.data"
#names = ['preg', 'plas', 'pres', 'skin', 'test', 'mass', 'pedi', 'age', 'class']
#data = pandas.read_csv(url, names=names)
#data.plot(kind='density', subplots=True, layout=(3,3), sharex=False)
# plt.show()

# Univariate Histograms
#import matplotlib.pyplot as plt
#import pandas
#url = "https://archive.ics.uci.edu/ml/machine-learning-databases/pima-indians-diabetes/pima-indians-diabetes.data"
#names = ['preg', 'plas', 'pres', 'skin', 'test', 'mass', 'pedi', 'age', 'class']
#data = pandas.read_csv(url, names=names)
# data.hist()
# plt.show()
