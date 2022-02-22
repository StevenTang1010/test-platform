#!/usr/bin/python
# -*- coding:utf-8 _*- 
"""
@author:TXU
@file:api_update_history.py
@time:2021/11/05
@email:tao.xu2008@outlook.com
@description: ApiUpdateHistory 处理
"""

from apps.api_test.view_set.base import ApiTestBaseViewSet
from apps.api_test.models import YApiEvent
from apps.api_test.filters import YApiEventFilter
from apps.api_test.serializers import YApiEventSerializer


class YApiEventViewSet(ApiTestBaseViewSet):
    serializer_class = YApiEventSerializer
    queryset = YApiEvent.objects.all().order_by('id')
    filterset_class = YApiEventFilter

    # 批量 更新数据
    def bulk_update(self, request, *args, **kwargs):
        self.serializer_class = YApiEventSerializer
        return super().bulk_update(request, *args, **kwargs)

    # 批量 局部更新数据
    def partial_bulk_update(self, request, *args, **kwargs):
        self.serializer_class = YApiEventSerializer
        return super().partial_bulk_update(request, *args, **kwargs)

    # 批量 删除数据
    def bulk_destroy(self, request, *args, **kwargs):
        self.serializer_class = YApiEventSerializer
        return super().bulk_destroy(request, *args, **kwargs)


if __name__ == '__main__':
    pass
