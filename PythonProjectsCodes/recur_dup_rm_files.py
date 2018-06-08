
import pandas as pd
import os
import chardet
import shutil




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


df = pd.DataFrame(content, columns=['url'])

df['name'] = df['url'].apply(lambda x: ''.join(x.split('/')[-1]))
df = df.set_index('name')

print 'folder contains: ',df.shape



CSV = raw_input('csv: to_be_deleted: ')

df2 = pd.read_csv(CSV, usecols=['name'])
df2['name'] = df2['name'].apply(lambda x: ''.join(x.split('/')[-1]))
df2 = df2.set_index('name')
print 'already have: ', df2.shape


df0 = df.join(df2, how='inner')
print 'to be delete: ', df0.shape

try:
    os.mkdir('duplicate')
except Exception as e:
    print e

fail=[]
for i in df0['url']:
    try:
        shutil.move(i,'duplicate')
    except Exception as e:
#         print e
        fail.append(i)
print 'failed to move: ', len(fail)
