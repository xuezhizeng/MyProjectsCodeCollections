
# coding: utf-8

# In[35]:

import pandas as pd
import os
from time import time, ctime

import concurrent.futures
import requests
from lxml import etree
from bs4 import BeautifulSoup

import sys
reload(sys)
sys.setdefaultencoding("utf-8")


# In[ ]:




# In[3]:

try:
    os.mkdir('bidder_pages')
except:
    print 'exists'


# In[8]:

df=pd.read_csv('uploads/users.gender.golden.csv')


# In[25]:

pre='https://www.freelancer.com/u/'


# In[27]:

print len(df['username'].unique()), df.shape


# In[31]:

allemp=df['username'].tolist()
print len(allemp)
allemp[:3]


# In[32]:

def getsingle(name):
    global fail
    try:
        one=requests.get(pre+name)
    except:
        print 'X',
        fail.append(name)
    with open('bidder_pages/{}.html'.format(name), 'w+') as fl:
        fl.write(one.text)
#     print 'O',
    


# In[36]:

getsingle('superwanchiu')


# In[37]:

def batch(allnames):
    start=time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        executor.map(getsingle, allnames)
    past='{:.2f}'.format(time()-start)
    now=ctime()[4:]

    print 'profiles ',len(allnames),'  used ',past,'s', now


# In[ ]:

fail=[]
batch(allemp)


# In[1]:

while len(fail)


# In[2]:

a=['123','fff','ccc']


# In[4]:

import pandas as pd


# In[6]:

pd.DataFrame(a, columns=['name'])


# In[ ]:



