# _*_ coding:utf-8 _*_

from scrapy_plus.core.spider import Spider
from scrapy_plus.http.request import Request


class BaiduSpider(Spider):
    name = 'baidu'
    start_urls = ['https://www.baidu.com', 'https://www.baidu.com']

    total = 0

    def parse(self, response):
        # self.total += 1
        # if self.total > 5:
        #     return
        yield Request(self.start_urls[0], filter=False, parse='parse_detail')

    def parse_detail(self, response):
        return []
