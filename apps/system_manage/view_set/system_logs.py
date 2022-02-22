#!/usr/bin/python
# -*- coding:utf-8 _*- 
"""
@author:TXU
@file:system_logs.py
@time:2022/01/07
@email:tao.xu2008@outlook.com
@description: 系统日志
"""
import logging
import os
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin
from rest_framework.viewsets import GenericViewSet
from django.conf import settings

from apps.api_test.view_set.base import JsonResponse

logger = logging.getLogger()


# 获取文件最后N行的函数
def tail_log(file_path, tail_num=0):
    tail_lines = ""
    with open(file_path, 'r', encoding='utf-8') as f:
        if tail_num == 0:
            tail_lines = f.read()
        else:
            file_size = os.path.getsize(file_path)
            block_size = 10240
            if file_size > block_size:
                max_seek_point = (file_size // block_size)
                f.seek((max_seek_point - 1) * block_size)
            elif file_size:
                f.seek(0, 0)

            lines = f.readlines()
            if lines:
                # tail_lines = lines[-1].strip()
                tail_lines = ''.join(lines[-tail_num:])

    return tail_lines


class SystemLogsViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    """获取 系统日志 内容"""
    def retrieve(self, request, *args, **kwargs):
        """获取 log 内容"""
        # logger.info(request.query_params)
        f_name = kwargs.get('pk')  # message | error | api_test
        tail_num = int(request.query_params.get('tail_num', 0))
        file_name = f_name + '.log'
        log_path = os.path.join(settings.BASE_DIR, 'logs', file_name)
        try:
            logger.info('读取日志：{}'.format(log_path))
            # with open(log_path, 'r', encoding='utf-8') as f:
            #     page = f.read()
            page = tail_log(log_path, tail_num)
            return JsonResponse(page.encode(encoding='utf-8'), status=200)
        except Exception as e:
            print(e)
            return JsonResponse(str(e), status=200)


if __name__ == '__main__':
    pass
