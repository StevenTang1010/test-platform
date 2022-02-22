from django.db import models


# Create your models here.

class System(models.Model):
    """系统表"""
    system_id = models.CharField(max_length=100, primary_key=True, unique=True, verbose_name='系统id')
    system_name = models.CharField(max_length=255, verbose_name='系统名')
    updated_by = models.CharField(max_length=20, null=True, verbose_name='更新人')
    update_time = models.DateField(auto_now=True, null=True, verbose_name='更新时间')

    def __str__(self):
        return f'{self.system_id}, {self.system_name}'

    class Meta:
        verbose_name = '系统表'
        verbose_name_plural = verbose_name


class PrimaryModule(models.Model):
    """一级模块"""
    system = models.ForeignKey(System, max_length=255, null=True, verbose_name='系统id',
                               on_delete=models.CASCADE)
    primary_module_id = models.CharField(max_length=100, primary_key=True, unique=True, verbose_name='一级模块id')
    primary_module_name = models.CharField(max_length=255, null=True, verbose_name='一级模块名')
    updated_by = models.CharField(max_length=20, null=True, verbose_name='更新人')
    update_time = models.DateField(auto_now=True, null=True, verbose_name='更新时间')

    def __str__(self):
        return f'{self.primary_module_id}, {self.primary_module_name}'

    class Meta:
        verbose_name = '一级模块'
        verbose_name_plural = verbose_name


class SecondaryModule(models.Model):
    """二级模块"""
    primary_module = models.ForeignKey(PrimaryModule, null=True, verbose_name='一级模块id',
                                       on_delete=models.CASCADE)
    secondary_module_id = models.CharField(max_length=100, primary_key=True, unique=True, verbose_name='二级模块id')
    secondary_module_name = models.CharField(max_length=255, null=True, verbose_name='二级模块名')
    updated_by = models.CharField(max_length=20, null=True, verbose_name='更新人')
    update_time = models.DateField(auto_now=True, null=True, verbose_name='更新时间')

    def __str__(self):
        return f'{self.secondary_module_id}, {self.secondary_module_name}'

    class Meta:
        verbose_name = '二级模块'
        verbose_name_plural = verbose_name


class ThirdModule(models.Model):
    """三级模块"""
    third_module_id = models.CharField(max_length=100, primary_key=True, unique=True, verbose_name='三级模块id')
    secondary_module = models.ForeignKey(SecondaryModule, null=True, verbose_name='二级模块id', on_delete=models.CASCADE)
    third_module_name = models.CharField(max_length=255, null=True, verbose_name='三级模块名')
    updated_by = models.CharField(max_length=20, null=True, verbose_name='更新人')
    update_time = models.DateField(auto_now=True, null=True, verbose_name='更新时间')

    def __str__(self):
        return f'{self.third_module_id}, {self.third_module_name}'

    class Meta:
        verbose_name = '三级模块'
        verbose_name_plural = verbose_name


class ModuleFunction(models.Model):
    """模块功能"""
    module_function_id = models.CharField(max_length=100, primary_key=True, unique=True, verbose_name='功能id')
    module_function_name = models.CharField(max_length=255, null=True, verbose_name='功能id')
    third_modle = models.ForeignKey(ThirdModule, null=True, verbose_name='三级模块id',
                                    on_delete=models.CASCADE)
    updated_by = models.CharField(max_length=20, null=True, verbose_name='更新人')
    update_time = models.DateField(auto_now=True, null=True, verbose_name='更新时间')

    def __str__(self):
        return f'{self.module_function_id}, {self.module_function_name}'

    class Meta:
        verbose_name = '模块功能'
        verbose_name_plural = verbose_name


class FunctionalRelevance(models.Model):
    """功能关联"""
    direct_func = models.ForeignKey(ModuleFunction, null=True, verbose_name='功能',
                                    on_delete=models.CASCADE, related_name='direct_func')
    indirect_impact_func = models.ForeignKey(ModuleFunction, null=True, verbose_name='关联功能',
                                             on_delete=models.CASCADE, related_name='indirect_impact_func')
    updated_by = models.CharField(max_length=20, null=True, verbose_name='更新人')
    update_time = models.DateField(auto_now=True, null=True, verbose_name='更新时间')

    def __str__(self):
        return f'{self.direct_func}, {self.indirect_impact_func}'

    class Meta:
        verbose_name = '功能关联'
        verbose_name_plural = verbose_name


class TestCase(models.Model):
    """用例表"""
    direct_func = models.ForeignKey(ModuleFunction, null=True, verbose_name='用例所属功能', on_delete=models.CASCADE)
    case_id = models.CharField(max_length=100, primary_key=True, unique=True, verbose_name='用例id')
    case_title = models.CharField(max_length=255, null=True, verbose_name='用例名')
    precondition = models.CharField(max_length=255, null=True, verbose_name='前置条件')
    operation_steps = models.CharField(max_length=1000, null=True, verbose_name='操作步骤')
    expected_results = models.CharField(max_length=255, null=True, verbose_name='预期结果')
    actual_results = models.CharField(max_length=255, null=True, verbose_name='实际结果')
    executor = models.CharField(max_length=20, null=True, verbose_name='执行人')
    execution_times = models.DateTimeField(null=True, verbose_name='执行时间')
    number_of_runs = models.IntegerField(null=True, verbose_name='执行次数')
    updated_by = models.CharField(max_length=20, null=True, verbose_name='更新人')
    update_time = models.DateField(auto_now=True, null=True, verbose_name='更新时间')

    def __str__(self):
        return self.case_id

    class Meta:
        verbose_name = '功能关联'
        verbose_name_plural = verbose_name
