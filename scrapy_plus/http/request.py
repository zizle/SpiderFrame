# _*_ coding:utf-8 _*_


class Request(object):
    """request对象"""
    def __init__(self, url, method="GET", headers=None, params=None, data=None, parse='parse', meta={}, filter=True):
        self.url = url
        self.method = method
        self.headers = headers
        self.params = params
        self.data = data

        self.parse = parse
        self.meta = meta
        self.filter = filter

