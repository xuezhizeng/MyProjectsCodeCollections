#! /usr/bin/python

import sys
from shutil import copyfile

def seq(gp, txt, word="IN-PROGRESS"):
    

        from time import strftime, localtime

        txt=str(txt)

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
        try:
            copyfile('./save_seq.seq', './'+txt)
        except:
            pass
        print (strings)

        return strings

if __name__=='__main__':

    passing = len(sys.argv)

    if passing==1:

        seq(0, "save_seq.seq")

        

    elif passing==2:

        groupNo=sys.argv[1]
        txtfile="save_seq.seq"

        seq(groupNo, txtfile)

    elif passing==3:

        groupNo, txtfile = sys.argv[1], sys.argv[2]

        seq(groupNo, txtfile)
        

    elif passing==4:

        groupNo, txtfile, Stat = sys.argv[1], sys.argv[2], sys.argv[3]

        seq(groupNo, txtfile, Stat)

        

    else:

        print 'too many inputs'

        exit(0)

