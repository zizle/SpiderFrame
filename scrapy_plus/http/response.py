# _*_ coding:utf-8 _*_

import re
import json

from lxml import etree


class Response(object):
    """response对象"""

    def __init__(self, url, status_code, headers, body, meta={}):
        self.url = url
        self.status = status_code
        self.headers = headers
        self.body = body

        self.meta = meta

    def xpath(self, rule):
        html = etree.HTML(self.body)
        return html.xpath(rule)

    @property
    def json(self):
        '''提供json解析
        如果content是json字符串，是才有效
        '''
        return json.loads(self.body)

    def re_findall(self, rule, data=None):
        '''封装正则的findall方法'''
        if data is None:
            data = self.body
        return re.findall(rule, data)
