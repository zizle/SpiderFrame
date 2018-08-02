# _*_ coding:utf-8 _*_


class DownloaderMiddeware(object):
    def process_request(self, request):
        print('这是下载中间件process_request方法')

        return request

    def process_response(self, response):
        print('这是下载中间件process_response方法')
        return response
