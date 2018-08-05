# _*_ coding:utf-8 _*_

from six.moves.queue import Queue


class Scheduler(object):
    def __init__(self):
        self.queue = Queue()
        # 记录总共的请求数
        self.total_request_number = 0  # 此处新增

    def add_request(self, request):
        self.queue.put(request)
        # 总请求数+1
        self.total_request_number += 1

    def get_request(self):
        try:
            request = self.queue.get(False)  # 设置为非阻塞
        except:
            return None
        else:
            return request

    def _filter_request(self):
        pass


