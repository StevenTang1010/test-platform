#!/usr/bin/python
# -*- coding:utf-8 _*- 
"""
@author:TXU
@file:__init__.py.py
@time:2021/09/09
@email:tao.xu2008@outlook.com
@description:
"""
import os
import datetime

from runner.config.opts import *

# 时间
time_str = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
# 项目root目录
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
# 测试用例*.py文件路径
testcase_path = os.path.join(root_dir, 'testcase')
# 保留历史构建数据的最大个数
testcase_max_rotation = 50

# 测试报告文件路径
report_path = os.path.join(root_dir, '../reports')


def zfill(number, width=6):
    """
    转换数字为字符串，并以’0‘填充左侧
    :param number:
    :param width: 最小宽度，如实际数字小于最小宽度，左侧填0
    :return: __zfill(123, 6) -> '000123'
    """
    return str(number).zfill(width)


class ReportAttr(object):
    """生成基于report.id的属性"""
    def __init__(self, report_id):
        self.zfill_report_id = zfill(report_id)

    @property
    def testcase_path(self):
        return os.path.join(testcase_path, 'test_{}'.format(self.zfill_report_id))

    @property
    def html_report_path(self):
        return os.path.join(report_path, self.zfill_report_id, "html", "report.html")

    @property
    def xml_report_path(self):
        return os.path.join(report_path, self.zfill_report_id, "xml")


# 创建配置对象为全局变量
cf = ConfigIni(os.path.join(root_dir, 'config', 'globals.ini'))

# 设置全局 key/value
_global_dict = {}


def set_global_value(key, value):
    global _global_dict
    # print(key, value)
    _global_dict[key] = value


def get_global_value(key, default_value=None):

    try:
        global _global_dict
        return _global_dict[key]
    except KeyError:
        return default_value


def get_global_dict():
    return _global_dict


__all__ = [
    "root_dir", "testcase_path", "time_str", "cf",
    "report_path", "testcase_max_rotation", "ReportAttr",
    "set_global_value", "get_global_value", "get_global_dict",
    "read_yaml"
]

if __name__ == '__main__':
    pass
