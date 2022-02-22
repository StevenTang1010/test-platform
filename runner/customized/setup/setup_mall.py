#!/usr/bin/python
# -*- coding:utf-8 _*- 
"""
@author:TXU
@file:setup_mall.py
@time:2021/08/19
@email:tao.xu2008@outlook.com
@description: 商城相关初始化
"""
import json
from loguru import logger
from runner.common.spiders.auth import Auth


class SetupMall(Auth):
    """商城管理初始化"""

    def __init__(self, env_id):
        super(SetupMall, self).__init__(env_id)
        self.env_id = env_id
        self.default_headers = {
            "Authorization": self.Authorization,
            "Content-Type": "application/json"
        }

    # 商城设置 - 自定义字段设置 - 关闭非必填项
    def disable_order_custom_fields_require(self):
        """
        商城设置 - 自定义字段设置 - 关闭非必填项
        :return:
        """
        logger.info("获取当前订单字段信息...")
        url_1 = self.base_url + "/mall/order/v1/mall_setting/order_custom_field"
        res_data = self.request("get", url_1, headers=self.default_headers).json().get("data")  # 获取所有字段信息
        fields = json.dumps(res_data)
        fields_changed = fields.replace('"require": true', '"require": false')  # 将所有字段的必填设置为关闭

        url_2 = self.base_url + "/mall/order/v1/mall_setting/update_order_custom_field"
        logger.info("设置订单字段为非必填...")
        res = self.request("post", url_2, headers=self.default_headers, json=json.loads(fields_changed))
        logger.info(res.text)
        return res

    # 商城设置 - 代客下单审核设置
    def set_valet_order(self, open_audit=True):
        """
        商城设置 - 代客下单审核设置： 打开订单创建审核，关闭后代客下单订单将直接进入待发货状态
        审查1次 -- 只保留 “审查1”
        :param open_audit: 开启、关闭订单创建审核
        :return:
        """
        logger.info("获取当前配置信息...")
        url_1 = self.base_url + "/mall/order/v1/mall_setting/base_setting/valet_setting/get"
        res_data = self.request("get", url_1, headers=self.default_headers).json().get("data")  # 获取所有配置信息
        res_data["open"] = open_audit  # 打开订单创建审核，关闭后代客下单订单将直接进入待发货状态
        if open_audit:
            login_uid = self.env.data.get("login_uid")
            login_user_name = self.env.data.get("login_name")
            add_audit = {
                "type": "user",
                "user": [
                    {
                        "id": login_uid,
                        "name": login_user_name
                    }
                ],
                "userIds": [login_uid],
                "roleIds": [],
                "deptIds": []
            }
            login_user_enabled = False
            for idx, audit in enumerate(res_data["auditList"]):
                if idx > 0:
                    res_data["auditList"].pop(idx)
                    continue
                if login_uid in audit["userIds"]:
                    # 增加当前登录用户到审查人员
                    login_user_enabled = True
                    continue
                else:
                    res_data["auditList"][idx]["userIds"].append(login_uid)
                    res_data["auditList"][idx]["user"].append({
                        "id": login_uid,
                        "name": login_user_name
                    })
                    login_user_enabled = True

            if not login_user_enabled:
                res_data["auditList"].append(add_audit)

        url_2 = self.base_url + "/mall/order/v1/mall_setting/base_setting/valet_setting/set"
        logger.info("代客下单审核设置:open={}...".format(open_audit))
        res = self.request("post", url_2, headers=self.default_headers, json=res_data)
        logger.info(res.text)
        return res


if __name__ == '__main__':
    pass
