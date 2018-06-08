
# coding: utf-8

# In[1]:

import concurrent.futures

import requests
from lxml import etree
from time import time, ctime

import pandas as pd
import cx_Oracle



db=cx_Oracle.connect("soyoung", "soyoung", "my.uconn.science:1521/xe")
print db.version
conn=db.cursor()

save=[]

def single((ID, url)):
    try:
        content=etree.HTML(requests.get(url, timeout=600).text).xpath('//div[@class="c"]//*[@title]/@src')
    except:
        save.append([ID, 'fail'])
    for i in content:      
        save.append([ID, i])


# In[2]:

# try:
#     conn.execute("create table single \
#              (ID int not null, url varchar2(150), get_time varchar2(50), ellipse number, \
#              constraint single_pk primary key (url))")
#     db.commit()
#     print 'create table single'
# except Exception as e:
#     print e
    
# try:
#     conn.execute("create table fail \
#              (ID int , url varchar2(150), get_time varchar2(50), ellipse number)")
#     db.commit()
#     print 'create table fail'
# except Exception as e:
#     print e   


# In[57]:




# In[5]:

# db.commit()


# In[6]:

# %%time

def batch(subber):
    global save
    start=time()
    save=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        executor.map(single, subber)

    past='{:.2f}'.format(time()-start)
    now=ctime()[4:]
    
    print 'get ',len(subber),' users used ',past,'s', now, 'images',len(save)

    for i in save:
        try:
            conn.execute("insert into single (ID, url, get_time, ellipse)             values ({},'{}','{}',{})".format(i[0], i[1], now, past))
        except:
            try:
                conn.execute("insert into fail (ID, url, get_time, ellipse)             values ({},'{}','{}',{})".format(i[0], i[1], now, past))        
            except:
                conn.execute("insert into fail (ID, url, get_time, ellipse)             values ({},'{}','{}',{})".format(i[0], 'failed', now, past))
    db.commit()
    print 'saved to the database ',ctime()[4:]
    print 'failed!: ',sum(map(lambda x: x[1]=='fail', save)) 

    


# In[7]:

def spl(lists, n):
    return  [lists[i:i + n] for i in range(0, len(lists), n)]


# In[ ]:

if __name__=='__main__':
    choose=raw_input('which set (60-85)?: ')
    df=pd.read_csv(str(choose)+'.csv')
    nn=df.shape[0]
    print nn,' IDs'
    
    urls = zip(df['id'], df['post_url'])
    print len(urls)==nn
    
    many=int(raw_input('how many IDs a batch?: '))
      
    
    p=0
    q=0
    for i in spl(urls, many):
        q+=1
        batch(i)
        p+=many/float(nn)
        print p*100,'%', nn, many*q 
