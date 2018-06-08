# -*- coding: utf-8 -*-
import scrapy
from research.items import DiaryItem

        
class PodcastlinkSpider(scrapy.Spider):
    
    
    name = 'podcastlink'
    allowed_domains = ['www.soyoung.com']
    link = 'http://www.soyoung.com/live/room?zhibo_id='
    start_urls=[]

    
    for ID in range(1,10001):
        start_urls.append(link + str(ID))
        
    
    print len(start_urls)
    
    

    print 'starting: ', len(start_urls), 'first: ', start_urls[0]

    def parse(self, response):
        
        dic={}
        
        try:
            video = response.css('video ::attr(src)').extract()
            if video:
                video_url = video[-1]
                podcastID=int(response.url.split('zhibo_id=')[-1])
                print 'O',len(video),podcastID, video_url
                
                
                dic['podcastID']=podcastID
                dic['video_url']=video_url 
                dic['podcast_link']=response.url
                
                if video_url[-4:]=='.mp4':
                    dic['valid']=True
                elif video_url[-4:]=='.flv':
                    dic['X_video']=True
                else:
                    dic['Null_video']=True
            
                    
            else:
                print 'ERROR podcast not exist'
                return
                
        except Exception as e:
            print 'eRROR'
            return
            

        
        yield dic
        



