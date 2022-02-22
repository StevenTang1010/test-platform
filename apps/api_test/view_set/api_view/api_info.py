#!/usr/bin/python
# -*- coding:utf-8 _*- 
"""
@author:TXU
@file:api_info.py
@time:2021/08/31
@email:tao.xu2008@outlook.com
@description:
"""
from apps.api_test.view_set.base import ApiTestBaseViewSet, GroupCountModelMixin, TotalCountModelMixin
from apps.api_test.models import ApiInfo
from apps.api_test.filters import ApiInfoFilter
from apps.api_test.serializers import ApiInfoSerializer, ApiInfoDeserializer


class ApiInfoViewSet(ApiTestBaseViewSet):
    serializer_class = ApiInfoSerializer
    queryset = ApiInfo.objects.all().order_by('id')
    filterset_class = ApiInfoFilter

    # 查询数据
    def list(self, request, *args, **kwargs):
        self.serializer_class = ApiInfoSerializer
        return super().list(request, *args, **kwargs)

    # 更新数据
    def update(self, request, *args, **kwargs):
        self.serializer_class = ApiInfoDeserializer
        return super().update(request, *args, **kwargs)

    # 创建数据
    def create(self, request, *args, **kwargs):
        self.serializer_class = ApiInfoDeserializer
        return super().create(request, *args, **kwargs)

    # 批量 更新数据
    def bulk_update(self, request, *args, **kwargs):
        self.serializer_class = ApiInfoDeserializer
        return super().bulk_update(request, *args, **kwargs)

    # 批量 局部更新数据
    def partial_bulk_update(self, request, *args, **kwargs):
        self.serializer_class = ApiInfoDeserializer
        return super().partial_bulk_update(request, *args, **kwargs)

    # 批量 删除数据
    def bulk_destroy(self, request, *args, **kwargs):
        self.serializer_class = ApiInfoDeserializer
        return super().bulk_destroy(request, *args, **kwargs)


class ToDoApiInfoViewSet(ApiInfoViewSet):
    queryset = ApiInfo.objects.filter(update_status__lt=2).order_by('id')


class NoCaseApiInfoViewSet(ApiInfoViewSet):
    queryset = ApiInfo.objects.filter(step_api__id__isnull=True).distinct().order_by('id')


# 统计数据
class ApiTotalViewSet(TotalCountModelMixin):
    """获取接口总数数据"""
    filterset_class = ApiInfoFilter
    queryset = ApiInfo.objects.filter(status__exact=True)


class ApiCountViewSet(GroupCountModelMixin):
    """获取接口统计数据"""
    filterset_class = ApiInfoFilter
    queryset = ApiInfo.objects.filter(status__exact=True)
    default_group_by_field = 'project'
    default_time_unit = None


class NoCaseApiCountViewSet(GroupCountModelMixin):
    """获取无用例覆盖接口统计数据"""
    filterset_class = ApiInfoFilter
    queryset = ApiInfo.objects.filter(status__exact=True, step_api__id__isnull=True)


class WithCaseApiCountViewSet(GroupCountModelMixin):
    """获取已有用例覆盖的接口统计数据"""
    filterset_class = ApiInfoFilter
    queryset = ApiInfo.objects.filter(status__exact=True, step_api__id__isnull=False)


class ToDoApiCountViewSet(GroupCountModelMixin):
    """获取存在更新待处理的接口统计数据"""
    filterset_class = ApiInfoFilter
    queryset = ApiInfo.objects.filter(status__exact=True, update_status__lt=2)


if __name__ == '__main__':
    pass
