# _*_ coding:utf-8 _*_

from scrapy_plus.core.spider import Spider
from scrapy_plus.http.request import Request
from scrapy_plus.item import Item


class DoubanSpider(Spider):
    name = 'douban'
    start_urls = []

    def start_requests(self):
        base_url = 'http://movie.douban.com/top250?start='
        for i in range(0, 250, 25):
            url = base_url + str(i)
            yield Request(url)

    def parse(self, response):
        title_list = []
        for li in response.xpath("//ol[@class='grid_view']/li"):
            # title = li.xpath(".//span[@class='title'][1]/text()")    # 提取该li标下的 标题
            # title_list.append(title[0])
            detail_url = li.xpath(".//div[@class='info']/div[@class='hd']/a/@href")[0]
            yield Request(url=detail_url, parse='parse_detail')
        # yield Item(title_list)    # 返回标题

    def parse_detail(self, response):
        '''解析详情页'''
        # print('详情页url：', response.url)  # 打印一下响应的url
        # return []  # 由于必须返回一个容器，这里返回一个空列表
        yield {'url': response.url} # 返回请求的url



