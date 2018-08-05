# _*_ coding:utf-8 _*_
import requests

from scrapy_plus.http.response import Response


class Downloader(object):
    def get_response(self, request):
        # 判断请求方法
        if request.method.upper() == 'GET':
            resp = requests.get(request.url, headers=request.headers, params=request.params)

        elif request.method.upper() == "POST":
            resp = requests.post(request.url, headers=request.headers, params=request.params, data=request.data)

        else:
            raise Exception('不支持的请求方法')

        # 返回响应对象
        return Response(url=resp.url, status_code=resp.status_code, headers=resp.headers, body=resp.content)
            

