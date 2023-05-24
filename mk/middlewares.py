# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import time

from scrapy import signals
from scrapy.http import HtmlResponse


class ProxyMiddleware(object):

    def process_request(self, request, spider):
        # ip = random.choice(self.ip)

        request.meta['Proxy'] = "http://" + "58.246.58.150:9002"


class MkSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class MkDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    # 我自定义的解析cookie方法
    def get_cookie_dict(self):
        cookie_str = 'adspc20211111=1635754111870; march2022=1648377658000; ' \
                     'imooc_uuid=a6820717-d37c-4238-83bd-fd44814395e4; imooc_isnew=1; imooc_isnew_ct=1684767300; ' \
                     'IMCDNS=0; Hm_lvt_c1c5f01e0fc4d75fd5cbb16f2e713d56=1684767323; ' \
                     'sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22174758fa86fa2-0e13a0b04293ba-58321f4d' \
                     '-1327104-174758fa8701a9%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22' \
                     '%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22' \
                     '%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89' \
                     '%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_utm_source%22%3A%22szjineng1' \
                     '%22%2C%22%24latest_utm_campaign%22%3A%22SEM%22%2C%22%24latest_utm_term%22%3A%22MapReduce%22%2C' \
                     '%22%24latest_utm_medium%22%3A%2252%22%7D%2C%22%24device_id%22%3A%22174758fa86fa2-0e13a0b04293ba' \
                     '-58321f4d-1327104-174758fa8701a9%22%2C%22identities%22%3A' \
                     '%22eyIkaWRlbnRpdHlfYW5vbnltb3VzX2lkIjoiMTc0NzU4ZmE4NmZhMi0wZTEzYTBiMDQyOTNiYS01ODMyMWY0ZC0xMzI3MTA0LTE3NDc1OGZhODcwMWE5IiwiJGlkZW50aXR5X2Nvb2tpZV9pZCI6IjE4ODQzZjUwNDkzNS0wN2ViNGM3YmU0MzAwYS03YjUxNTQ3NC0xMzI3MTA0LTE4ODQzZjUwNDk0Yjc3In0%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%7D; Hm_lvt_f0cfcccd7b1393990c78efdeebff3968=1684772616; MEIQIA_TRACK_ID=2QAAi0kwsqtlQV87oWApQX2WuCB; MEIQIA_VISIT_ID=2QAAi0vOjVznV4Qge2urlrqN4tM; Hm_lpvt_f0cfcccd7b1393990c78efdeebff3968=1684814471; Hm_lpvt_c1c5f01e0fc4d75fd5cbb16f2e713d56=1684819007; cvde=646b82440bcf0-287 '
        cookie_dict = {}
        for item in cookie_str.split(';'):
            key, value = item.split('=', maxsplit=1)
            cookie_dict[key] = value
        return cookie_dict

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        request.cookies = self.get_cookie_dict()
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


# selenium
class SeleniumDownloaderMiddleware(object):
    def process_request(self, request, spider):
        if spider.name == 'mkh':
            spider.driver.get(request.url)
            time.sleep(2)
            print(f"当前访问{request.url}")
            spider.driver.refresh()
            time.sleep(3)
            return HtmlResponse(url=spider.driver.current_url, body=spider.driver.page_source, encoding='utf-8')
