# _*_ coding:utf-8 _*_

from scrapy_plus.http.request import Request
from scrapy_plus.item import Item


class Spider(object):
    # start_url = 'http://www.baidu.com'
    start_urls = []

    def start_requests(self):
        """构建初始请求对象"""
        for url in self.start_urls:
            yield Request(url)

    def parse(self,response):
        """解析"""
        yield Item(response.body)
