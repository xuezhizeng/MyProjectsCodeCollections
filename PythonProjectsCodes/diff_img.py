
# coding: utf-8

# In[8]:

import concurrent.futures
import requests
import os

from time import time, ctime
import pandas as pd

fail=[]


# In[ ]:




# In[ ]:




# In[16]:

def download_image(img_url):
    global direct
    
    try:
        ID, url = img_url.split('__')
        cont = url.split('/')
        name= str(ID)+'_'+str(cont[-4])+str(cont[-1]).replace('_570','')
        
    except Exception as e:
        fail.append(img_url)
        print 'X1',

        
        
    try:
        img_request = requests.request(
            'get', url, stream=True, timeout=300)
        if img_request.status_code != 200:
            fail.append(img_url)
            print 'X2',
    except Exception as e:
        fail.append(img_url)
        print 'X3',

    try:
        img_content = img_request.content
        with open(os.path.join(direct,  name), 'wb') as f:
            byte_image = bytes(img_content)
            f.write(byte_image)
            
    except Exception as e:
        fail.append(img_url)
        print 'X4',



# In[17]:

def batch(subber):
    start=time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        executor.map(download_image, subber)
    past='{:.2f}'.format(time()-start)
    now=ctime()[4:]

    print 'imges ',len(subber),'  used ',past,'s', now


# In[18]:

def spl(lists, n):
    return  [lists[i:i + n] for i in range(0, len(lists), n)]


# In[ ]:

if __name__=='__main__':
    
    choose=raw_input('which set (1-24)?: ')
    try:
        os.mkdir('.img_'+str(choose))
    except Exception as e:
        print e
        print 'dir img_'+str(choose)+' exists'
    
    direct='img_'+str(choose)
    df=pd.read_csv('img_'+str(choose)+'.csv')
    nn=df.shape[0]
    print nn,' pics'
    
    
    #apply diff
    folder=pd.DataFrame(os.listdir('./img_'+str(choose)), columns=['url'])
    print folder.shape
    
    df['parse']=df['URL'].apply(lambda x: x.split('/')[-1]).apply(lambda x: x.split('_')[0])
    folder['parse']=folder['url'].apply(lambda x: x.split('_')[-1][:-4][-17:])
    
    joind=df.set_index('parse').join(folder.set_index('parse'))
    
    new_df = joind[joind['url'].isnull()][['ID','URL']]
    
    nnn=new_df.shape[0]
    print 'getiing ',nnn,'diff new pics!'
    
    
    
    urls=[]
    for i in new_df.itertuples():
        urls.append(str(i[1])+'__'+str(i[2]))
    # print len(urls)==nn
    
    many=int(raw_input('how many IDs a batch?: '))
      
    
    p=0
    q=0
    for i in spl(urls, many):
        q+=1
        batch(i)
        p+=many/float(nnn)
        print p*100,'%', nnn, many*q 

    fl = pd.DataFrame(fail, columns=['fail_url'])
    fl.to_csv('failed_img_'+str(choose)+'.csv', index=False)
# In[ ]:



