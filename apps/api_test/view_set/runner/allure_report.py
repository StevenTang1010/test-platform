#!/usr/bin/python
# -*- coding:utf-8 _*- 
"""
@author:TXU
@file:allure_report.py
@time:2021/09/13
@email:tao.xu2008@outlook.com
@description: 根据allure测试结果生成测试报告 --弃用
"""
import os
from loguru import logger
from rest_framework.views import APIView
from apps.api_test.view_set.base import JsonResponse


def generate_allure(data):
    """
    生成 allure 报告
    :param data: TestReport表数据
    :return:
    """
    allure_xml_path = data.get('allure_xml_path', '')
    allure_html_path = data.get('allure_html_path', '')
    if not allure_xml_path:
        return "没有找到pytest测试结果数据"
    # 生成allure报告
    cmd = f'allure generate {allure_xml_path} -o {allure_html_path} --clean'
    try:
        logger.info(f"  ******  开始生成测试报告  ******  \n {cmd}")
        os.popen(cmd)
        return "生成allure报告成功：{}".format(allure_html_path)
    except Exception as e:
        msg = '生成allure报告失败:\n'.format(e)
        logger.error(msg)
        return msg


def generate_allure_by_jenkins(data):
    """
    通过jenkins生成 allure 报告
    :param data: TestReport表数据
    :return:
    """
    # TODO


def is_allure_report_exist(data):
    """
    allure报告 是否存在
    :param data:
    :return:
    """
    allure_html_path = data.get('allure_html_path', '')
    if os.path.exists(allure_html_path):
        return True
    return False


def get_allure(data):
    """
    获取allure报告
    :param data:
    :return:
    """
    allure_html_path = data.get('allure_html_path', '')
    if not os.path.exists(allure_html_path):
        raise Exception("allure报告路径不存在！")
    return os.path.join(allure_html_path, 'index.html')


class AllureGenerateView(APIView):

    def post(self, request, *args, **kwargs):
        """
        生成 allure 报告
        :param request:
        """
        response = generate_allure(request.data)
        return JsonResponse(response, status=200)

    def get(self, request, *args, **kwargs):
        """
        检查allure报告是否已存在，如存在返回报告地址
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        response = get_allure(request.data)
        return JsonResponse(response, status=200)


if __name__ == '__main__':
    pass
