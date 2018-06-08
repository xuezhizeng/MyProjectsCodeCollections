import boto3
import os
from time import time
import json

from pymongo import MongoClient
mango = MongoClient(host='dsnotebook.bid', port=27017, username='face', password='rekognition')

db=mango['explore']
coll=db['research']

client = boto3.client(
    'rekognition',
    aws_access_key_id = '',
    aws_secret_access_key=''
)

def face2folder2mango(path):
    #collection={}
    if path[-1]!='/':
        path+='/'
    dr=os.listdir(path)
    
    print len(dr), 'files in the folder'
    flag = int(raw_input('all many pics do you want to push? '))
    if flag>=len(dr):
        flag=len(dr)
    dr=dr[0:flag]
    print 'pushing...', len(dr)
    
    n=0
    start=time()
    for i in dr:
        n+=1
        
        try:

            with open(path+i, 'rb') as image:
                response = client.detect_faces(Image={'Bytes': image.read()}, Attributes=['ALL',])
            print n, i,'{:.2f}s'.format(time()-start)
            
        except Exception as e:
            print e
            
        
        #collection['picture_name']=i
        #collection['api_result']=response
        try:
            with open('result.csv', 'a') as fh:
                one={'picture_name':i, 'api_result':response}
                fh.write(json.dumps(one))
                fh.write('\n')
        except Exception as e:
            print e
            
        try:
            coll.insert_one(one)
            start=time()
        except Exception as e:
            print e
            
    print 'done'
    #return collection
    
    
if __name__=='__main__':
    path=raw_input('path of folder that contains pictures: ')
    
    face2folder2mango(path)
