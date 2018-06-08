
# coding: utf-8

# In[7]:

import os
import shutil
import pandas as pd


# In[2]:

target=raw_input('target folder: ')


# In[5]:

save = 'keep'


# In[6]:

try:
    os.mkdir(save)
except:
    print 'X'


# In[11]:

df = pd.read_csv('combine_para.csv')
df.shape


# In[18]:

# df.head()


# In[16]:

for i in os.listdir(target):
    try:
        os.mkdir(save+'/'+i)
    except:
        print 'X',


# In[17]:

# for i in df['url']:
#     print i[7:]
#     break


# In[ ]:

fail=[]
for i in df['name']:
    
    try:
        shutil.move(target+'/'+i, save+'/'+i)
    except Exception as e:
	#print e
	#break
	try:
		shutil.move(target+'/'+i[:-3]+'JPG', save+'/'+i[:-3]+'jpg')
	except:
		print 'X',
		fail.append(i)

#print fail
print 
print len(fail)
pd.DataFrame(fail, columns=['fail']).to_csv('fail.csv',index=False)
