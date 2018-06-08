
# coding: utf-8

# In[1]:


# !ls -hl|grep csv
import pandas as pd
import numpy as np
import os
from time import time, ctime

from sklearn.metrics import accuracy_score, classification_report, classification, confusion_matrix
from sklearn.model_selection import train_test_split, KFold, cross_val_score, StratifiedKFold, StratifiedShuffleSplit

dim=lambda *x: [i.shape for i in x]


# In[2]:




# In[1]:


import os
import tensorflow as tf
from tensorflow.python.client import device_lib

from keras import backend as K

config = tf.ConfigProto()
config.gpu_options.allow_growth=True
sess = tf.Session(config=config)

K.set_session(sess)

# sess = tf.Session(config=tf.ConfigProto(log_device_placement=True))

os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"   # see issue #152
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

print(device_lib.list_local_devices())


# In[4]:




# In[5]:




# In[6]:


pd.options.display.max_columns=100
df.head(3)


# In[7]:


X = df.iloc[:,2:].values
print X.shape
y = df.iloc[:,1].map({'male':1,'female':0}).values
print y.shape


# In[8]:




# In[9]:




# In[10]:


# remove one dummy variable to avoid dummy variable trap
print X.shape
X = X[:, 1:]
print X.shape


# In[11]:


from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3,
                                                   random_state=7)
dim(X_train, X_test, y_train, y_test)


# In[12]:


# ### build ANN

# In[13]:


classifier = Sequential()
# first hidden layer
classifier.add(Dense(units = 256, 
                     input_dim=4491,
                     kernel_initializer='uniform', activation='relu'))
classifier.add(Dropout(rate= 0.5))
# second hidden layer
classifier.add(Dense(units = 128,  kernel_initializer='uniform', activation='relu'))
classifier.add(Dropout(rate= 0.4))
# second hidden layer
classifier.add(Dense(units = 64,  kernel_initializer='uniform', activation='relu'))
classifier.add(Dropout(rate= 0.3))
# thrid hidden layer
classifier.add(Dense(units = 48,  kernel_initializer='uniform', activation='relu'))
classifier.add(Dropout(rate= 0.2))
# thrid hidden layer
classifier.add(Dense(units = 32,  kernel_initializer='uniform', activation='relu'))
classifier.add(Dropout(rate= 0.1))
# thrid hidden layer
classifier.add(Dense(units = 24,  kernel_initializer='uniform', activation='relu'))
classifier.add(Dropout(rate= 0.1))
# thrid hidden layer
classifier.add(Dense(units = 256,  kernel_initializer='uniform', activation='relu'))
classifier.add(Dropout(rate= 0.5))
# # ouput layer
classifier.add(Dense(units = 1,  kernel_initializer='uniform', activation='sigmoid'))
# compiling the ANN
classifier.compile(optimizer='adam', loss='binary_crossentropy', metrics= ['accuracy'])
classifier.summary()


# In[14]:


from keras.callbacks import Callback, EarlyStopping
class TestCallback(Callback):
    def __init__(self, test_data):
        self.test_data = test_data
        

    def on_epoch_end(self, epoch, logs={}):
        x, y = self.test_data
        loss, acc = self.model.evaluate(x, y, verbose=1)
        print('\nTesting loss: {}, acc: {}\n'.format(loss, acc))


# In[15]:


stopping = EarlyStopping(monitor='acc', min_delta=0,
                              patience=6, verbose=1, mode='auto')


# In[16]:




# In[53]:




# ### parameter tuning

# In[19]:


from keras.wrappers.scikit_learn import KerasClassifier
# k-fold cross validation
from sklearn.model_selection import GridSearchCV

