
# coding: utf-8

# In[1]:


# !ls


# In[39]:


import pandas as pd
import os


# In[35]:


# df.isnull().all(axis=1).sum()


# In[36]:


# df['userId'].isnull().sum()


# In[37]:


# df.head(1)


# In[22]:


# n=0
# for i in df: 
#     n+=1
#     print n, i
#     print df[i].value_counts().tail(3)
#     print 


# In[30]:


def helper(x):
    try:
        return x.split()[0]
    except:
        return x


# In[51]:


for i in [i for i in os.listdir('.') if i.endswith('csv') and (i.startswith('golden') or (i.startswith('Json')))]:
    df = pd.read_csv(i)
    print i, df.shape
    df = df[~df['userId'].isnull()]
    df['public_firstname']=df['about.public_name'].apply(helper)
    df.to_csv('clean_'+i, index=False)
    print 'done saving'
    os.remove(i)
    print 'done deleting'


# In[38]:


# df.shape

