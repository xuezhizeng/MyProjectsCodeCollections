# -*- coding: utf-8 -*-

import scrapy
import json
from time import ctime

#mport urllib

pod = "http://www.soyoung.com/live/list?page={}&limit=10&is_json=1"

pre = "http://www.soyoung.com/live/room?zhibo_id="


class PodcastSpider(scrapy.Spider):
    
    name = 'podcast'
    allowed_domains = ['soyoung.com']


    
    start_urls=[pod.format(1)]

    print name, start_urls[0]
    
    
    
    def parse(self, response):
        unitext = response.body_as_unicode()
        base = json.loads(unitext)
        flag = int(base['has_more'])
        url = response.url
        
        page = int(url.split('page=')[-1].split('&limit')[0])
        
        try:
            lists = base['list']
        except:
            print url,'has 0 podcast' 
            return        
        
        tm=ctime()
        
        if len(lists):
            for i in lists:
                i['monitor_time']=tm
                i['page']=page
                i['podcast_link']=pre+i['zhibo_id']
                yield i
                
        if flag and page<200:
            yield scrapy.Request(url = pod.format(page+1), callback = self.parse)
                
                
