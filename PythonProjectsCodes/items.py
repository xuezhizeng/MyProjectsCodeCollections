# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DiaryItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    
    diary_link=scrapy.Field()    
    user_name=scrapy.Field()
    user_link=scrapy.Field()
    
    diary_name=scrapy.Field()
    diary_date=scrapy.Field()
    project_name=scrapy.Field()
    
    hospital=scrapy.Field()
    hospital_link=scrapy.Field()
    
    doctor_name=scrapy.Field()
    doctor_link=scrapy.Field()
    
    product_name=scrapy.Field()
    product_link=scrapy.Field()
    
    price=scrapy.Field()
    
    pre_surg_pic1=scrapy.Field()
    pre_surg_pic2=scrapy.Field()
    pre_surg_pic3=scrapy.Field()
    
    post_title=scrapy.Field()
    post_link=scrapy.Field()
    post_text=scrapy.Field()
    post_image1=scrapy.Field()
    post_image2=scrapy.Field()
    post_image3=scrapy.Field()
    post_image4=scrapy.Field()
    post_image5=scrapy.Field()
    post_image6=scrapy.Field()
    post_image7=scrapy.Field()
    post_image8=scrapy.Field()
    post_image9=scrapy.Field()
    
    post_type=scrapy.Field()
    video_image=scrapy.Field()
    
    posts_time=scrapy.Field()
    views=scrapy.Field()
    comments=scrapy.Field()
    favor=scrapy.Field()
    
    
