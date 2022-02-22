# --------------------------------------
# Date: 2021/8/5
# @Author: Steven_Tang
# FileName: serializers.py   
# Description: 工单详情序列化
# --------------------------------------


from rest_framework import serializers

from .models import Orders, ZtBug, TesterZtBug, DeveloperZtBug


class OrdersSerializer(serializers.ModelSerializer):
    # 设置必填项
    # team = serializers.CharField(required=True)
    category = serializers.CharField(required=True)

    class Meta:
        model = Orders
        extra_kwargs = {
            'severity': {'allow_blank': True},
            'bug_reason': {'allow_blank': True},
            'solution': {'allow_blank': True},
            'module': {'allow_blank': True},
        }
        fields = '__all__'


class ZtBugSerializer(serializers.ModelSerializer):
    # 设置必填项
    # 关联序列化

    class Meta:
        model = ZtBug
        fields = '__all__'


class TesterSerializer(serializers.ModelSerializer):
    # 设置必填项
    # 关联序列化
    zt_bug = ZtBugSerializer(many=True)

    class Meta:
        model = TesterZtBug
        fields = '__all__'


class DeveloperSerializer(serializers.ModelSerializer):
    # 设置必填项
    # category = serializers.CharField(required=True)
    # 关联序列化
    zt_bug = ZtBugSerializer(many=True)

    class Meta:
        model = DeveloperZtBug
        fields = '__all__'


class ZtBugNewSerializer(serializers.ModelSerializer):
    # 设置必填项
    # 关联序列化
    tester = TesterSerializer(many=True)
    developer = DeveloperSerializer(many=True)

    class Meta:
        model = ZtBug
        fields = '__all__'
