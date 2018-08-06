# _*_ coding:utf-8 _*_

from six.moves.queue import Queue
from scrapy_plus.utils.log import logger
import w3lib.url
import six
from hashlib import sha1

class Scheduler(object):
    def __init__(self):
        self.queue = Queue()
        # 记录总共的请求数

        self.repeat_request_num = 0  # 统计重复的数量
        self._filter_container = set()  # 去重容器,是一个集合,存储已经发过的请求的特征 url

    def add_request(self, request):
        if self._filter_request(request):
            self.queue.put(request)

    def get_request(self):
        try:
            request = self.queue.get(False)  # 设置为非阻塞
        except:
            return None
        else:
            return request

    def _filter_request(self, request):
        """去重"""
        request.fp = self._gen_fp(request)
        if request.fp not in self._filter_container:
            self._filter_container.add(request.fp)  # 向指纹容器集合添加一个指纹
            return True
        else:
            self.repeat_request_num += 1
            logger.info("发现重复的请求：<{} {}>".format(request.method, request.url))
            return False

    def _gen_fp(self, request):
        """生成请求指纹"""
        # 1 url排序
        url = w3lib.url.canonicalize_url(request.url)

        # 2 method处理
        method = request.method.upper()
        # 3 data排序
        data = request.data if request.data else {}
        data = sorted(data.items(), key=lambda x: x[0])
        # 4 利用sha1
        s1 = sha1()
        s1.update(self._to_bytes(url))
        s1.update(self._to_bytes(method))
        s1.update(self._to_bytes(str(data)))
        fp = s1.hexdigest()
        return fp

    def _to_bytes(self, string):
        if six.PY2:
            if isinstance(string, str):
                return string
            else:
                string.encode('utf-8')

        else:
            if isinstance(string, str):
                return string.encode('utf-8')
            else:
                return string




