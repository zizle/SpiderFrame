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

    def parse(self, response):
        '''解析豆瓣电影top250列表页'''
        for li in response.xpath("//ol[@class='grid_view']/li"):  # 遍历每一个li标签
            item = {}
            item["title"] = li.xpath(".//span[@class='title'][1]/text()")[0]  # 提取该li标下的 标题

            detail_url = li.xpath(".//div[@class='info']/div[@class='hd']/a/@href")[0]
            yield Request(detail_url, parse="parse_detail", meta={"item": item})  # 发起详情页的请求，并指定解析函数是parse_detail方法

    def parse_detail(self, response):
        '''解析详情页'''
        item = response.meta["item"]
        item["url"] = response.url
        print('item：', item)  # 打印一下响应的url
        return []  # 由于必须返回一个容器，这里返回一个空列表
        # yield Item(item)  #或者yield Item对象
