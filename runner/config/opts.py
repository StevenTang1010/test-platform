#!/usr/bin/python
# -*- coding:utf-8 _*- 
"""
@author:TXU
@file:opts.py
@time:2021/07/14
@email:tao.xu2008@outlook.com
@description:配置文件操作，读、写
"""
import codecs

import yaml
import configparser
from jsonpath import jsonpath


def read_yaml(file_path, yaml_loader=yaml.FullLoader):
    """
    读取yaml文件内容，返回字典
    :param file_path:
    :param yaml_loader:
    :return:
    """
    with codecs.open(file_path, 'r', 'utf-8') as f:
        data = yaml.load(f, Loader=yaml_loader)
    return data


def read_ini(file_path, section, option):
    """
    读取ini配置文件section->option的值，如：
    [TEST]
    url = https://xxxxx.com
    :param file_path:
    :param section: --TEST
    :param option: --url
    :return:
    """
    conf = configparser.ConfigParser()
    conf.read(file_path)
    return conf.get(section, option)


def read_ini_section(file_path, section):
    """
    读取ini配置文件section下所有键值对，返回字典
    :param file_path:
    :param section:
    :return:
    """
    conf = configparser.ConfigParser()
    conf.read(file_path)
    return dict(conf.items(section))


class ConfigIni(object):
    """读、写ini配置文件"""
    def __init__(self, file_path):
        """
        生成配置文件对象并读取配置文件
        :param file_path: 配置文件的绝对路径
        """
        self.file_path = file_path
        # 定义配置文件对象，并读取配置文件
        self.cf = configparser.ConfigParser()
        self.cf.read(file_path)

    def reload(self):
        self.cf.read(self.file_path)

    # 获取字符串的配置内容
    def get_str(self, section, option):
        """
        获取配置文件的value值
        :param section: 配置文件中section的值
        :param option: 配置文件中option的值
        :return value: 返回value的值
        """
        return self.cf.get(section, option)

    # 获取int数字型内容
    def get_int(self, section, option):
        """
        获取配置文件的value值
        :param section: 配置文件中section的值
        :param option: 配置文件中option的值
        :return value:  返回value的值
        """
        return self.cf.getint(section, option)

    # 获取float型数字内容
    def get_float(self, section, option):
        """
        获取配置文件的value值
        :param section: 配置文件中section的值
        :param option: 配置文件中option的值
        :return value:  返回value的值
        """
        return self.cf.getfloat(section, option)

    # 获取布尔值的返回内容
    def get_boolean(self, section, option):
        """
        获取配置文件的value值
        :param section: 配置文件中section的值
        :param option: 配置文件中option的值
        :return value:  返回value的值
        """
        return self.cf.getboolean(section, option)

    def get_kvs(self, section):
        return dict(self.cf.items(section))

    # 修改配置文件的value值
    def set_value(self, section, option, value):
        """
        修改value的值
        :param section: 配置文件中section的值
        :param option: 配置文件中option的值
        :param value: 修改value的值
        :return:
        """
        # python内存先修改值
        self.cf.set(section, option, value)
        # 需要通过文件的方式写入才行，不然实体文件的值不会改变
        with open(self.file_path, "w+") as f:
            self.cf.write(f)
        return True


def json_path(json_s, expr):
    """
    :param json_s: 传入json格式，发现json或者字典都ok
    :param expr: 要获取json内容的表达式
    :return: 返回想要的字符串
    """
    # print(json)
    # print(type(json))
    # string = json.dumps(json1, ensure_ascii=False)
    # print(string)
    return jsonpath(json_s, f"$..{expr}")


if __name__ == '__main__':
    # print(ConfigIni("globals.ini").get_str("SESSION", "url"))
    # print(read_ini("globals.ini", "TEST", "url"))
    # print(read_ini_section("globals.ini", "LOGGING"))
    print(read_yaml("xxx.yaml"))
