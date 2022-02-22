#!/usr/bin/python
# -*- coding:utf-8 _*- 
"""
@author:TXU
@file:run_pytest.py
@time:2022/01/10
@email:tao.xu2008@outlook.com
@description:
"""
import json
import os
import atexit
import traceback

import subprocess
from loguru import logger
from django.conf import settings
from datetime import datetime

from apps.api_test import logger as api_test_logger
from apps.api_test.models import TestReport, AppSetting
from apps.api_test.view_set.runner.converter import load_suite_data, load_case_data, load_step_data
from runner.pkgs.retry import retry
from runner.core.debug_data import DebugData
from runner.core.maker import main_make
from runner.core.utils import get_mac_address, to_safe_name, seconds_to_hms, rm_tree, zfill
from runner.config import cf, root_dir, report_path, testcase_path, testcase_max_rotation, ReportAttr
from runner.common.gen_mock_data import update_mock_data
from runner.common.get_env_data import update_env_data
from common.jenkins_opt import JenkinsOperation

default_filters = {
    # 不做进一步筛选
    '其他': {},
    # 巡检测试筛选规则：所有接口用例(场景用例+单接口用例：P0/P1/P2/P3)，即不筛选
    '业务巡检': {
        'test_case': {
            'department__in': '1,2,3,5,6,7,8'  # 临时去掉平台组的用例 -- 正式环境未开通获取bill session
        }
    },
    # 冒烟测试筛选规则：单接口用例（P0） + 场景用例  # TODO
    '冒烟测试': {},
    # 环境验证测试筛选规则：单接口用例，且P0：核心接口正向测试
    '环境验证': {
        'test_case': {
            'type': '单接口测试',
            'labels__name__contains': 'P0'
        }
    }
}


def __get_app_setting():
    try:
        app_setting = AppSetting.objects.first().data
        return app_setting
    except Exception as e:
        api_test_logger.error(e)
        return {}


def __rm_rotation_files():
    app_setting = __get_app_setting()
    tc_max_rotation = app_setting.get("testcase_max_rotation", 0) or testcase_max_rotation

    # - 删除旧的测试构建文件
    log_path = os.path.join(settings.BASE_DIR, "logs/runner/")

    # testcase/test_*
    rm_tree(testcase_path, "test_*", max_rotation=tc_max_rotation)
    # reports/*
    rm_tree(report_path, "*", max_rotation=tc_max_rotation)
    # logs/runner/*
    rm_tree(log_path, "*", max_rotation=tc_max_rotation)


def __create_new_report(time_str, build_type, env_id, env_name):
    report = TestReport.objects.create(
        **{
            "create_time": datetime.strptime(time_str, "%Y-%m-%d-%H-%M-%S-%f"),
            "build_type": build_type,
            "env_id": env_id
        }
    )
    log_path = os.path.join(
        settings.BASE_DIR,
        "logs/runner/"
        '{}-{}-{}-message.log'.format(zfill(report.id), to_safe_name(env_name), time_str)
    )
    report.log_path = log_path
    report.save()

    return report.id, log_path


def __parse_request_data(data):
    """
    解析请求数据，生成用例数据列表，[department::suite_list::case_list]
    :param data:
    :return:
    """
    # logger.debug(data)
    if not data:
        dept_data_list = DebugData().data_list
    else:
        env = data.get("env", {})
        validate = data.get("validate", {})
        level = data.get("level", "test_suite")
        build_type = data.get("build_type", "其他")
        body_list = data.get("list", [])  # 测试数据列表或字符串"all"
        filters = data.get("filters", {}) or {}
        if not env:
            msg = "参数错误！无环境配置"
            logger.error(msg)
            raise msg
        env_id = env['id']

        if not validate:
            msg = "参数错误！无校验规则"
            logger.error(msg)
            raise Exception(msg)
        validate_id = validate['id']

        if len(body_list) == 0:
            msg = "参数错误！无测试数据"
            logger.error(msg)
            raise Exception(msg)

        # 更新测试类型对应的用例筛选规则
        ext_filters = default_filters[build_type]
        filters.update(**ext_filters)

        # 更新测试环境Mock数据
        update_mock_data(env_id)
        # 更新测试环境session数据
        update_env_data(env_id)

        if level == 'test_case':
            dept_data_list = load_case_data(env_id, validate_id, body_list, filters)
        elif level == 'test_suite':
            dept_data_list = load_suite_data(env_id, validate_id, body_list, filters)
        elif level == 'test_step':
            dept_data_list = load_step_data(env_id, validate_id, body_list, filters)
        else:
            msg = "参数错误！level:test_case|test_suite"
            logger.error(msg)
            raise Exception(msg)
    return dept_data_list


def __run_with_data(data, report_id, log_path, log_level):
    """
    执行pytest
    :param data:前端传回参数，{"env": {}, "validate": {}, "level": "test_case", "list": []}
    :param report_id: 报告ID
    :param log_path: 日志路径
    :param log_level: 日志level
    :return:
    """
    report_attr = ReportAttr(report_id)

    # - 删除旧的测试构建文件
    __rm_rotation_files()

    # - 解析请求数据
    try:
        dept_data_list = __parse_request_data(data)
    except Exception as e:
        raise e

    # - 生成测试py文件
    pytest_files_run_set = main_make(dept_data_list, report_attr.testcase_path)
    logger.info(json.dumps(pytest_files_run_set, indent=2, ensure_ascii=False))

    # - 获取数据库信息，并传入pytest
    default_db = settings.DATABASES.get('default')
    db_info = {
        "ENGINE": default_db.get('ENGINE'),
        "DB_PATH": "",
        "USER": "",
        "PASSWORD": "",
        "HOST": "",
        "PORT": "",
        "NAME": "",
    }
    if default_db.get('ENGINE') == 'django.db.backends.sqlite3':
        db_info["DB_PATH"] = os.path.abspath(os.path.join(root_dir, '../db.sqlite3'))
    elif default_db.get('ENGINE') == 'django.db.backends.mysql':
        db_info["USER"] = default_db.get('USER')
        db_info["PASSWORD"] = default_db.get('PASSWORD')
        db_info["HOST"] = default_db.get('HOST')
        db_info["PORT"] = default_db.get('PORT')
        db_info["NAME"] = default_db.get('NAME')

    # - 构建pytest 参数

    argv = pytest_files_run_set + [
        '--log_path={}'.format(log_path),
        '--log_level={}'.format(log_level),
        '--db_info={}'.format(json.dumps(db_info)),
        '--report_id={}'.format(report_id),
        '-v', '-s', '--ignore-unknown-dependency',
        '-W', 'ignore:Module already imported:pytest.PytestWarning',
        '--html={}'.format(report_attr.html_report_path),
        '--self-contained-html',
        # '--capture=sys',
        '--allure-no-capture',  # 取消添加程序中捕获到控制台或者终端的log日志或者print输出到allure测试报告的Test Body中
        '--alluredir={}'.format(report_attr.xml_report_path), '--clean-alluredir',  # 生成allure xml结果
    ]
    # -q test_01.py

    # - 执行pytest
    # 执行方式一
    # import pytest
    # pytest.main(argv)
    # err_msg = ''
    # exit_code = 0

    # 执行方式二
    p = subprocess.Popen(['pytest'] + argv)
    p.wait()

    # - 获取结果并返回
    reports = TestReport.objects.filter(id__exact=report_id)
    if reports.count() == 0:
        raise Exception("未找到测试报告：{}".format(report_id))

    report = reports.first()
    report_id = report.id

    summary = {
        "status": report.status,
        "total": report.step_total,
        "pass": report.step_passed,
        "failed": report.step_failed,
        "error": report.step_error,
        "skipped": report.step_skipped,
        "pass_rate": "{}%".format(report.step_pass_rate*100),
        "duration": seconds_to_hms(report.duration)
    }
    return report_id, summary


@retry(tries=3, delay=3)
def __generate_allure_report(report_id):
    """
    从测试报告表中读取测试结果数据，生成allure报告。
    服务器运行：通过Jenkins生成allure报告
    本地运行：allure serve命令立即生成allure报告
    :param report_id:
    :return:
    """
    try:
        api_test_logger.info("generate allure report...")
        xml_report_path = ReportAttr(report_id).xml_report_path
        if get_mac_address() == '00:16:3e:17:7c:40':
            # 47.99.145.123 服务器运行
            if not report_id:
                api_test_logger.error("无测试结果记录，跳过报告生成！")
                return
            # 创建配置对象为全局变量
            jenkins_conf = cf.get_kvs('JENKINS')
            job_name = jenkins_conf.get('job_name')
            token = jenkins_conf.get('token')
            jenkins_opt = JenkinsOperation(
                url=jenkins_conf.get('url'),
                user=jenkins_conf.get('user'),
                password=jenkins_conf.get('password'),
            )
            parameters = {
                'xml_report_path': xml_report_path
            }
            api_test_logger.info(xml_report_path)
            # 获取jenkins下一次build number并立即构建
            build_number = jenkins_opt.get_next_build_number(job_name)
            number = jenkins_opt.trigger_build_job(job_name, parameters, token)
            api_test_logger.info(number)
            # allure_url = jenkins_opt.get_build_allure_url(job_name, build_number)
            # 保存jenkins job/build信息到测试报告表，便于后期读取
            TestReport.objects.filter(id__exact=report_id).update(
                client='47.99.145.123',
                jenkins_job_name='test-platform-report',
                jenkins_build_number=build_number,
                # allure_url=allure_url
            )
        else:
            # 本地调试
            allure_serve_cmd = 'allure serve {}'.format(xml_report_path)
            api_test_logger.info(allure_serve_cmd)
            subprocess.Popen(allure_serve_cmd, shell=True, close_fds=True)
            # p.wait()
    except Exception as e:
        api_test_logger.error(e)


def run_pytest_with_logger(data):
    api_test_logger.info('Call run_pytest_with_logger')
    # 创建报告 - 供后续数据跟踪
    try:
        env = data.get("env")
        env_id = env['id']
        env_name = env['name']
        build_type = data.get("build_type", "其他")
        time_str = datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f")  # 时间字符串，报告、日志唯一标识符
        # 创建报告 - 后续数据跟踪 report.id
        report_id, log_path = __create_new_report(time_str, build_type, env_id, env_name)
        log_level = __get_app_setting().get("file_log_level", "") or cf.get_str("LOGGER", "file_level") or "DEBUG"
    except Exception as e:
        raise e

    # 添加logger并执行测试。注：此处logger仅作用于pytest执行前的数据加载，pytest执行为新进程，需传相同log_path并在新进程中创建logger
    handler_id = None
    try:
        handler_id = logger.add(
            log_path,
            rotation='100 MB',
            retention='7 days',
            enqueue=True,
            encoding="utf-8",
            level=log_level
        )
        atexit.register(logger.remove)
        return __run_with_data(data, report_id, log_path, log_level)
    except Exception as e:
        raise e
    finally:
        logger.info("generate test log: {}".format(log_path))
        xml_report_path = ReportAttr(report_id).xml_report_path
        logger.info("result data path: {}".format(xml_report_path))
        try:
            logger.remove(handler_id)
        except Exception as e:
            api_test_logger.error(e)

        reports = TestReport.objects.filter(id__exact=report_id)
        if reports.count() > 0:
            report = reports.first()
            # 0执行，标记为 - 失败; 否则，生成报告
            if report.step_total == 0:
                # 无测试步骤被执行，标记为 - 失败
                report.status = False
                report.build_status = 'build-status-static'
                report.duration = 1
                report.save()
            else:
                # 生成报告
                __generate_allure_report(report_id)


def run_with_filters(env: dict, validate: dict, level: str, filters: dict):
    """
    执行测试，传参：环境、校验规则、级别、筛选器  -- 仅定时任务调用
    :param env: 测试环境
    :param validate: 校验规则
    :param level: 测试级别， test_suite | test_case | test_step
    :param filters: 注意，需要是符合规则的筛选器
    :return:
    """
    api_test_logger.warning(filters)

    data = {
        'env': env,
        'validate': validate,
        'level': level,
        'list': 'all',
        'filters': filters
    }
    try:
        report_id, summary = run_pytest_with_logger(data)
        __generate_allure_report(report_id)
        api_test_logger.info('测试执行完成！(报告ID：{})\n'.format(report_id, json.dumps(summary, indent=2)))
        return
    except Exception as e:
        # raise e  # debug
        # s = traceback.format_exc().replace('\n', '</br>')
        api_test_logger.error(traceback.format_exc())
        return


if __name__ == '__main__':
    pass
