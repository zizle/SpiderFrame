# _*_ coding:utf-8 _*_
class TestSpiderMiddleware1(object):

    def process_request(self, request):
        '''处理请求头，添加默认的user-agent'''
        print("TestSpiderMiddleware1: process_request")
        return request

    def process_response(self, response):
        '''处理数据对象'''
        print("TestSpiderMiddleware1: process_response")
        return response


class TestSpiderMiddleware2(object):

    def process_request(self, request):
        '''处理请求头，添加默认的user-agent'''
        print("TestSpiderMiddleware2: process_request")
        return request

    def process_response(self, response):
        '''处理数据对象'''
        print("TestSpiderMiddleware2: process_response")
        return response