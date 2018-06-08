
# coding: utf-8

# In[31]:


import pandas as pd
import os
import chardet
import shutil

the_encoding = chardet.detect('your string')['encoding']


# In[32]:




# In[33]:


path = ''
path = raw_input('target_folder: ')
path = path+'/'

# In[36]:


content =[]
for i in [i for i in os.listdir(path) if i.find('.')<0] :
    for j in os.listdir(path+i):
        for k in os.listdir(path+i+'/'+j):
            content.append(path+i+'/'+j+'/'+k)
print len(content)


# In[37]:


df = pd.DataFrame(content, columns=['name'])
df.shape


# In[38]:


df['chk'] = df['name'].apply(lambda x: chardet.detect(x)['encoding'])


# In[40]:


try:
    os.mkdir('utf_8')
except Exception as e:
    print e


# In[41]:


df[df['chk']!='ascii']


# In[ ]:


print 'to_be_moved: ',df[df['chk']!='ascii'].shape[0]


# In[42]:


fail=[]
for i in df[df['chk']!='ascii']['name']:
    try:
        shutil.move(i,'utf_8')
    except Exception as e:
        print e
        fail.append(i)
print len(fail)

