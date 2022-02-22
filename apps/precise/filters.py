# --------------------------------------
# Date: 2021/8/21
# @Author: Steven_Tang
# FileName: filters.py   
# Description: 精准自定义过滤
# --------------------------------------


import django_filters
# from django.db.models import Q

from .models import *


class PrimaryModuleFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = PrimaryModule
        fields = ['system']


class SecondaryModuleFilter(django_filters.rest_framework.FilterSet):
    primary = django_filters.CharFilter(field_name='primary_module', lookup_expr='exact')

    class Meta:
        model = SecondaryModule
        fields = ['primary']


class ThirdModuleFilter(django_filters.rest_framework.FilterSet):
    second = django_filters.CharFilter(field_name='secondary_module', lookup_expr='exact')

    class Meta:
        model = ThirdModule
        fields = ['second']


class ModuleFunctionFilter(django_filters.rest_framework.FilterSet):
    third = django_filters.CharFilter(field_name='third_modle', lookup_expr='exact')

    class Meta:
        model = ModuleFunction
        fields = ['third']


class FunctionalRelevanceFilter(django_filters.rest_framework.FilterSet):
    direct = django_filters.CharFilter(field_name='direct_func', lookup_expr='exact')
    indirect = django_filters.CharFilter(field_name='indirect_impact_func', lookup_expr='exact')

    class Meta:
        model = FunctionalRelevance
        fields = ['direct', 'indirect']
