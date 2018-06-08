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

def one(x,y):
    result=[]
    for i in range(len(y)):
        result.append(cosine_similarity(x.values.reshape(1,-1), y.iloc[i].values.reshape(1,-1))[0][0])
        sorting = pd.Series(result).sort_values(ascending=False)
    return sorting

df = pd.read_csv('reps.csv', header=None)
label = pd.read_csv('labels.csv', names=['label','name'])
name = label['name'].apply(lambda x: x[9:][:-3]+'jpg')
del label


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
    time_sorted_list = sorted(full_list, key=os.path.getmtime)
    sorted_filename_list = [ os.path.basename(i) for i in time_sorted_list]

    print sorted_filename_list
    all_image_files = []
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
        beginning = precious[:10]
        ending = precious[-5:]          
        print beginning                 
        print ending   
        
        good=[]
        bad=[]
        for i,j in zip(beginning.index, beginning):
            good.append([round(j,3)*100, name[i]])

        for i,j in zip(ending.index, ending):
            bad.append([round(j,3)*100, name[i]])
        print good, bad
    except:
        print 'first time yet'
        good = [[81.2, 'euroG2/(844).jpg'], [79.9, 'euroG2/(1244).jpg'], [77.60000000000001, 'euroG2/(964).jpg'], [77.5, 'euroG2/(1488).jpg'], [73.5, 'euroG2/(1324).jpg'], [72.1, 'euroG2/(1117).jpg'], [70.3, 'euroG1/(399).jpg'], [69.89999999999999, 'euroG2/(777).jpg'], [69.89999999999999, 'euroG2/(1411).jpg'], [68.8, 'euroG1/(250).jpg']]
        bad=[[-44.7, 'euroB2/(975).jpg'], [-45.2, 'euroB2/(801).jpg'], [-46.0, 'euroB1/(181).jpg'], [-46.9, 'euroB2/(1396).jpg'], [-47.699999999999996, 'euroB2/(1497).jpg']]
                      
                      
                      
                      
                
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
	    os.mkdir(saving)
	    os.mkdir(new)
	    os.mkdir(custDIR)
	    os.mkdir(chop)
	except Exception as e:
	    print e
	    print ip,'exists'

	 
	
        print file.filename
        print str(file.filename)
        print 
        upload_path = '{}/{}'.format(new, file.filename.lower().__str__())
        file.save(upload_path)
	
	sav=upload_path.replace('soyoung/','')
	print sav
	land = sav.split('uploads/')[0]+'uploads/'+str(ip)+'/land'
	print land

	print sav
	print os.getcwd()
	print new
	call(["python","shrink_single_argv.py",new])
	call(["docker","exec","openface","python","/home/face/facial_landmarks2.py",\
"--shape-predictor","/home/face/shape_predictor_68_face_landmarks.dat","--image",\
sav,"--output",land])
	print 'done landmark'
	print sav.split('pics/new')[0]+'pics/new'
	call(["docker","exec","openface","python","/root/openface/util/align-dlib.py",\
sav.split('pics/new')[0]+'pics/new',"align","outerEyesAndNose",land.replace('land','chop'),"--size","256"])
	print 'done chop'

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
	
	pre = source[:-1]+'pre'
	call("mkdir "+pre, shell=True)
	call("mv "+source+" "+pre+"/", shell=True)
	call(["docker","exec","openface","/root/openface/batch-represent/main.lua", \
	"-outDir", data.replace('soyoung/',''),"-data", source[:-1].replace('soyoung/','')])

	call("mkdir "+target, shell=True)
	call("mv "+pre+'/*'+" "+target, shell=True)
		
	flag=False
        return 'ok'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=80)
