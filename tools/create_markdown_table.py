#!/usr/bin/python
# -*- coding:utf-8 _*- 
"""
@author:TXU
@file:create_markdown_table.py
@time:2021/12/16
@email:tao.xu2008@outlook.com
@description: 生成markdown表格内容 - 附1：数据校验方法
"""
from prettytable import PrettyTable


def pretty_print(data_list):
    tb = PrettyTable(['ID', '方法', '支持的关键字', '描述'])
    for d in data_list:
        tb.add_row([d.get('id'), d.get('method'), ', '.join(d.get('keys')), d.get('desc')])

    print(tb)


if __name__ == '__main__':
    # 数据存于这个文件
    data = [
        {
            "id": 1,
            "method": "equal",
            "keys": [
                "eq",
                "equal",
                "equals"
            ],
            "desc": "验证元素值等于"
        },
        {
            "id": 2,
            "method": "not_equal",
            "keys": [
                "ne",
                "neq",
                "not_equal"
            ],
            "desc": "验证元素值不等于"
        },
        {
            "id": 3,
            "method": "greater_than",
            "keys": [
                "gt",
                "greater_than"
            ],
            "desc": "验证元素值大于"
        },
        {
            "id": 4,
            "method": "less_than",
            "keys": [
                "lt",
                "less_than"
            ],
            "desc": "验证元素值小于"
        },
        {
            "id": 5,
            "method": "greater_or_equals",
            "keys": [
                "ge",
                "greater_or_equals"
            ],
            "desc": "验证元素值大于等于"
        },
        {
            "id": 6,
            "method": "less_or_equals",
            "keys": [
                "le",
                "less_or_equals"
            ],
            "desc": "验证元素值小于等于"
        },
        {
            "id": 7,
            "method": "string_equals",
            "keys": [
                "str_eq",
                "string_equals"
            ],
            "desc": "验证元素值转换为string后等于"
        },
        {
            "id": 8,
            "method": "length_equal",
            "keys": [
                "len_eq",
                "length_equal"
            ],
            "desc": "验证元素长度不等于"
        },
        {
            "id": 9,
            "method": "length_greater_than",
            "keys": [
                "len_gt",
                "length_greater_than"
            ],
            "desc": "验证元素长度大于"
        },
        {
            "id": 10,
            "method": "length_greater_or_equals",
            "keys": [
                "len_ge",
                "length_greater_or_equals"
            ],
            "desc": "验证元素长度大于等于"
        },
        {
            "id": 11,
            "method": "length_less_than",
            "keys": [
                "len_lt",
                "length_less_than"
            ],
            "desc": "验证元素长度小于"
        },
        {
            "id": 12,
            "method": "length_less_or_equals",
            "keys": [
                "len_le",
                "length_less_or_equals"
            ],
            "desc": "验证元素长度小于等于"
        },
        {
            "id": 13,
            "method": "contains",
            "keys": [
                "contain",
                "contains"
            ],
            "desc": "验证元素的值中包含xxx"
        },
        {
            "id": 14,
            "method": "contains_if_exist",
            "keys": [
                "contain_if_exist",
                "contains_if_exist"
            ],
            "desc": "如果获取到元素不为空，验证元素的值中包含xxx"
        },
        {
            "id": 15,
            "method": "contained_by",
            "keys": [
                "contained_by",
                "in_list"
            ],
            "desc": "验证元素的值包含于xxx"
        },
        {
            "id": 16,
            "method": "not_contained_by",
            "keys": [
                "not_contained_by",
                "not_in_list"
            ],
            "desc": "验证元素的值不包含于xxx"
        },
        {
            "id": 17,
            "method": "has_key",
            "keys": [
                "has_key"
            ],
            "desc": "验证字典元素包含key或key列表"
        },
        {
            "id": 18,
            "method": "type_match",
            "keys": [
                "type_match"
            ],
            "desc": "验证元素的值类型为xxx（python数据类型名）"
        },
        {
            "id": 19,
            "method": "regex_match",
            "keys": [
                "regex_match"
            ],
            "desc": "验证元素的值匹配正则表达式"
        },
        {
            "id": 20,
            "method": "startswith",
            "keys": [
                "startswith"
            ],
            "desc": "验证元素的值转字符串后以xxx开头"
        },
        {
            "id": 21,
            "method": "endswith",
            "keys": [
                "endswith"
            ],
            "desc": "验证元素的值转字符串后以xxx结尾"
        }
    ]
    pretty_print(data)
