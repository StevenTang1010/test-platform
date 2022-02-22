#!/usr/bin/python
# -*- coding:utf-8 _*- 
"""
@author:TXU
@file:organization
@time:2022/02/09
@email:tao.xu2008@outlook.com
@description:
"""

from apps.api_test.view_set.base import ApiTestBaseViewSet
from apps.system_manage.models import Department
from apps.system_manage.serializers import DepartmentSerializer


class DepartmentViewSet(ApiTestBaseViewSet):
    serializer_class = DepartmentSerializer
    queryset = Department.objects.all().order_by('id')

    # 批量 更新数据
    def bulk_update(self, request, *args, **kwargs):
        self.serializer_class = DepartmentSerializer
        return super().bulk_update(request, *args, **kwargs)

    # 批量 局部更新数据
    def partial_bulk_update(self, request, *args, **kwargs):
        self.serializer_class = DepartmentSerializer
        return super().partial_bulk_update(request, *args, **kwargs)

    # 批量 删除数据
    def bulk_destroy(self, request, *args, **kwargs):
        self.serializer_class = DepartmentSerializer
        return super().bulk_destroy(request, *args, **kwargs)


if __name__ == '__main__':
    pass
