#! /home/shj16110/anaconda2/envs/3.6.1/bin/python

import sys
print (sys.version)

from time import time, ctime
import natsort
import os
import subprocess

path = '/home/shj16110/notebook/DeepGenderPred/AllText/'
p0 = '/home/shj16110/notebook/DeepGenderPred/'

print (p0)

want = os.listdir(path)
want = natsort.natsorted(want)
print(len(want), want[0], want[-1])

def run(tart_point, batch):
    n=start_point

    for i in want[start_point: start_point+batch]:
        n+=1
        start=time()
        print (n)
        print (i)
        stat0 = str(n)+': '+i+': '+ctime()
        command = ["/home/shj16110/anaconda2/envs/3.6.1/bin/python", p0+"Tensorflow/rude-carnie/guess.py", "--class_type", "gender","--model_type", "inception", "--model_dir", p0+"Tensorflow/21936", "--filename", path+i, "--target", p0+"predict/predict_"+str(n)+".csv"]
        print (command)
        
        subprocess.call(command)
        stat = 'used {:.2f} s, {:.2f} m, {:.2f} h'.format(time()-start, (time()-start)/60.0,(time()-start)/3600.0)+' : '+ctime()
        stat2 = '{:.2f} sceond per pic'.format((time()-start)/(300))
        print (stat)
        print (stat2)
        with open('log.txt','a+') as fl:
                fl.write(stat0+'\n')
                fl.write(stat+'\n')
                fl.write(stat2+'\n\n')
if __name__=="__main__":
	start_point=int(sys.argv[1])
	batch=int(sys.argv[2])
	print(want[start_point: start_point+1])
	run(start_point, batch)
