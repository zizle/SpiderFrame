# _*_ coding:utf-8 _*_

"""scrapy_plus协程模块, 为了兼容py2\py3使用gevent模块
由于gevent的Pool的没有close方法，也没有异常回调参数(error_callback)
需要对gevent的Pool进行进一步的封装，实现与线程池一样接口，实现线程和协程的无缝转换
"""

from gevent.pool import Pool as BasePool
import gevent.monkey
gevent.monkey.patch_all()


class Pool(BasePool):
    """
    协程池
       使得具有close方法
       使得gevent.pool的apply_async方法具有和线程池名字一样的接口
    """

    def apply_async(self, func, args=None, kwds=None, callback=None, error_callback=None):
        return super().apply_async(func, args=args, kwds=kwds, callback=callback)  # super()调用父类的apply_async方法

    def close(self):
        pass

