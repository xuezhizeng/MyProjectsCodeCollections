
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

folder='Combined_final_htmls/'
cont = os.listdir(folder)
cont = [i for i in cont if i[-4:]=='html']

#cont=cont[:10001]

print 'No. of files:',len(cont)
# In[11]:

def flatten_dict(data, layers=1, drop_deeper=False):

        for _ in range(layers):
            data = [(k, v) if not isinstance(v, dict) else [(k + '.' + k2, v2) for k2, v2 in v.items()] for k, v in
                    data.items()]
            data = [item for sublist in data for item in sublist if isinstance(sublist, list)] + [y for y in data if
                                                                                                  not isinstance(y,
                                                                                                                 list)]
            data = dict(data)

        if drop_deeper:
            data = {k: v for k, v in data.items() if not isinstance(v, dict) or isinstance(v, list)}

        return data


# In[12]:

from collections import defaultdict
iniDict = defaultdict(lambda: None)


# In[8]:






def get_columns(path):
    from time import ctime
    global failed_names, collect, n
    
    n+=1
    if n%5000==0 or n==1:
        print ctime(), ': processed', n, 'and failed: ',len(failed_names)
    get=[]
    
    with open(folder+path,'r') as fl:
        text=fl.read()
#         tree=etree.HTML(text)
    try:
#         script = tree.xpath('//script')[-2]
        data = re.search(r"window.profileData=(.*?)\n", text)        
        jsondata=data.group(1)[:-1]
        
        json_dict = json.loads(jsondata)
        flat = flatten_dict(json_dict, layers=1)
        for i in flat:
            iniDict[i]=str(flat[i])
        collect.append(pd.DataFrame(iniDict, index=[path]))
            
#         return pd.DataFrame(iniDict, index=[0])
#         names = flat.keys()
#         return flat
    except Exception as e:
        # print 'X',
        failed_names.append(path)
        collect.append(pd.DataFrame(index=[path]))
        

    


# 1533

# ### multi

# In[42]:

def batch(allnames):
    global collect
    start=time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=24) as executor:
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


#cont=cont[:5001]
# start
#eclipse = batch(cont)
for i in cont:
	get_columns(i)

print 'concat dataframe'
print ctime()
# print eclipse

n=0
print 'list count',len(collect)
#for i  in collect:
#    initial=initial.append(i)
#    n+=1
#    print n
#    print ctime()
# In[53]:

print ctime()
print 'start concat'
initial=pd.concat(collect)

print 'done df, copying'
print ctime()
start=initial.copy()
print 'done copy'
print ctime()


# In[55]:

print start.shape

# In[72]:
print 'start making df'
print ctime()
delete=[]
for i in start:
#     print i
#     print start[i].value_counts().head(5)
#     print 
#     print 
    try:
        if start[i].value_counts(dropna=False).head(1).sum()>=int(start.shape[0]*0.97):
            delete.append(i)
    except:
        print i
#         print i
print len(delete)
    


# In[76]:
print 'save df'
print ctime()
start = start.drop(delete, axis=1)
start = start.reset_index(drop=False)
print start.shape
print ctime()


print 'write to txt'
#start.to_csv('bidder1_JSON.csv',index=False,chucksize=100,mode='w')

#with open('result.txt','w') as fl:
#	for i in range(start.shape[0]):
#		for i in start.iloc[i,:]:
#			fl.write(str(i))
#			fl.write(',')
#		fl.write('\n')

#def saving(df):		
#	flag=True
#	while df.shape[0]!=0:
#	    tmp=df.iloc[:100,:]
#	    df=df.iloc[100:,:]
#	    if flag:
#	        tmp.to_csv('goden.csv', index=False, mode='a')
#	        flag=False
#		print ctime()
#	    else:
#	        tmp.to_csv('goden.csv', index=False,header=None, mode='a')
#		print ctime()
#	print 'saving complete'
#	print ctime()


print '! saving to csv'
print ctime()
#saving(start)
a=ctime().split()
aa='_'.join([a[1],a[2],a[-1]])
# In[77]:
aa='_'+aa


start.to_csv('Json_updated_debug'+aa+'.csv',index=False)
print 'done'
print ctime()

# In[ ]:




print ctime()

exit()
# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:



