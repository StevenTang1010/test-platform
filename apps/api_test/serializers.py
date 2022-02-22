#!/usr/bin/python
# -*- coding:utf-8 _*- 
"""
@author:TXU
@file:serializers.py
@time:2021/08/23
@email:tao.xu2008@outlook.com
@description:
"""
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_bulk import BulkSerializerMixin, BulkListSerializer
from rest_framework.authtoken.models import Token

from apps.api_test.models import Department, Project, ProjectDynamic, ProjectMember, \
    AppSetting, GlobalEnv, GlobalConst, GlobalHeader, GlobalResponseValidate, \
    ApiGroup, ApiInfo, ApiUpdateHistory, YApiEvent, GlobalLabel, \
    TestSuite, TestCase, TestStep, TestReport, TestTask, TestEnvMonitor


class TokenSerializer(serializers.ModelSerializer):
    """
    用户信息序列化
    """
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    phone = serializers.CharField(source="user.user.phone")
    email = serializers.CharField(source="user.email")
    date_joined = serializers.CharField(source="user.date_joined")

    class Meta:
        model = Token
        # fields = '__all__'
        fields = ('first_name', 'last_name', 'phone', 'email', 'key', 'date_joined')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')


class DepartmentSerializer(serializers.ModelSerializer):
    """
    部门信息序列化
    """
    class Meta:
        model = Department
        fields = '__all__'


class DepartmentDeserializer(BulkSerializerMixin, serializers.ModelSerializer):
    """
    部门信息反序列化
    """
    class Meta:
        model = Department
        fields = '__all__'
        list_serializer_class = BulkListSerializer


class ProjectSerializer(serializers.ModelSerializer):
    """
    项目信息序列化
    """
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    update_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    creator = UserSerializer()
    updater = UserSerializer()
    department = DepartmentSerializer()

    class Meta:
        model = Project
        fields = '__all__'


class ProjectDetailSerializer(serializers.ModelSerializer):
    """
    项目信息序列化
    """
    toUpdateApiCount = serializers.SerializerMethodField()
    toVerifyApiCount = serializers.SerializerMethodField()
    updatedApiCount = serializers.SerializerMethodField()
    apiCount = serializers.SerializerMethodField()
    apiNoCaseCount = serializers.SerializerMethodField()
    apiCoverage = serializers.SerializerMethodField()
    apiPassRate = serializers.SerializerMethodField()
    stepCount = serializers.SerializerMethodField()
    dynamicCount = serializers.SerializerMethodField()
    memberCount = serializers.SerializerMethodField()
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    update_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    creator = UserSerializer()
    updater = UserSerializer()
    department = DepartmentSerializer()

    class Meta:
        model = Project
        fields = ('id', 'name', 'version', 'department',
                  'create_time', 'update_time', 'delete_time', 'is_delete', 'status', 'description',
                  'creator', 'updater', 'apiCount', 'apiNoCaseCount', 'apiCoverage', 'stepCount',
                  'apiPassRate', 'toUpdateApiCount', 'toVerifyApiCount', 'updatedApiCount',
                  'dynamicCount', 'memberCount')

    def get_apiCount(self, obj):
        return obj.api_project.filter(status__exact=True).count()

    def get_apiNoCaseCount(self, obj):
        api_no_case_count = 0
        for api in obj.api_project.filter(status__exact=True):
            steps = api.step_api.filter(status__exact=True)
            if steps.count() == 0:
                # 接口无测试步骤
                api_no_case_count += 1
        return api_no_case_count

    def get_apiPassCount(self, obj):
        api_pass_count = 0
        for api in obj.api_project.filter(status__exact=True):
            steps = api.step_api.filter(status__exact=True)
            if steps.count() == 0:
                # 接口无测试步骤
                continue
            fail_steps = steps.exclude(result__exact='passed')
            if fail_steps.count() == 0:
                # 步骤全部通过
                api_pass_count += 1
        return api_pass_count

    def get_apiPassRate(self, obj):
        api_count = self.get_apiCount(obj)
        if api_count == 0:
            return 1
        pass_count = self.get_apiPassCount(obj)
        return round(pass_count / api_count, 3)

    def get_apiCoverage(self, obj):
        api_count = obj.api_project.filter(status__exact=True).count()
        if api_count == 0:
            return 1

        api_count_with_case = 0
        for api in obj.api_project.filter(status__exact=True):
            if api.step_api.filter(status__exact=True).count() > 0:
                api_count_with_case += 1
        return round(api_count_with_case/api_count, 3)

    def get_toUpdateApiCount(self, obj):
        to_update_api_count = 0
        for api in obj.api_project.filter(status__exact=True):
            updates = api.update_api.filter(api__id__exact=api.id)
            update_status_list = [u.update_status for u in updates]
            if update_status_list and min(update_status_list) == 0:
                to_update_api_count += 1
        return to_update_api_count
        # return obj.api_project.filter(update_status__exact=0, status__exact=True).count()

    def get_toVerifyApiCount(self, obj):
        to_verify_api_count = 0
        for api in obj.api_project.filter(status__exact=True):
            updates = api.update_api.filter(api__id__exact=api.id)
            update_status_list = [u.update_status for u in updates]
            if update_status_list and min(update_status_list) == 1:
                to_verify_api_count += 1
        return to_verify_api_count
        # return obj.api_project.filter(update_status__exact=1, status__exact=True).count()

    def get_updatedApiCount(self, obj):
        updated_api_count = 0
        for api in obj.api_project.filter(status__exact=True):
            updates = api.update_api.filter(api__id__exact=api.id)
            update_status_list = [u.update_status for u in updates]
            if not update_status_list or min(update_status_list) == 2:
                updated_api_count += 1
        return updated_api_count
        # return obj.api_project.filter(update_status__exact=2, status__exact=True).count()

    def get_stepCount(self, obj):
        # return obj.case_project.filter(status__exact=True).count()
        case_count = 0
        for api in obj.api_project.filter(status__exact=True):
            case_count += api.step_api.filter(status__exact=True).count()
        return case_count

    def get_dynamicCount(self, obj):
        return obj.dynamic_project.all().count()

    def get_memberCount(self, obj):
        return obj.member_project.all().count()


class ProjectDeserializer(BulkSerializerMixin, serializers.ModelSerializer):
    """
    项目信息反序列化
    """
    class Meta:
        model = Project
        fields = '__all__'
        list_serializer_class = BulkListSerializer


class ProjectDynamicDeserializer(serializers.ModelSerializer):
    """
    项目动态信息反序列化
    """
    class Meta:
        model = ProjectDynamic
        fields = ('id', 'project', 'time', 'type', 'operationObject', 'user', 'description')


class ProjectDynamicSerializer(serializers.ModelSerializer):
    """
    项目动态信息序列化
    """
    operationUser = serializers.CharField(source='user.first_name')
    time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = ProjectDynamic
        fields = ('id', 'time', 'type', 'operationObject', 'operationUser', 'description')


class ProjectMemberDeserializer(serializers.ModelSerializer):
    """
    项目成员信息反序列化
    """
    class Meta:
        model = ProjectMember
        fields = ('id', 'role', 'status', 'project', 'user')


class ProjectMemberSerializer(serializers.ModelSerializer):
    """
    项目成员信息序列化
    """
    user = UserSerializer(read_only=True)

    class Meta:
        model = ProjectMember
        fields = ('id', 'role', 'status', 'project', 'user')


class AppSettingSerializer(serializers.ModelSerializer):
    """
    env信息序列化
    """
    data = serializers.JSONField()

    class Meta:
        model = AppSetting
        fields = '__all__'


class GlobalEnvSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    """
    env信息序列化
    """
    config = serializers.JSONField()
    data = serializers.JSONField()
    mock = serializers.JSONField()

    class Meta:
        model = GlobalEnv
        fields = '__all__'
        list_serializer_class = BulkListSerializer


class GlobalConstSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    """
    global const信息序列化
    """

    class Meta:
        model = GlobalConst
        fields = '__all__'
        list_serializer_class = BulkListSerializer


class GlobalHeaderSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    """
    global const信息序列化
    """

    class Meta:
        model = GlobalHeader
        fields = '__all__'
        list_serializer_class = BulkListSerializer


class GlobalResponseValidateSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    """
    GlobalResponseValidate信息序列化
    """

    class Meta:
        model = GlobalResponseValidate
        fields = '__all__'
        list_serializer_class = BulkListSerializer


class GlobalLabelSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    """
    标签 信息序列化
    """
    type_name = serializers.SerializerMethodField()

    class Meta:
        model = GlobalLabel
        fields = ('id', 'name', 'type', 'type_name', 'status', 'description')
        list_serializer_class = BulkListSerializer

    def get_type_name(self, obj):
        return obj.get_type_display()


class ApiGroupSerializer(serializers.ModelSerializer):
    """
    接口一级分组信息序列化
    """
    project = ProjectSerializer()

    class Meta:
        model = ApiGroup
        fields = ('id', 'name', 'project',
                  'create_time', 'update_time', 'delete_time', 'is_delete', 'status', 'description')


class ApiGroupDeserializer(BulkSerializerMixin, serializers.ModelSerializer):
    """
    接口一级分组信息反序列化
    """
    class Meta:
        model = ApiGroup
        fields = '__all__'
        list_serializer_class = BulkListSerializer


class ApiInfoSerializer(serializers.ModelSerializer):
    """
    接口详细信息序列化
    """
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    update_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    creator = UserSerializer()
    updater = UserSerializer()
    project = ProjectSerializer()
    api_group = ApiGroupSerializer()
    labels = GlobalLabelSerializer(many=True, read_only=True)
    update_status_name = serializers.SerializerMethodField()
    test_case_count = serializers.SerializerMethodField()

    class Meta:
        model = ApiInfo
        fields = ('id', 'yapi_id', 'project', 'api_group', 'origin', 'name', 'http_type', 'method', 'path', 'host_tag',
                  'yapi_req_headers', 'yapi_req_params', 'yapi_req_query', 'yapi_req_body_form', 'yapi_req_body_other', 'yapi_res_body',
                  'req_headers', 'req_params', 'req_json', 'req_data', 'validator', 'update_status', 'labels',
                  'create_time', 'update_time', 'delete_time', 'is_delete', 'status', 'description',
                  'creator', 'updater', 'update_status_name', 'test_case_count')

    def get_update_status_name(self, obj):
        return obj.get_update_status_display()

    def get_test_case_count(self, obj):
        return obj.step_api.all().count()


class ApiInfoCountSerializer(serializers.ModelSerializer):
    """接口统计信息序列化"""
    api_count = serializers.SerializerMethodField()
    toUpdateApiCount = serializers.SerializerMethodField()
    toVerifyApiCount = serializers.SerializerMethodField()
    updatedApiCount = serializers.SerializerMethodField()


class ApiInfoDeserializer(BulkSerializerMixin, serializers.ModelSerializer):
    """
    接口详细信息序列化
    """
    class Meta:
        model = ApiInfo
        fields = '__all__'
        list_serializer_class = BulkListSerializer


class ApiUpdateHistorySerializer(serializers.ModelSerializer):
    """
    接口变更历史信息序列化
    """
    update_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    update_status_name = serializers.SerializerMethodField()

    class Meta:
        model = ApiUpdateHistory
        fields = ('id', 'api', 'event', 'content', 'updater', 'update_time', 'update_status', 'update_status_name')

    def get_update_status_name(self, obj):
        return obj.get_update_status_display()


class ApiUpdateHistoryDeserializer(serializers.ModelSerializer):
    """
    接口变更历史信息反序列化
    """
    class Meta:
        model = ApiUpdateHistory
        fields = ('id', 'api', 'event', 'content', 'updater', 'update_time', 'update_status')


class YApiEventSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    """
    YAPI变更事件信息序列化
    """
    update_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = YApiEvent
        fields = '__all__'
        list_serializer_class = BulkListSerializer


class TestSuiteSerializer(serializers.ModelSerializer):
    """
    测试用例集 信息序列化
    """
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    update_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    creator = UserSerializer()
    updater = UserSerializer()
    labels = GlobalLabelSerializer(many=True, read_only=True)
    department = DepartmentSerializer()

    class Meta:
        model = TestSuite
        fields = '__all__'


class TestSuiteDeserializer(BulkSerializerMixin, serializers.ModelSerializer):
    """
    测试用例集 信息序列化
    """

    class Meta:
        model = TestSuite
        fields = '__all__'
        list_serializer_class = BulkListSerializer


class TestCaseSerializer(serializers.ModelSerializer):
    """
    测试用例 信息序列化
    """
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    update_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    creator = UserSerializer()
    updater = UserSerializer()
    test_suite = TestSuiteSerializer()
    labels = GlobalLabelSerializer(many=True, read_only=True)

    class Meta:
        model = TestCase
        fields = '__all__'


class TestCaseDeserializer(BulkSerializerMixin, serializers.ModelSerializer):
    """
    用例信息反序列化
    """
    class Meta:
        model = TestCase
        fields = '__all__'
        list_serializer_class = BulkListSerializer


class TestStepBaseSerializer(serializers.ModelSerializer):
    """
    测试用例步骤 信息序列化
    """
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    update_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    creator = UserSerializer()
    updater = UserSerializer()
    test_case = TestCaseSerializer()
    apiInfo = ApiInfoSerializer()
    labels = GlobalLabelSerializer(many=True, read_only=True)

    class Meta:
        model = TestStep
        fields = '__all__'


class TestStepDeserializer(BulkSerializerMixin, serializers.ModelSerializer):
    """
    用例步骤信息反序列化
    """
    class Meta:
        model = TestStep
        fields = '__all__'
        list_serializer_class = BulkListSerializer


class TestStepSerializer(TestStepBaseSerializer):
    depends = TestStepDeserializer(many=True, read_only=True)


class TestReportSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    """
    测试结果 信息序列化
    """
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    env = GlobalEnvSerializer()

    class Meta:
        model = TestReport
        fields = '__all__'
        list_serializer_class = BulkListSerializer


class TestReportDeserializer(BulkSerializerMixin, serializers.ModelSerializer):
    """
    测试结果 反信息序列化
    """
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = TestReport
        fields = '__all__'
        list_serializer_class = BulkListSerializer


class TestTaskSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    """
    测试任务 信息序列化
    """
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    test_env = GlobalEnvSerializer()
    test_validate = GlobalResponseValidateSerializer(read_only=True)

    class Meta:
        model = TestTask
        fields = '__all__'
        list_serializer_class = BulkListSerializer


class TestTaskDeserializer(BulkSerializerMixin, serializers.ModelSerializer):
    """
    测试任务 信息序列化
    """
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = TestTask
        fields = '__all__'
        list_serializer_class = BulkListSerializer


class TestEnvMonitorSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    """
    测试环境验证、状态监控 信息序列化
    """
    env = GlobalEnvSerializer()
    validate = GlobalResponseValidateSerializer()
    report = TestReportSerializer()

    class Meta:
        model = TestEnvMonitor
        fields = '__all__'
        list_serializer_class = BulkListSerializer


class TestEnvMonitorDeserializer(BulkSerializerMixin, serializers.ModelSerializer):
    """
    测试环境验证、状态监控 反信息序列化
    """
    class Meta:
        model = TestEnvMonitor
        fields = '__all__'
        list_serializer_class = BulkListSerializer


if __name__ == '__main__':
    pass
