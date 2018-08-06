# _*_ coding:utf-8 _*_

from scrapy_plus.core.spider import Spider
from scrapy_plus.http.request import Request


class BaiduSpider(Spider):
    name = 'baidu'
    start_urls = ['https://www.baidu.com', 'https://www.baidu.com']

    def parse(self, response):
        for i in range(3):
            yield Request(self.start_urls[0])
