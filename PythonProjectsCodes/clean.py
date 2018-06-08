
# coding: utf-8

# In[1]:
import sys  

reload(sys)  
sys.setdefaultencoding('utf8')

# !ls


# In[39]:


import pandas as pd
import os


# In[35]:
from unidecode import unidecode

def FormatString(s):
    if isinstance(s, unicode):

        try:
            s.encode('ascii')
            return s
        except:
            return unidecode(s)
    else:
        return s


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


for i in [i for i in os.listdir('.') if i.endswith('csv') and (i.startswith('golden') or (i.startswith('Json')) or (i.startswith('first')))]:
    df = pd.read_csv(i)
    print i, df.shape
    try:
        df = df[~df['userId'].isnull()]
        df['public_firstname']=df['about.public_name'].apply(helper)
    except:
        print 'what?'
    print 'remove mismatching', df.shape
    df = df[((df['username'].str.lower()==df['about.username'].str.lower()) | (df['userId']==df['about.id']))].reset_index(drop=True)
    print 'done',df.shape
    df.to_csv('clean_'+i, index=False)
    print 'done saving'
    os.rename(i, 'old_'+i)
    print 'done deleting'
    df = df.applymap(FormatString)
    print 'convert to xlsx'
    df.to_excel('clean_'+i[:-3]+'xlsx', index=False)
    print 'done saving to xlsx'
# In[38]:


# df.shape

