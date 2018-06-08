
# coding: utf-8

# In[5]:


import os
import shutil


# In[6]:




# In[21]:


folder='new/'

folder = str(raw_input('folder name ? :  '))+'/'
pre = str(raw_input('pre name ? :  '))

# In[22]:


all_files = os.listdir(folder)
len(all_files)


# In[23]:


n=0
m=0
for i in all_files:
    
    if n==0 or n%5000==0:
        m+=1
        sub = pre+'_sub_'+str(m)+'/'
        print sub
        try:
            os.mkdir(folder+sub)
        except Exception as e:
            print e
            
    n+=1
    
    try:
        shutil.move(folder+i, folder+sub+i)
    except Exception as e:
        print e

