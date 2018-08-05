# _*_ coding:utf-8 _*_
from datetime import datetime
import time

from scrapy_plus.http.request import Request

from scrapy_plus.utils.log import logger

from .downloader import Downloader
from .pipeline import Pipeline
from .scheduler import Scheduler

from scrapy_plus.middlewares.spider_middleware import SpiderMiddleware
from scrapy_plus.middlewares.downloader_middlewares import DownloaderMiddeware


class Engine(object):
    def __init__(self, spider):
        self.spider = spider
        self.scheduler = Scheduler()
        self.downloader = Downloader()
        self.pipeline = Pipeline()

        self.spider_mid = SpiderMiddleware()
        self.downloader_mid = DownloaderMiddeware()

        self.total_request_nums = 0
        self.total_response_nums = 0

    def start(self):
        start = datetime.now()
        logger.info('开始运行时间%s' % start)
        self._start_engine()
        stop = datetime.now()
        logger.info('程序结束时间%s' % stop)
        logger.info('爬虫运行总耗时%.2f' % (stop - start).total_seconds())

        logger.info("总的请求数量:{}".format(self.total_request_nums))
        logger.info("总的响应数量:{}".format(self.total_response_nums))

    def _start_engine(self):
        self._start_request()
        while True:
            time.sleep(0.0001)
            self._execute_request_response_item()
            if self.total_response_nums >= self.total_request_nums:
                break

    def _start_request(self):
        # 1. 爬虫模块发出初始请求
        for start_request in self.spider.start_requests():
            # 2. 把初始请求添加给调度器
            # 利用爬虫中间件进行处理
            start_request = self.spider_mid.process_request(start_request)
            # 加入调度器队列
            self.scheduler.add_request(start_request)
            # 请求数+1
            self.total_request_nums += 1

    def _execute_request_response_item(self):
        # 3. 从调度器获取请求对象，交给下载器发起请求，获取一个响应对象
        request = self.scheduler.get_request()
        if request is None:
            return
        # 利用下载中间件进行处理
        request = self.downloader_mid.process_request(request)
        # 4. 利用下载器发起请求
        response = self.downloader.get_response(request)
        # meta对象的绑定
        response.meta = request.meta
        # response对象经过下载中间件的process_response进行处理
        response = self.downloader_mid.process_response(response)
        # response对象经过爬虫中间件的process_response进行处理
        response = self.spider_mid.process_response(response)

        # 解析方法的动态调用
        parse = getattr(self.spider, request.parse)

        # 5. 利用爬虫定义的解析方法，处理响应，得到结果
        for result in parse(response):
            # 6. 判断结果对象
            # 6.1 如果是请求对象，那么就再交给调度器
            if isinstance(result, Request):
                # 通过爬虫中间件处理
                result = self.spider_mid.process_request(result)
                # 加入调度器队列
                self.scheduler.add_request(result)
                # 请求数+1
                self.total_request_nums += 1
            # 6.2 否则，就交给管道处理
            else:
                self.pipeline.process_item(result)

        self.total_response_nums += 1





