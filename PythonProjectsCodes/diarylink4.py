# -*- coding: utf-8 -*-

import scrapy
import json
diary = "http://y.soyoung.com/cp{}?action=calendarlist"

#mport urllib

import pymysql

db = pymysql.connect(host="research.cdzq2e5ydtpm.us-east-1.rds.amazonaws.com",    # your host, usually localhost
                     user="scrapy",         # your username
                     passwd="soyoung",  # your password
                     port=3306,
                     db="research",
                     charset='utf8')

def chunks(l, n):
    for i in xrange(0, len(l), n):
        yield l[i:i+n]
        

split_chuck=4
selected_chuck=4


def One(ID):
    
    try:
        link = diary.format(ID)
        r = requests.get(link, timeout=6)
        base = json.loads(r.text)
        lists = base['group_list']['list']
        
        df = pd.DataFrame(map(lambda p: flatten_dict(p, layers=3), lists))

        col = list(df.columns)
        col = [col.pop(col.index('group_id')), col.pop(col.index('uid')), col.pop(col.index('user_name')), col.pop(col.index('top.summary'))]+col
        df = df[col]
        df.pop('other.summary')
        df.pop('item')
        df.pop('tag_info')
        df['from_product']=ID
        df = df.set_index('from_product')
        df.to_excel(folder + str(ID)+'.xlsx', encoding='utf-8')
        print 'O',
        
    except Exception as e:
        print ID, e
        try:
            print r.status_code,
        except:
            return
        try:
            df.shape
        except:
            return
        

        if df.shape[0]==0:
            return
        if r.status_code==200:
            return
        else:
                One(ID)

def diary_main():
    global diary, folder
    
    try:
        sys.path.append(os.getcwd())
        from info import diary
        print 'imported data from info'
        sys.path.remove(os.getcwd())

    except:
        print 'lack of info.py'
        exit(0)    
    
    
    ct = ctime().split()
    folder= ct[2]+ct[1]+ct[-1]+'_diary/'
    try:
        os.mkdir(folder)
    except:
        print 'R' 
    
    
    
    
    content = pd.read_csv('./diary_products.csv', names=['product_id'])['product_id'].tolist()
    cpu = int(raw_input('(multi-processing) how many process to run ? '))

    have = list(map(lambda x: int(x.split('.')[0]) ,os.listdir(folder)))
    want = list(set(content)-set(have))
    
    print 'all product diary - already scraped'
    print len(content), len(have), len(want)
    
    
    
    start=time()

    pool = ThreadPool(cpu)
    
    results = pool.map(One, want)
    
    pool.close()
    pool.join()
    
    end = time()
    elapse = end - start 
    
    print 'used {:.2f} s, {:.2f} mins'.format(elapse, elapse/60)
    
    
    
    print 'start concating data'
    start2=time()
    
    files = os.listdir(folder)
    print len(files)
    

    tmp = []
    for i in files:
        try:
            tmp.append(pd.read_excel(folder+i))
        except:
            print i,
    print len(tmp)
    df = pd.concat(tmp)
    print df.shape    
    
    end2 = time()
    elapse2 = end2 - start2 
    print 'used {:.2f} s, {:.2f} mins'.format(elapse2, elapse2/60)
    
    print 'removing duplicates'
    
    col = list(df.columns)
    col = [col.pop(col.index('group_id')), col.pop(col.index('uid')), col.pop(col.index('user_name')), col.pop(col.index('top.summary'))]+col
    df = df[col]
    
    pics = ['avatar.u',
    'middle.img.u',
    'middle.img.u_n',
    'middle.img.u_z',
    'other.img.u',
    'top.color',
    'top.img.u',
    'top.img.u_z',
    'top.img.u_n',
    'top.record_post_img',]
    
    for p in pics:
        try:
            df.pop(p)
            print 'Pop',p
        except:
            print 'F',p
    df = df.reset_index(drop=True)
    df = df.loc[df['group_id'].drop_duplicates().index,:]
    print df.shape




    print 'saving to diary.xlsx'
    
    df.to_excel(strftime("%Y-%m-%d-%H-%M",localtime())+ ' diary.xlsx', encoding='utf-8', index=False)
    print 'done!', ctime()
    

class DiarylinkSpider(scrapy.Spider):
    
    name = 'diarylink4'
    allowed_domains = ['soyoung.com']

    cur=db.cursor()
    cur.execute('select ID from research.product order by date asc')
    collections = list(map(lambda x: int(x[0]), cur.fetchall()))
    
    
    
    custom_settings = {
        'ITEM_PIPELINES': {
            'research.pipelines.DuplicatesDiary': 200
        }
    }
    
    #csvPath = 'https://s3.amazonaws.com/shichaoji/fullPid.csv'
    
    
    start_urls=[]
    #opener = urllib.URLopener()
    #fh = opener.open(csvPath)
    
    for ID in collections:
        start_urls.append(diary.format(str(ID)))
        
    #start_urls=start_urls[1:]    

    parts = list(chunks(start_urls, len(start_urls)/split_chuck+1))
    print len(parts)
    for part in parts: 
        print len(part)    
        
    start_urls = parts[selected_chuck-1]
    
    print name, len(start_urls)
    
    
    
    def parse(self, response):
        unitext = response.body_as_unicode()
        base = json.loads(unitext)
        lists = base['group_list']['list']
        
        if len(lists):
            for i in lists:
                yield i
