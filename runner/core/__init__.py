#!/usr/bin/python
# -*- coding:utf-8 _*- 
"""
@author:TXU
@file:__init__.py
@time:2021/10/25
@email:tao.xu2008@outlook.com
@description:核心逻辑、驱动代码
"""
__version__ = '1.0.1'
__description__ = "fast solution for API testing."

from runner.core.ext.locust import main_locusts
from runner.core.parser import parse_parameters as Parameters
from runner.core.runner import ApiRunner
from runner.core.testcase import Config, Step, RunRequest, RunTestCase

__all__ = [
    "__version__",
    "__description__",
    "ApiRunner",
    "Config",
    "Step",
    "RunRequest",
    "RunTestCase",
    "Parameters",
]


if __name__ == '__main__':
    pass
