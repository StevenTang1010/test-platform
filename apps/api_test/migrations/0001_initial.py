# Generated by Django 3.2.5 on 2022-01-27 02:09

import apps.api_test.models
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import re


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ApiGroup',
            fields=[
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')),
                ('delete_time', models.DateTimeField(default=None, null=True, verbose_name='删除时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否已删除')),
                ('status', models.BooleanField(default=True, verbose_name='状态（1正常 0停用）')),
                ('description', models.CharField(blank=True, max_length=4096, null=True, verbose_name='描述')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50, verbose_name='接口分组名称')),
            ],
            options={
                'verbose_name': '接口分组',
                'verbose_name_plural': '接口分组',
            },
        ),
        migrations.CreateModel(
            name='ApiInfo',
            fields=[
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')),
                ('delete_time', models.DateTimeField(default=None, null=True, verbose_name='删除时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否已删除')),
                ('status', models.BooleanField(default=True, verbose_name='状态（1正常 0停用）')),
                ('description', models.CharField(blank=True, max_length=4096, null=True, verbose_name='描述')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('yapi_id', models.IntegerField(default=0, verbose_name='YAPI接口ID')),
                ('origin', models.CharField(choices=[('yapi', 'yapi'), ('xmind', 'xmind'), ('excel', 'excel'), ('manual', 'manual')], default='manual', max_length=50, verbose_name='接口数据来源')),
                ('name', models.CharField(max_length=500, verbose_name='接口名称')),
                ('http_type', models.CharField(choices=[('HTTP', 'HTTP'), ('HTTPS', 'HTTPS')], default='HTTP', max_length=50, verbose_name='HTTP/HTTPS')),
                ('host_tag', models.CharField(choices=[('mk', '服务商后台地址'), ('qw', '企微端地址'), ('oss_bill', '运营计费地址'), ('oss_official', '运营官方地址'), ('qyapi', '企业微信API')], default='mk', max_length=30, verbose_name='指定host')),
                ('method', models.CharField(choices=[('POST', 'POST'), ('GET', 'GET'), ('PUT', 'PUT'), ('DELETE', 'DELETE'), ('CALL', 'CALL')], max_length=50, verbose_name='请求方式')),
                ('path', models.CharField(max_length=1024, verbose_name='接口地址')),
                ('yapi_req_headers', models.TextField(blank=True, null=True, verbose_name='yapi定义-请求头')),
                ('yapi_req_params', models.TextField(blank=True, null=True, verbose_name='yapi定义-请求参数-params')),
                ('yapi_req_query', models.TextField(blank=True, null=True, verbose_name='yapi定义-请求参数-query')),
                ('yapi_req_body_form', models.TextField(blank=True, null=True, verbose_name='yapi定义-请求参数-body_form')),
                ('yapi_req_body_other', models.TextField(blank=True, null=True, verbose_name='yapi定义-请求参数-body_other')),
                ('yapi_res_body', models.TextField(blank=True, null=True, verbose_name='yapi定义-响应body')),
                ('req_headers', models.TextField(blank=True, null=True, verbose_name='请求头')),
                ('req_params', models.TextField(blank=True, null=True, verbose_name='请求参数-params')),
                ('req_data', models.TextField(blank=True, null=True, verbose_name='请求参数-data')),
                ('req_json', models.TextField(blank=True, null=True, verbose_name='请求参数-json')),
                ('validator', models.TextField(blank=True, null=True, verbose_name='响应数据验证')),
                ('update_status', models.IntegerField(choices=[(0, '待处理'), (1, '待验证'), (2, '已处理')], default=1, verbose_name='更新状态')),
                ('api_group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='api_group', to='api_test.apigroup', verbose_name='接口分组')),
                ('creator', models.ForeignKey(max_length=20, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='api_info_creator', to=settings.AUTH_USER_MODEL, verbose_name='创建人')),
            ],
            options={
                'verbose_name': '接口',
                'verbose_name_plural': '接口管理',
            },
        ),
        migrations.CreateModel(
            name='AppSetting',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(default='app系统配置', max_length=50, null=True, verbose_name='Name')),
                ('data', models.JSONField(default=apps.api_test.models.default_app_setting, verbose_name='APP配置数据')),
                ('description', models.CharField(blank=True, max_length=1024, null=True, verbose_name='描述')),
                ('status', models.BooleanField(default=True, verbose_name='状态')),
            ],
            options={
                'verbose_name': 'app系统配置',
                'verbose_name_plural': 'app系统配置',
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')),
                ('delete_time', models.DateTimeField(default=None, null=True, verbose_name='删除时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否已删除')),
                ('status', models.BooleanField(default=True, verbose_name='状态（1正常 0停用）')),
                ('description', models.CharField(blank=True, max_length=4096, null=True, verbose_name='描述')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50, verbose_name='部门名称')),
                ('safe_name', models.SlugField(blank=True, default='', null=True, verbose_name='部门标识（用作文件夹名）')),
                ('leader', models.CharField(blank=True, default='', max_length=50, null=True, verbose_name='负责人')),
            ],
            options={
                'verbose_name': '部门',
                'verbose_name_plural': '部门',
            },
        ),
        migrations.CreateModel(
            name='GlobalConst',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('value', models.TextField(blank=True, null=True, verbose_name='Value')),
                ('description', models.CharField(blank=True, max_length=1024, null=True, verbose_name='描述')),
                ('status', models.BooleanField(default=True, verbose_name='状态')),
            ],
            options={
                'verbose_name': 'Const',
                'verbose_name_plural': '全局Const管理',
            },
        ),
        migrations.CreateModel(
            name='GlobalEnv',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50, verbose_name='名称')),
                ('config', models.JSONField(default=apps.api_test.models.default_env_config, verbose_name='环境基础配置')),
                ('qw_external_contact_config', models.JSONField(default=apps.api_test.models.default_qw_external_contact_config, verbose_name='企微客户联系配置')),
                ('data', models.JSONField(default=dict, verbose_name='环境数据')),
                ('mock', models.JSONField(default=dict, verbose_name='环境mock数据')),
                ('mock_dynamic', models.BooleanField(default=True, verbose_name='动态更新mock')),
                ('description', models.CharField(blank=True, max_length=1024, null=True, verbose_name='描述')),
                ('status', models.BooleanField(default=True, verbose_name='状态')),
                ('is_default', models.BooleanField(default=False, verbose_name='默认配置')),
            ],
            options={
                'verbose_name': '环境配置',
                'verbose_name_plural': '环境配置管理',
            },
        ),
        migrations.CreateModel(
            name='GlobalHeader',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=1024, verbose_name='名称')),
                ('value', models.TextField(blank=True, null=True, verbose_name='内容')),
                ('description', models.CharField(blank=True, max_length=1024, null=True, verbose_name='描述')),
                ('status', models.BooleanField(default=True, verbose_name='状态')),
            ],
            options={
                'verbose_name': '全局请求头',
                'verbose_name_plural': '全局请求头管理',
            },
        ),
        migrations.CreateModel(
            name='GlobalLabel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50, verbose_name='标签名')),
                ('type', models.CharField(choices=[('priority', '优先级'), ('severity', '严重等级'), ('function', '业务功能'), ('testsuite_type', '测试集类型'), ('other', '其他')], default='priority', max_length=20, verbose_name='标签类型')),
                ('status', models.BooleanField(default=True, verbose_name='状态')),
                ('description', models.CharField(blank=True, max_length=1024, null=True, verbose_name='描述')),
            ],
            options={
                'verbose_name': '标签',
                'verbose_name_plural': '标签管理',
            },
        ),
        migrations.CreateModel(
            name='GlobalResponseValidate',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(default='默认校验', max_length=1024, verbose_name='名称')),
                ('description', models.CharField(blank=True, max_length=1024, null=True, verbose_name='描述')),
                ('check_status_code', models.BooleanField(default=True, verbose_name='检查状态代码')),
                ('check_json_schema', models.BooleanField(default=True, verbose_name='检查json-schema')),
                ('check_response_data', models.BooleanField(default=True, verbose_name='检查响应数据')),
                ('status_code', models.CharField(default='200', max_length=500, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:,\\d+)*\\Z'), code='invalid', message='Enter only digits separated by commas.')], verbose_name='期望状态代码')),
                ('status', models.BooleanField(default=True, verbose_name='状态')),
                ('is_default', models.BooleanField(default=False, verbose_name='默认配置')),
            ],
            options={
                'verbose_name': '通用校验规则配置',
                'verbose_name_plural': '通用校验规则配置管理',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')),
                ('delete_time', models.DateTimeField(default=None, null=True, verbose_name='删除时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否已删除')),
                ('status', models.BooleanField(default=True, verbose_name='状态（1正常 0停用）')),
                ('description', models.CharField(blank=True, max_length=4096, null=True, verbose_name='描述')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50, verbose_name='项目名称')),
                ('version', models.CharField(max_length=50, null=True, verbose_name='版本')),
                ('creator', models.ForeignKey(max_length=20, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='project_creator', to=settings.AUTH_USER_MODEL, verbose_name='创建人')),
                ('department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api_test.department', verbose_name='部门')),
                ('updater', models.ForeignKey(max_length=20, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='project_updater', to=settings.AUTH_USER_MODEL, verbose_name='更新人')),
            ],
            options={
                'verbose_name': '项目',
                'verbose_name_plural': '项目',
            },
        ),
        migrations.CreateModel(
            name='TestCase',
            fields=[
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')),
                ('delete_time', models.DateTimeField(default=None, null=True, verbose_name='删除时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否已删除')),
                ('status', models.BooleanField(default=True, verbose_name='状态（1正常 0停用）')),
                ('description', models.CharField(blank=True, max_length=4096, null=True, verbose_name='描述')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50, verbose_name='用例名称')),
                ('safe_name', models.SlugField(verbose_name='用例集标识（用作py类名）')),
                ('type', models.CharField(choices=[('单接口测试', '单接口测试'), ('场景测试', '场景测试'), ('性能测试', '性能测试'), ('setup', 'setup'), ('teardown', 'teardown')], default='单接口测试', max_length=20, verbose_name='测试类型')),
                ('variables', models.TextField(blank=True, null=True, verbose_name='用例变量')),
                ('depends', models.TextField(blank=True, null=True, verbose_name='依赖项（用例）')),
                ('severity', models.CharField(choices=[('blocker', '阻塞缺陷（功能未实现，无法下一步）'), ('critical', '严重缺陷（功能点缺失）'), ('normal', '一般缺陷（边界情况，格式错误）'), ('minor', '次要缺陷（界面错误与ui需求不符）'), ('trivial', '轻微缺陷（必须项无提示，或者提示不规范）')], default='normal', max_length=20, verbose_name='用例等级')),
                ('result', models.CharField(choices=[('passed', '成功'), ('failed', '失败'), ('skipped', '跳过'), ('error', '故障'), ('', '未执行')], default='null', max_length=30, verbose_name='测试结果')),
                ('creator', models.ForeignKey(max_length=20, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='case_creator', to=settings.AUTH_USER_MODEL, verbose_name='创建人')),
                ('labels', models.ManyToManyField(blank=True, default=[], related_name='case_label', to='api_test.GlobalLabel', verbose_name='标签')),
            ],
            options={
                'verbose_name': '用例',
                'verbose_name_plural': '用例管理',
            },
        ),
        migrations.CreateModel(
            name='YApiEvent',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('yapi_id', models.IntegerField(default=0, verbose_name='YAPI接口ID')),
                ('event', models.CharField(blank=True, max_length=100, null=True, verbose_name='变更事件')),
                ('content', models.TextField(blank=True, null=True, verbose_name='变更内容')),
                ('updater', models.CharField(blank=True, max_length=50, null=True, verbose_name='更新人')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='变更时间')),
            ],
            options={
                'verbose_name': 'yapi接口事件',
                'verbose_name_plural': 'yapi接口事件管理',
            },
        ),
        migrations.CreateModel(
            name='TestTask',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(default='', max_length=100, verbose_name='名称')),
                ('priority', models.IntegerField(default=0, verbose_name='优先级')),
                ('cron', models.CharField(default='', max_length=100, verbose_name='cron表达式')),
                ('status', models.SmallIntegerField(choices=[(0, '等待中'), (1, '运行中'), (2, '已完成'), (3, '暂停'), (4, '无效'), (5, '异常')], default=0, verbose_name='状态')),
                ('next_run', models.CharField(blank=True, default='', max_length=50, null=True, verbose_name='下一次执行时间')),
                ('duration', models.IntegerField(default=0, verbose_name='耗时（秒）')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('job_state', models.JSONField(blank=True, default=dict, null=True, verbose_name='job state')),
                ('test_level', models.CharField(blank=True, choices=[('test_suite', 'test_suite'), ('test_case', 'test_case'), ('test_step', 'test_step')], default='test_case', max_length=20, null=True, verbose_name='测试类别')),
                ('test_filters', models.JSONField(blank=True, default=dict, null=True, verbose_name='查询筛选器')),
                ('creator', models.ForeignKey(max_length=20, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='task_creator', to=settings.AUTH_USER_MODEL, verbose_name='创建人')),
                ('test_env', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='test_env', to='api_test.globalenv', verbose_name='执行环境')),
                ('test_validate', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='test_validate', to='api_test.globalresponsevalidate', verbose_name='校验规则')),
            ],
            options={
                'verbose_name': '测试任务',
                'verbose_name_plural': '测试任务',
            },
        ),
        migrations.CreateModel(
            name='TestSuite',
            fields=[
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')),
                ('delete_time', models.DateTimeField(default=None, null=True, verbose_name='删除时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否已删除')),
                ('status', models.BooleanField(default=True, verbose_name='状态（1正常 0停用）')),
                ('description', models.CharField(blank=True, max_length=4096, null=True, verbose_name='描述')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50, verbose_name='用例集')),
                ('safe_name', models.SlugField(verbose_name='用例集标识（用作py文件夹名）')),
                ('headers', models.TextField(blank=True, null=True, verbose_name='请求头')),
                ('setup', models.JSONField(blank=True, default=list, null=True, verbose_name='setup')),
                ('setup_class', models.JSONField(blank=True, default=list, null=True, verbose_name='setup_class')),
                ('teardown', models.JSONField(blank=True, default=list, null=True, verbose_name='teardown')),
                ('teardown_class', models.JSONField(blank=True, default=list, null=True, verbose_name='teardown_class')),
                ('creator', models.ForeignKey(max_length=20, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='suite_creator', to=settings.AUTH_USER_MODEL, verbose_name='创建人')),
                ('department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='suite_dept', to='api_test.department', verbose_name='部门')),
                ('labels', models.ManyToManyField(blank=True, default=[], related_name='suite_label', to='api_test.GlobalLabel', verbose_name='标签')),
                ('updater', models.ForeignKey(max_length=20, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='suite_updater', to=settings.AUTH_USER_MODEL, verbose_name='更新人')),
            ],
            options={
                'verbose_name': '用例集',
                'verbose_name_plural': '用例集管理',
            },
        ),
        migrations.CreateModel(
            name='TestStep',
            fields=[
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')),
                ('delete_time', models.DateTimeField(default=None, null=True, verbose_name='删除时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否已删除')),
                ('status', models.BooleanField(default=True, verbose_name='状态（1正常 0停用）')),
                ('description', models.CharField(blank=True, max_length=4096, null=True, verbose_name='描述')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('sid', models.IntegerField(default=0, verbose_name='执行步骤ID')),
                ('name', models.CharField(max_length=50, verbose_name='步骤名称')),
                ('depends', models.TextField(blank=True, null=True, verbose_name='依赖项（步骤）')),
                ('skipif', models.TextField(blank=True, default='', null=True, verbose_name='skipif')),
                ('setup_hooks', models.JSONField(blank=True, default=list, null=True, verbose_name='setup_hooks')),
                ('teardown_hooks', models.JSONField(blank=True, default=list, null=True, verbose_name='teardown_hooks')),
                ('req_path_extend', models.CharField(blank=True, default='', max_length=1024, null=True, verbose_name='请求path扩展')),
                ('req_headers', models.TextField(blank=True, null=True, verbose_name='请求头')),
                ('req_params', models.TextField(blank=True, null=True, verbose_name='请求参数-params')),
                ('req_json', models.TextField(blank=True, null=True, verbose_name='请求参数-json')),
                ('req_data', models.TextField(blank=True, null=True, verbose_name='请求参数-data')),
                ('validator', models.TextField(blank=True, null=True, verbose_name='响应数据验证')),
                ('extractor', models.TextField(blank=True, null=True, verbose_name='响应数据变量提取')),
                ('result', models.CharField(choices=[('passed', '成功'), ('failed', '失败'), ('skipped', '跳过'), ('error', '故障'), ('', '未执行')], default='null', max_length=30, verbose_name='测试结果')),
                ('apiInfo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='step_api', to='api_test.apiinfo', verbose_name='所属接口')),
                ('creator', models.ForeignKey(max_length=20, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='step_creator', to=settings.AUTH_USER_MODEL, verbose_name='创建人')),
                ('labels', models.ManyToManyField(blank=True, default=[], related_name='step_label', to='api_test.GlobalLabel', verbose_name='标签')),
                ('test_case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='step_case', to='api_test.testcase', verbose_name='所属用例')),
                ('updater', models.ForeignKey(max_length=20, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='step_updater', to=settings.AUTH_USER_MODEL, verbose_name='更新人')),
            ],
            options={
                'verbose_name': '测试用例步骤',
                'verbose_name_plural': '测试用例步骤管理',
            },
        ),
        migrations.CreateModel(
            name='TestReport',
            fields=[
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')),
                ('delete_time', models.DateTimeField(default=None, null=True, verbose_name='删除时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否已删除')),
                ('description', models.CharField(blank=True, max_length=4096, null=True, verbose_name='描述')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('build_type', models.CharField(choices=[('环境验证', '环境验证'), ('冒烟测试', '冒烟测试'), ('业务巡检', '业务巡检'), ('其他', '其他')], default='其他', max_length=20, verbose_name='构建类型')),
                ('build_status', models.CharField(choices=[('build-status-static', '构建完成'), ('build-status-in-progress', '构建正在进行中')], default='build-status-in-progress', max_length=50, verbose_name='构建状态')),
                ('status', models.BooleanField(default=True, verbose_name='状态')),
                ('duration', models.IntegerField(default=0, verbose_name='耗时（秒）')),
                ('case_total', models.IntegerField(default=0, verbose_name='用例总数')),
                ('case_passed', models.IntegerField(default=0, verbose_name='用例成功数量')),
                ('case_failed', models.IntegerField(default=0, verbose_name='用例失败数量')),
                ('case_skipped', models.IntegerField(default=0, verbose_name='用例跳过数量')),
                ('case_error', models.IntegerField(default=0, verbose_name='用例故障数量')),
                ('case_pass_rate', models.FloatField(default=0, verbose_name='用例通过率')),
                ('step_total', models.IntegerField(default=0, verbose_name='步骤总数')),
                ('step_passed', models.IntegerField(default=0, verbose_name='步骤成功数量')),
                ('step_failed', models.IntegerField(default=0, verbose_name='步骤失败数量')),
                ('step_skipped', models.IntegerField(default=0, verbose_name='步骤跳过数量')),
                ('step_error', models.IntegerField(default=0, verbose_name='步骤故障数量')),
                ('step_pass_rate', models.FloatField(default=0, verbose_name='步骤通过率')),
                ('broken_apis', models.JSONField(default=dict, verbose_name='阻塞接口')),
                ('client', models.CharField(blank=True, default='localhost', max_length=50, null=True, verbose_name='测试机器Client端')),
                ('log_path', models.TextField(blank=True, max_length=500, null=True, verbose_name='日志文件地址')),
                ('html_report_path', models.TextField(blank=True, max_length=500, null=True, verbose_name='pytest-html报告地址')),
                ('allure_xml_path', models.TextField(blank=True, max_length=500, null=True, verbose_name='allure xml数据地址')),
                ('allure_url', models.URLField(blank=True, max_length=500, null=True, verbose_name='allure 报告地址')),
                ('jenkins_job_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='jenkins job name')),
                ('jenkins_build_number', models.IntegerField(blank=True, default=0, null=True, verbose_name='jenkins build number')),
                ('env', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='report_env', to='api_test.globalenv', verbose_name='报告关联测试环境')),
            ],
            options={
                'verbose_name': '测试报告',
                'verbose_name_plural': '测试报告',
            },
        ),
        migrations.CreateModel(
            name='TestEnvMonitor',
            fields=[
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')),
                ('delete_time', models.DateTimeField(default=None, null=True, verbose_name='删除时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否已删除')),
                ('status', models.BooleanField(default=True, verbose_name='状态（1正常 0停用）')),
                ('description', models.CharField(blank=True, max_length=4096, null=True, verbose_name='描述')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('build_type', models.CharField(choices=[('环境验证', '环境验证'), ('冒烟测试', '冒烟测试'), ('业务巡检', '业务巡检'), ('其他', '其他')], default='其他', max_length=20, verbose_name='构建类型')),
                ('creator', models.ForeignKey(max_length=20, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='monitor_creator', to=settings.AUTH_USER_MODEL, verbose_name='创建人')),
                ('env', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='monitor_env', to='api_test.globalenv', verbose_name='被监控环境')),
                ('report', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='env_report', to='api_test.testreport', verbose_name='环境报告')),
                ('validate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='monitor_validate', to='api_test.globalresponsevalidate', verbose_name='校验规则')),
            ],
            options={
                'verbose_name': '测试环境监控',
                'verbose_name_plural': '测试环境监控',
            },
        ),
        migrations.AddField(
            model_name='testcase',
            name='test_suite',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='case_suite', to='api_test.testsuite', verbose_name='所属用例集'),
        ),
        migrations.AddField(
            model_name='testcase',
            name='updater',
            field=models.ForeignKey(max_length=20, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='case_updater', to=settings.AUTH_USER_MODEL, verbose_name='更新人'),
        ),
        migrations.CreateModel(
            name='ProjectMember',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('role', models.CharField(choices=[('超级管理员', '超级管理员'), ('开发人员', '开发人员'), ('测试人员', '测试人员'), ('测试开发', '测试开发'), ('游客', '游客')], max_length=50, verbose_name='角色')),
                ('status', models.BooleanField(default=True, verbose_name='状态')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='member_project', to='api_test.project', verbose_name='所属项目')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='member_user', to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '项目成员',
                'verbose_name_plural': '项目成员',
            },
        ),
        migrations.CreateModel(
            name='ProjectDynamic',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('time', models.DateTimeField(max_length=128, verbose_name='操作时间')),
                ('type', models.CharField(max_length=50, verbose_name='操作类型')),
                ('operationObject', models.CharField(max_length=50, verbose_name='操作对象')),
                ('description', models.CharField(blank=True, max_length=1024, null=True, verbose_name='描述')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dynamic_project', to='api_test.project', verbose_name='所属项目')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='userName', to=settings.AUTH_USER_MODEL, verbose_name='操作人')),
            ],
            options={
                'verbose_name': '项目动态',
                'verbose_name_plural': '项目动态',
            },
        ),
        migrations.CreateModel(
            name='DictType',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(default='', max_length=100, verbose_name='字典名称')),
                ('type', models.CharField(default='', max_length=100, verbose_name='字典类型')),
                ('remark', models.CharField(default='', max_length=500, verbose_name='备注')),
                ('creator', models.ForeignKey(max_length=20, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='dict_type_creator', to=settings.AUTH_USER_MODEL, verbose_name='创建人')),
                ('updater', models.ForeignKey(max_length=20, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='dict_type_updater', to=settings.AUTH_USER_MODEL, verbose_name='更新人')),
            ],
            options={
                'verbose_name': '字典类型表',
                'verbose_name_plural': '字典类型表',
            },
        ),
        migrations.CreateModel(
            name='DictData',
            fields=[
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')),
                ('delete_time', models.DateTimeField(default=None, null=True, verbose_name='删除时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否已删除')),
                ('status', models.BooleanField(default=True, verbose_name='状态（1正常 0停用）')),
                ('description', models.CharField(blank=True, max_length=4096, null=True, verbose_name='描述')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('dict_sort', models.CharField(default='', max_length=100, verbose_name='字典排序')),
                ('dict_label', models.CharField(default='', max_length=100, verbose_name='字典标签')),
                ('dict_value', models.CharField(default='', max_length=100, verbose_name='字典键值')),
                ('list_class', models.CharField(default='', max_length=100, verbose_name='表格回显样式（success/info/warning/danger）')),
                ('is_default', models.BooleanField(default=False, verbose_name='是否默认（1是 0否）')),
                ('remark', models.CharField(default='', max_length=500, verbose_name='备注')),
                ('creator', models.ForeignKey(max_length=20, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='dict_data_creator', to=settings.AUTH_USER_MODEL, verbose_name='创建人')),
                ('dict_type', models.ForeignKey(max_length=50, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='data_dict', to='api_test.dicttype', verbose_name='字典名称')),
                ('updater', models.ForeignKey(max_length=20, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='dict_data_updater', to=settings.AUTH_USER_MODEL, verbose_name='更新人')),
            ],
            options={
                'verbose_name': '字典数据表',
                'verbose_name_plural': '字典数据表',
            },
        ),
        migrations.CreateModel(
            name='CustomMethod',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50, verbose_name='方法名')),
                ('description', models.CharField(blank=True, max_length=1024, null=True, verbose_name='描述')),
                ('type', models.CharField(max_length=50, verbose_name='类型')),
                ('dataCode', models.TextField(verbose_name='代码')),
                ('status', models.BooleanField(default=True, verbose_name='状态')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api_test.project', verbose_name='项目')),
            ],
            options={
                'verbose_name': '自定义方法',
                'verbose_name_plural': '自定义方法',
            },
        ),
        migrations.CreateModel(
            name='ApiUpdateHistory',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('event', models.CharField(blank=True, max_length=100, null=True, verbose_name='变更事件')),
                ('content', models.TextField(blank=True, null=True, verbose_name='变更内容')),
                ('updater', models.CharField(blank=True, max_length=50, null=True, verbose_name='更新人')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='变更时间')),
                ('update_status', models.IntegerField(choices=[(0, '待处理'), (1, '待验证'), (2, '已处理')], default=0, verbose_name='变更处理状态')),
                ('api', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='update_api', to='api_test.apiinfo', verbose_name='所属接口')),
            ],
            options={
                'verbose_name': '接口变更历史',
                'verbose_name_plural': '接口变更历史管理',
            },
        ),
        migrations.AddField(
            model_name='apiinfo',
            name='labels',
            field=models.ManyToManyField(blank=True, default=[], related_name='api_label', to='api_test.GlobalLabel', verbose_name='标签'),
        ),
        migrations.AddField(
            model_name='apiinfo',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='api_project', to='api_test.project', verbose_name='所属项目'),
        ),
        migrations.AddField(
            model_name='apiinfo',
            name='updater',
            field=models.ForeignKey(max_length=20, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='api_info_updater', to=settings.AUTH_USER_MODEL, verbose_name='更新人'),
        ),
        migrations.AddField(
            model_name='apigroup',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api_test.project', verbose_name='项目'),
        ),
    ]
