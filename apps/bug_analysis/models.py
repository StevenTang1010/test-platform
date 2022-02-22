# --------------------------------------
# Date: 2021/8/4
# @Author: Steven_Tang
# FileName: models.py
# Description: 数据库表设计
# --------------------------------------

from django.db import models


# 工单表
class Orders(models.Model):
    """工单表模型"""
    CATEGORY = (
        ('穿透', '穿透'),
        ('运维问题', '运维问题'),
        ('需求', '需求'),
        ('使用配置', '使用配置'),
    )
    TECHNICAL = (
        ('前端', '前端'),
        ('后端', '后端'),
        ('性能', '性能'),
        ('产品设计', '产品设计')
    )
    BUG_REASON = (
        ('漏测', '漏测'),
        ('影响范围', '影响范围'),
        ('夹带', '夹带'),
        ('无法模拟场景', '无法模拟场景'),
        ('环境问题', '环境问题'),
        ('人为操作', '人为操作'),
        ('已知BUG', '已知BUG'),
        ('第三方', '第三方'),
    )
    BUSINESS_DOMAIN = (
        ('CRM', 'CRM'),
        ('营销', '营销'),
        ('商城', '商城'),
        ('客服', '客服'),
        ('运营', '运营'),
        ('私有云', '私有云'),
        ('业务中台', '业务中台'),
        ('数据中台', '数据中台'),
        ('技术中台', '技术中台'),
        ('', ''),
    )

    ticket_number = models.CharField(max_length=20, primary_key=True, unique=True, verbose_name='工单编号')
    priority = models.CharField(max_length=20, null=True, verbose_name='优先级')
    severity = models.CharField(max_length=20, null=True, verbose_name='严重程度')
    content = models.CharField(max_length=2048, null=True, verbose_name='问题描述')
    bug_state = models.CharField(max_length=11, default='否', null=True, verbose_name='是否是BUG')
    category = models.CharField(max_length=20, choices=CATEGORY, null=True, verbose_name='分类')
    bug_reason = models.CharField(max_length=512, choices=BUG_REASON, null=True, verbose_name='BUG原因')
    reason = models.CharField(max_length=2048, null=True, verbose_name='问题根源')
    solver = models.CharField(max_length=20, null=True, verbose_name='解决人')
    solution = models.CharField(max_length=1024, null=True, verbose_name='解决方案')
    handling_time = models.FloatField(default=0, null=True, verbose_name='处理时长')
    thorough = models.BooleanField(default=0, null=True, verbose_name='是否彻底解决')
    domain = models.CharField(max_length=30, choices=BUSINESS_DOMAIN, null=True, verbose_name='归属业务域')
    technical = models.CharField(max_length=30, choices=TECHNICAL, null=True, verbose_name='技术归属')
    module = models.CharField(max_length=30, null=True, verbose_name='所属模块')
    pub_date = models.DateField(verbose_name='工单日期')
    update_time = models.DateField(null=True, auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return self.ticket_number

    class Meta:
        verbose_name = '工单详情'
        verbose_name_plural = verbose_name
        ordering = ('-pub_date',)


# 禅道版本质量统计表
class ZtBug(models.Model):
    """禅道BUG统计结果表模型"""
    BUILD_STATE = (
        ('完结', '完结'),
        ('暂停', '暂停'),
        ('作废', '作废'),
    )
    RESULT = (
        ('通过', '通过'),
        ('不通过', '不通过'),
    )

    edition_id = models.CharField(max_length=20, primary_key=True, unique=True, verbose_name='禅道版本id')
    edition_name = models.CharField(max_length=200, null=True, verbose_name='版本名')
    project = models.CharField(max_length=32, null=True, verbose_name='归属产品')
    bug_total = models.IntegerField(default=0, null=True, verbose_name='BUG总数')
    severity = models.IntegerField(default=0, null=True, verbose_name='严重数')
    usages = models.IntegerField(default=0, null=True, verbose_name='有效数')
    solve = models.IntegerField(default=0, null=True, verbose_name='解决数')
    reopen = models.IntegerField(default=0, null=True, verbose_name='reopen数')
    closed = models.IntegerField(default=0, null=True, verbose_name='关闭数')
    leave_over = models.IntegerField(default=0, null=True, verbose_name='遗留数')
    prd = models.IntegerField(default=0, null=True, verbose_name='PRD评审次数')
    ui = models.IntegerField(default=0, null=True, verbose_name='UI评审次数')
    prd_changes = models.IntegerField(default=0, null=True, verbose_name='需求变更次数')
    technology = models.IntegerField(default=0, null=True, verbose_name='技术评审次数')
    test = models.IntegerField(default=0, null=True, verbose_name='测分评审次数')
    smoke = models.IntegerField(default=0, null=True, verbose_name='提测次数')
    result = models.CharField(max_length=10, choices=RESULT, null=True, verbose_name='测试结果')
    release = models.IntegerField(default=0, null=True, verbose_name='上线次数')
    is_delay = models.BooleanField(null=True, default=False, verbose_name='是否延期')
    delay = models.IntegerField(default=0, null=True, verbose_name='延期时长')
    delay_reason = models.CharField(max_length=256, null=True, verbose_name='延期原因')
    remark = models.TextField(max_length=2048, null=True, verbose_name='备注')
    build_state = models.CharField(max_length=10, choices=BUILD_STATE, null=True, verbose_name='版本状态')
    create_time = models.DateField(null=True, verbose_name='创建时间')
    release_time = models.DateField(null=True, verbose_name='上线时间')
    update_time = models.DateField(null=True, auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return self.edition_id

    class Meta:
        verbose_name = '禅道BUG统计数据'
        verbose_name_plural = verbose_name
        ordering = ('-create_time',)


# 禅道BUG创建人员数据统计表
class TesterZtBug(models.Model):
    """禅道BUG人员数据统计表模型"""

    id = models.AutoField(primary_key=True, unique=True, verbose_name='记录id')
    tester_id = models.IntegerField(null=True, verbose_name='创建人id')
    tester_name = models.CharField(max_length=20, null=True, verbose_name='创建人姓名')
    edition_id = models.ForeignKey(ZtBug, verbose_name='版本id', on_delete=models.CASCADE, db_constraint=False,
                                   related_name='zt_test_bug')
    edition_name = models.CharField(max_length=200, null=True, verbose_name='版本名')
    work_pd = models.IntegerField(default=0, null=True, verbose_name='参与pd数')
    bug_total = models.IntegerField(default=0, null=True, verbose_name='提BUG总数')
    severity = models.IntegerField(default=0, null=True, verbose_name='严重数')
    usages = models.IntegerField(default=0, null=True, verbose_name='有效数')
    closed = models.IntegerField(default=0, null=True, verbose_name='关闭数')
    leave_over = models.IntegerField(default=0, null=True, verbose_name='遗留数')
    remark = models.TextField(max_length=2048, null=True, verbose_name='备注')
    update_time = models.DateField(null=True, auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return self.tester_name

    class Meta:
        verbose_name = '禅道BUG创建人统计数据'
        verbose_name_plural = verbose_name


# 禅道BUG解决人员数据统计表
class DeveloperZtBug(models.Model):
    """禅道BUG人员数据统计表模型"""

    ROLE = (
        ('产品', '产品'),
        ('前端', '前端'),
        ('后端', '后端'),
    )

    id = models.AutoField(primary_key=True, unique=True, verbose_name='记录id')
    solve_id = models.IntegerField(null=True, verbose_name='解决人员id')
    solver_name = models.CharField(max_length=20, null=True, verbose_name='解决人姓名')
    edition_id = models.ForeignKey(ZtBug, verbose_name='归属版本id', on_delete=models.CASCADE, db_constraint=False,
                                   related_name='zt_dev_bug')
    edition_name = models.CharField(max_length=200, null=True, verbose_name='版本名')
    dept = models.CharField(max_length=100, choices=ROLE, null=True, verbose_name='角色')
    work_pd = models.IntegerField(default=0, null=True, verbose_name='参与pd数')
    bug_total = models.IntegerField(default=0, null=True, verbose_name='BUG总数')
    severity = models.IntegerField(default=0, null=True, verbose_name='严重数')
    solve = models.IntegerField(default=0, null=True, verbose_name='解决数')
    reopen = models.IntegerField(default=0, null=True, verbose_name='reopen数')
    remark = models.TextField(max_length=2048, null=True, verbose_name='备注')
    update_time = models.DateField(null=True, auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return self.solver_name

    class Meta:
        verbose_name = '禅道BUG解决人统计数据'
        verbose_name_plural = verbose_name
        # ordering = ('-create_time',)
