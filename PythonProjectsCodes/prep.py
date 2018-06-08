import pandas as pd

from sklearn.metrics import roc_auc_score, make_scorer, accuracy_score
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from sklearn.preprocessing import StandardScaler, Normalizer, MinMaxScaler


from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score

from xgboost import XGBClassifier
from sklearn.feature_selection import RFE


from time import strftime, strptime, mktime, time, ctime

from sklearn import model_selection

from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB 
from sklearn.svm import LinearSVC

from xgboost import XGBClassifier
import xgboost as xgb

from sklearn.tree import DecisionTreeClassifier, ExtraTreeClassifier
from sklearn.ensemble import AdaBoostClassifier, BaggingClassifier,\
ExtraTreesClassifier, GradientBoostingClassifier, VotingClassifier, RandomForestClassifier

from mlxtend.classifier import StackingClassifier, StackingCVClassifier
from mlxtend.feature_selection import ColumnSelector

from sklearn.pipeline import make_pipeline
import numpy as np

from sklearn.feature_selection import RFE

import gc
