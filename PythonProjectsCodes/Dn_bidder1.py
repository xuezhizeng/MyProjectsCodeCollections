
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

try:
    os.mkdir('./bidder_pages')
except:
    print 'exists'


# In[25]:

pre='https://www.freelancer.com/u/'


# In[32]:

def getsingle(name):
    global fail, n
    n+=1
    if n%5000==0 or n==1:
        print ctime(), 'of ', n, 'failed', len(fail)
    try:
        one=requests.get(pre+name)
    except:
#         print 'X',
        fail.append(name)
    with open('bidder_pages/{}.html'.format(name), 'w+') as fl:
        fl.write(one.text)
#     print 'O',
    


# In[37]:

def batch(allnames):
    global n
    n=0
    start=time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=64) as executor:
        executor.map(getsingle, allnames)
    past='{:.2f}'.format(time()-start)
    now=ctime()[4:]

    print 'profiles ',len(allnames),'  used ',past,'s', now


# In[ ]:




# In[ ]:




# In[ ]:

if __name__=='__main__':
    try:
        f=pd.read_csv('fail.csv')
	print 'fail exists'
        if f.shape[0]>20:
            fail=[]
            batch(f.values)
     	    os.remove('fail.csv')
	    print 'Done!'
	    print 1
	    exit()
            # pd.DataFrame(fail, columns=['username']).to_csv('fail.csv',index=False)
        else:
            print 'Scrape Success!!!'
            print len(os.listdir('./bidder_pages'))
            os.remove('fail.csv')
	    print 2
            exit()
        
    except:
	print 3
	print 'fail not exists'
        df=pd.read_csv('users.gender.golden.csv')
        print len(df['username'].unique()), df.shape
        allemp=df['username'].tolist()
        print len(allemp)
        fail=[]
        batch(allemp)
	if len(fail)>50:
        	pd.DataFrame(fail, columns=['username']).to_csv('fail.csv',index=False)
    	else:
		print 'done!', ctime()


# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[1]:



# In[2]:


