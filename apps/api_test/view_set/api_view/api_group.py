#!/usr/bin/python
# -*- coding:utf-8 _*- 
"""
@author:TXU
@file:api_group.py
@time:2021/08/30
@email:tao.xu2008@outlook.com
@description: 接口分组
"""
from apps.api_test.view_set.base import ApiTestBaseViewSet
from apps.api_test.models import ApiGroup
from apps.api_test.serializers import ApiGroupSerializer, ApiGroupDeserializer
from apps.api_test.filters import ApiGroupFilter


class ApiGroupViewSet(ApiTestBaseViewSet):
    serializer_class = ApiGroupSerializer
    queryset = ApiGroup.objects.all().order_by('id')
    filterset_class = ApiGroupFilter

    # 更新数据
    def update(self, request, *args, **kwargs):
        self.serializer_class = ApiGroupDeserializer
        return super().update(request, *args, **kwargs)

    # 创建数据
    def create(self, request, *args, **kwargs):
        self.serializer_class = ApiGroupDeserializer
        return super().create(request, *args, **kwargs)

    # 批量 更新数据
    def bulk_update(self, request, *args, **kwargs):
        self.serializer_class = ApiGroupDeserializer
        return super().bulk_update(request, *args, **kwargs)

    # 批量 局部更新数据
    def partial_bulk_update(self, request, *args, **kwargs):
        self.serializer_class = ApiGroupDeserializer
        return super().partial_bulk_update(request, *args, **kwargs)

    # 批量 删除数据
    def bulk_destroy(self, request, *args, **kwargs):
        self.serializer_class = ApiGroupDeserializer
        return super().bulk_destroy(request, *args, **kwargs)


if __name__ == '__main__':
    pass

