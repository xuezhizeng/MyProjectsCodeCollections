
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
    os.mkdir('./all_htmls')
except:
    print 'exists'


# In[25]:

pre='https://www.freelancer.com/users/'


# In[32]:

def getsingle(name):
    global fail, n
    n+=1
    if n%5000==0 or n==1:
        print ctime(), 'of ', n, 'failed', len(fail)
    try:
        one=requests.get(pre+str(name)+'.html')
    except:
#         print 'X',
        fail.append(name)
    with open('all_htmls/{}.html'.format(name), 'w+') as fl:
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
        f=pd.read_csv('fail2.csv')
	print 'fail exists'
        if f.shape[0]>20:
            fail=[]
            batch(f.values)
     	    os.remove('fail2.csv')
	    print 'Done!'
	    print 1
	    exit()
            # pd.DataFrame(fail, columns=['username']).to_csv('fail.csv',index=False)
        else:
            print 'Scrape Success!!!'
            print len(os.listdir('./all_htmls'))
            os.remove('fail2.csv')
	    print 2
            exit()
        
    except:
	print 3
	print 'fail not exists'
        df=pd.read_csv('IDAll.csv')
        print len(df['ID'].unique()), df.shape
        allemp=df['ID'].tolist()
        print len(allemp)
        fail=[]
        batch(allemp)
	if len(fail)>-1:
        	pd.DataFrame(fail, columns=['ID']).to_csv('fail2.csv',index=False)
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


