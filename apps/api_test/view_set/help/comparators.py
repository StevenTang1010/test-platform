#!/usr/bin/python
# -*- coding:utf-8 _*- 
"""
@author:TXU
@file:comparators.py
@time:2021/12/01
@email:tao.xu2008@outlook.com
@description:
"""

from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from runner.core.builtin.comparators import comparators_define
from apps.api_test.view_set.base import JsonResponse


class ComparatorHelpViewSet(ListModelMixin, GenericViewSet):
    # 查询数据
    def list(self, request, *args, **kwargs):
        data_list = []
        for idx, (method, keys, desc) in enumerate(comparators_define):
            data_list.append({
                'id': idx+1,
                'method': method,
                'keys': list(keys),
                'desc': desc,
            })

        return JsonResponse({'list': data_list}, status=200)


if __name__ == '__main__':
    pass
