# --------------------------------------
# Date: 2021/8/5
# @Author: Steven_Tang
# FileName: serializers.py
# Description:
# --------------------------------------
from django.http import FileResponse, Http404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from collections import OrderedDict

from .filters import OrdersFilter, TesterFilter
from common.base_viewset import BaseViewSet, GroupViewSet, ReturnMsg
from .serializers import OrdersSerializer, ZtBugNewSerializer, TesterSerializer
from .models import Orders, ZtBug, TesterZtBug, DeveloperZtBug
from tools.orders import OrderList, EchartsDataAnalysis
from tools.zt_bug import BugReport
# from .resource import OrderResource, write_excel

ol = OrderList()


# 工单详情定制化分页
class OrdersPagination(PageNumberPagination):
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


# 工单列表查询
class OrdersViewSet(BaseViewSet):
    queryset = Orders.objects.all().order_by('-ticket_number')
    serializer_class = OrdersSerializer
    pagination_class = OrdersPagination  # 分页

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filter_class = OrdersFilter

    # 批量新增数据
    def create(self, request, *args, **kwargs):
        obj = [Orders(ticket_number=row['ticket_number'], priority=row['priority'], severity=row['severity'],
                      content=row['content'], domain=row['domain'],
                      pub_date=row['pub_date']) for row in
               ol.get_orders_data()]
        try:
            Orders.objects.bulk_create(obj, ignore_conflicts=True)
            response = {'code': 2, 'msg': f'更新成功【{len(obj) - 1}】条数据'}
        except Exception as exc:
            response = {'code': 0, 'msg': '更新失败', 'errors': exc}
        return Response(ReturnMsg(**response).dict())


# 工单数据统计
class StatisticsViewSet(GroupViewSet):
    queryset = Orders.objects.filter().order_by('-ticket_number')
    serializer_class = OrdersSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filter_class = OrdersFilter


# BUG分类统计趋势
class BugTrendViewSet(BaseViewSet):
    queryset = Orders.objects.all().order_by('-ticket_number')
    serializer_class = OrdersSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filter_class = OrdersFilter

    # 查询添加功能
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        res_data = response.data
        statistics_data = EchartsDataAnalysis(res_data.get('data').serializer).bug_trend()
        res_data['data'] = statistics_data
        return Response(ReturnMsg(**res_data).dict(), status=response.status_code)


# 工单趋势分析
class AnalysisViewSet(GroupViewSet):
    queryset = Orders.objects.all().order_by('-ticket_number')
    serializer_class = OrdersSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filter_class = OrdersFilter


# 通用导出接口
# class ExportViewSet(BaseViewSet):
#     queryset = Orders.objects.all().order_by('-ticket_number')
#     serializer_class = OrdersSerializer
#     filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
#     filter_class = OrdersFilter
#
#     # 导出功能
#     # def list(self, request, *args, **kwargs):
#     #     response = super().list(request, *args, **kwargs)
#     #     res_data = response.data
#     #     dataset = OrderResource().export(res_data.get('data').serializer.instance)
#     #     filename = write_excel(dataset)
#     #     try:
#     #         with open(filename, 'rb') as f:
#     #             res = FileResponse(f.read())
#     #             res['Content-Disposition'] = f'attachment; filename="{filename.name}"'
#     #             res['content_type'] = 'application/octet-stream'
#     #             # response.write(write_excel(dataset))
#     #             # res_data['data'] = write_excel(dataset)
#     #             print(res.filename)
#     #             res.status_code = 200
#     #         return res
#     #     except:
#     #         return Http404
#     #     # return Response(ReturnMsg(**res_data).dict(), status=200)
