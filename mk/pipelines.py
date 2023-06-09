# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import scrapy
from scrapy.pipelines.images import ImagesPipeline
import json

class MkPipeline(object):
    """将爬取的信息保存为Json格式"""

    def __init__(self):
        self.f = open('mk.txt', 'w')

    def process_item(self, item, spider):
        # 默认传过来的item是json格式
        import json
        # 读取item中的数据， 并转成json格式;
        line = json.dumps(dict(item), ensure_ascii=False, indent=4)
        self.f.write(line + '\n')
        # 一定要加， 返回给调度器；
        return item

    def open_spider(self, spider):
        """开启爬虫时执行的函数"""
        pass

    def close_spider(self, spider):
        """当爬虫全部爬取结束的时候执行的函数"""
        self.f.close()


class CsvPipeline(object):
    # 保存为csv数据格式
    def __init__(self):
        self.f = open('mk.csv', 'w')

    def process_item(self, item, spider):
        # 默认传过来的item为json数据
        item = dict(item)
        self.f.write("{0}:{1}:{2}:{3}:{4}:{5}:{6}:{7}:{8}:{9}\n".format(item['name'],
                                                                        item['img'],
                                                                        item['course_Links'],
                                                                        item['type'],
                                                                        item['level'],
                                                                        item['number'],
                                                                        item['content'],
                                                                        item['price'],
                                                                        item['discountedPrice'],
                                                                        item['evaluationCont'],
                                                                        ))
        return item

    def open_spider(self, spider):
        """开启爬虫时执行的函数"""
        pass

    def close_spider(self, spider):
        """当爬虫全部爬取结束的时候执行的函数"""
        self.f.close()


class MysqlPipeline(object):
    """
    将爬取的信息保存到数据库中

    """

    def __init__(self):
        super(MysqlPipeline, self).__init__()
        self.conn = pymysql.connect(
            host='localhost',
            user='root',
            password='root',
            db='mk',
            charset='utf8',
        )

        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        # xxxx:xxxxx:xxxx
        # item时一个对象,
        item = dict(item)
        info = (item['name'],
                item['img'],
                item['course_Links'],
                item['type'],
                item['level'],
                item['number'],
                item['content'],
                item['price'],
                item['discountedPrice'],
                json.dumps(item['evaluationCont']))

        insert_sqli = "insert into mkInformationS values('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'); " % (info)
        # open('mooc.log', 'w').write(insert_sqli)
        # # 用来检测代码是否达到指定位置， 并用来调试并解析页面信息;
        self.cursor.execute(insert_sqli)
        self.conn.commit()
        return item

    def open_spider(self, spider):
        """开启爬虫时执行的函数"""
        create_sqli = "create table if not exists  moocinfo (title varchar(50), url varchar(200), image_url varchar(" \
                      "200), introduction varchar(500), student int) "
        self.cursor.execute(create_sqli)

    def close_spider(self, spider):
        """当爬虫全部爬取结束的时候执行的函数"""
        self.cursor.close()
        self.conn.close()


class ImagePipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        # 返回一个request请求， 包含图片的url地址
        yield scrapy.Request(item['img'])

    # 当下载请求完成后执行的函数/方法
    def item_completed(self, results, item, info):

        # open('mooc.log', 'w').write(results)
        #  获取下载的地址
        image_path = [x['path'] for ok, x in results if ok]
        if not image_path:
            raise Exception("不包含图片")
        else:
            return item
