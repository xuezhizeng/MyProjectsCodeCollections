
# coding: utf-8

# In[1]:

import pandas as pd
import os
import shutil


# In[ ]:

csvN = raw_input('para_csv name: ')


# In[2]:

df = pd.read_csv('./'+csvN, usecols=['name'])
print df.shape


# In[ ]:

df0=df.copy()


# In[11]:

path = '/home/soyoung/face/newFlask/static/phos/'

df['exists']=df['name'].apply(lambda x: os.path.exists(path+x))
# In[12]:



# In[13]:

print 'exists file: ', df['exists'].sum()


# In[14]:

df[~df['exists']].index


# In[21]:

# 538009-537967


# In[17]:

# df0 = pd.read_csv('./2_Nov_54W_V6.csv')
# df0.shape


# In[18]:

df1 = df0.iloc[df[df['exists']].index,:]
df1.shape


# In[19]:

df1 = df1.reset_index(drop=True)
df1.shape


# In[1]:

# df1.tail()


# In[ ]:

print 'missing and to be removed', df0.shape[0]-df['exists'].sum()
yes = raw_input('r u sure y/n ?: ')
if yes=='y':
    pass
else:
    exit()


# In[ ]:

# df1.to_csv('./'+csvN, index=False)


# In[ ]:



