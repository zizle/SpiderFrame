# _*_ coding:utf-8 _*_
class TestDownloaderMiddleware1(object):

    def process_request(self, request):
        '''处理请求头，添加默认的user-agent'''
        print("测试下载中间件1: process_request")
        return request

    def process_response(self, response):
        '''处理数据对象'''
        print("测试下载中间件1: process_response")
        return response


class TestDownloaderMiddleware2(object):

    def process_request(self, request):
        '''处理请求头，添加默认的user-agent'''
        print("测试下载中间件2: process_request")
        return request

    def process_response(self, response):
        '''处理数据对象'''
        print("测试下载中间件2: process_response")
        return response