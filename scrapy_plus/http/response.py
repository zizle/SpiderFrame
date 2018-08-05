# _*_ coding:utf-8 _*_


class Response(object):
    """response对象"""
    def __init__(self, url, status_code, headers, body):
        self.url = url
        self.status = status_code
        self.headers = headers
        self.body = body
