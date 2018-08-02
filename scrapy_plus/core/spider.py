# _*_ coding:utf-8 _*_

from scrapy_plus.http.request import Request
from scrapy_plus.item import Item


class Spider(object):
    start_url = 'http://www.baidu.com'

    def start_requests(self):
        """构建初始请求对象"""
        return Request(self.start_url)

    def parse(self,response):
        """解析"""
        return Item(response.body)
