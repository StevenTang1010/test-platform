#!/usr/bin/python
# -*- coding:utf-8 _*- 
"""
@author:TXU
@file:serializers
@time:2022/02/09
@email:tao.xu2008@outlook.com
@description:
"""
from rest_framework import serializers
from rest_framework_bulk import BulkSerializerMixin, BulkListSerializer
from apps.system_manage.models import Department
from apps.user_auth.serializers import UserProfileSerializer


class DepartmentSerializer(serializers.ModelSerializer):
    """
    部门信息序列化
    """
    leader = UserProfileSerializer(read_only=True)
    members = UserProfileSerializer(many=True, read_only=True)

    class Meta:
        model = Department
        fields = '__all__'


class DepartmentDeserializer(BulkSerializerMixin, serializers.ModelSerializer):
    """
    部门信息反序列化
    """
    class Meta:
        model = Department
        fields = '__all__'
        list_serializer_class = BulkListSerializer


if __name__ == '__main__':
    pass
