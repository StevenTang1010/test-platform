#!/usr/bin/python
# -*- coding:utf-8 _*- 
"""
@author:TXU
@file:api_update_history.py
@time:2021/11/05
@email:tao.xu2008@outlook.com
@description: ApiUpdateHistory 处理
"""
from rest_framework.views import APIView
from apps.api_test.view_set.base import JsonResponse
from apps.api_test.view_set.base import ApiTestBaseViewSet
from apps.api_test.models import ApiUpdateHistory
from apps.api_test.filters import ApiUpdateHistoryFilter
from apps.api_test.serializers import ApiUpdateHistorySerializer, ApiUpdateHistoryDeserializer
# from apps.api_test.throttle import ApiUpdateHistoryAddThrottle, MyThrottle


class ApiUpdateHistoryViewSet(ApiTestBaseViewSet):
    serializer_class = ApiUpdateHistorySerializer
    queryset = ApiUpdateHistory.objects.all().order_by('id')
    filterset_class = ApiUpdateHistoryFilter

    # 查询数据
    def list(self, request, *args, **kwargs):
        self.serializer_class = ApiUpdateHistorySerializer
        return super().list(request, *args, **kwargs)

    # 更新数据
    def update(self, request, *args, **kwargs):
        self.serializer_class = ApiUpdateHistoryDeserializer
        return super().update(request, *args, **kwargs)

    # 创建数据
    def create(self, request, *args, **kwargs):
        print(request.data)
        self.serializer_class = ApiUpdateHistoryDeserializer
        return super().create(request, *args, **kwargs)


class ApiSyncUpdateStatusToHistoryViewSet(APIView):

    def put(self, request, *args, **kwargs):
        """
        修改ApiUpdateHistory 对应接口的字段 update_status
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        api_id = request.data.get("api_id")
        update_status = request.data.get("update_status")
        ApiUpdateHistory.objects.filter(api__id__exact=api_id, update_status__lt=update_status).\
            update(**{"update_status": update_status})
        response = {
            "msg": "update_status 同步更新成功！"
        }
        return JsonResponse(response, status=200)


if __name__ == '__main__':
    pass
