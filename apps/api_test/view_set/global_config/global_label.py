#!/usr/bin/python
# -*- coding:utf-8 _*- 
"""
@author:TXU
@file:global_label.py
@time:2021/09/03
@email:tao.xu2008@outlook.com
@description:
"""
from apps.api_test.view_set.base import ApiTestBaseViewSet
from apps.api_test.models import GlobalLabel
from apps.api_test.serializers import GlobalLabelSerializer
from apps.api_test.filters import GlobalLabelFilter


class GlobalLabelViewSet(ApiTestBaseViewSet):
    serializer_class = GlobalLabelSerializer
    queryset = GlobalLabel.objects.all().order_by('id')
    filterset_class = GlobalLabelFilter

    # 批量 更新数据
    def bulk_update(self, request, *args, **kwargs):
        self.serializer_class = GlobalLabelSerializer
        return super().bulk_update(request, *args, **kwargs)

    # 批量 局部更新数据
    def partial_bulk_update(self, request, *args, **kwargs):
        self.serializer_class = GlobalLabelSerializer
        return super().partial_bulk_update(request, *args, **kwargs)

    # 批量 删除数据
    def bulk_destroy(self, request, *args, **kwargs):
        self.serializer_class = GlobalLabelSerializer
        return super().bulk_destroy(request, *args, **kwargs)


if __name__ == '__main__':
    pass
