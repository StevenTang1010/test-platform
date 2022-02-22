#!/usr/bin/python
# -*- coding:utf-8 _*- 
"""
@author:TXU
@file:user.py
@time:2021/08/24
@email:tao.xu2008@outlook.com
@description:
"""

from apps.api_test.view_set.base import ApiTestBaseViewSet
from apps.api_test.models import User
from apps.api_test.serializers import UserSerializer


class UserViewSet(ApiTestBaseViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all().order_by('id')


if __name__ == '__main__':
    pass
