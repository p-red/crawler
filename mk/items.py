# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MkItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    type = scrapy.Field()  # 爬取该本书的类型
    course_Links = scrapy.Field()  # 爬取该书本的课程链接
    name = scrapy.Field()  # 爬取该书本的内容
    img = scrapy.Field()  # 爬取该书本的图片
    number = scrapy.Field()  # 爬取该书本的人数
    level = scrapy.Field()  # 爬取该书本的级别
    price = scrapy.Field()  # 价格
    discountedPrice = scrapy.Field()  # 优惠价
    content = scrapy.Field()  # 课程详情
    evaluationCont = scrapy.Field()  # 评价人以及评价内容
