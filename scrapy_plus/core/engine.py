# _*_ coding:utf-8 _*_
from datetime import datetime
import time
import importlib
from scrapy_plus.conf.settings import SPIDERS, PIPELINES, SPIDER_MIDDLEWARES, DOWNLOADER_MIDDLEWARES
from scrapy_plus.http.request import Request
from scrapy_plus.utils.log import logger
from .downloader import Downloader
from .scheduler import Scheduler


class Engine(object):
    def __init__(self):

        self.spiders = self._auto_import_instances(SPIDERS, isspider=True)
        self.scheduler = Scheduler()
        self.downloader = Downloader()
        self.pipelines = self._auto_import_instances(PIPELINES)  # 管道
        self.spider_mids = self._auto_import_instances(SPIDER_MIDDLEWARES)  # 爬虫中间件
        self.downloader_mids = self._auto_import_instances(DOWNLOADER_MIDDLEWARES)  # 下载中间件

        self.total_request_nums = 0
        self.total_response_nums = 0

    def _auto_import_instances(self, path=[], isspider=False):
        instance = {} if isspider else []
        for p in path:
            module_name = p.rsplit('.', 1)[0]
            cls_name = p.rsplit('.', 1)[1]
            ret = importlib.import_module(module_name)
            cls = getattr(ret, cls_name)
            if isspider:
                instance[cls_name] = cls()
            else:
                instance.append(cls())

        return instance

    def start(self):
        start = datetime.now()
        logger.info('开始运行时间%s' % start)
        self._start_engine()
        stop = datetime.now()
        logger.info('程序结束时间%s' % stop)
        logger.info('爬虫运行总耗时%.2f' % (stop - start).total_seconds())

        logger.info("总的请求数量:{}".format(self.total_request_nums))
        logger.info("重复请求数量:{}".format(self.scheduler.repeat_request_num))
        logger.info("总的响应数量:{}".format(self.total_response_nums))

    def _start_engine(self):
        self._start_request()
        while True:
            time.sleep(0.0001)
            self._execute_request_response_item()
            # 成功的响应数+重复的数量>=总的请求数量 程序结束
            if self.total_response_nums + self.scheduler.repeat_request_num>= self.total_request_nums:
                break

    def _start_request(self):
        # 1. 爬虫模块发出初始请求
        for spider_name, spider in self.spiders.items():
            for start_request in spider.start_requests():
                # 2. 把初始请求添加给调度器
                # 利用爬虫中间件进行处理
                for spider_mid in self.spider_mids:
                    start_request = spider_mid.process_request(start_request)
                # 绑定爬虫名称
                start_request.spider_name = spider_name
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
        for downloader_mid in self.downloader_mids:
            request = downloader_mid.process_request(request)
        # 4. 利用下载器发起请求
        response = self.downloader.get_response(request)
        # meta对象的绑定
        response.meta = request.meta
        # response对象经过下载中间件的process_response进行处理
        for downloader_mid in self.downloader_mids:
            response = downloader_mid.process_response(response)
        # response对象经过爬虫中间件的process_response进行处理
        for spider_mid in self.spider_mids:
            response = spider_mid.process_response(response)
        # 获取当前爬虫
        spider = self.spiders[request.spider_name]
        # 解析方法的动态调用
        # parse = getattr(self.spider, request.parse)
        parse = getattr(spider, request.parse)

        results = parse(response)
        if results is not None:
            # 5. 利用爬虫定义的解析方法，处理响应，得到结果
            for result in results:
                # 6. 判断结果对象
                # 6.1 如果是请求对象，那么就再交给调度器
                if isinstance(result, Request):
                    # 通过爬虫中间件处理
                    for spider_mid in self.spider_mids:
                        result = spider_mid.process_request(result)
                    # 给request对象添加爬虫名字
                    result.spider_name = request.spider_name
                    # 加入调度器队列
                    self.scheduler.add_request(result)
                    # 请求数+1
                    self.total_request_nums += 1
                # 6.2 否则，就交给管道处理
                else:
                    for pipeline in self.pipelines:
                        pipeline.process_item(result, spider)
        # 响应数+1
        self.total_response_nums += 1
