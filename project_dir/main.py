# _*_ coding:utf-8 _*_


from scrapy_plus.core.engine import Engine

# from spiders import BaiduSpider, DoubanSpider
from spiders.baidu import BaiduSpider
from spiders.douban import DoubanSpider
from pipelines import BaiduPipeline, DoubanPipeline

if __name__ == '__main__':
    baidu_spider = BaiduSpider()
    douban_spider = DoubanSpider()
    spiders = {baidu_spider.name: baidu_spider, douban_spider.name: douban_spider}
    pipelines = [BaiduPipeline(), DoubanPipeline()]
    engine = Engine(spiders, pipelines=pipelines)
    engine.start()
