import boto3
import os
from time import time
import json

from pymongo import MongoClient
mango = MongoClient(host='dsnotebook.bid', port=27017, username='face', password='rekognition')

db=mango['explore']
coll=db['compare']

client = boto3.client(
    'rekognition',
    aws_access_key_id = '',
    aws_secret_access_key=''
)



def face2compare(path):
    #collection={}
    if path[-1]!='/':
        path+='/'
    dr=os.listdir(path)
    
    print len(dr), 'files in the folder'
    
    pairs = [(i.split('_cpr.jpg')[0]+'.jpg',i) for i in dr if i.endswith('_cpr.jpg')]
    print 'should be',len(pairs), 'paris'
    flag = raw_input('proceed? y/n ')
    if flag!='y':exit(0)
    print 'pushing...', len(dr)
    
    n=0
    start=time()
    
    for i,j in pairs:
        n+=1
        
        try:

            with open(path+i, 'rb') as image1:
                b1 = image1.read()

            with open(path+j, 'rb') as image2:
                b2 = image2.read()
                
                response = client.compare_faces(SourceImage={'Bytes': b1}, TargetImage={'Bytes': b2}, SimilarityThreshold=0)
                
            print n, i,j,'{:.2f}s'.format(time()-start)
            
        except Exception as e:
            print e
            
        
        #collection['picture_name']=i
        #collection['api_result']=response
        try:
            with open('compare.csv', 'a') as fh:
                one={'pair_root_name':i, 'api_result':response}
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
    path=raw_input('path of folder that contains pictures (name.jpg, name_cpr.jpg collections) to compare: ')
    
    face2compare(path)
