# --------------------------------------
# Date: 2021/8/10
# @Author: Steven_Tang
# FileName: exception_handler.py   
# Description: 
# --------------------------------------
from django.http import Http404
from rest_framework import exceptions
from django.core.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import set_rollback


# 定义异常请求处理
def exception_handler(exc, context):
    """
    Returns the response that should be used for any given exception.

    By default we handle the REST framework `APIException`, and also
    Django's built-in `Http404` and `PermissionDenied` exceptions.

    Any unhandled exceptions may return `None`, which will cause a 500 error
    to be raised.
    """
    if isinstance(exc, Http404):
        exc = exceptions.NotFound()
    elif isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()

    if isinstance(exc, exceptions.APIException):
        headers = {}
        if getattr(exc, 'auth_header', None):
            headers['WWW-Authenticate'] = exc.auth_header
        if getattr(exc, 'wait', None):
            headers['Retry-After'] = '%d' % exc.wait

        if isinstance(exc.detail, (list, dict)):
            if isinstance(exc.detail, list):
                errors = exc.detail
            else:
                errors = {k: v[0] for k, v in exc.detail.items()}
        else:
            errors = exc.detail

        set_rollback()
        return Response({'code': 0, 'msg': 'failed', 'errors': errors, 'data': []}, status=exc.status_code,
                        headers=headers)

    return None
