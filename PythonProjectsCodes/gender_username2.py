# coding: utf-8
import nltk
import pandas as pd
import numpy as np
from nltk.classify import SklearnClassifier
from sklearn.naive_bayes import BernoulliNB
from sklearn.metrics import confusion_matrix
from sklearn.svm import SVC
from sklearn.model_selection import KFold
import os
# os.chdir('D:/Dropbox/FreelancerDataMining/names')

# *** To do 1: tune model parameters (if any) and add additional models ***
method = ['SVM','NB','ME'][2]
# Target variable: use fname.gender for now, namely gender from first name
# fname.gender will be updated once first names for some users become available on website

truth = ['fname.gender','pic.gender'][0]
# Whether or not to over sample female to get balanced training set
# Use original imbalanced for now
balanced_sample = False

# bi-gram of username
def extract_features2(name, N=2):
    name = name.lower()
    features = {'nchar': len(name)}
    for i in range(len(name)-N):
        features["count({})".format(name[i:i+N])] = name.lower().count(name[i:i+N])
    for letter in 'abcdefghijklmnopqrstuvwxyz':
        features["count({})".format(letter)] = name.lower().count(letter)
    return features

# features extracted from username
def extract_features(name):
    name = name.lower()
    features = {
        'last': name[-1],
        'last_two': name[-2:],
        'last_three': name[-3:],
        'first': name[0],
        'first2': name[:1],
        'first3': name[:2],
        'nchar': len(name),
        'vowels.pct': sum(c in 'aoeiu' for c in name)/len(name),
        'digits.pct': sum(c.isdigit() for c in name)/len(name),
        'endwd': name[-1].isdigit(),
    }
    # commented because these features are not useful
    #for letter in 'abcdefghijklmnopqrstuvwxyz':
        #features["count({})".format(letter)] = name.lower().count(letter)
    return features

# *** To do 2: Extend the extract_features function to incorporate additional info such as users' profile info
# Note that extra features does not necessarily make the model better off


# 1. Load users
users = pd.read_csv('users.gender.golden.csv', na_values='')
# Focus on users with usernames
users = users[users['username'].notnull()]
# Only use users with predicted gender (by firstname) to train a model
if truth=='fname.gender':
    cand = users[users[truth].notnull() & abs(users['male.prob']-0.5)>0.4]
if truth=='pic.gender': 
    cand = users[users[truth].notnull()]
if balanced_sample:
    cand_pos = cand[cand[truth]=='male']
    cand_neg = cand[cand[truth]!='male']
    train = pd.concat([cand, cand_neg.sample(len(cand_pos)-len(cand_neg), replace=True)])
else: train = cand
print('Number of obs in training set:', len(train))
Xy = [(extract_features(n), g) for n, g in zip(train['username'], train[truth])]


# *** To do 3: Some feature selection and standardization (z-score) might be helpful before cross validation***


# 2. Cross-Valiation
#k_fold = KFold(n_splits=5, shuffle=True)
#accu = []
#for train_idx, test_idx in k_fold.split(Xy):
#    train = [Xy[i] for i in train_idx]
#    test = [Xy[i] for i in test_idx]
#    if method == 'SVM':
#        classifier = SklearnClassifier(SVC(kernel='linear', C=10, random_state=1), sparse=True).train(train)
#    if method == 'NB':
#        classifier = nltk.NaiveBayesClassifier.train(train)
#    if method == 'ME':
#        classifier = nltk.classify.MaxentClassifier.train(train, trace=3, max_iter=50)    
#    accu.append( nltk.classify.util.accuracy(classifier, test) )
#    print('accuracy:', accu[len(accu)-1])    
## select the best model based on CV performance shown below
#print('Final accuracy:', np.mean(accu))    
    

# 3. Train model on the entire training set and generate predictions.
if method == 'SVM':
    classifier = SklearnClassifier(SVC(kernel='linear', C=10, random_state=1), sparse=True).train(Xy)
if method == 'NB':
    classifier = nltk.NaiveBayesClassifier.train(Xy)
if method == 'ME':
    classifier = nltk.classify.MaxentClassifier.train(Xy, trace=3, max_iter=50)
users['uname.gender'] = [classifier.classify(extract_features(e)) for e in users.username]
users.to_csv('users.%s.%s.%s.csv' % (method, truth, balanced_sample), index=False, na_rep='')
sub = users[users[truth].notnull()]
print('Confusion Matrix:')
print(confusion_matrix(sub[truth], sub['uname.gender'])/len(sub))
print('Done!')
