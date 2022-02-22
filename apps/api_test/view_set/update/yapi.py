#!/usr/bin/python
# -*- coding:utf-8 _*- 
"""
@author:TXU
@file:update.py
@time:2021/11/11
@email:tao.xu2008@outlook.com
@description:
"""
import traceback

from rest_framework.views import APIView
from apps.api_test import logger
from apps.api_test.view_set.base import JsonResponse
from apps.api_test.models import YApiEvent
from apps.api_test.yapi.yapi_sync import APICaseTemplate, YAPIEventDataSync


# 用例模板更新：读取接口YAPI定义数据，生成并更新接口请求用例模板
class APICaseTemplateUpdateView(APIView):
    """读取接口YAPI定义数据，生成并更新接口请求用例模板"""
    def post(self, request, *args, **kwargs):
        api_list = request.data
        api_temp = APICaseTemplate()
        if 'all' in api_list:
            res_list = api_temp.update_all()
        else:
            res_list = api_temp.bulk_update_template(api_list)
        response = {"msg": "用例模板更新完成！", "data": res_list}
        return JsonResponse(response, status=200)


# yapi事件监听：YAPI web hook事件监听，接受事件并插入YAPIEvent表
class YAPIEventMonitorView(APIView):
    def post(self, request, *args, **kwargs):
        """
        YAPI接口变更事件监听处理
        1. 客户端更新接口成功后触发
            {'_id': 365459, 'YApiEvent': 'yapi_interface_update'}
        2. 客户端新增接口成功后触发
            TODO
        3. 客户端删除接口成功后触发
            TODO
        :param request:
        """
        data = request.data
        print('data:{}'.format(data))
        yapi_id = data.get("_id", 0)
        event = data.get("YApiEvent", "null")
        exist_events = YApiEvent.objects.filter(yapi_id__exact=yapi_id, event__exact=event)
        if exist_events.count() > 0:
            response = {
                "msg": "yapi变更事件已存在，忽略",
                "data": data
            }
        else:
            YApiEvent.objects.create(
                **{
                    'yapi_id': yapi_id,
                    'event': event,
                    'content': data,
                }
            )
            response = {
                "msg": "yapi变更事件添加成功",
                "data": data
            }

        return JsonResponse(response, status=200)


# yapi数据同步：YAPI变更事件->同步数据到本地接口
class YAPIEventDataSyncView(APIView):
    """YAPI变更事件->同步数据到本地接口"""

    def post(self, request, *args, **kwargs):
        """
        {'list':'all'}  -- data_sync()
        {'list':[]}  -- data_sync_single(yapi_event)
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        yapi_event_list = request.data
        yapi_data_sync = YAPIEventDataSync()
        if 'all' in yapi_event_list:
            res_list = yapi_data_sync.data_sync_all()
        else:
            res_list = yapi_data_sync.data_sync_bulk(yapi_event_list)
        response = {"msg": "更新处理完成！", "data": res_list}

        return JsonResponse(response, status=200)


# 接口拉取同步：本地接口主动拉取YAPI数据同步
class APIDataSyncView(APIView):
    """本地接口主动拉取YAPI数据同步"""

    def post(self, request, *args, **kwargs):
        api_list = request.data
        v_yapi_events = []
        yapi_data_sync = YAPIEventDataSync()
        for api in api_list:
            logger.info("更新接口：{} -> {}".format(api.get('id'), api.get('name')))
            yapi_id = api.get('yapi_id', '')
            # 构建类YAPIEvent字典，调用YAPIEventDataSync同步数据
            v_yapi_events.append({
                'id': 0,
                'yapi_id': yapi_id,
                'event': 'pull_yapi_info',
                'api_id': api.get('id'),
                'method': api.get('method'),
                'path': api.get('path'),
            })
        res_list = yapi_data_sync.data_sync_bulk(v_yapi_events)
        response = {"msg": "更新处理完成！", "data": res_list}
        return JsonResponse(response, status=200)


if __name__ == '__main__':
    pass
