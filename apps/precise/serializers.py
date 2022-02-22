# --------------------------------------
# Date: 2021/8/21
# @Author: Steven_Tang
# FileName: serializers.py
# Description: 精准内容序列化
# --------------------------------------


from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from .models import *


# 用例表序列化
class TestCaseSerializer(ModelSerializer):
    class Meta:
        model = TestCase
        fields = '__all__'


# 功能关联表序列化
class FunctionalRelevanceSerializer(ModelSerializer):
    class Meta:
        model = FunctionalRelevance
        fields = ['direct_func', 'indirect_impact_func']


# 功能表序列化
class ModuleFunctionSerializer(ModelSerializer):
    class Meta:
        model = ModuleFunction
        fields = ['module_function_id', 'module_function_name']


# 三级模块表序列化
class ThirdSerializer(ModelSerializer):
    class Meta:
        model = ThirdModule
        fields = ['third_module_id', 'third_module_name']


# 二级模块序列化
class SecondarySerializer(ModelSerializer):

    class Meta:
        model = SecondaryModule
        fields = ['secondary_module_id', 'secondary_module_name']


# 一级模块序列化
class PrimarySerializer(ModelSerializer):
    class Meta:
        model = PrimaryModule
        fields = ['primary_module_id', 'primary_module_name']


# 系统表序列化
class SystemSerializer(ModelSerializer):
    class Meta:
        model = System
        fields = ['system_id', 'system_name']
