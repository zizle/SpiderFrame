# _*_ coding:utf-8 _*_

from scrapy_plus.core.spider import Spider


class BaiduSpider(Spider):
    name = 'baidu'
    start_urls = ['https://www.baidu.com']
