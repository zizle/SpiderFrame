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

# 设置调度器的内容是否要持久化
# 量个值：True和False
# 如果是True，那么就是使用分布式，同时也是基于请求的增量式爬虫
# 如果是False, 不使用redis队列，会使用python的set存储指纹和请求
SCHEDULER_PERSIST = False

# redis默认配置,默认为本机的redis
REDIS_SET_NAME = 'scrapy_plus_fp_set' # fp集合
REDIS_QUEUE_NAME = 'scrapy_plus_request_queue' # request队列
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_DB = 0


# 启用的爬虫
SPIDERS = []

# 启用的默认管道类
PIPELINES = []

# 启用的默认爬虫中间件类
SPIDER_MIDDLEWARES = []

# 启用的默认下载器中间件类
DOWNLOADER_MIDDLEWARES = []

# 默认异步线程最大并发数
MAX_ASYNC_THREAD_NUMBER = 16

# 指纹是否持久化
# 默认为True 即持久化请求对象的指纹,达到断点续爬的目的
# 如果为False,则在爬虫结束的时候清空指纹库
# 可以在项目的settings.py中重新赋值进行覆盖
FP_PERSIST = True
