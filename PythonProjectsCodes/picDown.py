import concurrent.futures
import requests
import os

from time import time, ctime
import pandas as pd



def download_image(input_list):
    ID, url, folder = input_list
    fail=[]
    name= str(ID)+'_profile.jpg'
        
        
    try:
        img_request = requests.request(
            'get', url, stream=True, timeout=300)
        if img_request.status_code != 200:
            fail.append(ID)
            print 'X2',
    except Exception as e:
        # print e
        fail.append(ID)
        print 'X3',

    try:
        img_content = img_request.content
        with open(os.path.join(folder,  name), 'wb') as f:
            byte_image = bytes(img_content)
            f.write(byte_image)
            
    except Exception as e:
        # print e
        fail.append(ID)
        print 'X4',
    if fail!=[]:
        
        print list(set(fail)),

def batch(func, subber):
    start=time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        executor.map(func, subber)
    past='{:.2f}'.format(time()-start)
    now=ctime()[4:]

    print 'imges ',len(subber),'  used ',past,'s', now
