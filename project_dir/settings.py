# _*_ coding:utf-8 _*_

# 修改默认日志文件名称
DEFAULT_LOG_FILENAME = '日志.log'    # 默认日志文件名称

# 启用的爬虫类
SPIDERS = [
    'spiders.baidu.BaiduSpider',
    'spiders.douban.DoubanSpider'
]

# 启用的管道类
PIPELINES = [
    'pipelines.BaiduPipeline',
    'pipelines.DoubanPipeline'
]

# 启用的爬虫中间件类
SPIDER_MIDDLEWARES = [
    'middlewares.spider_middlewares.TestSpiderMiddleware1',
    'middlewares.spider_middlewares.TestSpiderMiddleware2',
    ]

# 启用的下载器中间件类
DOWNLOADER_MIDDLEWARES = [
    'middlewares.downloader_middlewares.TestDownloaderMiddleware1',
    'middlewares.downloader_middlewares.TestDownloaderMiddleware2',
]

# 使用协程并发
ASYNC_TYPE = 'coroutine'