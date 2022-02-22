#!/usr/bin/python
# -*- coding:utf-8 _*- 
"""
@author:TXU
@file:global_host.py
@time:2021/08/26
@email:tao.xu2008@outlook.com
@description:
"""
from rest_framework.views import APIView

from apps.api_test import logger
from apps.api_test.view_set.base import ApiTestBaseViewSet, JsonResponse
from apps.api_test.models import GlobalEnv
from apps.api_test.serializers import GlobalEnvSerializer
from runner.common.get_env_data import GetEnvData
from runner.common.gen_mock_data import GenMockData
from apps.api_test.filters import GlobalEnvFilter


class GlobalEnvViewSet(ApiTestBaseViewSet):
    serializer_class = GlobalEnvSerializer
    queryset = GlobalEnv.objects.all().order_by('name')
    filter_fields = ("name", "id",)
    filterset_class = GlobalEnvFilter

    # 批量 更新数据
    def bulk_update(self, request, *args, **kwargs):
        self.serializer_class = GlobalEnvSerializer
        return super().bulk_update(request, *args, **kwargs)

    # 批量 局部更新数据
    def partial_bulk_update(self, request, *args, **kwargs):
        self.serializer_class = GlobalEnvSerializer
        return super().partial_bulk_update(request, *args, **kwargs)

    # 批量 删除数据
    def bulk_destroy(self, request, *args, **kwargs):
        self.serializer_class = GlobalEnvSerializer
        return super().bulk_destroy(request, *args, **kwargs)


class GetEnvDefaultConfigView(APIView):

    def get(self, request, *args, **kwargs):
        """
        获取环境默认 基础配置
        :param request:
        """
        response = GlobalEnv().get_default_config()
        return JsonResponse(response, status=200)


class GetEnvDefaultQWExternalContactConfigView(APIView):

    def get(self, request, *args, **kwargs):
        """
        获取环境默认 企微客户联系配置
        :param request:
        """
        response = GlobalEnv().get_default_qw_external_contact_config()
        return JsonResponse(response, status=200)


class EnvDataViewSet(GlobalEnvViewSet):
    """获取并更新环境结构数据"""

    def get_new_data(self, env_id):
        new_env_data = {}
        new_mock_data = {}
        # 更新环境数据
        GlobalEnv.objects.filter(id__exact=env_id).update(data={})  # 先清空data，避免无效session被取到
        env_data_obj = GetEnvData(env_id)
        logger.warning(env_data_obj.get_props())
        for k in env_data_obj.get_props():
            try:
                v = env_data_obj.__getattribute__(k)
                logger.debug("环境数据：{}:{}".format(k, v))
                new_env_data.update({k: v})
            except Exception as e:
                logger.error(e)

        # 更新mock数据
        mock_data_obj = GenMockData()
        for k in mock_data_obj.get_props():
            try:
                v = mock_data_obj.__getattribute__(k)
                logger.debug("环境mock数据：{}:{}".format(k, v))
                new_mock_data.update({k: v})
            except Exception as e:
                logger.error(e)
        return new_env_data, new_mock_data

    def retrieve(self, request, *args, **kwargs):
        new_env_data, new_mock_data = self.get_new_data(kwargs['pk'])
        response_data = {
            "data": new_env_data,
            "mock": new_mock_data,
        }
        return JsonResponse(response_data, status=200)

    def update(self, request, *args, **kwargs):
        print(request.query_params)
        env_id = 1
        new_env_data, new_mock_data = self.get_new_data(env_id)
        kwargs['data'].update(new_env_data)
        kwargs['mock'].update(new_mock_data)
        return super().update(request, *args, **kwargs)


if __name__ == '__main__':
    pass
