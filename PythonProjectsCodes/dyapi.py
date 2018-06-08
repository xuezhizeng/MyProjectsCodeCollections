#! /home/shj16110/anaconda2/bin/python
import os
import sys
import shutil
from time import ctime
from subprocess import call

SS = "https://storage.scrapinghub.com/items/276632/";
key = "apikey=40ca9487a91348299af8280754d48cce"
cell = "format=csv&fields=post_ID,comments,favor,views&include_headers=1"

def api(ID, start, end):
    ID, start, end = int(ID), int(start), int(end)
    for i in range(start, end+1):
        string = SS+str(ID)+'/'+str(i)+'?'+key+'&'+cell
        print ID, i, ctime()
        name = 'diary_'+str(ID)+'_'+str(i)+'.csv'
        print string
        print name
        
        return string, name
        
def clean():        
    CSVs = [i for i in os.listdir('.') if i.endswith('csv')]
    for j in CSVs:
        st = os.stat(j)
        if st.st_size<1000:
            shutil.move(j, 'archive/'+j)
        else:
            shutil.move(j, 'data/'+j)
    
if __name__=='__main__':
    ID, start, end = sys.argv[1], sys.argv[2], sys.argv[3]
    api(ID, start, end)
    