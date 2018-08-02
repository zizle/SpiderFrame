# _*_ coding:utf-8 _*_


class Item(object):
    """Item对象的封装"""
    def __init__(self, data):
        self._data = data

    @property
    def data(self):
        return self._data