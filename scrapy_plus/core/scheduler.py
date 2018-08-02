# _*_ coding:utf-8 _*_

from six.moves.queue import Queue


class Scheduler(object):
    def __init__(self):
        self.queue = Queue()

    def add_request(self, request):
        self.queue.put(request)

    def get_request(self):
        request = self.queue.get()
        return request

    def _filter_request(self):
        pass


