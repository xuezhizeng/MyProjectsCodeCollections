
# coding: utf-8

# In[3]:


import pandas as pd
import shutil
import os


# In[4]:


path = '/home/soyoung/face/newFlask/static/phos/'
# path = '/home/soyoung/face/Handsome_Pics/handsome/ori/keep/'


# In[1]:


path = raw_input('target_phos_folder: ')

path = path+'/'
# In[ ]:


CSV = raw_input('csv: to_be_deleted: ')


# In[16]:


df = pd.read_csv(CSV, usecols=['name'])
print df.shape
print df.head(3)


# In[18]:


trash = 'trash0/'
try:
    os.mkdir(trash)
except Exception as e:
    print e


# In[21]:


failed=[]
for i in df['name']:
    try:
        shutil.move(path+i, trash+''.join(i.split('/')[-1:]))
    except Exception as e:
#         print e
        failed.append(i)
#         print 'X',
print 'failed num',len(failed)

