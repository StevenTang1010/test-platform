#!/usr/bin/python
# -*- coding:utf-8 _*- 
"""
@author:TXU
@file:debug_data.py
@time:2022/01/11
@email:tao.xu2008@outlook.com
@description: 模拟数据，供maker debug使用
"""
import random
from pypinyin import lazy_pinyin


class DebugData(object):
    """
    模拟数据，供maker debug使用:
    [
        {
            "name": "部门A"，
            "test_suite_list": [
                {
                    "name": "Suite1",
                    "test_case_list": [
                        "name": "case-1"
                        "test_step_list": [
                            "name": "step-1",
                            "method": "POST"
                            "path": "/api/test/login"
                        ]
                    ]
                }
            ]
        }
    ]
    """

    @property
    def case(self):
        """
        这是一个用例data模拟数据，做代码测试用
        :return:
        """
        config = {
            "name": "case" + str(random.randint(1, 100)),
            "base_url": "https://postman-echo.com",
            "verify": False,
            "path": ""
        }
        step = {
            "name": "step1",
            "testcase": "",
            "variables": {},
            "request": {
                "method": "GET",
                "url": "/api/test1",
                "id": 2,
                "name": "登录-正常值",
                "description": "正常值登录",
                "cookies": {},
                "headers": {},
                "req_json": {},
                "data": {},
                "response": {},
                "set_vars": {},
                "severity": "normal",
                "skipif": "",
                "sleep": 0,
                "host_tag": "host_mk",
                "status": True
            },
            "setup_hooks": [],
            "teardown_hooks": [],
            "extract": {},
            "validators": [],
            "validate_script": []
        }
        case = {
            "config": config,
            "teststeps": [
                step
            ]
        }

        return case

    @property
    def data_list(self):
        """
        这是一个用例data模拟数据，做代码测试用
        :return:
        """
        config = {
            "name": "商城",
            "base_url": "https://postman-echo.com",
            "verify": True,
            "path": ""
        }
        suite = {
            "config": config,
            "safe_name": "suite_a",
            "testcases": [self.case]
        }

        data = {
            "name": "商城",
            "safe_name": '_'.join(lazy_pinyin("商城")),
            "testsuites": [
                suite
            ]
        }
        return [data]


if __name__ == '__main__':
    pass
