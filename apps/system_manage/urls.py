#!/usr/bin/python
# -*- coding:utf-8 _*- 
"""
@author:TXU
@file:urls.py
@time:2022/02/07
@email:tao.xu2008@outlook.com
@description:
"""

from django.conf.urls import url
from django.urls import path, include
# from rest_framework.routers import DefaultRouter
from rest_framework_bulk.routes import BulkRouter

from apps.system_manage.view_set.department import DepartmentViewSet
from apps.system_manage.view_set.system_logs import SystemLogsViewSet

# router = DefaultRouter()
router = BulkRouter()


# 团队组织
router.register(r'department/bulk', DepartmentViewSet),  # 批量处理
router.register(r'department/list', DepartmentViewSet, basename='list'),
router.register(r'department/detail', DepartmentViewSet, basename='retrieve'),
router.register(r'department/add', DepartmentViewSet, basename='create'),
router.register(r'department/update', DepartmentViewSet, basename='update'),
router.register(r'department/del', DepartmentViewSet, basename='destroy')

# 系统日志
router.register(r'logs', SystemLogsViewSet, basename='retrieve'),

urlpatterns = [
    # 数据表管理
    path('', include(router.urls))
]


if __name__ == '__main__':
    pass
