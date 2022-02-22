#!/usr/bin/python
# -*- coding:utf-8 _*- 
"""
@author:TXU
@file:setup_customer.py
@time:2021/08/18
@email:tao.xu2008@outlook.com
@description: 客户管理相关初始化
"""
import json
from loguru import logger
from requests import Response
from runner.common.spiders.auth import Auth


class SetupCustomer(Auth):
    """配置中心-客户设置"""

    def __init__(self, env_id):
        super(SetupCustomer, self).__init__(env_id)
        self.env_id = env_id
        self.default_headers = {
            "Authorization": self.Authorization,
            "Content-Type": "application/json"
        }

    # 新增客户前重置客户字段设置
    def setup_customer_fields(self):
        """
        新增客户前重置客户字段设置
        :return:
        """
        logger.info("获取当前客户字段信息...")
        url_1 = self.base_url + "/qw-scrm-svc/action/customer/getCusTmpInfo"
        res_data = self.request("post", url_1, headers=self.default_headers).json().get("data")  # 获取所有销售机会字段信息
        fields = json.dumps(res_data)
        fields_changed = fields.replace('"require": true', '"require": false')  # 将所有字段的必填设置为关闭
        fields_finall = fields_changed.replace('"require": false', '"require": true', 1)  # 将姓名字段必填设置开启

        url_2 = self.base_url + "/qw-scrm-svc/action/customer/uptCusTmpInfo"
        logger.info("设置客户字段为非必填...")
        res = self.request("post", url_2, headers=self.default_headers, json=json.loads(fields_finall))
        logger.info(res.text)

        response = Response()
        response.status_code = 200
        return response

    # 重置销售机会字段（取消非必要必填项）
    def setup_sale_chance_fields(self):
        """
        重置销售机会字段（取消非必要必填项）
        :return:
        """
        logger.info("获取当前销售机会字段信息...")
        url_1 = self.base_url + "/qw-scrm-svc/action/sale-chance/filter-fields"
        fields = self.request("get", url_1, headers=self.default_headers).json().get("data")  # 获取所有销售机会字段信息

        url_2 = self.base_url + "/qw-scrm-svc/action/sale-chance/fields"
        logger.info("设置销售机会字段为非必填...")
        for field in fields.get("stable")+fields.get("custom"):
            if field["isBan"] or not field["require"]:  # 固定字段或必填字段
                continue
            # 请求更新客户字段设置
            data = {
                "id": field["id"],
                "name": field["name"],
                "show": field["show"],
                "enable": field["enable"],
                "require": False,
                "options": field["options"]
            }
            res = self.request("PATCH", url_2, headers=self.default_headers, json=data)
            logger.info(res.text)

        response = Response()
        response.status_code = 200
        return response


if __name__ == '__main__':
    pass
