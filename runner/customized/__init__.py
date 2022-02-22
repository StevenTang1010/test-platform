#!/usr/bin/python
# -*- coding:utf-8 _*- 
"""
@author:TXU
@file:__init__.py.py
@time:2021/12/01
@email:tao.xu2008@outlook.com
@description:
"""
# 初始化django -- 新进程
import django

django.setup()

from runner.customized.callback_functions import *
from runner.customized.mall_functions import *
from runner.customized.settings_functions import *

if __name__ == '__main__':
    pass
