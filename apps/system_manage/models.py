#!/usr/bin/python
# -*- coding:utf-8 _*-
"""
@author:TXU
@file:models.py
@time:2022/02/09
@email:tao.xu2008@outlook.com
@description:
"""

from django.db import models
# from django.contrib.auth.models import User
from apps.user_auth.models import UserProfile


# 团队部门表
class Department(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name='部门名称')
    safe_name = models.SlugField(default='',  blank=True, null=True, max_length=50, verbose_name='部门标识')  # 用作文件夹名
    leader = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, max_length=20,
                               verbose_name="负责人", related_name="dept_creator")
    members = models.ManyToManyField(UserProfile, blank=True, default=[], verbose_name='成员', related_name="dept_user")
    status = models.BooleanField(default=True, verbose_name='状态（1正常 0停用）')
    description = models.CharField(max_length=4096, blank=True, null=True, verbose_name='描述')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '部门'
        verbose_name_plural = '部门'
