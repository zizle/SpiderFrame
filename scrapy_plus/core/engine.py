# _*_ coding:utf-8 _*_
from datetime import datetime

from scrapy_plus.http.request import Request

from scrapy_plus.utils.log import logger

from .spider import Spider
from .downloader import Downloader
from .pipeline import Pipeline
from .scheduler import Scheduler

from scrapy_plus.middlewares.spider_middleware import SpiderMiddleware
from scrapy_plus.middlewares.downloader_middlewares import DownloaderMiddeware


class Engine(object):
    def __init__(self):
        self.spider = Spider()
        self.scheduler = Scheduler()
        self.downloader = Downloader()
        self.pipeline = Pipeline()

        self.spider_mid = SpiderMiddleware()
        self.downloader_mid = DownloaderMiddeware()

    def _start_engine(self):
        # 1. 爬虫模块发出初始请求
        start_request = self.spider.start_requests()

        # 2. 把初始请求添加给调度器
        # 利用爬虫中间件进行处理
        self.spider_mid.process_request(start_request)

        self.scheduler.add_request(start_request)
        # 3. 从调度器获取请求对象，交给下载器发起请求，获取一个响应对象
        request = self.scheduler.get_request()
        # 利用下载中间件进行处理
        self.downloader_mid.process_request(request)
        # 4. 利用下载器发起请求
        response = self.downloader.get_response(request)
        # 5. 利用爬虫的解析响应的方法，处理响应，得到结果
        # 利用下载中间件处理响应
        self.downloader_mid.process_response(response)
        result = self.spider.parse(response)
        # 6. 判断结果对象
        # 6.1 如果是请求对象，那么就再交给调度器
        if isinstance(result, Request):
            result = self.spider_mid.process_request(result)
            self.scheduler.add_request(result)
        # 6.2 否则，就交给管道处理
        else:
            self.pipeline.process_item(result)

    def start(self):
        start = datetime.now()
        logger.info('开始运行时间%s' % start)
        self._start_engine()
        stop = datetime.now()
        logger.info('程序结束时间%s' % stop)
        logger.info('爬虫运行总耗时%.2f' % (stop - start).total_seconds())


