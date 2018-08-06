# _*_ coding:utf-8 _*_


from scrapy_plus.core.engine import Engine

# from spiders import BaiduSpider, DoubanSpider
from spiders.baidu import BaiduSpider
from spiders.douban import DoubanSpider
from pipelines import BaiduPipeline, DoubanPipeline
from middlewares.spider_middlewares import TestSpiderMiddleware1, TestSpiderMiddleware2
from middlewares.downloader_middlewares import TestDownloaderMiddleware1, TestDownloaderMiddleware2

if __name__ == '__main__':
    baidu_spider = BaiduSpider()
    douban_spider = DoubanSpider()
    spiders = {baidu_spider.name: baidu_spider, douban_spider.name: douban_spider}
    pipelines = [BaiduPipeline(), DoubanPipeline()]

    spider_mids = [TestSpiderMiddleware1(), TestSpiderMiddleware2()]
    downloader_mids = [TestDownloaderMiddleware1(), TestSpiderMiddleware2()]

    engine = Engine(spiders, pipelines=pipelines, spider_mids=spider_mids, downloader_mids=downloader_mids)
    engine.start()
