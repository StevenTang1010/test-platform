#!/usr/bin/python
# -*- coding:utf-8 _*- 
"""
@author:TXU
@file:global_response_validate.py
@time:2021/08/30
@email:tao.xu2008@outlook.com
@description: 通用校验规则配置管理
"""
from apps.api_test.view_set.base import ApiTestBaseViewSet
from apps.api_test.models import GlobalResponseValidate
from apps.api_test.serializers import GlobalResponseValidateSerializer
from apps.api_test.filters import GlobalResponseValidateFilter


class GlobalResponseValidateViewSet(ApiTestBaseViewSet):
    serializer_class = GlobalResponseValidateSerializer
    queryset = GlobalResponseValidate.objects.all().order_by('id')
    filter_fields = ("name", "is_default", )
    filterset_class = GlobalResponseValidateFilter

    # 批量 更新数据
    def bulk_update(self, request, *args, **kwargs):
        self.serializer_class = GlobalResponseValidateSerializer
        return super().bulk_update(request, *args, **kwargs)

    # 批量 局部更新数据
    def partial_bulk_update(self, request, *args, **kwargs):
        self.serializer_class = GlobalResponseValidateSerializer
        return super().partial_bulk_update(request, *args, **kwargs)

    # 批量 删除数据
    def bulk_destroy(self, request, *args, **kwargs):
        self.serializer_class = GlobalResponseValidateSerializer
        return super().bulk_destroy(request, *args, **kwargs)


if __name__ == '__main__':
    pass
