# -*- coding:utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

#This program is written with the sole aim of study of coding,
#I will take NO responsibilities of any kind of the results of improper using.


import os

from time import time
from PIL import Image

from multiprocessing.dummy import Pool as ThreadPool




Format = ['bmp', 'gif', 'jpg', 'png', 'jpeg']

rate=50


# make small thumbnail images of downloaded HD pics for index viewing

def process(file):

    file=path+'/'+file
    extension = os.path.splitext(file)[1]

    if extension=='.JPG':
        try:
            os.rename(file, file[:-3]+'jpg')
        except:
            print 'X',
    extension = extension.lower()[1:]
    

    if extension in Format:
        if extension !='jpg':
            try:
                img=Image.open(file)
                img =  img.convert('RGB')
                print '!',

                if extension=='jpeg':
                    img.save(file[:-4]+'jpg')
                    os.remove(file)
                else:
                    img.save(file[:-3]+'jpg')
                    os.remove(file)     

                
            except:
                print '?',

def shrink(file):

    file=path+'/'+file


    try:
        img=Image.open(file)            
        size=os.path.getsize(file)/1000
    except Exception as e:
        print '?',
##        print e

        
    try:
        
        if size>2500:
            rate=25            
        elif size>2000:
            rate=30
        elif size>1500:
            rate=40
        elif size>1000:
            rate=50
        elif size>500:
            rate=60
        elif size>400:
            rate=65
        elif size>300:
            rate=75
        elif size>200:
            rate=80
        elif size>100:
            rate=85
##        elif size>60:
##            rate=90                 
        else:
            rate=100

        
        img.thumbnail((img.size[0]*rate/100, img.size[1]*rate/100))

        img.save(file[:-3]+'jpg')


    
        print '%',

        # print 'cannot do the processing, wtf'
        # pass

    except Exception as e:
        print '?'
##        print e

def multiimage(lis):
    print 'processing pics......'
    
    start=time()

##    lis=os.listdir(id)
##
##    lis=map(lambda x:str(id)+'/'+x,lis)

    # print lis
    
    pool = ThreadPool(8)

    results = pool.map(shrink, lis)

    pool.close()
    pool.join()

    end = time()


    elapse = end - start    



if __name__ == '__main__':
    path = sys.argv[1]

    try:
        fg = sys.argv[2]
    except:
        fg=0

    print fg
    
    if fg==0:
        print 'convert to jpg'
        d = os.listdir(path)
        e = [i for i in d if i.find('.')>0]
            
        for i in e:
            process(i)

    

    d = os.listdir(path)
    e = [i for i in d if i.find('.')>0]

    multiimage(e)

 



