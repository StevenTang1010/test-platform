import json
from django.utils import timezone
from django.db import models
from django.core.validators import validate_comma_separated_integer_list
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

# 测试结果选项
RESULT_CHOICE = (
    ('passed', '成功'),
    ('failed', '失败'),
    ('skipped', '跳过'),
    ('error', '故障'),
    ('', '未执行'),
)
# 接口变更处理进度选项
API_UPDATE_STATUS_CHOICE = (
    (0, '待处理'),
    (1, '待验证'),
    (2, '已处理')
)
# 测试构建类型选项
BUILD_TYPE_CHOICE = (
    ('环境验证', '环境验证'),
    ('冒烟测试', '冒烟测试'),
    ('业务巡检', '业务巡检'),
    ('其他', '其他')
)


class SoftDelTableQuerySet(models.QuerySet):
    def delete(self):
        self.update(is_delete=True, delete_time=timezone.now())


class BaseManager(models.Manager):
    _queryset_class = SoftDelTableQuerySet

    def get_queryset(self):
        return super().get_queryset().filter(is_delete=False)


# 基础表：公共字段列 - 创建时间/更新时间/状态/描述
class BaseModel(models.Model):
    """
    公共字段列
    """

    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='更新时间', null=True, auto_now=True)
    delete_time = models.DateTimeField(verbose_name="删除时间", null=True, default=None)
    is_delete = models.BooleanField(verbose_name='是否已删除', default=False)

    # creator = models.CharField(verbose_name="创建人", max_length=20, null=True)
    # updater = models.CharField(verbose_name="更新人", max_length=20, null=True)
    status = models.BooleanField(default=True, verbose_name='状态（1正常 0停用）')
    description = models.CharField(max_length=4096, blank=True, null=True, verbose_name='描述')

    def delete(self, using=None, keep_parents=False):
        self.is_delete = True
        self.delete_time = timezone.now()
        self.save()

    objects = BaseManager()

    class Meta:
        abstract = True  # 抽象基类
        verbose_name = "公共字段表"
        db_table = 'base_table'


# 字典类型表 - 灵活配置、kv存储
class DictType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, default='', verbose_name='字典名称')
    type = models.CharField(max_length=100, default='', verbose_name='字典类型')
    remark = models.CharField(max_length=500, default='', verbose_name='备注')

    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, max_length=20,
                                verbose_name="创建人", related_name="dict_type_creator")
    updater = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, max_length=20,
                                verbose_name="更新人", related_name="dict_type_updater")

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '字典类型表'
        verbose_name_plural = '字典类型表'


# 字典数据表 - 灵活配置、kv存储
class DictData(BaseModel):
    id = models.AutoField(primary_key=True)
    dict_type = models.ForeignKey(DictType, on_delete=models.SET_NULL, null=True, max_length=50,
                                  verbose_name="字典名称", related_name="data_dict")
    dict_sort = models.CharField(max_length=100, default='', verbose_name='字典排序')
    dict_label = models.CharField(max_length=100, default='', verbose_name='字典标签')
    dict_value = models.CharField(max_length=100, default='', verbose_name='字典键值')
    list_class = models.CharField(max_length=100, default='', verbose_name='表格回显样式（success/info/warning/danger）')
    is_default = models.BooleanField(default=False, verbose_name='是否默认（1是 0否）')
    remark = models.CharField(max_length=500, default='', verbose_name='备注')

    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, max_length=20,
                                verbose_name="创建人", related_name="dict_data_creator")
    updater = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, max_length=20,
                                verbose_name="更新人", related_name="dict_data_updater")

    def __unicode__(self):
        return self.dict_type.type

    def __str__(self):
        return self.dict_type.type

    class Meta:
        verbose_name = '字典数据表'
        verbose_name_plural = '字典数据表'


# 部门表
class Department(BaseModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name='部门名称')
    safe_name = models.SlugField(default='',  blank=True, null=True, max_length=50, verbose_name='部门标识（用作文件夹名）')
    leader = models.CharField(default='',  blank=True, null=True, max_length=50, verbose_name='负责人')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '部门'
        verbose_name_plural = '部门'


# 项目表
class Project(BaseModel):
    """项目表"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name='项目名称', max_length=50)
    version = models.CharField(verbose_name='版本', max_length=50, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, verbose_name='部门')
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, max_length=20,
                                verbose_name="创建人", related_name="project_creator")
    updater = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, max_length=20,
                                verbose_name="更新人", related_name="project_updater")

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '项目'
        verbose_name_plural = '项目'


# 项目动态 --TODO
class ProjectDynamic(models.Model):
    """项目动态"""
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, related_name='dynamic_project', on_delete=models.CASCADE, verbose_name='所属项目')
    time = models.DateTimeField(verbose_name='操作时间', max_length=128)
    type = models.CharField(verbose_name='操作类型', max_length=50)
    operationObject = models.CharField(verbose_name='操作对象', max_length=50)
    user = models.ForeignKey(User, blank=True, null=True, related_name='userName',
                             on_delete=models.SET_NULL, verbose_name='操作人')
    description = models.CharField(max_length=1024, blank=True, null=True, verbose_name='描述')

    def __unicode__(self):
        return self.type

    class Meta:
        verbose_name = '项目动态'
        verbose_name_plural = '项目动态'


# 项目成员
class ProjectMember(models.Model):
    """"""
    CHOICES = (
        ('超级管理员', '超级管理员'),
        ('开发人员', '开发人员'),
        ('测试人员', '测试人员'),
        ('测试开发', '测试开发'),
        ('游客', '游客')
    )
    id = models.AutoField(primary_key=True)
    role = models.CharField(max_length=50, verbose_name='角色', choices=CHOICES)
    status = models.BooleanField(default=True, verbose_name='状态')
    project = models.ForeignKey(Project, related_name='member_project', on_delete=models.CASCADE, verbose_name='所属项目')
    user = models.ForeignKey(User, related_name='member_user', on_delete=models.CASCADE, verbose_name='用户')

    def __unicode__(self):
        return self.role

    def __str__(self):
        return self.role

    class Meta:
        verbose_name = '项目成员'
        verbose_name_plural = '项目成员'


# app系统配置
def default_app_setting():
    setting = {
        "debug": {"value": True, "description": "Debug模式"},
        "file_log_level": {"value": 'DEBUG', "description": "日志等级（文件）"},
        "console_log_level": {"value": 'INFO', "description": "日志等级（控制台）"},
        "testcase_max_rotation": {"value": 50, "description": "保留历史构建数据的最大个数"}
    }
    return setting


class AppSetting(models.Model):
    """app系统配置，如debug模式、构建保留数等"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, null=True, default='app系统配置', verbose_name='Name')
    data = models.JSONField(default=default_app_setting, verbose_name='APP配置数据')
    description = models.CharField(max_length=1024, blank=True, null=True, verbose_name='描述')
    status = models.BooleanField(default=True, verbose_name='状态')

    def delete(self, using=None, keep_parents=False):
        return "app系统配置，禁止删除!"

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    def get_default_app_setting(self):
        return default_app_setting()

    class Meta:
        verbose_name = 'app系统配置'
        verbose_name_plural = 'app系统配置'


# 全局环境配置
def default_env_config():
    config = {
        "company_id": {"value": '', "description": "公司ID"},
        "base_url_mk": {"value": '', "description": "服务商后台地址"},
        "base_url_qw": {"value": '', "description": "企微端地址"},
        "base_url_oss_bill": {"value": '', "description": "运营计费地址"},
        "base_url_oss_official": {"value": '', "description": "运营官方地址"},
        "base_url_qyapi": {"value": 'https://qyapi.weixin.qq.com', "description": "企业微信地址"},
        "corp_id": {"value": '', "description": "企微企业标识corp_id"}
    }
    return config


def default_qw_external_contact_config():
    cf = {
        "external_contact_token": {"value": '', "description": "企微客户联系Token"},
        "external_contact_aes_key": {"value": '', "description": "企微客户联系AESKey"},
        "external_contact_corp_secret": {"value": '', "description": "企微客户联系Secret"},
    }
    return cf


class GlobalEnv(models.Model):
    """
    测试环境配置 environment
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name='名称')
    config = models.JSONField(default=default_env_config, verbose_name='环境基础配置')
    qw_external_contact_config = models.JSONField(default=default_qw_external_contact_config, verbose_name='企微客户联系配置')
    data = models.JSONField(default=dict, verbose_name='环境数据')
    mock = models.JSONField(default=dict, verbose_name='环境mock数据')
    mock_dynamic = models.BooleanField("动态更新mock", default=True)
    description = models.CharField(max_length=1024, blank=True, null=True, verbose_name='描述')
    status = models.BooleanField(default=True, verbose_name='状态')
    is_default = models.BooleanField("默认配置", default=False)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    def get_default_config(self):
        return default_env_config()

    def get_default_qw_external_contact_config(self):
        return default_qw_external_contact_config()

    class Meta:
        verbose_name = '环境配置'
        verbose_name_plural = '环境配置管理'


# 全局const
class GlobalConst(models.Model):
    """全局const"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name='Name')
    value = models.TextField(blank=True, null=True, verbose_name='Value')
    description = models.CharField(max_length=1024, blank=True, null=True, verbose_name='描述')
    status = models.BooleanField(default=True, verbose_name='状态')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Const'
        verbose_name_plural = '全局Const管理'


# 全局Header
class GlobalHeader(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=1024, verbose_name="名称")
    value = models.TextField(blank=True, null=True, verbose_name='内容')
    description = models.CharField(max_length=1024, blank=True, null=True, verbose_name='描述')
    status = models.BooleanField(default=True, verbose_name='状态')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '全局请求头'
        verbose_name_plural = '全局请求头管理'


# 通用校验规则配置
class GlobalResponseValidate(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=1024, default='默认校验', verbose_name="名称")
    description = models.CharField(max_length=1024, blank=True, null=True, verbose_name='描述')
    check_status_code = models.BooleanField(default=True, verbose_name='检查状态代码')
    check_json_schema = models.BooleanField(default=True, verbose_name='检查json-schema')
    check_response_data = models.BooleanField(default=True, verbose_name='检查响应数据')
    status_code = models.CharField(default='200', max_length=500, verbose_name='期望状态代码',
                                   validators=[validate_comma_separated_integer_list])
    status = models.BooleanField(default=True, verbose_name='状态')
    is_default = models.BooleanField("默认配置", default=False)

    def save(self, *args, **kwargs):
        if self.is_default:
            try:
                GlobalResponseValidate.objects.filter(is_default=True).update(is_default=False)
            except GlobalResponseValidate.DoesNotExist:
                pass
        super(GlobalResponseValidate, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '通用校验规则配置'
        verbose_name_plural = '通用校验规则配置管理'


# 全局标签
class GlobalLabel(models.Model):
    """
    全局标签
    """
    LABEL_TYPE_CHOICE = (
        ('priority', '优先级'),  # 如 P0、P1、P2
        ('severity', '严重等级'),  # 如 normal、blocker
        ('function', '业务功能'),  # 如 登录、权限检查
        ('testsuite_type', '测试集类型'),  # 如 冒烟、巡检、环境验证
        ('other', '其他'),
    )
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name='标签名')
    type = models.CharField(verbose_name='标签类型', choices=LABEL_TYPE_CHOICE, default='priority', max_length=20)
    status = models.BooleanField(default=True, verbose_name='状态')
    description = models.CharField(max_length=1024, blank=True, null=True, verbose_name='描述')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = '标签管理'


# 自定义方法 --TODO
class CustomMethod(models.Model):
    """
    自定义方法
    """
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='项目')
    name = models.CharField(max_length=50, verbose_name='方法名')
    description = models.CharField(max_length=1024, blank=True, null=True, verbose_name='描述')
    type = models.CharField(max_length=50, verbose_name='类型')
    dataCode = models.TextField(verbose_name='代码')
    status = models.BooleanField(default=True, verbose_name='状态')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = '自定义方法'
        verbose_name_plural = '自定义方法'


# 接口分组
class ApiGroup(BaseModel):
    """
    接口分组
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name='接口分组名称')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='项目')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '接口分组'
        verbose_name_plural = '接口分组'


# 接口信息
class ApiInfo(BaseModel):
    """
    接口信息
    """
    HTTP_CHOICE = (
        ('HTTP', 'HTTP'),
        ('HTTPS', 'HTTPS')
    )
    REQUEST_TYPE_CHOICE = (
        ('POST', 'POST'),
        ('GET', 'GET'),
        ('PUT', 'PUT'),
        ('DELETE', 'DELETE'),
        ('CALL', 'CALL')
    )
    HOST_TAG_CHOICE = (
        ('mk', '服务商后台地址'),
        ('qw', '企微端地址'),
        ('oss_bill', '运营计费地址'),
        ('oss_official', '运营官方地址'),
        ('qyapi', '企业微信API'),
    )
    # 接口数据来源，默认manual - 手动添加
    ORIGIN_CHOICE = (
        ('yapi', 'yapi'),
        ('xmind', 'xmind'),
        ('excel', 'excel'),
        ('manual', 'manual'),
    )

    id = models.AutoField(primary_key=True)
    yapi_id = models.IntegerField(default=0, verbose_name="YAPI接口ID", )
    project = models.ForeignKey(Project, related_name='api_project', null=True, on_delete=models.CASCADE,
                                verbose_name='所属项目')
    api_group = models.ForeignKey(ApiGroup, blank=True, null=True, related_name='api_group',
                                  on_delete=models.SET_NULL, verbose_name='接口分组')
    origin = models.CharField(max_length=50, default='manual', verbose_name='接口数据来源', choices=ORIGIN_CHOICE)
    name = models.CharField(max_length=500, verbose_name='接口名称')
    http_type = models.CharField(max_length=50, default='HTTP', verbose_name='HTTP/HTTPS', choices=HTTP_CHOICE)
    host_tag = models.CharField(max_length=30, verbose_name='指定host', default='mk', choices=HOST_TAG_CHOICE)
    method = models.CharField(max_length=50, verbose_name='请求方式', choices=REQUEST_TYPE_CHOICE)
    path = models.CharField(max_length=1024, verbose_name='接口地址')
    # yapi定义参数 - diff
    yapi_req_headers = models.TextField(blank=True, null=True, verbose_name='yapi定义-请求头')  # json字符串，diff
    yapi_req_params = models.TextField(blank=True, null=True, verbose_name='yapi定义-请求参数-params')  # json字符串，diff
    yapi_req_query = models.TextField(blank=True, null=True, verbose_name='yapi定义-请求参数-query')  # json字符串，diff
    yapi_req_body_form = models.TextField(blank=True, null=True, verbose_name='yapi定义-请求参数-body_form')  # json字符串，diff
    yapi_req_body_other = models.TextField(blank=True, null=True, verbose_name='yapi定义-请求参数-body_other')  # json字符串，diff
    yapi_res_body = models.TextField(blank=True, null=True, verbose_name='yapi定义-响应body')  # json字符串，diff
    # 参数模板
    req_headers = models.TextField(blank=True, null=True, verbose_name='请求头')  # json字符串
    req_params = models.TextField(blank=True, null=True, verbose_name='请求参数-params')  # json字符串
    req_data = models.TextField(blank=True, null=True, verbose_name='请求参数-data')  # json字符串
    req_json = models.TextField(blank=True, null=True, verbose_name='请求参数-json')  # json字符串
    validator = models.TextField(blank=True, null=True, verbose_name='响应数据验证')  # json字符串

    update_status = models.IntegerField(default=1, verbose_name="更新状态", choices=API_UPDATE_STATUS_CHOICE)
    labels = models.ManyToManyField(GlobalLabel, blank=True, default=[],
                                    verbose_name='标签', related_name="api_label")
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, max_length=20,
                                verbose_name="创建人", related_name="api_info_creator")
    updater = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, max_length=20,
                                verbose_name="更新人", related_name="api_info_updater")

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '接口'
        verbose_name_plural = '接口管理'


# 接口变更历史
class ApiUpdateHistory(models.Model):
    id = models.AutoField(primary_key=True)
    api = models.ForeignKey(ApiInfo, related_name='update_api', on_delete=models.CASCADE, verbose_name='所属接口')
    event = models.CharField(blank=True, null=True, max_length=100,
                             verbose_name='变更事件')  # "interface_add", "interface_del", "interface_update"
    content = models.TextField(blank=True, null=True, verbose_name='变更内容')
    updater = models.CharField(blank=True, null=True, max_length=50, verbose_name="更新人")
    update_time = models.DateTimeField(verbose_name='变更时间', auto_now=True)
    update_status = models.IntegerField(default=0, verbose_name="变更处理状态", choices=API_UPDATE_STATUS_CHOICE)

    def __unicode__(self):
        return self.id

    def __str__(self):
        return self.id

    class Meta:
        verbose_name = '接口变更历史'
        verbose_name_plural = '接口变更历史管理'


# yapi接口变更事件 -- 即事件待同步处理任务列表，yapi hook秒call几十上百次变更，同步处理完成不了，存储事件表后遍历处理
class YApiEvent(models.Model):
    id = models.AutoField(primary_key=True)
    yapi_id = models.IntegerField(default=0, verbose_name='YAPI接口ID')
    event = models.CharField(blank=True, null=True, max_length=100, verbose_name='变更事件')
    content = models.TextField(blank=True, null=True, verbose_name='变更内容')
    updater = models.CharField(blank=True, null=True, max_length=50, verbose_name="更新人")
    update_time = models.DateTimeField(verbose_name='变更时间', auto_now=True)

    def __unicode__(self):
        return self.id

    def __str__(self):
        return self.id

    class Meta:
        verbose_name = 'yapi接口事件'
        verbose_name_plural = 'yapi接口事件管理'


# 测试用例集
class TestSuite(BaseModel):
    """测试用例集"""
    from django.core import serializers
    serializers.get_serializer("json")()

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name='用例集')
    safe_name = models.SlugField(max_length=50, verbose_name='用例集标识（用作py文件夹名）')
    department = models.ForeignKey(Department, related_name='suite_dept', on_delete=models.CASCADE, null=True, verbose_name='部门')
    headers = models.TextField(blank=True, null=True, verbose_name='请求头')
    labels = models.ManyToManyField(GlobalLabel, blank=True, default=[], verbose_name='标签', related_name="suite_label")

    setup = models.JSONField(blank=True, null=True, default=list, verbose_name='setup')
    setup_class = models.JSONField(blank=True, null=True, default=list, verbose_name='setup_class')
    teardown = models.JSONField(blank=True, null=True, default=list, verbose_name='teardown')
    teardown_class = models.JSONField(blank=True, null=True, default=list, verbose_name='teardown_class')

    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, max_length=20,
                                verbose_name="创建人", related_name="suite_creator")
    updater = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, max_length=20,
                                verbose_name="更新人", related_name="suite_updater")

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '用例集'
        verbose_name_plural = '用例集管理'


# 测试用例
class TestCase(BaseModel):
    """测试用例"""
    TEST_TYPE_CHOICE = (
        ('单接口测试', '单接口测试'),
        ('场景测试', '场景测试'),
        ('性能测试', '性能测试'),
        ('setup', 'setup'),
        ('teardown', 'teardown'),
    )
    SEVERITY_CHOICE = (
        ('blocker', '阻塞缺陷（功能未实现，无法下一步）'),
        ('critical', '严重缺陷（功能点缺失）'),
        ('normal', '一般缺陷（边界情况，格式错误）'),
        ('minor', '次要缺陷（界面错误与ui需求不符）'),
        ('trivial', '轻微缺陷（必须项无提示，或者提示不规范）'),
    )
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name='用例名称')
    safe_name = models.SlugField(max_length=50, verbose_name='用例集标识（用作py类名）')
    test_suite = models.ForeignKey(TestSuite, related_name='case_suite', on_delete=models.CASCADE, verbose_name='所属用例集')
    labels = models.ManyToManyField(GlobalLabel, blank=True, default=[], verbose_name='标签', related_name="case_label")
    type = models.CharField(verbose_name='测试类型', choices=TEST_TYPE_CHOICE, default='单接口测试', max_length=20)
    variables = models.TextField(blank=True, null=True, verbose_name='用例变量')  # json字符串，Dict[Text, Any]
    depends = models.TextField(blank=True, null=True, verbose_name='依赖项（用例）')  # depends依赖项
    severity = models.CharField(verbose_name='用例等级', choices=SEVERITY_CHOICE, default='normal', max_length=20)  # 暂时没使用
    result = models.CharField(verbose_name='测试结果', choices=RESULT_CHOICE, max_length=30, default='null')
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, max_length=20,
                                verbose_name="创建人", related_name="case_creator")
    updater = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, max_length=20,
                                verbose_name="更新人", related_name="case_updater")

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '用例'
        verbose_name_plural = '用例管理'


# 测试用例步骤
class TestStep(BaseModel):
    """
    测试用例步骤
    """
    id = models.AutoField(primary_key=True)
    sid = models.IntegerField(default=0, verbose_name='执行步骤ID')
    name = models.CharField(max_length=50, verbose_name='步骤名称')
    test_case = models.ForeignKey(TestCase, related_name='step_case', on_delete=models.CASCADE, verbose_name='所属用例')
    apiInfo = models.ForeignKey(ApiInfo, related_name='step_api', on_delete=models.CASCADE, verbose_name='所属接口')
    labels = models.ManyToManyField(GlobalLabel, blank=True, default=[], verbose_name='标签', related_name="step_label")
    depends = models.ManyToManyField('self', blank=True, default=[], verbose_name='依赖项（步骤）', related_name='step_depends')  # depends依赖项
    skipif = models.TextField(blank=True, null=True, default='', verbose_name='skipif')  # 是否跳过步骤：条件表达式
    setup_hooks = models.JSONField(blank=True, null=True, default=list, verbose_name='setup_hooks')
    teardown_hooks = models.JSONField(blank=True, null=True, default=list, verbose_name='teardown_hooks')
    req_path_extend = models.CharField(blank=True, null=True, max_length=1024, default='', verbose_name='请求path扩展')
    req_headers = models.TextField(blank=True, null=True, verbose_name='请求头')  # json字符串
    req_params = models.TextField(blank=True, null=True, verbose_name='请求参数-params')  # json字符串
    req_json = models.TextField(blank=True, null=True, verbose_name='请求参数-json')  # json字符串
    req_data = models.TextField(blank=True, null=True, verbose_name='请求参数-data')  # json字符串
    validator = models.TextField(blank=True, null=True, verbose_name='响应数据验证')  # json字符串
    extractor = models.TextField(blank=True, null=True, verbose_name='响应数据变量提取')  # json字符串
    result = models.CharField(verbose_name='测试结果', choices=RESULT_CHOICE, max_length=30, default='null')
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, max_length=20,
                                verbose_name="创建人", related_name="step_creator")
    updater = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, max_length=20,
                                verbose_name="更新人", related_name="step_updater")

    def __unicode__(self):
        return self.description

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = '测试用例步骤'
        verbose_name_plural = '测试用例步骤管理'


# 测试报告
class TestReport(BaseModel):
    BUILD_STATUS_CHOICE = (
        ('build-status-static', '构建完成'),
        ('build-status-in-progress', '构建正在进行中')
    )
    id = models.AutoField(primary_key=True)
    # 构建信息
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    build_type = models.CharField(verbose_name='构建类型', choices=BUILD_TYPE_CHOICE, default='其他', max_length=20)
    build_status = models.CharField(verbose_name='构建状态', choices=BUILD_STATUS_CHOICE, default='build-status-in-progress', max_length=50)
    env = models.ForeignKey(GlobalEnv, blank=True, null=True, related_name='report_env', on_delete=models.CASCADE,
                            verbose_name='报告关联测试环境')
    # 结果
    status = models.BooleanField(default=True, verbose_name='状态')
    duration = models.IntegerField(default=0, verbose_name='耗时（秒）')
    # case统计
    case_total = models.IntegerField(default=0, verbose_name='用例总数')
    case_passed = models.IntegerField(default=0, verbose_name='用例成功数量')
    case_failed = models.IntegerField(default=0, verbose_name='用例失败数量')
    case_skipped = models.IntegerField(default=0, verbose_name='用例跳过数量')
    case_error = models.IntegerField(default=0, verbose_name='用例故障数量')
    case_pass_rate = models.FloatField(default=0, verbose_name='用例通过率')
    # step 统计
    step_total = models.IntegerField(default=0, verbose_name='步骤总数')
    step_passed = models.IntegerField(default=0, verbose_name='步骤成功数量')
    step_failed = models.IntegerField(default=0, verbose_name='步骤失败数量')
    step_skipped = models.IntegerField(default=0, verbose_name='步骤跳过数量')
    step_error = models.IntegerField(default=0, verbose_name='步骤故障数量')
    step_pass_rate = models.FloatField(default=0, verbose_name='步骤通过率')
    broken_apis = models.JSONField(default=dict, verbose_name='阻塞接口')
    # 报告、日志地址记录
    client = models.CharField(default='localhost', max_length=50, blank=True, null=True, verbose_name='测试机器Client端')
    log_path = models.TextField(max_length=500, blank=True, null=True, verbose_name='日志文件地址')
    html_report_path = models.TextField(max_length=500, blank=True, null=True, verbose_name='pytest-html报告地址')
    allure_xml_path = models.TextField(max_length=500, blank=True, null=True, verbose_name='allure xml数据地址')
    allure_url = models.URLField(max_length=500, blank=True, null=True, verbose_name='allure 报告地址')
    jenkins_job_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='jenkins job name')
    jenkins_build_number = models.IntegerField(default=0, blank=True, null=True, verbose_name='jenkins build number')

    def __unicode__(self):
        return self.status

    def __str__(self):
        return self.status

    class Meta:
        verbose_name = '测试报告'
        verbose_name_plural = '测试报告'


# 测试任务
class TestTask(models.Model):
    """测试任务"""
    TAST_STATUS_CHOICE = (
        (0, '等待中'),
        (1, '运行中'),
        (2, '已完成'),
        (3, '暂停'),
        (4, '无效'),
        (5, '异常')
    )
    TEST_LEVEL_CHOICE = (
        ('test_suite', 'test_suite'),  # 查询 用例集 并执行
        ('test_case', 'test_case'),  # 查询 用例 并执行
        ('test_step', 'test_step'),  # 查询 用例步骤 并执行
    )
    # 任务 - 定时
    id = models.AutoField(primary_key=True)
    name = models.CharField(default='', max_length=100, verbose_name='名称')
    priority = models.IntegerField(default=0, verbose_name='优先级')
    cron = models.CharField(default='', max_length=100, verbose_name='cron表达式')
    status = models.SmallIntegerField(choices=TAST_STATUS_CHOICE, default=0, verbose_name='状态')
    next_run = models.CharField(blank=True, null=True, default='', max_length=50, verbose_name='下一次执行时间')
    duration = models.IntegerField(default=0, verbose_name='耗时（秒）')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, max_length=20,
                                verbose_name="创建人", related_name="task_creator")
    # APScheduler job state
    job_state = models.JSONField(blank=True, null=True, default=dict, verbose_name='job state')

    # 测试参数
    test_env = models.ForeignKey(GlobalEnv, blank=True, null=True, related_name='test_env', on_delete=models.CASCADE, verbose_name='执行环境')
    test_validate = models.ForeignKey(GlobalResponseValidate, blank=True, null=True, related_name='test_validate', on_delete=models.CASCADE, verbose_name='校验规则')
    test_level = models.CharField(blank=True, null=True, choices=TEST_LEVEL_CHOICE, default='test_case', max_length=20,
                                  verbose_name='测试类别')
    test_filters = models.JSONField(blank=True, null=True, default=dict, verbose_name='查询筛选器')  # dict

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '测试任务'
        verbose_name_plural = '测试任务'


def default_cron_job():
    job_info = {
        "id": 0,
        "job_state": {},
        "next_run_time": ''
    }
    return job_info


# 测试环境: 验证、状态监控
class TestEnvMonitor(BaseModel):
    """测试环境监控: 环境验证、冒烟测试、业务巡检"""
    id = models.AutoField(primary_key=True)
    env = models.ForeignKey(GlobalEnv, related_name='monitor_env', on_delete=models.CASCADE, verbose_name='被监控环境')
    validate = models.ForeignKey(GlobalResponseValidate, related_name='monitor_validate', on_delete=models.CASCADE, verbose_name='校验规则')
    cron = models.CharField(default='', blank=True, null=True, max_length=100, verbose_name='cron表达式')
    cron_job = models.JSONField(default=default_cron_job, verbose_name='cron_job信息')
    build_type = models.CharField(max_length=20, choices=BUILD_TYPE_CHOICE, default='其他', verbose_name='构建类型')
    report = models.ForeignKey(TestReport, blank=True, null=True, related_name='env_report', on_delete=models.CASCADE, verbose_name='环境报告')
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, max_length=20, null=True, verbose_name="创建人", related_name="monitor_creator")

    def __unicode__(self):
        return self.env.name

    def __str__(self):
        return self.env.name

    class Meta:
        verbose_name = '测试环境监控'
        verbose_name_plural = '测试环境监控'
