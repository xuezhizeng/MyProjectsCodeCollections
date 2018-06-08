
# coding: utf-8

print 'start'
# In[2]:


import sys
reload(sys)
sys.setdefaultencoding('utf8')


# In[9]:

import pandas as pd
import os
from time import time, ctime

import concurrent.futures

from lxml import etree
import json
import re

import ast


# In[10]:

# path='technosystem.html'

folder='Golden_cookie_htmls/'
cont = os.listdir(folder)
cont = [i for i in cont if i[-4:]=='html']

#cont=cont[:100]


print 'No. of files:',len(cont)

collect=[]

def get_columns(path):
    from time import ctime
    global failed_names, collect, n
    
    n+=1
    if n%5000==0 or n==1:
        print ctime(), ': processed', n, 'and failed: ',len(failed_names)
    get=[]
    
    with open(folder+path,'r') as fl:
        text=fl.read()
        tree=etree.HTML(text)
    try:
        collect.append([path, tree.xpath('//h1[@class="PageProfile-info-name"]/text()')[0].strip()])    
    except Exception as e:
        failed_names.append(path)
        

    


# 1533

# ### multi

# In[42]:

def batch(allnames):
    global collect
    start=time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=64) as executor:
        executor.map(get_columns, allnames)
    past='{:.2f}'.format(time()-start)
    now=ctime()[4:]

    print 'profiles ',len(allnames),'  used ',past,'s', now
    return past


# ### multi starts

# In[43]:

# initialize
n=0
initial = pd.DataFrame()
collect=[]
failed_names=[]


# start
eclipse = batch(cont)

print 'concat dataframe'
print ctime()
print eclipse

print ctime()
delete=[]
    
df=pd.DataFrame(collect, columns=['UsernameOrUserID','name'])
def helper(x):
    S = x.split()
    if len(S)>1:
        return S[0]
    else:
        return x

df['FirstName']= df['name'].apply(helper)
df['UsernameOrUserID']=df['UsernameOrUserID'].str[:-5]


# In[76]:
print 'save df'
print ctime()


print 'write to txt'

print '! saving to csv'
print ctime()
#saving(start)
a=ctime().split()
aa='_'.join([a[1],a[2],a[-1]])
# In[77]:
aa='_'+aa


df.to_csv('firstname_golden'+aa+'.csv',index=False)
print 'done'
print ctime()

# In[ ]:




print ctime()

exit()
# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:



