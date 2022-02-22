# --------------------------------------
# Date: 2021/8/10
# @Author: Steven_Tang
# FileName: base_viewset.py   
# Description: 
# --------------------------------------
from django.db.models import Count
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet


# 定义返回类，统一处理返回信息
class ReturnMsg:
    def __init__(self, code=2, msg='success', errors=None, data=None):
        self.code = code
        self.msg = msg
        self.errors = errors
        self.data = data

    def dict(self):
        return {
            'code': self.code,
            'msg': self.msg,
            'errors': self.errors,
            'data': self.data
        }


# 定义继承viewset的基类，重写接口返回内容
class BaseViewSet(ModelViewSet):
    # 创建数据
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response(ReturnMsg(data=response.data).dict(), status=response.status_code)

    # 检索数据
    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return Response(ReturnMsg(data=response.data).dict(), status=response.status_code)

    # 更新数据
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response(ReturnMsg(data=response.data).dict(), status=response.status_code)

    # 部分更新数据
    def partial_update(self, request, *args, **kwargs):
        response = super().partial_update(request, *args, **kwargs)
        return Response(ReturnMsg(data=response.data).dict(), status=response.status_code)

    # 删除数据
    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        return Response(ReturnMsg(data=response.data).dict(), status=response.status_code)

    # 查询数据
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response(ReturnMsg(data=response.data).dict(), status=response.status_code)


class GroupViewSet(BaseViewSet):
    # 重写分组逻辑
    def list(self, request, *args, **kwargs):
        """
        :param request:
        group_by_field: 分组字段
        time_unit: 若按时间分组，可设置时间单位 year | month | day
        :param args:
        :param kwargs:
        :return:
        """
        group_by_field = 'ticket_number'
        time_unit = ''
        time_unit_str = {
            'year': '%%Y',
            'month': '%%Y-%%m',
            'week': '%%x-%%v',
            'day': '%%Y-%%m-%%d'
        }
        if 'group_by' in request.query_params:
            request.query_params._mutable = True
            group_by_field = request.query_params.get('group_by')
            request.query_params.__delitem__('group_by')
            request.query_params._mutable = False

        if 'time_unit' in request.query_params:
            request.query_params._mutable = True
            time_unit = request.query_params.get('time_unit')
            request.query_params.__delitem__('time_unit')
            request.query_params._mutable = False

        extra_select = {
            group_by_field: "DATE_FORMAT({}, '{}')".format(group_by_field, time_unit_str[time_unit])
        } if time_unit else {}
        queryset = self.filter_queryset(self.get_queryset().extra(select=extra_select).values(group_by_field)). \
            order_by(group_by_field).annotate(count=Count("pk")).values(group_by_field, "count")
        return Response(ReturnMsg(data=list(queryset.all())).dict(), status=200)
