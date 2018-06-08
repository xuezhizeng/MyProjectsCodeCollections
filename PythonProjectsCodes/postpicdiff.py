import scrapy
import urllib
import time



class postpicdiffSpider(scrapy.Spider):

    name = 'postpicdiff'
    allowed_domains = ['freelancer.com']
    
    
    csvPath = 'https://s3.amazonaws.com/shichaoji/diffpics.csv'
    
    
    start_urls=[]
    opener = urllib.URLopener()
    fh = opener.open(csvPath)
    for line in fh.readlines():
        start_urls.append(line.strip())
    
    print name, len(start_urls)
    
    def parse(self, response):
        dic={}
        
        dic['postlink'] = response.url
        
        dstime=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        dic['scrape_time']=dstime
        
        n=0
        for i in response.css('div.c img ::attr(src)'):
            pic = i.extract().strip()
            if pic.startswith('http://img'):
                n+=1
                dic['image_'+str(n)] = i.extract().strip()
                
        #response.css('div c img ::attr(src)')
        
        yield dic