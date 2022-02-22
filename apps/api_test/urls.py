#!/usr/bin/python
# -*- coding:utf-8 _*- 
"""
@author:TXU
@file:urls.py
@time:2021/08/23
@email:tao.xu2008@outlook.com
@description:
"""

from django.conf.urls import url
from django.urls import path, include
# from rest_framework.routers import DefaultRouter
from rest_framework_bulk.routes import BulkRouter
from apps.api_test.view_set.story.department import DepartmentViewSet
from apps.api_test.view_set.story.project import ProjectViewSet
from apps.api_test.view_set.story.project_member import ProjectMemberViewSet
from apps.api_test.view_set.global_config.app_setting import AppSettingViewSet, GetDefaultAppSettingView
from apps.api_test.view_set.global_config.global_env import GlobalEnvViewSet, EnvDataViewSet, \
    GetEnvDefaultConfigView, GetEnvDefaultQWExternalContactConfigView
from apps.api_test.view_set.global_config.global_header import GlobalHeaderViewSet
from apps.api_test.view_set.global_config.global_const import GlobalConstViewSet
from apps.api_test.view_set.global_config.global_label import GlobalLabelViewSet
from apps.api_test.view_set.global_config.global_response_validate import GlobalResponseValidateViewSet
from apps.api_test.view_set.api_view.api_info import ApiInfoViewSet, NoCaseApiInfoViewSet, ToDoApiInfoViewSet, \
    ApiTotalViewSet, ApiCountViewSet, NoCaseApiCountViewSet, WithCaseApiCountViewSet, ToDoApiCountViewSet
from apps.api_test.view_set.api_view.api_update_history import ApiUpdateHistoryViewSet, \
    ApiSyncUpdateStatusToHistoryViewSet
from apps.api_test.view_set.api_view.api_group import ApiGroupViewSet
from apps.api_test.view_set.api_view.yapi_event import YApiEventViewSet
from apps.api_test.view_set.update.yapi import YAPIEventMonitorView, YAPIEventDataSyncView, \
    APIDataSyncView, APICaseTemplateUpdateView
from apps.api_test.view_set.test_view.test_suite import TestSuiteViewSet, TestSuiteCountViewSet, TestSuiteTotalViewSet
from apps.api_test.view_set.test_view.test_case import TestCaseViewSet, TestCaseCountViewSet, TestCaseTotalViewSet
from apps.api_test.view_set.test_view.test_step import TestStepViewSet, TestStepCountViewSet, TestStepTotalViewSet
from apps.api_test.view_set.test_view.test_report import TestReportViewSet, PytestHtmlViewSet, JenkinsAllureViewSet, \
    TestLogsViewSet
from apps.api_test.view_set.test_view.test_env_monitor import TestEnvMonitorViewSet
from apps.api_test.view_set.task.test_task import TestTaskViewSet
from apps.api_test.view_set.upload.case_upload import UploadFileView

from apps.api_test.view_set.help.comparators import ComparatorHelpViewSet
from apps.api_test.view_set.help.functions import BuiltinFunctionHelpViewSet, CustomizedCallBackFunctionHelpViewSet, \
    CustomizedMallFunctionHelpViewSet, CustomizedSettingsFunctionHelpViewSet

from apps.api_test.view_set.runner.run import TestRunViewSet

# router = DefaultRouter()
router = BulkRouter()

# department
router.register(r'department/bulk', DepartmentViewSet),  # 批量处理
router.register(r'department/list', DepartmentViewSet, basename='list'),
router.register(r'department/detail', DepartmentViewSet, basename='retrieve'),
router.register(r'department/add', DepartmentViewSet, basename='create'),
router.register(r'department/update', DepartmentViewSet, basename='update'),
router.register(r'department/del', DepartmentViewSet, basename='destroy')

# project
router.register(r'project/bulk', ProjectViewSet),  # 批量处理
router.register(r'project/list', ProjectViewSet, basename='list'),
router.register(r'project/detail', ProjectViewSet, basename='retrieve'),
router.register(r'project/add', ProjectViewSet, basename='create'),
router.register(r'project/update', ProjectViewSet, basename='update'),
router.register(r'project/del', ProjectViewSet, basename='destroy')

# project member
router.register(r'project/member/list', ProjectMemberViewSet, basename='list'),
router.register(r'project/member/detail', ProjectMemberViewSet, basename='retrieve'),
router.register(r'project/member/add', ProjectMemberViewSet, basename='create'),
router.register(r'project/member/update', ProjectMemberViewSet, basename='update'),
router.register(r'project/member/del', ProjectMemberViewSet, basename='destroy')

# app系统配置
router.register(r'global/app_setting/list', AppSettingViewSet, basename='list'),
router.register(r'global/app_setting/detail', AppSettingViewSet, basename='retrieve'),
router.register(r'global/app_setting/add', AppSettingViewSet, basename='create'),
router.register(r'global/app_setting/update', AppSettingViewSet, basename='update'),
router.register(r'global/app_setting/del', AppSettingViewSet, basename='destroy'),
router.register(r'global/app_setting/data', GetDefaultAppSettingView, basename='retrieve'),

# global env 环境配置
router.register(r'global/env/bulk', GlobalEnvViewSet),
router.register(r'global/env/list', GlobalEnvViewSet, basename='list'),
router.register(r'global/env/detail', GlobalEnvViewSet, basename='retrieve'),
router.register(r'global/env/add', GlobalEnvViewSet, basename='create'),
router.register(r'global/env/update', GlobalEnvViewSet, basename='update'),
router.register(r'global/env/del', GlobalEnvViewSet, basename='destroy'),
router.register(r'global/env/data', EnvDataViewSet, basename='retrieve'),

# global header
router.register(r'global/header/bulk', GlobalHeaderViewSet),
router.register(r'global/header/list', GlobalHeaderViewSet, basename='list'),
router.register(r'global/header/detail', GlobalHeaderViewSet, basename='retrieve'),
router.register(r'global/header/add', GlobalHeaderViewSet, basename='create'),
router.register(r'global/header/update', GlobalHeaderViewSet, basename='update'),
router.register(r'global/header/del', GlobalHeaderViewSet, basename='destroy'),

# global const
router.register(r'global/const/bulk', GlobalConstViewSet),
router.register(r'global/const/list', GlobalConstViewSet, basename='list'),
router.register(r'global/const/detail', GlobalConstViewSet, basename='retrieve'),
router.register(r'global/const/add', GlobalConstViewSet, basename='create'),
router.register(r'global/const/update', GlobalConstViewSet, basename='update'),
router.register(r'global/const/del', GlobalConstViewSet, basename='destroy'),

# global label
router.register(r'global/label/bulk', GlobalLabelViewSet),
router.register(r'global/label/list', GlobalLabelViewSet, basename='list'),
router.register(r'global/label/detail', GlobalLabelViewSet, basename='retrieve'),
router.register(r'global/label/add', GlobalLabelViewSet, basename='create'),
router.register(r'global/label/update', GlobalLabelViewSet, basename='update'),
router.register(r'global/label/del', GlobalLabelViewSet, basename='destroy'),

# global response_validate
router.register(r'global/response_validate/bulk', GlobalResponseValidateViewSet),
router.register(r'global/response_validate/list', GlobalResponseValidateViewSet, basename='list'),
router.register(r'global/response_validate/detail', GlobalResponseValidateViewSet, basename='retrieve'),
router.register(r'global/response_validate/add', GlobalResponseValidateViewSet, basename='create'),
router.register(r'global/response_validate/update', GlobalResponseValidateViewSet, basename='update'),
router.register(r'global/response_validate/del', GlobalResponseValidateViewSet, basename='destroy'),

# api group
router.register(r'api/group/bulk', ApiGroupViewSet),
router.register(r'api/group/list', ApiGroupViewSet, basename='list'),
router.register(r'api/group/detail', ApiGroupViewSet, basename='retrieve'),
router.register(r'api/group/add', ApiGroupViewSet, basename='create'),
router.register(r'api/group/update', ApiGroupViewSet, basename='update'),
router.register(r'api/group/del', ApiGroupViewSet, basename='destroy'),

# api info
router.register(r'api/bulk', ApiInfoViewSet),
router.register(r'api/list', ApiInfoViewSet, basename='list'),
router.register(r'api/nocase/list', NoCaseApiInfoViewSet, basename='no_case_list'),
router.register(r'api/todo/list', ToDoApiInfoViewSet, basename='todo_list'),
router.register(r'api/detail', ApiInfoViewSet, basename='retrieve'),
router.register(r'api/add', ApiInfoViewSet, basename='create'),
router.register(r'api/update', ApiInfoViewSet, basename='update'),
router.register(r'api/del', ApiInfoViewSet, basename='destroy'),
router.register(r'api/total', ApiTotalViewSet, basename='list'),
router.register(r'api/count', ApiCountViewSet, basename='list'),
router.register(r'api/count/no_case', NoCaseApiCountViewSet, basename='list'),
router.register(r'api/count/with_case', WithCaseApiCountViewSet, basename='list'),
router.register(r'api/count/todo', ToDoApiCountViewSet, basename='list'),

# api update history
router.register(r'api/update_history/list', ApiUpdateHistoryViewSet, basename='list'),
router.register(r'api/update_history/detail', ApiUpdateHistoryViewSet, basename='retrieve'),
router.register(r'api/update_history/add', ApiUpdateHistoryViewSet, basename='create'),
router.register(r'api/update_history/update', ApiUpdateHistoryViewSet, basename='update'),
router.register(r'api/update_history/del', ApiUpdateHistoryViewSet, basename='destroy'),

# yapi event
router.register(r'api/yapi_event/bulk', YApiEventViewSet),
router.register(r'api/yapi_event/list', YApiEventViewSet, basename='list'),
router.register(r'api/yapi_event/detail', YApiEventViewSet, basename='retrieve'),
# router.register(r'api/yapi_event/add', YApiEventViewSet, basename='create'),  # YAPIEventMonitorView 调用
router.register(r'api/yapi_event/update', YApiEventViewSet, basename='update'),
router.register(r'api/yapi_event/del', YApiEventViewSet, basename='destroy'),

# test suite
router.register(r'test/suite/bulk', TestSuiteViewSet),  # 批量处理
router.register(r'test/suite/list', TestSuiteViewSet, basename='list'),
router.register(r'test/suite/detail', TestSuiteViewSet, basename='detail'),
router.register(r'test/suite/add', TestSuiteViewSet, basename='create'),
router.register(r'test/suite/update', TestSuiteViewSet, basename='update'),
router.register(r'test/suite/del', TestSuiteViewSet, basename='destroy'),
router.register(r'test/suite/total', TestSuiteTotalViewSet, basename='list'),
router.register(r'test/suite/count', TestSuiteCountViewSet, basename='list'),

# test case
router.register(r'test/case/bulk', TestCaseViewSet),  # 批量处理
router.register(r'test/case/list', TestCaseViewSet, basename='list'),
router.register(r'test/case/detail', TestCaseViewSet, basename='retrieve'),
router.register(r'test/case/add', TestCaseViewSet, basename='create'),
router.register(r'test/case/update', TestCaseViewSet, basename='update'),
router.register(r'test/case/del', TestCaseViewSet, basename='destroy'),
router.register(r'test/case/total', TestCaseTotalViewSet, basename='list'),
router.register(r'test/case/count', TestCaseCountViewSet, basename='list'),

# test step
router.register(r'test/step/bulk', TestStepViewSet),  # 批量处理
router.register(r'test/step/list', TestStepViewSet, basename='list'),
router.register(r'test/step/detail', TestStepViewSet, basename='retrieve'),
router.register(r'test/step/add', TestStepViewSet, basename='create'),
router.register(r'test/step/update', TestStepViewSet, basename='update'),
router.register(r'test/step/del', TestStepViewSet, basename='destroy'),
router.register(r'test/step/total', TestStepTotalViewSet, basename='list'),
router.register(r'test/step/count', TestStepCountViewSet, basename='list'),

# 测试执行
router.register(r'test/run', TestRunViewSet, basename='create'),

# 测试报告
router.register(r'test/report/bulk', TestReportViewSet),  # 批量处理
router.register(r'test/report/list', TestReportViewSet, basename='list'),
router.register(r'test/report/detail', TestReportViewSet, basename='retrieve'),
router.register(r'test/report/update', TestReportViewSet, basename='update'),
router.register(r'test/report/pytest_html', PytestHtmlViewSet, basename='retrieve'),
router.register(r'test/report/jenkins_allure', JenkinsAllureViewSet, basename='retrieve'),
router.register(r'test/report/logs', TestLogsViewSet, basename='retrieve'),

# 测试环境验证、状态监控
router.register(r'test/env_monitor/bulk', TestEnvMonitorViewSet),  # 批量处理
router.register(r'test/env_monitor/list', TestEnvMonitorViewSet, basename='list'),
router.register(r'test/env_monitor/detail', TestEnvMonitorViewSet, basename='retrieve'),
router.register(r'test/env_monitor/add', TestEnvMonitorViewSet, basename='create'),
router.register(r'test/env_monitor/update', TestEnvMonitorViewSet, basename='update'),
router.register(r'test/env_monitor/del', TestEnvMonitorViewSet, basename='destroy'),

# 测试任务
# router.register(r'test/task/bulk', TestTaskViewSet),  # 批量处理 - 暂不支持
router.register(r'test/task/add', TestTaskViewSet, basename='create'),
router.register(r'test/task/update', TestTaskViewSet, basename='update'),
router.register(r'test/task/del', TestTaskViewSet, basename='destroy'),
router.register(r'test/task/list', TestTaskViewSet, basename='list'),
router.register(r'test/task/detail', TestTaskViewSet, basename='retrieve'),

# 帮助信息
router.register(r'help/comparator/list', ComparatorHelpViewSet, basename='list'),
router.register(r'help/builtin_functions/list', BuiltinFunctionHelpViewSet, basename='list')
router.register(r'help/callback_functions/list', CustomizedCallBackFunctionHelpViewSet, basename='list')
router.register(r'help/mall_functions/list', CustomizedMallFunctionHelpViewSet, basename='list')
router.register(r'help/settings_functions/list', CustomizedSettingsFunctionHelpViewSet, basename='list')

urlpatterns = [
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # 数据表管理
    path('', include(router.urls)),

    # file xmind
    url(r"file/upload", UploadFileView.as_view()),
    # 获取env默认数据
    url(r'global/env/config/default', GetEnvDefaultConfigView.as_view()),
    url(r'global/env/qw_external_contact_config/default', GetEnvDefaultQWExternalContactConfigView.as_view()),
    # YAPI事件监听
    url(r'api/yapi_event/add', YAPIEventMonitorView.as_view()),
    # YAPI事件数据同步到本地接口
    url(r'api/yapi_event/data_sync', YAPIEventDataSyncView.as_view()),
    # 本地接口拉取YAPI数据同步
    url(r'api/data_sync', APIDataSyncView.as_view()),
    # 本地接口用例模板更新
    url(r'api/update/case_template', APICaseTemplateUpdateView.as_view()),
    # 接口update_status同步到接口变更历史表
    url(r'api/sync/update_history/update_status', ApiSyncUpdateStatusToHistoryViewSet.as_view()),
]


if __name__ == '__main__':
    pass
