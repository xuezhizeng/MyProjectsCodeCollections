
# coding: utf-8

# In[29]:

import pandas as pd


# In[30]:

df1=pd.read_csv('labels.csv', names=['name'])
df1=df1.reset_index(drop=True)
df1.shape


# In[31]:

df2=pd.read_csv('reps.csv', header=None)
df2.shape


# In[32]:

length = len(df1['name'][0].split('/')[0])+1
df1['name']=df1['name'].apply(lambda x: x[length:-3]+'jpg')


# In[33]:

df1.head()


# In[34]:

df2['name']=df1['name']
df2.shape


# In[36]:

df2.to_csv('combine_para.csv', index=False)


# In[ ]:




