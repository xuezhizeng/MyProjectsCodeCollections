# -*- coding: utf-8 -*-
import scrapy
from research.items import DiaryItem
import urllib

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
selected_chuck=3
        
class Diary1Spider(scrapy.Spider):
    
    custom_settings = {
        'ITEM_PIPELINES': {
            'research.pipelines.Post2Database': 200
        }
    }        
    
    #csvPath = 'https://s3.amazonaws.com/shichaoji/diaryID.csv'
    
    cur=db.cursor()
    cur.execute('select ID from research.diarylink order by date asc')
    try:
        collections = list(map(lambda x: int(x[0]), cur.fetchall()))
    except:
        print 'fail database'
        exit(0)

    name = 'diary3'
    allowed_domains = ['www.soyoung.com']
    link = 'http://www.soyoung.com/dpg'
    start_urls=[]

    #opener = urllib.URLopener()
    #fh = opener.open(csvPath)
    
    for ID in collections:
        start_urls.append(link + str(ID))
        
    #start_urls=start_urls[1:]
    
    print len(start_urls)
    

    
    parts = list(chunks(start_urls, len(start_urls)/split_chuck+1))
    print len(parts)
    for part in parts: 
        print len(part)
    
    start_urls = parts[selected_chuck-1]
    print name
    print len(start_urls)
    
    
    #df = pd.read_csv(csvPath)
    #for l in df['group_id'].tolist():
        #start_urls.append(link+str(l))    
    

    print 'starting: ', len(start_urls), 'first: ', start_urls[0]

    def parse(self, response):
        
        if response.url == 'http://www.soyoung.com/dp':
            return
        
        basic={}


        basic['diary_link']= response.url
        basic['diary_name'] = response.css('div.diary-info > h2::text').extract()[0]

        user = response.css('div.diary-info > div.avatar-box > p > a')
        basic['user_name'] = user.css('::text').extract()[0].strip()
        basic['user_link'] = user.css('::attr(href)').extract()[0].strip()

        dinfo = response.css('div.diary-info > div.info-box > div.row')

        try:
            proj, dtime, hos, doc, prod, price, pre_img = dinfo
        except Exception as e:
            print 'X1',e

        try:
            basic['project_name'] = proj.css('div.value.tag::text').extract()[0].strip()
        except Exception as e:
            print 'pj',e        


        try:
            basic['diary_date'] = dtime.css('div.value.date::text').extract()[0].strip()
        except Exception as e:
            print 'pt',e        


        try:
            hx = hos.css('a::text').extract()
            hy = hos.css('a::attr(href)').extract()
            if len(hx)>0 and len(hy)>0:
                basic['hospital'] = hx[0].strip()
                basic['hospital_link'] = hy[0].strip()            
             
        except Exception as e:
            print 'hp',e       

        try:    
            dx = doc.css('a::text').extract()
            dy = doc.css('a::attr(href)').extract()

            if len(dx)>0 and len(dy)>0:
                basic['doctor_name'] = dx[0].strip()
                basic['doctor_link'] = dy[0].strip()
        except Exception as e:
            print 'dc',e     

        try:    
            basic['product_name'] = prod.css('a::text').extract()[0].strip()
            basic['product_link'] = prod.css('a::attr(href)').extract()[0].strip()
        except Exception as e:
            print 'pd',e   

        try:    
            basic['price'] = price.css('div.value.price::text').extract()[0].strip()
        except Exception as e:
            print 'pc',e       


        try:    
            m=0
            for img in pre_img.css('div.before-photos > a'):
                m+=1
                basic['pre_surg_pic'+str(m)] = img.css('::attr(href)').extract()[0].strip()    

        except Exception as e:
            print 'pi',e    




        for i in response.css('div.diary-list > ul > li.diary-item'):
            item=DiaryItem(basic)


            item['post_title'] = i.css('span.day::text').extract()[0]
            item['post_link'] = i.css('p.describe > a::attr(href)').extract()[0]
            item['post_text'] = i.css('p.describe > a::text').extract()[0]
            item['post_time']=i.css('div.date::text').extract()[0]

            n=0
            for p in i.css('ul.photo-list > li > a > img::attr(data-img)').extract():
                n+=1
                item['post_image'+str(n)] = p
            tp='photo-diary'

            vid = i.css('div.video-poster > a > img::attr(data-img)').extract()
            if len(vid)>0:
                tp='video-diary'
                item['video_image'] = vid[0]

            item['post_type'] = tp

            coll = i.css('div.other-box a::text').extract()
            
            item['views']= coll[0]
            item['comments']= coll[1]
            item['favor']= coll[2]

            yield item
            #lll.append(item)


