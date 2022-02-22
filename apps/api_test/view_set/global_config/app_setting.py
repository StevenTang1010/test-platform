#!/usr/bin/python
# -*- coding:utf-8 _*- 
"""
@author:TXU
@file:app_setting.py
@time:2021/08/26
@email:tao.xu2008@outlook.com
@description:
"""
from apps.api_test.view_set.base import ApiTestBaseViewSet, JsonResponse
from apps.api_test.models import AppSetting
from apps.api_test.serializers import AppSettingSerializer


class AppSettingViewSet(ApiTestBaseViewSet):
    serializer_class = AppSettingSerializer
    queryset = AppSetting.objects.all().order_by('id')
    filter_fields = ("name", "id",)

    # 创建数据
    def create(self, request, *args, **kwargs):
        self.serializer_class = AppSettingSerializer
        return super().create(request, *args, **kwargs)


class GetDefaultAppSettingView(ApiTestBaseViewSet):

    def retrieve(self, request, *args, **kwargs):
        response = AppSetting().get_default_app_setting()
        return JsonResponse(response, status=200)


if __name__ == '__main__':
    pass
