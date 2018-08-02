# _*_ coding:utf-8 _*_

from scrapy_plus.http.request import Request

from .spider import Spider
from .downloader import Downloader
from .pipeline import Pipeline
from .scheduler import Scheduler


class Engine(object):
    def __init__(self):
        self.spider = Spider()
        self.scheduler = Scheduler()
        self.downloader = Downloader()
        self.pipeline = Pipeline()

    def _start_engine(self):
        # 1. 爬虫模块发出初始请求
        start_request = self.spider.start_requests()

        # 2. 把初始请求添加给调度器
        self.scheduler.add_request(start_request)
        # 3. 从调度器获取请求对象，交给下载器发起请求，获取一个响应对象
        request = self.scheduler.get_request()

        # 4. 利用下载器发起请求
        response = self.downloader.get_response(request)
        # 5. 利用爬虫的解析响应的方法，处理响应，得到结果
        result = self.spider.parse(response)
        # 6. 判断结果对象
        # 6.1 如果是请求对象，那么就再交给调度器
        if isinstance(result, Request):
            self.scheduler.add_request(result)
        # 6.2 否则，就交给管道处理
        else:
            self.pipeline.process_item(result)

    def start(self):
        self._start_engine()


