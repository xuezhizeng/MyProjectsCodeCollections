# coding=utf-8

import pandas as pd
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from subprocess import call
from sklearn.metrics.pairwise import cosine_similarity

from flask import Flask, render_template, request
import os
from time import time



df = pd.read_csv('parameter/27_Oct_31W.csv')
name = df.pop('name').to_frame()


app = Flask(__name__)
UPLOAD_PATH = 'static/uploads'
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, UPLOAD_PATH)

app.config['MAX_CONTENT_LENGTH'] = 6 * 1024 * 1024

custDIR=''
flag=True
@app.route('/')
def index():
    global ip, custDIR, flag
    ip = request.remote_addr
    print 'ip:',ip

    custDIR=UPLOAD_FOLDER+"/"+str(ip)+"/land/"
    print custDIR
    try:
        landmarks=os.listdir(custDIR)
        flag=False
    except:
        landmarks=[]
        print 'not yet uploadad any image'
    name_list = landmarks
    full_list = [os.path.join(custDIR,i) for i in name_list]
    
    print full_list
    
    time_sorted_list = sorted(full_list, key=os.path.getmtime)
    #time_sorted_list = full_list
    
    sorted_filename_list = [ os.path.basename(i) for i in time_sorted_list]

    print sorted_filename_list
    all_image_files = ["static/uploads/initial/land/anne-hathaway.jpg"]
    # all_mp3_files = []
    for filename in sorted_filename_list:
        # image
        if (isImageFormat(filename)):
            # all_image_files.append(custDIR.split('/newFlask/')[-1]+filename)
            all_image_files.insert(0,custDIR.split('/newFlask/')[-1]+filename)
    print flag    
    try:
        df0 = pd.read_csv(custDIR.replace('land','chop/data/reps.csv')[:-1],header=None)
        
        print df0.shape
        dating = df0.tail(1)
        
        dating1=dating.as_matrix().reshape(1,-1)
        start=time()
        df1=df.as_matrix()
        #precious = one(dating, df)
        precious=cosine_similarity(dating1, df1)
        precious=pd.Series(precious[0])
        precious=precious.sort_values(ascending=False)
        
        print 'used {:.2f} s'.format(time()-start)  
        print precious.shape
        
        # choose how many pics to pick up 
        beginning0 = precious[:100]
        bat = beginning0.shape[0]
        
        #''' try showing pics with less duplicates
        
        # drop similar precision with 0.001%
        beginning0 = beginning0.apply(lambda x: round(x,5)).drop_duplicates()
        
        # only save the top 2 of 99% or more
        # nine = beginning0[beginning0>=.99]
        # beginning0 = nine.head(1).append(nine.tail(1)).append(beginning0[beginning0<.99])    
        beginning0 = beginning0[beginning0>=.99].head(2).append(beginning0[beginning0<.99])   
        #'''
        
        try:
            beginning = beginning0[:20]
        except:
            beginning = beginning0
        
        ending = precious[-4:]    
        
        leave=beginning0.shape[0]
        
        print beginning                 
        print ending   
        
        print type(beginning), type(ending)
        good=[]
        bad=[]
        for i,j in zip(beginning.index, beginning):
            good.append([round(j,3)*100, name.iloc[i][0]])

        for i,j in zip(ending.index, ending):
            bad.append([round(j,3)*100, name.iloc[i][0]])
        print good, bad
        
        good_len, bad_len = len(good), len(bad)
    except Exception as e:
        print 
        print e
        print 
        print 'first time yet'
        good = [[94.5, 'sub_49/23F90EBEFEDA14D9658C42F7472B811B.jpg'], [91.0, 'sub_97/Img332962459.jpg'], [90.7, 'sub_107/U8828P1195DT20130729220620.jpg'], [90.5, 'sub_32/20120504125357066250.jpg'], [90.0, 'sub_55/349643882438516219.jpg'], [89.0, 'sub_106/U2190P28T3D2335077F326DT20090109145134.jpg'], [88.7, 'euroG2/(972).jpg'], [87.8, 'sub_98/Img333360801.jpg'], [87.7, 'sub_6/06-075930_190.jpg'], [86.6, 'sub_32/20111219185202.jpg']]
        bad=[[-59.3, 'sub_97/i0189143u7z_ori_3.jpg'], [-59.599999999999994, 'sub_44/20160817083246710.jpg'], [-59.9, 'sub_26/17-101222131633.jpg'], [-60.6, 'sub_39/20150703034613184.jpg'], [-65.5, 'sub_32/20120315210138_XNfCY.jpg']]
                      
                      
    if all_image_files[0][-4:].lower()=='jpeg':
        all_image_files[0]=all_image_files[0][:-4]+'jpg'

                      
                
    return render_template('index.html', **locals())


# good image
def isImageFormat(link):
    link=link.lower()
    if (link.find('.jpg') > -1 or link.find('.png') > -1 or link.find('.gif') > -1 or link.find('.jpeg') > -1 or link.find('.bmp') > -1):
        return True
    return False


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    ip = request.remote_addr
    
    global flag
    if request.method == 'POST':
	
        file = request.files['file']
	test = file.filename
	print test
	if not isImageFormat(test):
		print 'bad'	
		return 'no pics!'

	saving=custDIR.replace('land/','pics')
	new=custDIR.replace('land/','pics/new')
	chop=custDIR.replace('land/','chop')
	print custDIR, saving, chop, new
	try:
	    print ip
	    os.mkdir(custDIR.replace('land/',''))
	except Exception as e:
	    print e
	    print ip,'exists1'
	try:
	    print ip
	    os.mkdir(saving)
	except Exception as e:
	    print e
	    print ip,'exists2'
	try:
	    print ip
	    os.mkdir(new)
	except Exception as e:
	    print e
	    print ip,'exists3'
	try:
	    print ip
	    os.mkdir(custDIR)
	except Exception as e:
	    print e
	    print ip,'exists4'
	try:
	    print ip
	    os.mkdir(chop)
	except Exception as e:
	    print e
	    print ip,'exists5'         
	 
	
        print file.filename
        print str(file.filename)
        print 
        upload_path = '{}/{}'.format(new, file.filename.lower().__str__())
        file.save(upload_path)
        
        file.save(upload_path.replace('pics/new','land/'))
                  
	
	sav=upload_path.replace('soyoung/','')
	print sav
	land = sav.split('uploads/')[0]+'uploads/'+str(ip)+'/land'
	print land

	print sav
	print os.getcwd()
	print new
	call(["python","shrink_single_argv.py",new])
	print "WTF!!!"
	print custDIR
	print file.filename.find('jpeg')
	if file.filename.find('jpeg')>0:
		this=file.filename[:-4]+'jpg'
		print 1,this,       
	else:
		this=file.filename[:-3]+'jpg'
		print 2,this 
	print 'before copy'    
	#print sav
	print land+'/pics/new'
	print '------'
	print land
	print '------'
	print land.split('uploads')[-1]
	call(["cp", land.replace('/land','/pics/new/').replace('home/face','home/soyoung/face')+this, land.replace('home/face','home/soyoung/face')])
	print 'after copy'    
	start01=time()
	call(["docker","exec","openface","python","/home/face/facial_landmarks2.py",\
"--shape-predictor","/home/face/shape_predictor_68_face_landmarks.dat","--image",\
sav,"--output",land])
    
	print 'done landmark',  'used {:.2f} s'.format(time()-start01)
	print sav.split('pics/new')[0]+'pics/new'
    
	start02=time()
	call(["docker","exec","openface","python","/root/openface/util/align-dlib.py",\
sav.split('pics/new')[0]+'pics/new',"align","outerEyesAndNose",land.replace('land','chop'),"--size","96"])
	print 'done chop',  'used {:.2f} s'.format(time()-start02)

	call(['pwd'])	
	print new
	call(['ls',new])
	call("mv "+new+"/* "+new.split('pics/new')[0]+"pics/", shell=True)
	print new
	source = new.replace('pics/new','chop/new/*')
	target = new.replace('pics/new','chop/pics/')
	print source
	print target
	print "mv "+source+" "+target
	
	data = source.replace('new/*','data')
	start03=time()
	pre = source[:-1]+'pre'
	call("mkdir "+pre, shell=True)
	call("mv "+source+" "+pre+"/", shell=True)
	call(["docker","exec","openface","/root/openface/batch-represent/main.lua", \
	"-outDir", data.replace('soyoung/',''),"-data", source[:-1].replace('soyoung/','')])
	print 'done converting ',  'used {:.2f} s'.format(time()-start03)
    
	call("mkdir "+target, shell=True)
	call("mv "+pre+'/*'+" "+target, shell=True)
		
	flag=False
        return 'ok'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=80)
