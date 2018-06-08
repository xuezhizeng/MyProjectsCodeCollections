
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


# In[1]:


import os
import tensorflow as tf
from tensorflow.python.client import device_lib

# from keras import backend as K

# config = tf.ConfigProto()
# config.gpu_options.allow_growth=True
# sess = tf.Session(config=config)

# K.set_session(sess)

# sess = tf.Session(config=tf.ConfigProto(log_device_placement=True))

#os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"   # see issue #152
#os.environ["CUDA_VISIBLE_DEVICES"] = "1"

print(device_lib.list_local_devices())


# In[4]:


from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from keras.optimizers import Adam
from keras.preprocessing.image import ImageDataGenerator



import os



# from tensorflow.python.client import device_lib
# print(device_lib.list_local_devices())


# In[5]:


df = pd.read_csv('./ready.csv')
print (df.shape)
X=df.values

# In[6]:
y=pd.read_csv('./label_ready.csv')['label'].values

# In[7]:




# In[8]:




# In[11]:


from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3,
                                                   random_state=7)


# In[12]:


from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
# fit on training set
X_train = sc.fit_transform(X_train)
# only transform on test set
X_test = sc.transform(X_test)
print (dim(X_train,X_test, y_train, y_test))


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
classifier.compile(optimizer='adam',loss='binary_crossentropy', metrics= ['accuracy'])
print (classifier.summary())


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


# fitting ANN with training set
classifier.fit(X_train, y_train, 
               batch_size=128, epochs=128,
               validation_data=(X_test, y_test),
          callbacks=[TestCallback((X_test, y_test))])
#           callbacks=[stopping])
    


# In[53]:


y_pred = classifier.predict(X_test)
y_pred = (y_pred> 0.5)

print (accuracy_score(y_test, y_pred))
cm = confusion_matrix(y_test, y_pred)
print (cm)

