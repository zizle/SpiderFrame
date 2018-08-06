# _*_ coding:utf-8 _*_
import logging

# 默认的日志配置
DEFAULT_LOG_LEVEL = logging.INFO    # 默认等级
DEFAULT_LOG_FMT = '%(asctime)s %(filename)s[line:%(lineno)d] \
                  %(levelname)s: %(message)s'   # 默认日志格式
DEFUALT_LOG_DATEFMT = '%Y-%m-%d %H:%M:%S'  # 默认时间格式
DEFAULT_LOG_FILENAME = 'log.log'    # 默认日志文件名称

# 异步并发的方式 thread or coroutine 线程 或 协程
# 可以在项目的settings.py中重新设置该值，自动覆盖
ASYNC_TYPE = 'thread' # 默认为线程的方式


# 启用的爬虫
SPIDERS = []

# 启用的默认管道类
PIPELINES = []

# 启用的默认爬虫中间件类
SPIDER_MIDDLEWARES = []

# 启用的默认下载器中间件类
DOWNLOADER_MIDDLEWARES = []

# 默认异步线程最大并发数
MAX_ASYNC_THREAD_NUMBER = 5
