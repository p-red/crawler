# -*- coding: utf-8 -*-
import time

import scrapy
from pydispatch import dispatcher
from scrapy import signals
from scrapy.http import HtmlResponse
from selenium import webdriver

from ..items import MkItem


class MkhSpider(scrapy.Spider):
    name = 'mkh'
    # allowed_domains = ['coding.imooc.com/']
    start_urls = ['https://coding.imooc.com/']

    # 初始化selenium
    def __init__(self, *args, **kwargs):
        option = webdriver.ChromeOptions()  # 实例化一个浏览器对象
        option.binary_location = r'D:\Google\Chrome\Application\chrome.exe'
        option.add_argument('--headless')  # 添加参数，option可以是headless，--headless，-headless
        self.driver = webdriver.Chrome(options=option)  # 创建一个无头浏览器
        # self.driver = webdriver.Chrome()  # 创建一个无头浏览器
        time.sleep(3)
        super(MkhSpider, self).__init__(*args, **kwargs)
        dispatcher.connect(self.close_driver, signals.spider_closed)

    def parse(self, response: HtmlResponse):
        # 实例化对象
        courseDetails = response.xpath('//ul[@class="course-list clearfix"]/li/a')
        for courseDetail in courseDetails:
            mk = MkItem()
            course_Links = courseDetail.xpath('./@href').extract_first()
            mk['name'] = courseDetail.xpath('./p[1]/text()').extract_first()
            img = courseDetail.xpath('./div/@style').extract()
            src_c = 'https://coding.imooc.com' + course_Links
            for a in img:
                src = 'http:' + a[22:-1]
            number_of_levels = courseDetail.xpath('./p[2]/span/text()').extract_first()
            price = courseDetail.xpath('./p[3]/span[1]/text()').extract_first().strip()
            price_1 = courseDetail.xpath(
                './p[@class="two clearfix"]/span[@class="price l red bold"]/text()').extract_first().strip()
            discountedPrice = courseDetail.xpath(
                './p[3]/span[@class="origin-price l delete-line"]/text()').extract_first()
            if price:
                price = price
            elif price_1:
                price = price_1
            mk['img'] = src
            mk['course_Links'] = src_c
            mk['number'] = number_of_levels.split("·")[1].strip().split("人")[0]
            mk['level'] = number_of_levels.split("·")[0].strip()
            mk['type'] = courseDetail.xpath(
                '//ul[@class="course-list clearfix"]/li/@data-typestr').extract_first()
            mk['price'] = price
            mk['discountedPrice'] = discountedPrice
            # print(src_c, name, src, number_of_levels, price)
            # yield mk
            yield scrapy.Request(url=src_c, callback=self.parse_detail, meta={'data': mk})
        # 爬取新网站
        url = response.xpath('.//a[contains(text(), "下一页")]/@href')[0].extract()
        last_page = response.xpath('.//a[contains(text(), "下一页")]/@class').extract()
        # print(last_page)
        last_page = self.getvalue(last_page)
        if last_page != 'disabled_page':
            # 构建新的url
            page = "https://coding.imooc.com" + url
            yield scrapy.Request(page, callback=self.parse, dont_filter=True)

    def parse_detail(self, response):
        mk = response.meta['data']
        content = response.xpath('//*[@id="classDesc"]/div/div[@class="desc-box"]/text()').extract()
        content_1 = response.xpath('/html/body/div[5]/div[4]/div[4]/p/text()').extract()
        if self.getvalue(content):
            content = content
        elif self.getvalue(content_1):
            content = content_1
        evaluationContS = response.xpath('//*[@id="evaluation"]/div')
        evaluationContDic = {}
        for evaluationCont in evaluationContS:
            user = evaluationCont.xpath('./div[@class="right-box"]/span[@class="nicname"]/text()').extract_first()
            contents = evaluationCont.xpath('./div[@class="right-box"]/div[@class="content"]/text()').extract_first()
            evaluationContDic[user] = contents
        mk['content'] = content[0]
        mk['evaluationCont'] = evaluationContDic
        user_Comments = response.xpath('.//a[contains(text(), "用户评价")]/@href').extract_first()
        if user_Comments is None:
            yield mk
        else:
            user_Comments_url = 'https://coding.imooc.com' + user_Comments
            yield scrapy.Request(url=user_Comments_url, callback=self.parse_last, meta={'data': mk})

    def parse_last(self, response):
        mk = response.meta['data']
        evaluationContDic = {}
        evaluationContS = response.xpath('//ul[@class="cmt-list"]/li')
        for evaluationCont in evaluationContS:
            user = evaluationCont.xpath('.//a[@class="name"]/text()').extract_first()
            contents = evaluationCont.xpath('.//p[@class="cmt-txt"]/text()').extract_first()
            evaluationContDic.setdefault(user, contents)
            # evaluationContDic[user] = contents
        mk['evaluationCont'] = evaluationContDic
        yield mk

    # 关闭selenium
    def close_driver(self):
        print("爬虫正在退出，执行关闭浏览器哦")
        time.sleep(2)
        self.driver.quit()

    def getvalue(self, value):
        # return value[0] if value else ''
        if value == []:
            return ''
        else:
            return value[0]
