#!/usr/bin/python
# -*- coding:utf-8 _*- 
"""
@author:TXU
@file:project_member.py
@time:2021/09/16
@email:tao.xu2008@outlook.com
@description:
"""
from apps.api_test.view_set.base import ApiTestBaseViewSet
from apps.api_test.models import ProjectMember
from apps.api_test.serializers import ProjectMemberSerializer, ProjectMemberDeserializer
from apps.api_test.filters import ProjectMemberFilter


class ProjectMemberViewSet(ApiTestBaseViewSet):
    serializer_class = ProjectMemberSerializer
    queryset = ProjectMember.objects.all().order_by('id')
    filterset_class = ProjectMemberFilter

    # 创建数据
    def create(self, request, *args, **kwargs):
        self.serializer_class = ProjectMemberDeserializer
        return super().create(request, *args, **kwargs)

    # 更新数据
    def update(self, request, *args, **kwargs):
        self.serializer_class = ProjectMemberDeserializer
        return super().update(request, *args, **kwargs)


if __name__ == '__main__':
    pass
