#! /usr/bin/python

import sys
from shutil import copyfile

def seq(txt, word="IN-PROGRESS"):
    

        from time import strftime, localtime

        txt=str(txt)

        with open('save_seq.seq','a+') as fl:

                data = fl.readlines()

                fl.seek(0)

                fl.truncate()

                

                if len(data)==0:

                    seq=1

                    tm = strftime("%Y-%m-%d %H:%M:%S", localtime())

                    strings = str(seq)+','+tm+','+word

                      

                    fl.write(strings)

                    fl.write('\n')

                    

                else:

                    seq = int(data[-1].split(',')[0])

                    seq+=1

                    

                    tm = strftime("%Y-%m-%d %H:%M:%S", localtime())

                    strings = str(seq)+','+tm+','+word

                    

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

        seq("save_seq.seq")

        

    elif passing==2:

        txtfile=sys.argv[1]
        

        seq(txtfile)

    elif passing==3:

        txtfile, info = sys.argv[1], sys.argv[2]

        seq(txtfile, info)
        
        

    else:

        print 'too many inputs'

        exit(0)

