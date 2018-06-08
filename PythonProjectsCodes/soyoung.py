# -*- coding: utf-8 -*-
import scrapy
from test.items import TestItem

class SoyoungSpider(scrapy.Spider):
    name = 'soyoung'
    allowed_domains = ['y.soyoung.com']
    start_urls = ['http://y.soyoung.com/']

    def parse(self, response):
        pass
