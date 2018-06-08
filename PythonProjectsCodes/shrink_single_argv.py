# -*- coding:utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

#This program is written with the sole aim of study of coding,
#I will take NO responsibilities of any kind of the results of improper using.


import os

from time import time
from PIL import Image






Format = ['bmp', 'gif', 'jpg', 'png', 'jpeg']

rate=50


# make small thumbnail images of downloaded HD pics for index viewing

def process(file):

    file=path+'/'+file
    extension = os.path.splitext(file)[1].lower()[1:]

    if extension in Format:
        if extension !='jpg':
            try:
                img=Image.open(file)
                img =  img.convert('RGB')

                if file[-4:]=='jpeg':
                    img.save(file[:-4]+'jpg')
                    os.remove(file)
                else:
                    img.save(file[:-4]+'.jpg')
                    os.remove(file)     

                
            except:
                print '?',

def shrink(file):

    file=path+'/'+file


    try:
        img=Image.open(file)            
        size=os.path.getsize(file)/1000
    except Exception as e:
        print e

        
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
        elif size>60:
            rate=90                 
        else:
            rate=100

        
        img.thumbnail((img.size[0]*rate/100, img.size[1]*rate/100))

        img.save(file)


    
        print '%',

        # print 'cannot do the processing, wtf'
        # pass

    except Exception as e:
        print e

    



if __name__ == '__main__':
    path = sys.argv[1]

    d = os.listdir(path)
    e = [i for i in d if i.find('.')>0]
        
    for i in e:
        process(i)



    d = os.listdir(path)
    e = [i for i in d if i.find('.')>0]

    for i in e:
        shrink(i)



