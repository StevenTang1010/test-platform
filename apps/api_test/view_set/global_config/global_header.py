#!/usr/bin/python
# -*- coding:utf-8 _*- 
"""
@author:TXU
@file:global_header.py
@time:2021/08/26
@email:tao.xu2008@outlook.com
@description:
"""
from apps.api_test.view_set.base import ApiTestBaseViewSet
from apps.api_test.models import GlobalHeader
from apps.api_test.serializers import GlobalHeaderSerializer
from apps.api_test.filters import GlobalHeaderFilter


class GlobalHeaderViewSet(ApiTestBaseViewSet):
    serializer_class = GlobalHeaderSerializer
    queryset = GlobalHeader.objects.all().order_by('id')
    filter_fields = ("name",)
    filterset_class = GlobalHeaderFilter

    # 批量 更新数据
    def bulk_update(self, request, *args, **kwargs):
        self.serializer_class = GlobalHeaderSerializer
        return super().bulk_update(request, *args, **kwargs)

    # 批量 局部更新数据
    def partial_bulk_update(self, request, *args, **kwargs):
        self.serializer_class = GlobalHeaderSerializer
        return super().partial_bulk_update(request, *args, **kwargs)

    # 批量 删除数据
    def bulk_destroy(self, request, *args, **kwargs):
        self.serializer_class = GlobalHeaderSerializer
        return super().bulk_destroy(request, *args, **kwargs)


if __name__ == '__main__':
    pass
