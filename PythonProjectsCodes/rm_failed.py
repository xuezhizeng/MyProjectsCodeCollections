
# coding: utf-8

# In[1]:

import pandas as pd


# In[2]:

df = pd.read_csv('fail.csv')
df.shape


# In[19]:

df0=pd.read_csv('combine_para.csv')
df0.shape


# In[9]:

dic={}


# In[10]:

for i in df['fail']:
    dic[i[:-3]]=0


# In[16]:

def chk(x):
    x=x[:-3]
    try:
        dic[x]
        return False
    except:
        return True


# In[24]:

# %%time
df9 = df0[df0['name'].apply(chk)]
df9 = df9.reset_index(drop=True)
df9.to_csv('para_combine_rm.csv', index=False)


# In[ ]:




