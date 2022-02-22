#!/usr/bin/python
# -*- coding:utf-8 _*- 
"""
@author:TXU
@file:functions.py
@time:2022/01/05
@email:tao.xu2008@outlook.com
@description: 商城管理-配置
"""
from runner.customized.setup.setup_mall import SetupMall


def disable_order_custom_fields_require(env_id):
    """
    商城设置 - 自定义字段设置 - 关闭非必填项
    :param env_id:
    :return:
    """
    mall = SetupMall(env_id)
    return mall.disable_order_custom_fields_require()


def set_valet_order(env_id, open_audit=True):
    """
    商城设置 - 代客下单审核设置： 打开订单创建审核，关闭后代客下单订单将直接进入待发货状态
    审查1次 -- 只保留 “审查1”
    :param env_id:
    :param open_audit: 设置状态，默认打开
    :return:
    """
    mall = SetupMall(env_id)
    return mall.set_valet_order(open_audit)


if __name__ == '__main__':
    pass
