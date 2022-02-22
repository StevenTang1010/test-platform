#!/usr/bin/python
# -*- coding:utf-8 _*- 
"""
@author:TXU
@file:throttle.py
@time:2021/11/13
@email:tao.xu2008@outlook.com
@description: 限制 单独一个用户的 访问次数
"""
import time

from rest_framework.throttling import SimpleRateThrottle


class ApiUpdateHistoryAddThrottle(SimpleRateThrottle):
    scope = "api_update_history_add"

    def get_cache_key(self, request, view):
        return self.get_ident(request)


visit_record = {}


class MyThrottle(object):
    # 限制访问时间
    VISIT_TIME = 30
    VISIT_COUNT = 1

    # 定义方法 方法名和参数不能变
    def allow_request(self, request, view):
        # 获取登录主机的id
        id = request.META.get('REMOTE_ADDR')
        self.now = time.time()

        if id not in visit_record:
            visit_record[id] = []

        self.history = visit_record[id]
        # 限制访问时间
        while self.history and self.now - self.history[-1] > self.VISIT_TIME:
            self.history.pop()
        # 此时 history中只保存了最近10秒钟的访问记录
        if len(self.history) >= self.VISIT_COUNT:
            return False
        else:
            self.history.insert(0, self.now)
            return True

    def wait(self):
        return self.history[-1] + self.VISIT_TIME - self.now


if __name__ == '__main__':
    pass
