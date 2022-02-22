#!/usr/bin/python
# -*- coding:utf-8 _*- 
"""
@author:TXU
@file:functions.py
@time:2022/01/05
@email:tao.xu2008@outlook.com
@description: 配置中心 - 客户配置 - xxx
"""

from runner.customized.setup.setup_customer import SetupCustomer


# 客户管理 - 客户字段设置
def setup_customer_fields(env_id):
    """
    配置中心-客户管理-客户字段设置：新增客户前重置客户字段设置
    :param env_id:
    :return:
    """
    cus = SetupCustomer(env_id)
    return cus.setup_customer_fields()


# 销售机会设置
def setup_sale_chance_fields(env_id):
    """
    配置中心-销售机会设置：新增客户前重置客户字段设置（取消非必要必填项）
    :param env_id:
    :return:
    """
    cus = SetupCustomer(env_id)
    return cus.setup_sale_chance_fields()


if __name__ == '__main__':
    pass
