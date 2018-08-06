# _*_ coding:utf-8 _*_
import time
from scrapy_plus.core.spider import Spider
from scrapy_plus.http.request import Request


class Baidu2Spider(Spider):
    name = 'baidu2_spider'
    start_urls = ['https://www.baidu.com']
    timed_task = True # 表示 这是一个定时爬虫

    def start_requests(self):
        while True:
            for url in self.start_urls:
                yield Request(url, parse='parse', filter=False) # 注意这个parse接收的是字符串
                time.sleep(6)  # 定时发起请求，此时程序不会停止！

    def parse(self, response):
        print(response.body)
        yield response.body # 一定要写yield
