# _*_ coding:utf-8 _*_


from scrapy_plus.core.engine import Engine

from spiders import BaiduSpider, DoubanSpider


if __name__ == '__main__':
    baidu_spider = BaiduSpider()
    douban_spider = DoubanSpider()

    spiders = {
        baidu_spider.name: baidu_spider,
        douban_spider.name: douban_spider,
    }
    engine = Engine(spiders)
    engine.start()
