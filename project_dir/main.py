# _*_ coding:utf-8 _*_


from scrapy_plus.core.engine import Engine

from spiders import BaiduSpider, DoubanSpider


if __name__ == '__main__':
    # spider = BaiduSpider()
    spider = DoubanSpider()
    engine = Engine(spider)
    engine.start()
