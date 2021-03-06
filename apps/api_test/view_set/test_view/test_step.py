#!/usr/bin/python
# -*- coding:utf-8 _*- 
"""
@author:TXU
@file:test_case.py
@time:2021/09/01
@email:tao.xu2008@outlook.com
@description:
"""
from apps.api_test.view_set.base import ApiTestBaseViewSet, GroupCountModelMixin, TotalCountModelMixin
from apps.api_test.models import TestStep
from apps.api_test.filters import TestStepFilter
from apps.api_test.serializers import TestStepSerializer, TestStepDeserializer


class TestStepViewSet(ApiTestBaseViewSet):
    serializer_class = TestStepSerializer
    queryset = TestStep.objects.all().order_by('id')
    filterset_class = TestStepFilter

    # 查询数据
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    # 更新数据
    def update(self, request, *args, **kwargs):
        self.serializer_class = TestStepDeserializer
        return super().update(request, *args, **kwargs)

    # 局部更新数据
    def partial_update(self, request, *args, **kwargs):
        self.serializer_class = TestStepDeserializer
        return super().update(request, *args, **kwargs)

    # 创建数据
    def create(self, request, *args, **kwargs):
        self.serializer_class = TestStepDeserializer
        return super().create(request, *args, **kwargs)

    # 批量 更新数据
    def bulk_update(self, request, *args, **kwargs):
        self.serializer_class = TestStepDeserializer
        return super().bulk_update(request, *args, **kwargs)

    # 批量 局部更新数据
    def partial_bulk_update(self, request, *args, **kwargs):
        self.serializer_class = TestStepDeserializer
        return super().partial_bulk_update(request, *args, **kwargs)

    # 批量 删除数据
    def bulk_destroy(self, request, *args, **kwargs):
        self.serializer_class = TestStepDeserializer
        return super().bulk_destroy(request, *args, **kwargs)


# 统计数据
class TestStepTotalViewSet(TotalCountModelMixin):
    """获取接口总数数据"""
    filterset_class = TestStepFilter
    queryset = TestStep.objects.filter(status__exact=True)


class TestStepCountViewSet(GroupCountModelMixin):
    """获取测试步骤统计数据"""
    filterset_class = TestStepFilter
    queryset = TestStep.objects.filter(status__exact=True)
    default_group_by_field = 'result'
    default_time_unit = None


if __name__ == '__main__':
    pass
