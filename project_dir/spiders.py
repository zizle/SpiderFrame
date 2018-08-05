# _*_ coding:utf-8 _*_

from scrapy_plus.core.spider import Spider

from scrapy_plus.http.request import Request


class BaiduSpider(Spider):
    start_urls = ['http://www.baidu.com', 'https://www.taobao.com']


class DoubanSpider(Spider):
    start_urls = []

    def start_requests(self):
        # 重写start_requests方法，返回多个请求
        base_url = 'http://movie.douban.com/top250?start='
        for i in range(0, 250, 25):
            url = base_url + str(i)
            yield Request(url)

    def parse(self,response):
        pass
