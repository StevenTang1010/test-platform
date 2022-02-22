from collections import OrderedDict

# Create your views here.

# 工单详情定制化分页
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .filters import *
from .serializers import *
from .models import *
from common.base_viewset import BaseViewSet, ReturnMsg

from tools.precise_search import search_model, search_third_elevance, search_func_elevance, match_func, create_func, \
    update_func


class ModelPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('page', self.page.number),
            ('results', data)
        ]))

    page_size = 50
    page_size_query_param = 'page_size'  # 每页多少条
    page_query_param = 'p'  # 页码的名称
    max_page_size = 100


# 获取system列表
class SystemViewSet(BaseViewSet):
    queryset = System.objects.all()
    serializer_class = SystemSerializer


# 根据system获取一级模块列表
class PrimaryViewSet(BaseViewSet):
    queryset = PrimaryModule.objects.all()
    serializer_class = PrimarySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filter_fields = ('system',)
    filter_class = PrimaryModuleFilter


# 根据一级模块获取二级模块列表
class SecondaryViewSet(BaseViewSet):
    queryset = SecondaryModule.objects.all()
    serializer_class = SecondarySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filter_fields = ('primary',)
    filter_class = SecondaryModuleFilter


# 根据二级模块获取三级模块列表
class ThirdViewSet(BaseViewSet):
    queryset = ThirdModule.objects.all()
    serializer_class = ThirdSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filter_fields = ('second',)
    filter_class = ThirdModuleFilter


# 根据搜索项获取所有func数据
class SearchViewSet(BaseViewSet):
    queryset = ModuleFunction.objects.all()
    serializer_class = ModuleFunctionSerializer

    # pagination_class = ModelPagination

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        res_data = response.data
        system = request.query_params.get('system')
        primary = request.query_params.get('primary')
        secondary = request.query_params.get('secondary')
        third = request.query_params.get('third')
        func_data = search_model(system, primary, secondary, third)
        res_data['data'] = func_data
        return Response(ReturnMsg(**res_data).dict(), status=response.status_code)


# 跳转详情
class DirectDetail(BaseViewSet):
    queryset = ThirdModule.objects.all()
    serializer_class = ThirdSerializer

    # pagination_class = ModelPagination

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        res_data = response.data
        third_name = request.query_params.get('third')
        func_name = request.query_params.get('func')
        if third_name:
            detail_data = search_third_elevance(third_name)
            detail_data.update({'third_name': third_name, 'total': len(detail_data.get('detail'))})
        elif func_name:
            detail_data = search_func_elevance(func_name)
            detail_data.update({'func_name': func_name, 'total': len(detail_data.get('detail'))})
        else:
            detail_data = {'error': '参数错误'}
        res_data['data'] = detail_data
        return Response(ReturnMsg(**res_data).dict(), status=response.status_code)


# 模糊匹配所有功能
class MatchFunc(BaseViewSet):
    queryset = ModuleFunction.objects.all()
    serializer_class = ModuleFunctionSerializer

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        res_data = response.data
        query_string = request.query_params.get('query')
        res_data['data'] = match_func(query_string)
        return Response(ReturnMsg(**res_data).dict(), status=response.status_code)


# 新增功能
class CreateFunc(BaseViewSet):
    queryset = FunctionalRelevance.objects.all()
    serializer_class = FunctionalRelevanceSerializer

    def create(self, request, *args, **kwargs):
        # response = super().create(request, *args, **kwargs)
        # res_data = response.data
        result = create_func(request.data)
        if result:
            return Response(ReturnMsg(data=result).dict(), status=200)
        else:
            return Response(ReturnMsg(code=0, msg='failed', errors=result).dict(), status=400)


# 编辑功能关联
class UpdateFunc(BaseViewSet):
    queryset = FunctionalRelevance.objects.all()
    serializer_class = FunctionalRelevanceSerializer

    def create(self, request, *args, **kwargs):
        # response = super().create(request, *args, **kwargs)
        # res_data = response.data
        result = update_func(request.data)
        if result:
            return Response(ReturnMsg(data=result).dict(), status=200)
        else:
            return Response(ReturnMsg(code=0, msg='failed', errors=result).dict(), status=400)
