#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Invoker"

from json import JSONDecodeError
from functools import partialmethod
import requests


class APIBase(object):
    """自定义web请求类，封装requests

    >>> base = APIBase()

    >>> data = base._get("https://httpbin.org/get", params=dict(foo="bar"))

    >>> data["url"]
    'https://httpbin.org/get?foo=bar'

    >>> data["args"]
    {'foo': 'bar'}

    >>> data = base._post("https://httpbin.org/post", json=dict(foo="bar"))

    >>> data["url"]
    'https://httpbin.org/post'

    >>> data["data"]
    '{"foo": "bar"}'

    >>> data["headers"]["Content-Type"]
    'application/json'

    >>> data = base._post("https://httpbin.org/post", data=dict(foo="bar"))

    >>> data["url"]
    'https://httpbin.org/post'

    >>> data["form"]
    {'foo': 'bar'}

    >>> data["headers"]["Content-Type"]
    'application/x-www-form-urlencoded'

    >>> data = base._put('https://httpbin.org/put', json=dict(foo="bar"))

    >>> data["url"]
    'https://httpbin.org/put'

    >>> data["data"]
    '{"foo": "bar"}'

    >>> data["headers"]["Content-Type"]
    'application/json'

    >>> data = base._delete('https://httpbin.org/delete')

    >>> data["url"]
    'https://httpbin.org/delete'
    """
    def __init__(self, req=None):
        self._client = req or requests
        self.__connect_timeout = 5.0
        self.__socket_timeout = 5.0
        self.__proxies = {}

    def set_connection_timeout(self, ms):
        """设置请求超时时间，单位毫秒"""
        self.__connect_timeout = ms / 1000.0

    def set_socket_timeout(self, ms):
        """设置响应超时时间，单位毫秒"""
        self.__socket_timeout = ms / 1000.0

    def set_proxies(self, proxies):
        """设置代理"""
        self.__proxies = proxies

    def _request(self, method, url, params=None, data=None, json=None, **kw):
        """自定义请求"""
        try:
            resp = self._client.request(
                method.upper().strip(),
                url,
                params=params,
                data=data,
                json=json,
                timeout=(self.__connect_timeout, self.__socket_timeout),
                proxies=self.__proxies,
                **kw,
            )
            data = resp.json()
        except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectTimeout):
            return {
                "errcode": "sdk001",
                "errmsg": "connection or read data timeout",
            }
        except JSONDecodeError:
            return {
                "errcode": "sdk002",
                "errmsg": "invalid json data",
            }
        return data

    _get = partialmethod(_request, "GET")
    _post = partialmethod(_request, "POST")
    _put = partialmethod(_request, "PUT")
    _delete = partialmethod(_request, "DELETE")


if __name__ == '__main__':
    import doctest
    doctest.testmod()
