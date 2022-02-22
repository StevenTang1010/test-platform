#!/usr/bin/python
# -*- coding:utf-8 _*- 
"""
@author:TXU
@file:exceptions.py
@time:2021/12/07
@email:tao.xu2008@outlook.com
@description: exceptions，自定义异常
"""


class MyBaseError(Exception):
    pass


class FileTypeError(MyBaseError):
    pass


class FileImportError(MyBaseError):
    pass


class FileParseError(MyBaseError):
    pass


class ParamsError(MyBaseError):
    pass


class NotFoundError(MyBaseError):
    pass


class FileNotFound(FileNotFoundError, NotFoundError):
    pass


if __name__ == '__main__':
    pass
