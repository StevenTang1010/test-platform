#!/usr/bin/python
# -*- coding:utf-8 _*- 
"""
@author:TXU
@file:converter.py
@time:2021/10/29
@email:tao.xu2008@outlook.com
@description: 测试用例信息转换为runner格式对应的DICT
"""
import copy
from pypinyin import lazy_pinyin
from typing import Dict, List
from collections import defaultdict
from loguru import logger

from django.db import models
from apps.api_test.models import GlobalEnv, GlobalResponseValidate, Department, TestSuite, TestCase, TestStep
from apps.api_test.filters import TestSuiteFilter, TestCaseFilter, TestStepFilter
from runner.core import utils
from runner.core.builtin.comparators import comparators_define

"""
解析数据库查询返回的数据，转成字典List[Dict]:
    [
        {
            "name": "部门A"，
            "test_suite_list": [
                {
                    "name": "Suite1",
                    "test_case_list": [
                        "name": "case-1"
                        "test_step_list": [
                            "name": "step-1",
                            "method": "POST"
                            "path": "/api/test/login"
                        ]
                    ]
                }
            ]
        }
    ]
"""


RESPONSE_KEYS = ('body', 'cookies', 'headers', 'status_code')
COMPARATOR_KEYS = []
for _, keys, _ in comparators_define:
    COMPARATOR_KEYS.extend(keys)


def __is_objects_queryset(objects):
    """
    判断 objects 类型是否为 django.db.models.query.QuerySet
    QuerySet | List
    :param objects:
    :return:
    """
    if isinstance(objects, models.query.QuerySet):
        qs = True
    elif isinstance(objects, list):
        if not objects:
            raise Exception("参数错误！测试数据列表为空！")
        qs = False
    else:
        raise Exception("不支持的测试数据类型：{}".format(type(objects)))
    return qs


def _format_config(env_id, base_url_tag='base_url_mk') -> Dict:
    """格式化测试配置信息"""
    env = GlobalEnv.objects.get(id__exact=env_id)
    data = {
        "name": "",
        "verify": False,
        "base_url": env.config.get(base_url_tag).get("value"),
        "variables": dict(**env.config, **env.qw_external_contact_config, **env.data, **env.mock),
        "parameters": {},
    }
    return data


def _format_global_validator(global_validate_id) -> (List, bool):
    """格式化测试配置信息"""
    validate_list = []
    validate = GlobalResponseValidate.objects.get(id__exact=global_validate_id)
    if validate.check_status_code and validate.status_code:
        validate_list.append(
            {"contained_by": ["status_code", [int(sc) for sc in validate.status_code.split(',')]]}
        )
    return validate_list, validate.check_response_data


def _format_step_validator(validator: dict, check: bool = True) -> List:
    """
    1. validator如果没有比较方法，默认设置为eq，即相等
    2. 遍历validator kv比较内容，转换字典为列表，如：[{'eq':[expr, expect]}]
    :param validator:
    :param check:
    :return:
    """
    validator_list = []
    if not check:
        return validator_list
    # validator如果没有比较方法，默认设置为eq，即相等
    vd_keys = validator.keys()
    if not set(vd_keys).issubset(set(COMPARATOR_KEYS)):
        validator = {"eq": validator}

    # 遍历validator kv比较内容，转换字典为列表，如：[{'eq':[expr, expect]}]
    for compare, kv in validator.items():
        for expr, v in kv.items():
            expr_split = expr.split('.')
            if expr.startswith('$..'):
                if expr_split[2] not in RESPONSE_KEYS:
                    expr = expr.replace('$..', '$..body.')
            elif expr_split[0] not in RESPONSE_KEYS:
                expr = 'body.' + expr
            validator_list.append({compare: [expr, v]})

    # logger.debug(validator_list)
    return validator_list


def _format_steps(env, case_id=None, step_ids=None, global_validator=None, check_data=True, filters: dict = None) -> List[Dict]:
    if global_validator is None:
        global_validator = []
    t_steps = []
    step_filters = copy.deepcopy(filters.get('test_step', {}) if filters else {})  # 筛选项
    if case_id:
        step_filters.update({"test_case_id__exact": case_id})
    if step_ids:
        step_filters.update({"id__in": step_ids})
    steps = TestStep.objects.filter(**step_filters)

    for step in steps.order_by('sid'):
        if not step.status:  # skip
            continue
        # logger.debug("load test step: {}->{}".format(step.sid, step.name))
        try:
            req_headers = utils.json_loads_str(step.req_headers or '{}')
            req_params = utils.json_loads_str(step.req_params or '{}')
            req_json = utils.json_loads_str(step.req_json or '{}')
            req_data = utils.json_loads_str(step.req_data or '{}')
            validator = utils.json_loads_str(step.validator or '{}')
            extractor = utils.json_loads_str(step.extractor or '{}')
        except Exception as e:
            raise Exception("case(id:{}):{} -> step(sid:{}):{}\n{}".format(
                step.test_case.id, step.test_case.name, step.sid, step.name, e))

        # 置空则使用默认的 base_url
        base_url = ''
        base_url_tag = "base_url_" + step.apiInfo.host_tag
        if base_url_tag not in ['base_url_', 'base_url_mk']:
            base_url = env.config.get(base_url_tag).get("value")

        # validator 字典转列表
        validator_list = global_validator + _format_step_validator(validator, check_data)
        logger.error(step.depends.all())

        t_step = {
            "name": step.name,
            "id": step.id,
            "sid": step.sid,
            "description": step.description or step.name,
            "api_id": step.apiInfo.id,
            "api_description": step.apiInfo.description or step.apiInfo.name,
            "is_skip": not step.status,
            "is_api_valid": step.apiInfo.status,  # api状态： True/False
            "is_api_updated": step.apiInfo.update_status == 0,  # 更新状态： 待处理
            "testcase": None,
            "variables": {},
            "skipif": step.skipif or '',
            "depends": [d.id for d in step.depends.all() if d.sid < step.sid],
            "base_url": base_url,
            "request": {
                "method": step.apiInfo.method.upper(),
                "url": step.apiInfo.path + step.req_path_extend,
                "cookies": {},
                "headers": req_headers,
                "params": req_params,
                "json": req_json,
                "data": req_data
            },
            "setup_hooks": [{sh['var_name']: sh.get('hook_content')} for sh in step.setup_hooks if sh.get('var_name')] if step.setup_hooks else [],
            "teardown_hooks": [{th['var_name']: th.get('hook_content')} for th in step.teardown_hooks if th.get('var_name')] if step.teardown_hooks else [],
            "extract": extractor,
            "validate": validator_list,
            "validate_script": []
        }
        t_steps.append(t_step)

    return t_steps


def _format_case(env_id, case_id, step_ids=None, global_validator=None, check_data=True,
                 setup_tcs=None, teardown_tcs=None, filters: dict = None) -> Dict:
    """格式化测试用例信息"""
    if teardown_tcs is None:
        teardown_tcs = []
    if setup_tcs is None:
        setup_tcs = []
    case = TestCase.objects.get(id__exact=case_id)
    test_suite = case.test_suite
    dept_name = test_suite.department.name
    case_class_name = utils.to_class_name(case.safe_name)
    case_desc = utils.select_chinese_one([case.name, case.description])
    suite_desc = utils.select_chinese_one([test_suite.name, test_suite.description])
    logger.info("load test case: {}->{}->{}:{}".format(dept_name, suite_desc, case.id, case_desc))

    variables = utils.json_loads_str(case.variables or '{}')
    env = GlobalEnv.objects.get(id__exact=env_id)
    config = _format_config(env_id)
    config['name'] = case_class_name
    config['description'] = case_desc
    config['variables'].update(variables)
    config['department_name'] = dept_name
    config['suite_name'] = suite_desc
    config['case_id'] = case.id
    config['case_name'] = case_desc
    data = {
        "id": case_id,
        "config": config,
        "department": dept_name,
        "test_type": case.type,
        "tags": [t.name for t in case.labels.all()],
        "teststeps": _format_steps(env, case_id, step_ids, global_validator, check_data, filters=filters),
        "setups": [tc["testcase"]["config"]["name"] for tc in setup_tcs],
        "teardowns": [tc["testcase"]["config"]["name"] for tc in teardown_tcs],
    }
    return data


def _format_suite(env_id, global_validate_id, suite_id, case_ids=None, filters: dict = None) -> Dict:
    """格式化测试用例集信息"""
    global_validator, check_data = _format_global_validator(global_validate_id)
    suite = TestSuite.objects.get(id__exact=suite_id)
    logger.info("load test suite: {}->{}".format(suite.id, suite.name))
    config = _format_config(env_id)
    config['name'] = utils.to_safe_name(suite.safe_name)
    config['department_name'] = suite.department.name
    config['description'] = suite.description or suite.name

    def _format_testcase_ref(case_id):
        case_obj = TestCase.objects.get(id__exact=case_id)
        tc_ref = {
            "name": "{}_{}".format(str(case_id).zfill(3), utils.to_safe_name(case_obj.safe_name)),
            "testcase": _format_case(env_id, case_obj.id, None, global_validator, check_data, filters=filters)
        }
        return tc_ref

    setup_tcs, setup_class_tcs, teardown_tcs, teardown_class_tcs = [], [], [], []
    # 获取用例集下所有 setup
    for setup in suite.setup:
        if setup["id"]:
            setup_tcs.append(_format_testcase_ref(setup["id"]))

    # 获取用例集下所有 setup_class
    for setup_class in suite.setup_class:
        if setup_class["id"]:
            setup_class_tcs.append(_format_testcase_ref(setup_class["id"]))

    # 获取用例集下所有 teardown
    for teardown in suite.teardown:
        if teardown["id"]:
            teardown_tcs.append(_format_testcase_ref(teardown["id"]))

    # 获取用例集下所有 teardown_class
    for teardown_class in suite.teardown_class:
        if teardown_class["id"]:
            teardown_class_tcs.append(_format_testcase_ref(teardown_class["id"]))

    t_cases = []
    # 获取用例集下所有用例
    case_filters = copy.deepcopy(filters.get('test_case', {}) if filters else {})  # 筛选项
    if case_ids:
        case_filters.update({"id__in": case_ids})
    cases = TestCase.objects.filter(test_suite_id__exact=suite_id, **case_filters)
    for case in cases:
        if not case.status:  # skip
            continue
        if case.type in ['setup', 'teardown']:  # setup/teardown类型测试用例跳过执行
            continue
        t_case_ref = {
            "name": "{}_{}".format(str(case.id).zfill(3), utils.to_safe_name(case.safe_name)),
            "testcase": _format_case(env_id, case.id, None, global_validator, check_data, setup_tcs, teardown_tcs,
                                     filters=filters),
        }
        t_cases.append(t_case_ref)

    data = {
        "config": config,
        "testcases": t_cases,
        "setup_tcs": setup_tcs,
        "teardown_tcs": teardown_tcs,
        "setup_class_tcs": setup_class_tcs,
        "teardown_class_tcs": teardown_class_tcs,
    }
    return data


def _format_department() -> List[Dict]:
    """格式化web回传用例数据body，返回：部门->用例集->用例->步骤"""
    t_depts = []
    departments = Department.objects.all()
    for dept in departments:
        dept_name = utils.to_safe_name(dept.safe_name) if dept.safe_name else '_'.join(lazy_pinyin(dept.name))
        t_dept = {
            "id": dept.id,
            "name": dept_name,
            "testsuites": []
        }
        t_depts.append(t_dept)
    return t_depts


def load_suite_data(env_id, global_validate_id, objects, filters: dict = None) -> List[Dict]:
    """
    格式化web回传用例集数据body，返回：部门->用例集->用例->步骤
    :param env_id:
    :param global_validate_id:
    :param objects: all | django.db.models.query.QuerySet | List
    :param filters: Dict({"test_suite":"", "test_case":"", "test_step":""})
    :return:
    """
    suite_filters = filters.get('test_suite', {}) if filters else {}
    logger.info("suite_filters: {}".format(suite_filters))
    t_depts = _format_department()
    if objects == 'all':
        # objects = TestSuite.objects.filter(**suite_filters)
        objects = TestSuiteFilter(suite_filters).qs
        is_queryset = True
    else:
        is_queryset = __is_objects_queryset(objects)
        if is_queryset:
            # objects = objects.filter(**suite_filters)
            objects = TestSuiteFilter(suite_filters).filter_queryset(objects)

    for body in objects:
        suite_id = body.id if is_queryset else body['id']
        suite = _format_suite(env_id, global_validate_id, suite_id=suite_id)
        ts = TestSuite.objects.get(id__exact=suite_id)
        for idx, t_dept in enumerate(t_depts):
            if t_dept['id'] == ts.department.id:
                t_depts[idx]['testsuites'].append(suite)
                break
    return t_depts


def load_case_data(env_id, global_validate_id, objects, filters=None) -> List[Dict]:
    """
    格式化web回传用例数据body，返回：部门->用例集->用例->步骤
    :param env_id:
    :param global_validate_id:
    :param objects: all | django.db.models.query.QuerySet | List
    :param filters: Dict({"test_suite":"", "test_case":"", "test_step":""})
    :return:
    """
    case_filters = filters.get('test_case', {}) if filters else {}
    logger.info("case_filters: {}".format(case_filters))
    t_depts = _format_department()
    if objects == 'all':
        # objects = TestCase.objects.filter(**case_filters)
        objects = TestCaseFilter(case_filters).qs
        # logger.warning(objects)
        is_queryset = True
    else:
        is_queryset = __is_objects_queryset(objects)
        if is_queryset:
            # objects = objects.filter(**case_filters)
            objects = TestCaseFilter(case_filters).filter_queryset(objects)

    if is_queryset:
        suite_ids = list(set([body.test_suite.id for body in objects]))
        case_ids = [body.id for body in objects]
    else:
        suite_ids = list(set([body['test_suite']['id'] for body in objects]))
        case_ids = [body['id'] for body in objects]

    for suite_id in suite_ids:
        suite = _format_suite(env_id, global_validate_id, suite_id, case_ids=case_ids)
        ts = TestSuite.objects.get(id__exact=suite_id)
        for idx, t_dept in enumerate(t_depts):
            if t_dept['id'] == ts.department.id:
                t_depts[idx]['testsuites'].append(suite)
                break
    return t_depts


def load_step_data(env_id, global_validate_id, objects, filters=None) -> List[Dict]:
    """
    格式化web回传用例步骤数据body，返回：部门->用例集->用例->步骤
    :param env_id:
    :param global_validate_id:
    :param objects: all | django.db.models.query.QuerySet | List
    :param filters: Dict({"test_suite":"", "test_case":"", "test_step":""})
    :return:
    """
    step_filters = filters.get('test_step', {}) if filters else {}
    if objects == 'all':
        # objects = TestStep.objects.filter(**step_filters)
        objects = TestStepFilter(step_filters).qs
        is_queryset = True
    else:
        is_queryset = __is_objects_queryset(objects)
        if is_queryset:
            # objects = objects.filter(**step_filters)
            objects = TestStepFilter(step_filters).filter_queryset(objects)

    global_validator, check_data = _format_global_validator(global_validate_id)
    config = _format_config(env_id)
    config['name'] = 'MixedSteps'
    case_step_dict = defaultdict(list)
    for body in objects:
        step_id = body.id if is_queryset else body.get('id')
        case = body.test_case if is_queryset else body.get('test_case')
        case_id = case.id if is_queryset else case.get('id')
        case_step_dict[case_id].append(step_id)

    testcases = []
    for case_id, step_ids in case_step_dict.items():
        case = TestCase.objects.get(id__exact=case_id)
        testcases.append(
            {
                "name": utils.to_safe_name(case.safe_name),
                "testcase": _format_case(env_id, case_id, step_ids, global_validator, check_data)
            }
        )

    suite_config = copy.deepcopy(config)
    suite_config['name'] = 'mixed_steps'
    suite = {
        "config": suite_config,
        "testcases": testcases,
        "setup_tcs": [],
        "teardown_tcs": [],
        "setup_class_tcs": [],
        "teardown_class_tcs": [],
    }
    t_dept = {
        "id": 0,
        "name": 'mixed_department',
        "testsuites": [suite]
    }
    return [t_dept]


if __name__ == '__main__':
    pass
