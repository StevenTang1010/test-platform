# Generated by Django 3.2.5 on 2022-01-27 02:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('ticket_number', models.CharField(max_length=20, primary_key=True, serialize=False, unique=True, verbose_name='工单编号')),
                ('priority', models.CharField(max_length=20, null=True, verbose_name='优先级')),
                ('severity', models.CharField(max_length=20, null=True, verbose_name='严重程度')),
                ('content', models.CharField(max_length=2048, null=True, verbose_name='问题描述')),
                ('bug_state', models.CharField(default='否', max_length=11, null=True, verbose_name='是否是BUG')),
                ('category', models.CharField(choices=[('穿透', '穿透'), ('运维问题', '运维问题'), ('需求', '需求'), ('使用配置', '使用配置')], max_length=20, null=True, verbose_name='分类')),
                ('bug_reason', models.CharField(choices=[('漏测', '漏测'), ('影响范围', '影响范围'), ('夹带', '夹带'), ('无法模拟场景', '无法模拟场景'), ('环境问题', '环境问题'), ('人为操作', '人为操作'), ('已知BUG', '已知BUG'), ('第三方', '第三方')], max_length=512, null=True, verbose_name='BUG原因')),
                ('reason', models.CharField(max_length=2048, null=True, verbose_name='问题根源')),
                ('solver', models.CharField(max_length=20, null=True, verbose_name='解决人')),
                ('solution', models.CharField(max_length=1024, null=True, verbose_name='解决方案')),
                ('handling_time', models.FloatField(default=0, null=True, verbose_name='处理时长')),
                ('thorough', models.BooleanField(default=0, null=True, verbose_name='是否彻底解决')),
                ('domain', models.CharField(choices=[('CRM', 'CRM'), ('营销', '营销'), ('商城', '商城'), ('客服', '客服'), ('运营', '运营'), ('私有云', '私有云'), ('业务中台', '业务中台'), ('数据中台', '数据中台'), ('技术中台', '技术中台'), ('', '')], max_length=30, null=True, verbose_name='归属业务域')),
                ('technical', models.CharField(choices=[('前端', '前端'), ('后端', '后端'), ('性能', '性能'), ('产品设计', '产品设计')], max_length=30, null=True, verbose_name='技术归属')),
                ('module', models.CharField(max_length=30, null=True, verbose_name='所属模块')),
                ('pub_date', models.DateField(verbose_name='工单日期')),
                ('update_time', models.DateField(auto_now=True, null=True, verbose_name='更新时间')),
            ],
            options={
                'verbose_name': '工单详情',
                'verbose_name_plural': '工单详情',
                'ordering': ('-pub_date',),
            },
        ),
        migrations.CreateModel(
            name='ZtBug',
            fields=[
                ('edition_id', models.CharField(max_length=20, primary_key=True, serialize=False, unique=True, verbose_name='禅道版本id')),
                ('edition_name', models.CharField(max_length=200, null=True, verbose_name='版本名')),
                ('project', models.CharField(max_length=32, null=True, verbose_name='归属产品')),
                ('bug_total', models.IntegerField(default=0, null=True, verbose_name='BUG总数')),
                ('severity', models.IntegerField(default=0, null=True, verbose_name='严重数')),
                ('usages', models.IntegerField(default=0, null=True, verbose_name='有效数')),
                ('solve', models.IntegerField(default=0, null=True, verbose_name='解决数')),
                ('reopen', models.IntegerField(default=0, null=True, verbose_name='reopen数')),
                ('closed', models.IntegerField(default=0, null=True, verbose_name='关闭数')),
                ('leave_over', models.IntegerField(default=0, null=True, verbose_name='遗留数')),
                ('prd', models.IntegerField(default=0, null=True, verbose_name='PRD评审次数')),
                ('ui', models.IntegerField(default=0, null=True, verbose_name='UI评审次数')),
                ('prd_changes', models.IntegerField(default=0, null=True, verbose_name='需求变更次数')),
                ('technology', models.IntegerField(default=0, null=True, verbose_name='技术评审次数')),
                ('test', models.IntegerField(default=0, null=True, verbose_name='测分评审次数')),
                ('smoke', models.IntegerField(default=0, null=True, verbose_name='提测次数')),
                ('result', models.CharField(choices=[('通过', '通过'), ('不通过', '不通过')], max_length=10, null=True, verbose_name='测试结果')),
                ('release', models.IntegerField(default=0, null=True, verbose_name='上线次数')),
                ('is_delay', models.BooleanField(default=False, null=True, verbose_name='是否延期')),
                ('delay', models.IntegerField(default=0, null=True, verbose_name='延期时长')),
                ('delay_reason', models.CharField(max_length=256, null=True, verbose_name='延期原因')),
                ('remark', models.TextField(max_length=2048, null=True, verbose_name='备注')),
                ('build_state', models.CharField(choices=[('完结', '完结'), ('暂停', '暂停'), ('作废', '作废')], max_length=10, null=True, verbose_name='版本状态')),
                ('create_time', models.DateField(null=True, verbose_name='创建时间')),
                ('release_time', models.DateField(null=True, verbose_name='上线时间')),
                ('update_time', models.DateField(auto_now=True, null=True, verbose_name='更新时间')),
            ],
            options={
                'verbose_name': '禅道BUG统计数据',
                'verbose_name_plural': '禅道BUG统计数据',
                'ordering': ('-create_time',),
            },
        ),
        migrations.CreateModel(
            name='TesterZtBug',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True, verbose_name='记录id')),
                ('tester_id', models.IntegerField(null=True, verbose_name='创建人id')),
                ('tester_name', models.CharField(max_length=20, null=True, verbose_name='创建人姓名')),
                ('edition_name', models.CharField(max_length=200, null=True, verbose_name='版本名')),
                ('work_pd', models.IntegerField(default=0, null=True, verbose_name='参与pd数')),
                ('bug_total', models.IntegerField(default=0, null=True, verbose_name='提BUG总数')),
                ('severity', models.IntegerField(default=0, null=True, verbose_name='严重数')),
                ('usages', models.IntegerField(default=0, null=True, verbose_name='有效数')),
                ('closed', models.IntegerField(default=0, null=True, verbose_name='关闭数')),
                ('leave_over', models.IntegerField(default=0, null=True, verbose_name='遗留数')),
                ('remark', models.TextField(max_length=2048, null=True, verbose_name='备注')),
                ('update_time', models.DateField(auto_now=True, null=True, verbose_name='更新时间')),
                ('edition_id', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, related_name='zt_test_bug', to='bug_analysis.ztbug', verbose_name='版本id')),
            ],
            options={
                'verbose_name': '禅道BUG创建人统计数据',
                'verbose_name_plural': '禅道BUG创建人统计数据',
            },
        ),
        migrations.CreateModel(
            name='DeveloperZtBug',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True, verbose_name='记录id')),
                ('solve_id', models.IntegerField(null=True, verbose_name='解决人员id')),
                ('solver_name', models.CharField(max_length=20, null=True, verbose_name='解决人姓名')),
                ('edition_name', models.CharField(max_length=200, null=True, verbose_name='版本名')),
                ('dept', models.CharField(choices=[('产品', '产品'), ('前端', '前端'), ('后端', '后端')], max_length=100, null=True, verbose_name='角色')),
                ('work_pd', models.IntegerField(default=0, null=True, verbose_name='参与pd数')),
                ('bug_total', models.IntegerField(default=0, null=True, verbose_name='BUG总数')),
                ('severity', models.IntegerField(default=0, null=True, verbose_name='严重数')),
                ('solve', models.IntegerField(default=0, null=True, verbose_name='解决数')),
                ('reopen', models.IntegerField(default=0, null=True, verbose_name='reopen数')),
                ('remark', models.TextField(max_length=2048, null=True, verbose_name='备注')),
                ('update_time', models.DateField(auto_now=True, null=True, verbose_name='更新时间')),
                ('edition_id', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, related_name='zt_dev_bug', to='bug_analysis.ztbug', verbose_name='归属版本id')),
            ],
            options={
                'verbose_name': '禅道BUG解决人统计数据',
                'verbose_name_plural': '禅道BUG解决人统计数据',
            },
        ),
    ]
