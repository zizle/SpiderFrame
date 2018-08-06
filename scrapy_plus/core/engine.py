# _*_ coding:utf-8 _*_
import time
import importlib
from datetime import datetime
from scrapy_plus.conf.settings import SPIDERS, PIPELINES, SPIDER_MIDDLEWARES, DOWNLOADER_MIDDLEWARES, MAX_ASYNC_THREAD_NUMBER, ASYNC_TYPE, SCHEDULER_PERSIST

from scrapy_plus.utils.stats_collector import NormalStatsCollector, RedisStatsCollector


# 判断使用的异步方式，导入相应的异步池
if ASYNC_TYPE == 'thread':
    from multiprocessing.dummy import Pool
elif ASYNC_TYPE == 'coroutine':
    from scrapy_plus.async.coroutine import Pool
else:
    raise Exception("不支持的异步类型：{}, 只能是'thread'或者'coroutine'".format(ASYNC_TYPE))


from scrapy_plus.http.request import Request
from scrapy_plus.utils.log import logger
from .downloader import Downloader
from .scheduler import Scheduler


class Engine(object):
    def __init__(self):

        self.spiders = self._auto_import_instances(SPIDERS, isspider=True)
        # 启用分布式
        if SCHEDULER_PERSIST:
            self.collector = RedisStatsCollector()
        else:
            self.collector = NormalStatsCollector()
        # 调度器
        self.scheduler = Scheduler(self.collector)
        # 下载器
        self.downloader = Downloader()
        self.pipelines = self._auto_import_instances(PIPELINES)  # 管道
        self.spider_mids = self._auto_import_instances(SPIDER_MIDDLEWARES)  # 爬虫中间件
        self.downloader_mids = self._auto_import_instances(DOWNLOADER_MIDDLEWARES)  # 下载中间件

        self.pool = Pool()
        self.is_running = False

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
        t_start = datetime.now()
        logger.info("爬虫开始启动：{}".format(t_start))
        logger.info("爬虫运行模式：{}".format(ASYNC_TYPE))
        logger.info("框架是否启用Redis分布式：{}".format(SCHEDULER_PERSIST))
        logger.info("最大并发数：{}".format(MAX_ASYNC_THREAD_NUMBER))
        logger.info("启动的爬虫有：{}".format(list(self.spiders.keys())))
        logger.info("启动的爬虫中间件有：\n{}".format(SPIDER_MIDDLEWARES))
        logger.info("启动的下载中间件有：\n{}".format(DOWNLOADER_MIDDLEWARES))
        logger.info("启动的管道有：\n{}".format(PIPELINES))
        # 开启引擎
        self._start_engine()
        # 结束
        t_end = datetime.now()
        logger.info("爬虫运行结束：{}".format(t_end))
        logger.info("耗时：%s" % (t_end - t_start).total_seconds())
        logger.info("一共获取了请求：{}个".format(self.collector.request_nums))
        logger.info("重复的请求：{}个".format(self.collector.repeat_request_nums))
        logger.info("成功的请求：{}个".format(self.collector.response_nums))
        self.collector.clear()  # 清除redis中所有的计数的值,但不清除指纹集合

    def _callback(self, temp):
        if self.is_running:
            self.pool.apply_async(self._execute_request_response_item, callback=self._callback, error_callback=self._error_callback)

    def _error_callback(self, exception):
        """异常回调函数"""
        try:
            raise exception  # 抛出异常后，才能被日志进行完整记录下来
        except Exception as e:
            logger.exception(e)

    def _start_engine(self):
        # 运行状态设置为True
        self.is_running = True
        # 异步线程池加入请求
        self.pool.apply_async(self._start_request, error_callback=self._error_callback)
        # 并发数控制
        for i in range(MAX_ASYNC_THREAD_NUMBER):
            # 异步线程池执行队列中的请求
            self.pool.apply_async(self._execute_request_response_item, callback=self._callback, error_callback=self._error_callback)

        # self._start_request()
        while True:
            time.sleep(0.0001)
            # self._execute_request_response_item()
            if self.collector.request_nums != 0:

                # 成功的响应数+重复的数量>=总的请求数量 程序结束
                if self.collector.response_nums + self.collector.repeat_request_nums >= self.collector.request_nums:
                # if self.total_response_nums + self.scheduler.repeat_request_num>= self.total_request_nums:
                    self.is_running = False
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
                self.collector.incr(self.collector.request_nums_key)

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
                    self.collector.incr(self.collector.request_nums_key)
                # 6.2 否则，就交给管道处理
                else:
                    for pipeline in self.pipelines:
                        pipeline.process_item(result, spider)
        # 响应数+1
        self.collector.incr(self.collector.response_nums_key)
