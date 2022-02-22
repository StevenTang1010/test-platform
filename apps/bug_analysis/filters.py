# --------------------------------------
# Date: 2021/8/5
# @Author: Steven_Tang
# FileName: filters.py   
# Description: 自定义过滤
# --------------------------------------


import django_filters
# from django.db.models import Q

from .models import Orders, ZtBug, TesterZtBug, DeveloperZtBug


class OrdersFilter(django_filters.rest_framework.FilterSet):
    # 定义filter支持的类型【精确等于（忽略大小写），包含（忽略大小写）， 大于，大于等于，小于，小于等于，以...开头，
    # 以...结尾，在..范围内，日期字段的年份，日期的月，日期的日，是否为空】
    # ['exact', 'contains', 'gt', 'gte', 'lt', 'lte', 'startswith',
    #                       'endswith', 'range', 'year', 'month', 'day', 'isnull']
    # 开始时间
    start = django_filters.DateFilter(field_name='pub_date', lookup_expr='gte')
    # 结束时间
    end = django_filters.DateFilter(field_name='pub_date', lookup_expr='lte')
    # 年份过滤
    year = django_filters.DateFilter(field_name='pub_date__year', lookup_expr='exact')
    # 月份过滤
    month = django_filters.DateFilter(field_name='pub_date__month', lookup_expr='exact')
    # 天过滤
    day = django_filters.DateFilter(field_name='pub_date__day', lookup_expr='exact')
    # 工单编号
    ticketNumber = django_filters.CharFilter(field_name='ticket_number')
    # 架构域模糊匹配
    domain__contains = django_filters.CharFilter(field_name='domain', lookup_expr='contains')
    # 查询bug
    is_bug = django_filters.CharFilter(field_name='bug_state', lookup_expr='exact')
    # bug原因是否排除空
    bug_reason_isnull = django_filters.BooleanFilter(field_name='bug_reason', lookup_expr='isnull')
    # 架构域是否排除空
    domain_isnull = django_filters.BooleanFilter(field_name='domain', lookup_expr='isnull')
    # 技术归属是否排除空
    technical_isnull = django_filters.BooleanFilter(field_name='technical', lookup_expr='isnull')

    class Meta:
        model = Orders
        # fields = ['ticketNumber', 'category', 'severity', 'start', 'end']
        fields = '__all__'


class ZtBugFilter(django_filters.rest_framework.FilterSet):
    # 定义filter支持的类型【精确等于（忽略大小写），包含（忽略大小写）， 大于，大于等于，小于，小于等于，以...开头，
    # 以...结尾，在..范围内，日期字段的年份，日期的月，日期的日，是否为空】
    # ['exact', 'contains', 'gt', 'gte', 'lt', 'lte', 'startswith',
    #                       'endswith', 'range', 'year', 'month', 'day', 'isnull']

    class Meta:
        model = ZtBug
        fields = '__all__'


class TesterFilter(django_filters.rest_framework.FilterSet):
    # 定义filter支持的类型【精确等于（忽略大小写），包含（忽略大小写）， 大于，大于等于，小于，小于等于，以...开头，
    # 以...结尾，在..范围内，日期字段的年份，日期的月，日期的日，是否为空】
    # ['exact', 'contains', 'gt', 'gte', 'lt', 'lte', 'startswith',
    #                       'endswith', 'range', 'year', 'month', 'day', 'isnull']

    class Meta:
        model = TesterZtBug
        fields = '__all__'


class DeveloperFilter(django_filters.rest_framework.FilterSet):
    # 定义filter支持的类型【精确等于（忽略大小写），包含（忽略大小写）， 大于，大于等于，小于，小于等于，以...开头，
    # 以...结尾，在..范围内，日期字段的年份，日期的月，日期的日，是否为空】
    # ['exact', 'contains', 'gt', 'gte', 'lt', 'lte', 'startswith',
    #                       'endswith', 'range', 'year', 'month', 'day', 'isnull']

    class Meta:
        model = DeveloperZtBug
        fields = '__all__'
