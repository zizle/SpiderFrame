# _*_ coding:utf-8 _*_

from spiders.baidu import BaiduSpider
from spiders.douban import DoubanSpider

class BaiduPipeline(object):

    def process_item(self, item, spider):
        if isinstance(spider, BaiduSpider):
            print("百度爬虫的数据：", item)
        return item  # 最后必须返回item


class DoubanPipeline(object):

    def process_item(self, item, spider):
        if isinstance(spider, DoubanSpider):
            print('豆瓣爬虫的数据：', item)

        return item

