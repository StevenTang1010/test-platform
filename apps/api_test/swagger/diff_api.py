#!/usr/bin/python
# -*- coding:utf-8 _*- 
"""
@author:TXU
@file:diff_api.py
@time:2021/11/10
@email:tao.xu2008@outlook.com
@description: diff swagger 和api接口表内容
"""
import json
from typing import List, Dict
from dictdiffer import diff
from apps.api_test import logger


def diff_swagger_api(swagger_data: List[Dict]):
    from apps.api_test.models import ApiInfo, ApiUpdateHistory
    for swagger_api in swagger_data:
        method = swagger_api.get('method')
        url = swagger_api.get('url')
        api_list = ApiInfo.objects.filter(method__exact=method, url__exact=url).all()
        api_n = len(api_list)
        if api_n == 0:
            # 数据库无该接口，表示swagger中接口为新增接口
            # 接口表 - 新增数据
            ApiInfo.objects.update(swagger_api)
            new_api = ApiInfo.objects.get(method__exact=method, url__exact=url)
            # 接口变更历史 - 新增数据
            ApiUpdateHistory.objects.update({
                "api": new_api.id,
                "event": "interface_add",
                "content": "新增接口",
                "update_status": 0
            })
        else:
            if api_n > 1:
                # 数据库存在该接口但是不唯一，警告
                logger.warning("接口重复，ID列表：{}".format([a.id for a in api_list]))
            # 数据库存在该接口，表示swagger中接口为变更事件，更新第一个接口
            api = api_list[0]
            diff_result = diff(api, swagger_api)
            # 接口变更历史 - 新增数据
            ApiUpdateHistory.objects.update({
                "api": api.id,
                "event": "interface_update",
                "content": json.dumps(list(diff_result)),
                "update_status": 0
            })
    return True


if __name__ == '__main__':
    first = {
        "title": "hello",
        "fork_count": 20,
        "stargazers": ["/users/20", "/users/30"],
        "settings": {
            "assignees": [100, 101, 201],
            "ass": "123"
        }
    }

    second = {
        "title": "hellooo",
        "fork_count": 20,
        "stargazers": ["/users/20", "/users/30", "/users/40"],
        "settings": {
            "assignees": [100, 101, 202],
            "ass": "1234"
        },
        "new_ky": ''
    }
    result = diff(first, second)
    print(list(result))
    # [
    #     ('change', 'title', ('hello', 'hellooo')),
    #     ('add', 'stargazers', [(2, '/users/40')]),
    #     ('change', ['settings', 'assignees', 2], (201, 202)),
    #     ('change', 'settings.ass', ('123', '1234')),
    #     ('add', '', [('new_ky', '')])
    # ]