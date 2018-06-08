# coding=utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf8')

from subprocess import call

from flask import Flask, render_template, request
import os

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
    return render_template('index.html', **locals())


# good image
def isImageFormat(link):
    link=link.lower()
    if (link.find('.jpg') > -1 or link.find('.png') > -1 or link.find('.gif') > -1 or link.find('.jpeg') > -1 or link.find('.bmp') > -1):
        return True
    return False


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    ip=request.remote_addr
    global flag
    if request.method == 'POST':
	
        file = request.files['file']
	test = file.filename
	print test
	if not isImageFormat(test):
		print 'bad'	
		return 'no pics!'

	saving=custDIR.replace('land/','pics')
	chop=custDIR.replace('land/','chop')
	print custDIR, saving, chop
	try:
	    print ip
	    os.mkdir(custDIR.replace('land/',''))
	    os.mkdir(saving)
	    os.mkdir(custDIR)
	    os.mkdir(chop)
	except Exception as e:
	    print e
	    print ip,'exists'

	 
	
        print file.filename
        print str(file.filename)
        print 
        upload_path = '{}/{}'.format(saving, file.filename.lower().__str__())
        file.save(upload_path)
	
	sav=upload_path.replace('soyoung/','')
	print sav
	land = sav.split('uploads/')[0]+'uploads/'+str(ip)+'/land'
	print land
	call(["docker","exec","openface","python","/home/face/facial_landmarks2.py",\
"--shape-predictor","/home/face/shape_predictor_68_face_landmarks.dat","--image",\
sav,"--output",land])
	print 'done landmark'
	call(["docker","exec","openface","python","/root/openface/util/align-dlib.py",\
sav.split('pics')[0]+'pics',"align","outerEyesAndNose",land.replace('land','chop'),"--size","256"])
	print 'done chop'
	
	flag=False
        return 'ok'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=80)
