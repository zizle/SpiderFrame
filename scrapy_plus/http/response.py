# _*_ coding:utf-8 _*_
from lxml import etree

class Response(object):
    """response对象"""
    def __init__(self, url, status_code, headers, body):
        self.url = url
        self.status = status_code
        self.headers = headers
        self.body = body

    def xpath(self, rule):
        html = etree.HTML(self.body)
        return html.xpath(rule)
