#! /usr/bin/python

import sys

def seq(gp=0, word="IN-PROGRESS"):
        from time import strftime, localtime
        
        with open('save_seq.seq','a+') as fl:
                data = fl.readlines()
                fl.seek(0)
                fl.truncate()
                
                if len(data)==0:
                    seq=1
                    tm = strftime("%Y-%m-%d %H:%M:%S", localtime())
                    strings = str(seq)+','+str(gp)+','+tm+','+word
                      
                    fl.write(strings)
                    fl.write('\n')
                    
                else:
                    seq = int(data[-1].split(',')[0])
                    seq+=1
                    
                    tm = strftime("%Y-%m-%d %H:%M:%S", localtime())
                    strings = str(seq)+','+str(gp)+','+tm+','+word
                    
                    fl.write(strings)
                    fl.write('\n')

        print (strings)
        return strings

if __name__=='__main__':
    passing = len(sys.argv)
    if passing==1:
        print 'you need to pass a group NO.'
	exit(0)
    if passing==2:
        groupNo=sys.argv[1]
        seq(groupNo)
	exit(0)
    if passing==3:
        groupNo, Stat = sys.argv[1], sys.argv[2]
        seq(groupNo, Stat)
	exit(0)
    else:
        print 'too many inputs'
	exit(0)

    
