#!/usr/bin/python
# -*- coding:utf-8 _*- 
"""
@author:TXU
@file:singleton.py
@time:2021/12/07
@email:tao.xu2008@outlook.com
@description: 线程锁实现单例模式 metaclass
"""
import time
import threading


class Singleton(type):
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        time.sleep(1)
        with cls._lock:
            if not hasattr(cls, "_instance"):
                cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


if __name__ == '__main__':
    pass
