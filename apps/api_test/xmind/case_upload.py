"""@author:sh
@file:update.py
@time:2021/11/27
@email:
@description: file upload and download
"""
import json
import os
import re
import copy
from enum import Enum
from collections import defaultdict

from xmindparser import xmind_to_dict
from django.conf import settings
from apps.api_test import logger
from apps.api_test.xmind.exceptions import FileTypeError, FileImportError, FileParseError
from apps.api_test.models import TestSuite, TestCase, TestStep, ApiInfo
from runner.core.utils import to_class_name, to_safe_name


VALIDATETYPE = [
    "eq",  # 验证元素值等于
    "neq",  # 验证元素值不等于
    "ne",  # 验证元素值不等于
    "contain",  # 验证元素的字符串值中包含字符串"xxx"
    "contain_if_exist",  # 如果获取到元素不为空，则验证元素的字符串值中包含字符串"xxx"
    "in_list",  # 验证列表元素包含字符串"xxx"
    "not_in_list",  # 验证列表元素不包含字符串"xxx"
    "has_key",  # 验证字典元素包含的key或key列表
]


# 用例类型枚举值
class CaseTypt(Enum):
    CASETYPE = '0'
    APITYPE = '1'


# 导入方式
class UploadTypt(Enum):
    INTELLIGENT = '0'
    COMPLETE = '1'


BASE_DIR = os.path.join(os.getcwd() + settings.STATIC_URL + r"case_data/")
HOST_TAG_CHOICE = ["mk", "qw", "bill", "qyapi"]  # 对应 host_<mk/qw>
PRIORITY_TAG_CHOICE = ["critical", "blocker", "normal"]
UPLOAD_FILE_TYPE_CHOICE = ("xmind", )


class ReadXmind(object):
    """读取xmind内容，返回字典列表（list[dict1,dict2]）"""
    def __init__(self, file_path, canvas=""):
        logger.info("读取并解析xmind文件：{}".format(file_path))
        self.file_path = file_path
        self.canvas = canvas
        self.xmind_dict_list = xmind_to_dict(file_path)

    def get_canvas_name_list(self):
        return [self.canvas] if self.canvas else [cv.get('title') for cv in self.xmind_dict_list]

    def get_canvas_topic(self, canvas="画布 1"):
        """
        根据初始指定的画布名称（对应于excel的sheel表），返回该画布的数据
        :return: {'title': '', 'topics': []}
        """
        for cv in self.xmind_dict_list:
            if cv.get('title') == canvas:
                return cv.get('topic')
        else:
            raise Exception("Xmind中画布<{}>不存在!".format(canvas))

    def get_canvas_data(self, canvas):
        """
        获取画布内所有API-STEP信息
        :param canvas: 画布名称（对应一个用例）
        :return: eg:
        {
            'case_name': 'DistributionSideBar',
            'case_desc': '分销：企微',
            'api_list': [
                {
                    'api_name': 'waitPage',
                    'api_desc': '分销员待审核列表',
                    'path': '',
                    'method': '',
                    'req_headers': '',
                    'req_params': '',
                    ...
                    'step_list': [
                        {
                            'name': '',
                            'req_params': ''
                            ...
                        }
                    ]
                }
            ]
        }
        """

        case_data = {}
        api_step_dict_list = []
        canvas_topic = self.get_canvas_topic(canvas)
        case_name = canvas_topic.get('title')
        case_data['case_desc'] = canvas
        case_data['case_name'] = case_name
        api_list = canvas_topic.get('topics') or []
        for api in api_list:
            api_dict = {}
            api_name = api.get('title') if api.get('title') else ""
            api_desc = api.get('note') if api.get('note') else ""
            api_labels = api.get('labels')  # depends、host、sleep
            api_dict['api_name'] = api_name
            api_dict['api_desc'] = api_desc
            api_dict['depends'] = []  # depends 依赖标签
            api_dict['sleep'] = 0  # sleep 标签
            api_dict['skipif'] = ""  # skipif 标签
            host_tag = "host_" + HOST_TAG_CHOICE[0]  # host 标签
            if api_labels:
                for alb in api_labels:
                    lb_dps = alb.split("depends=")
                    lb_dps2 = alb.split("name=")
                    lb_sleep = alb.split("sleep=")
                    lb_skipif = alb.split("skipif=")
                    lb_host = alb.split("host=")
                    if len(lb_dps) == 2:
                        api_dict['depends'].append(lb_dps[-1])
                    if len(lb_dps2) == 2:
                        api_dict['depends'].append(lb_dps2[-1])
                    if len(lb_sleep) == 2:
                        api_dict['sleep'] = int(lb_sleep[-1])
                    if len(lb_skipif) == 2:
                        api_dict['skipif'] = lb_skipif[-1]
                    if len(lb_host) == 2 and lb_host[-1] in HOST_TAG_CHOICE:
                        host_tag = "host_" + lb_host[-1]
            api_dict['host_tag'] = host_tag
            api_detail = api.get('topics')[0]
            path = api_detail.get('title') or ""
            rq = api_detail.get('topics')[0]
            method = rq.get('title') or ""
            api_dict['path'] = path
            api_dict['method'] = method

            api_dict['step_list'] = []
            step_cf_list = rq.get('topics')
            if api_name.startswith('#'):  # 被注释掉的接口，不解析用例参数
                continue
            for idx, step in enumerate(step_cf_list):
                if step.get('title').startswith('#'):  # 被注释掉的用例
                    continue
                step_dict = {}
                step_labels = step.get('labels')  # priority
                step_dict['host_tag'] = host_tag  # host_qw / host_mk
                step_dict['depends'] = api_dict['depends']  # api依赖
                step_dict['sleep'] = api_dict['sleep']  # api sleep
                step_dict['skipif'] = api_dict['skipif']  # api skipif
                step_dict['step_name'] = api_name  # f"{api_name}_" + str(idx+1).zfill(3)  # case名
                step_dict['step_desc'] = step.get('title')  # 描述
                step_dict['priority'] = "normal"  # 优先级
                if step_labels:
                    for clb in step_labels:
                        if clb in PRIORITY_TAG_CHOICE:
                            step_dict['priority'] = clb
                            break
                # 输入
                step_input_output = step.get('topics')[0]
                str_req = step_input_output.get('title')  # 输入
                step_dict['req_headers'] = {}
                step_dict['req_params'] = {}
                step_dict['req_json'] = {}
                step_dict['req_data'] = {}
                formatted_str_req = replace_str(str_req)
                try:
                    req_data = json.loads(formatted_str_req, strict=False)  # 输入
                except Exception as e:
                    logger.error("API:{0}->{1}\nJSON Content:{2}".format(case_name, api_name, formatted_str_req))
                    raise e
                else:
                    data_keys = req_data.keys()
                    if len(data_keys) > 0 and set(data_keys).issubset({"params", "json", "data"}):  # 即传入参数指定了参数类型
                        if 'params' in req_data:
                            step_dict['req_params'] = req_data['params']
                        if 'json' in req_data:
                            step_dict['req_json'] = req_data['json']
                        if 'data' in req_data:
                            step_dict['req_data'] = req_data['data']
                    elif method == "GET":
                        step_dict['req_params'] = req_data
                    else:
                        step_dict['req_json'] = req_data

                # 输出
                step_dict['validator'] = {}
                output_set_vars = step_input_output.get('topics')
                str_expect = output_set_vars[0].get('title')
                try:
                    res_data = json.loads(str_expect, strict=False)  # 输出
                except Exception as e:
                    logger.error("API:{0}->{1}\nJSON Content:{2}".format(case_name, api_name, str_expect))
                    raise e
                else:
                    validator = copy.deepcopy(res_data)
                    for k, v in res_data.items():
                        if v in ['', {}, []]:
                            # 历史问题：无效校验，去除
                            validator.pop(k)
                    exp_keys = validator.keys()
                    if not set(exp_keys).issubset(set(VALIDATETYPE)):
                        # 配置默认比较方法：eq
                        step_dict['validator'] = {"eq": validator}
                    else:
                        step_dict['validator'] = validator

                # 变量提取
                step_dict['extractor'] = {}
                if len(output_set_vars) > 1:
                    str_extractor = output_set_vars[1].get('title')
                    try:
                        step_dict['extractor'] = json.loads(str_extractor, strict=False)  # 需要设置为全局的变量，key-value， key为保存变量名，value为字段查询名或jsonpath
                    except Exception as e:
                        logger.error("API:{0}->{1}\nJSON Content:{2}".format(case_name, api_name, str_extractor))
                        raise e

                api_dict['step_list'].append(dict(step_dict))
            api_step_dict_list.append(api_dict)

        case_data['api_list'] = api_step_dict_list
        return case_data

    def get_xmind_data(self):
        """
        获取xmind文件数据
        :return: [{case1}, {case2}]
        """
        return [self.get_canvas_data(cv) for cv in self.get_canvas_name_list()]


class FileImportHandle:
    def __init__(self, file_req, file_type="xmind"):
        self.req = file_req
        if not os.path.exists(BASE_DIR):
            os.makedirs(BASE_DIR)
        self.file_path = BASE_DIR + self.req.name
        self.file_type = file_type
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

    def dist_file(self):
        with open(self.file_path, 'wb+') as f:
            for ch in self.req.chunks():
                f.write(ch)
        return True

    def handle_file(self):
        if self.file_type not in UPLOAD_FILE_TYPE_CHOICE:
            raise FileTypeError("文件类型不支持, 请重新上传!")
        try:
            self.dist_file()
            return self.file_path
        except Exception as e:
            raise FileImportError(e)


def replace_str(target):
    """
    字符串数据处理（请求输入、输出、）
    :param target:
    :return:
    """
    # 去掉\r\n和空格符
    target = target.replace(" ", "").replace("\t", "").replace("\n", "").replace("\r", "")
    # $var --> "$var"
    variable_regex_compile = re.compile(r'[^"](\$\w+)[,}]')
    try:
        match_start_position = target.index("$", 0)
    except ValueError:
        return target

    while match_start_position < len(target):
        var_match = variable_regex_compile.match(target, match_start_position - 1)
        if var_match and "\\" not in target[match_start_position-3:match_start_position]:
            # 找到$var格式变量且对应key值不包含\符（包含\符可能是）
            var_name = var_match.group(1)
            target = target[0:match_start_position] + '"{}"'.format(var_name) + target[var_match.end() - 1:]
            match_start_position = var_match.end()
            continue

        curr_position = match_start_position
        try:
            # find next $ location
            match_start_position = target.index("$", curr_position + 1)
        except ValueError:
            # break while loop
            break
    return target


class DataInsertHandle:
    def __init__(self, file_path, file_type='', file_name='', data_type="", load_type="0", department=None):
        self.file_path = file_path
        self.file_name = file_name or os.path.basename(file_path).split('.')[0]
        self.file_type = file_type or file_path.split('.')[-1]
        self.data_type = data_type
        self.load_type = load_type
        self.department = department

        self.suite_name = self.file_name
        self.api_origin = self.file_type

    def parse_file(self) -> list:
        try:
            if self.file_type.lower() == "xmind":
                return ReadXmind(self.file_path).get_xmind_data()
        except Exception as e:
            raise FileParseError(e)

    def insert(self):
        """
        处理导入的文件插入数据库
        :return:
        """
        response = {"test_suite": self.suite_name, 'test_cases': defaultdict(int)}
        case_list = self.parse_file()
        try:
            # 插入用例集TestSuite
            suite_objs = TestSuite.objects.filter(name=self.suite_name)
            if suite_objs.count() == 0:
                logger.info("插入用例集TestSuite: {}".format(self.suite_name))
                suite_obj = TestSuite(
                    name=self.suite_name,
                    safe_name=to_safe_name(self.suite_name),
                    department_id=self.department
                )
                suite_obj.save()
            else:
                suite_obj = suite_objs.first()
            # 插入用例
            for case in case_list:
                case_name = case["case_name"]
                case_desc = case["case_desc"]
                case_info = {
                    "name": case_name,
                    "safe_name": to_class_name(case_name),
                    "description": case_desc,
                    "test_suite": suite_obj
                }
                # 插入测试用例TestCase
                case_objs = TestCase.objects.filter(name=case_name, test_suite__name=self.suite_name)
                if case_objs.count() == 0:
                    logger.info("插入测试用例TestCase: {}->{}".format(self.suite_name, case_name))
                    case_obj = TestCase.objects.create(**case_info)
                else:
                    if self.load_type == UploadTypt.COMPLETE.value:
                        logger.info("更新测试用例TestCase: {}->{}".format(self.suite_name, case_name))
                        case_objs.update(**case_info)
                    case_obj = case_objs.first()

                # 插入/更新接口
                idx = 0
                for api in case.get("api_list"):
                    # 待插入/更新 接口信息
                    api_name = api["api_name"]
                    method = api["method"]
                    path = api["path"]
                    api_info = {
                        'name': api_name,
                        'description': api["api_desc"],
                        'path': path,
                        'method': method,
                        'origin': self.api_origin
                    }
                    step_list = api.get('step_list', [])
                    if step_list:
                        step_template = step_list[0]
                        api_info.update({
                            "req_params": step_template.get("req_params", {}),
                            "req_data": step_template.get("req_data", {}),
                            "req_json": step_template.get("req_json", {}),
                            "validator": step_template.get("validator", {}),
                        })

                    # 插入接口信息ApiInfo
                    api_objs = ApiInfo.objects.filter(method=method, path=path)
                    if api_objs.count() == 0:
                        logger.info("插入接口信息ApiInfo: {} {} {}".format(api_name, method, path))
                        api_obj = ApiInfo.objects.create(**api_info)
                    else:
                        # 完全覆盖--将匹配的api全部更新，智能合并--不再插入数据
                        if self.load_type == UploadTypt.COMPLETE.value:
                            logger.info("更新接口信息ApiInfo: {} {}".format(api_name, method, path))
                            api_objs.update(**api_info)
                        api_obj = api_objs.first()

                    # 插入测试用例步骤 TestStep
                    for step in step_list:
                        idx += 1
                        step_name = step.get('step_name')
                        step_info = {
                            'name': step.get('step_name'),
                            'description': step.get('step_desc'),
                            'sid': idx,
                            'test_case': case_obj,
                            'apiInfo': api_obj,
                            'req_params': json.dumps(step.get('req_params', '{}'), ensure_ascii=False),
                            'req_json': json.dumps(step.get('req_json', '{}'), ensure_ascii=False),
                            'req_data': json.dumps(step.get('req_data', '{}'), ensure_ascii=False),
                            'validator': json.dumps(step.get('validator', '{}'), ensure_ascii=False),
                            'extractor': json.dumps(step.get('extractor', '{}'), ensure_ascii=False)
                        }
                        step_objs = TestStep.objects.filter(
                            sid=idx, name=step_name, test_case_id=case_obj.id, apiInfo_id=api_obj.id)
                        if step_objs.count() > 0:
                            logger.info("更新测试步骤TestStep: {}->{}->{}".format(case_name, idx, step_name))
                            step_objs.update(**step_info)
                        else:
                            logger.info("插入测试步骤TestStep: {}->{}->{}".format(case_name, idx, step_name))
                            TestStep.objects.create(**step_info)
                response['test_cases'][case_name] = idx
            return response
        except Exception as e:
            raise Exception("数据插入故障：{}".format(e))
