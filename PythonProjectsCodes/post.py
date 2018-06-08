# -*- coding: utf-8 -*-

#import MySQLdb
import scrapy
import urllib
import re

postlink = 'http://www.soyoung.com/p{}'

import pymysql

db = pymysql.connect(host="research.cdzq2e5ydtpm.us-east-1.rds.amazonaws.com",    # your host, usually localhost
                     user="scrapy",         # your username
                     passwd="soyoung",  # your password
                     port=3306,
                     db="research",
                     charset='utf8')

cur=db.cursor()
cur.execute('select postID from research.post order by date asc')
try:
    collections = list(map(lambda x: int(x[0]), cur.fetchall()))
except:

    print 'fail database'
    exit(0)

        

class PostSpider(scrapy.Spider):
    name = 'Post'
    allowed_domains = ['soyoung.com']

#    custom_settings = {
#        'ITEM_PIPELINES': {
#            'research.pipelines.DuplicatesDiary': 200
#        }
#    }
    
    #csvPath = 'https://s3.amazonaws.com/shichaoji/postID.csv'
    
    
    start_urls=[]
    #opener = urllib.URLopener()
    #fh = opener.open(csvPath)
    for ID in collections:
        start_urls.append(postlink.format(ID))
    #start_urls=start_urls[1:]    
    
    print 'starting Posts'
    print name, len(start_urls)
    
    
    
    def parse(self, response):
        dic={}
        
        dic['postlink'] = response.url
        user = response.css('li.first_f div.head_pic')
        try:
            dic['userlink'] = user.css('a.name::attr(href)').extract()[0].strip()
            dic['username'] = user.css('a.name::text').extract()[0].strip()
            dic['day'] = int(response.css('div.date_box span.day::text').extract()[0])
        except Exception as e:
            #print e
            print 'error user info or day', response.url
        
        key=0
        for k in response.css('div.beauty_tool span a'): 
            key+=1
            dic['label_text_'+str(key)] = k.css('::text').extract()[0]
            dic['label_link_'+str(key)] = k.css('::attr(href)').extract()[0]
            
        
        rate = response.css('div.level_box ul.level_list')
        r = rate.css('span.level span')
        try:
            dic['rate_satisfy'], dic['rate_swell'], dic['rate_hurt'], dic['rate_scar'] = \
            [i.split('width:')[-1].replace(';','').strip() for i in r.css('::attr(style)').extract()]
        except:
            pass

        
        text = response.css('li.first_f div.content div.c ::text').extract()

        string=''
        for t in text:
            try:
                string = string +'\n' + t.strip()
            except Exception as e:
                print e
                pass
        string = re.sub(r'\n\n+', '\n', string.strip()).strip()
        if string:
            dic['text'] = string
            
        
        n=0
        for i in response.css('li.first_f div.content div.c img ::attr(src)'):
            pic = i.extract().strip()
            if pic.startswith('http://img2.soyoung.com'):
                n+=1
                dic['image_'+str(n)] = i.extract().strip()
            
        N=0
        for v in response.css('li.first_f div.content div.c video ::attr(src)'):
            N+=1
            dic['video_'+str(N)] = v.extract().strip()
        
        
        
        product= response.css('li.first_f div.con_t a.name')
        try:
            dic['product_name'] =  product.css('::text').extract()[0].strip()
            dic['product_link'] = product.css('::attr(href)').extract()[0].strip()    
        except:
            print 'no product', response.url
        
        yield dic