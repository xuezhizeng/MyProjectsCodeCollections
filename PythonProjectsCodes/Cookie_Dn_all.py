
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

C=[{u'domain': u'www.freelancer.com',
  u'expiry': 1544207018,
  u'httpOnly': False,
  u'name': u'uniform_id_linked',
  u'path': u'/',
  u'secure': True,
  u'value': u'linked'},
 {u'domain': u'www.freelancer.com',
  u'expiry': 1544207018,
  u'httpOnly': False,
  u'name': u'_tracking_session',
  u'path': u'/',
  u'secure': False,
  u'value': u'003d1f83-0499-2267-9889-de6faf69e341'},
 {u'domain': u'.freelancer.com',
  u'expiry': 1575743036,
  u'httpOnly': False,
  u'name': u'_ga',
  u'path': u'/',
  u'secure': False,
  u'value': u'GA1.2.39179155.1512671019'},
 {u'domain': u'www.freelancer.com',
  u'expiry': 1513275834,
  u'httpOnly': False,
  u'name': u'XSRF-TOKEN',
  u'path': u'/',
  u'secure': True,
  u'value': u'cP901C5DlKNE7eozLmVqEwnpQpKVhNGx96Zd20HXv9QKsHwbFyDAbgeC6hwwCjlz'},
 {u'domain': u'.freelancer.com',
  u'expiry': 1515263034.616373,
  u'httpOnly': False,
  u'name': u'GETAFREE_USER_ID',
  u'path': u'/',
  u'secure': True,
  u'value': u'26600248'},
 {u'domain': u'.freelancer.com',
  u'expiry': 1515263034.616431,
  u'httpOnly': False,
  u'name': u'GETAFREE_AUTH_HASH_V2',
  u'path': u'/',
  u'secure': True,
  u'value': u'sgwgk7UMRsCwu24FzTqmTBeKhzB%2BPYZ52wskJU%2FmESw%3D'},
 {u'domain': u'www.freelancer.com',
  u'expiry': 1528223034.616457,
  u'httpOnly': True,
  u'name': u'qfence',
  u'path': u'/',
  u'secure': True,
  u'value': u'eyJhbGciOiJIUzI1NiIsInR5cCI6IkZyZWVsYW5jZXJcXEdBRlxcQ29yZVxcSldUXFxKV1QifQ.eyIyNjYwMDI0OCI6MTUxMjY3MTAzNCwic3ViIjoicXVpY2tsb2dpbmZlbmNlIiwiaWF0IjoxNTEyNjcxMDM0fQ.5x_lMucGsOmnQI4EyBpuwJz2Mm7ZfPooIRViV0uRAqE'},
 {u'domain': u'.freelancer.com',
  u'expiry': 1828031034.616486,
  u'httpOnly': False,
  u'name': u'GETAFREE_NOTNEW',
  u'path': u'/',
  u'secure': True,
  u'value': u'true'},
 {u'domain': u'.freelancer.com',
  u'expiry': 1544207034.616527,
  u'httpOnly': False,
  u'name': u'GETAFREE_LANGUAGE',
  u'path': u'/',
  u'secure': True,
  u'value': u'en'},
 {u'domain': u'.freelancer.com',
  u'expiry': 1512757436,
  u'httpOnly': False,
  u'name': u'_gid',
  u'path': u'/',
  u'secure': False,
  u'value': u'GA1.2.889223541.1512671019'},
 {u'domain': u'.freelancer.com',
  u'expiry': 1512672837,
  u'httpOnly': False,
  u'name': u'_uetsid',
  u'path': u'/',
  u'secure': False,
  u'value': u'_uete2aebc29'},
 {u'domain': u'.freelancer.com',
  u'expiry': 1512672837,
  u'httpOnly': False,
  u'name': u'__asc',
  u'path': u'/',
  u'secure': False,
  u'value': u'a21410551603238028438af533c'},
 {u'domain': u'.freelancer.com',
  u'expiry': 1544293437,
  u'httpOnly': False,
  u'name': u'__auc',
  u'path': u'/',
  u'secure': False,
  u'value': u'a21410551603238028438af533c'},
 {u'domain': u'www.freelancer.com',
  u'expiry': 1544207038,
  u'httpOnly': False,
  u'name': u'session2',
  u'path': u'/',
  u'secure': False,
  u'value': u'e731100c67f1da9aba000daca698570f98d4f8a0f464e6287712304aeb9ef5fcf4e4e1be65941cdf'}]
# In[ ]:

s = requests.Session()
for cookie in C:
    s.cookies.set(cookie['name'], cookie['value'])

try:
    os.mkdir('./All_cookie_htmls')
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
        one=s.get(pre+str(name)+'.html')
    except:
#         print 'X',
        fail.append(name)
    with open('All_cookie_htmls/{}.html'.format(name), 'w+') as fl:
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
            print len(os.listdir('./All_cookie_htmls'))
            os.remove('fail.csv')
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
	if len(fail)>50:
        	pd.DataFrame(fail, columns=['ID']).to_csv('fail.csv',index=False)
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
