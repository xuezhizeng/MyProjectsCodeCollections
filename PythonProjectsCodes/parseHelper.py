import ast
import pandas as pd
from collections import defaultdict

iniDict = defaultdict(lambda: None)
n=0
initial = pd.DataFrame()
collect=[]
failed_names=[]


def flatten_dict(data, layers=1, drop_deeper=False):

        for _ in range(layers):
            data = [(k, v) if not isinstance(v, dict) else [(k + '.' + k2, v2) for k2, v2 in v.items()] for k, v in
                    data.items()]
            data = [item for sublist in data for item in sublist if isinstance(sublist, list)] + [y for y in data if
                                                                                                  not isinstance(y,
                                                                                                                 list)]
            data = dict(data)

        if drop_deeper:
            data = {k: v for k, v in data.items() if not isinstance(v, dict) or isinstance(v, list)}

        return data







def string_dict(string, layers=1, val=None):
    dictionary = ast.literal_eval(string)
    flattened = flatten_dict(dictionary, layers=layers)
    if val:
        return flattened[val]
    else:
        return flattened
    


def SeriesStringDictToDataframe(Series, layer=2):
    coll=[]
    def make(string):
        dic = ast.literal_eval(string)
        flattened = flatten_dict(dic, layers=layer)
        return flattened
    for i in Series:
        coll.append(make(i))
    df=pd.DataFrame(coll)
    return df

def CountListLength(String):
  
    List = ast.literal_eval(String)
    return len(List)


import matplotlib.pyplot as plt
import numpy as np
import itertools

def plot_confusion_matrix(cm, classes, normalize=False,
                  title='Confusion matrix',
                  cmap=plt.cm.Blues):

    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.show()

