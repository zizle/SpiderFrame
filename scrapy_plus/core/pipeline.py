# _*_ coding:utf-8 _*_


class Pipeline(object):
    """管道"""
    def process_item(self, item):
        print('收集到item对象:', item)
