#!/usr/bin/python
# -*- coding:utf-8 _*- 
"""
@author:TXU
@file:models.py
@time:2021/10/25
@email:tao.xu2008@outlook.com
@description: pydantic 数据模型定义

typing[类型提示]: https://docs.python.org/zh-cn/3/library/typing.html
pydantic[类型校验]: https://pydantic-docs.helpmanual.io/
用上这两个库就有点强类型语言的味儿了
泛型: https://docs.python.org/zh-cn/3/library/typing.html#generics
枚举: https://docs.python.org/zh-cn/3/library/enum.html
"""
import os
from enum import Enum
from typing import Any
from typing import Dict, Text, Union, Callable
from typing import List

from pydantic import BaseModel, Field
from pydantic import HttpUrl

Name = Text
Desc = Text
Url = Text
BaseUrl = Union[HttpUrl, Text]
VariablesMapping = Dict[Text, Any]
FunctionsMapping = Dict[Text, Callable]
Headers = Dict[Text, Text]
Cookies = Dict[Text, Text]
Verify = bool
Hooks = List[Union[Text, Dict[Text, Text]]]
Export = List[Text]
Validators = List[Dict]
Env = Dict[Text, Any]


class TestStatusEnum(Text, Enum):
    PASSED = 'passed'
    FAILED = 'failed'
    ERROR = 'error'
    SKIPPED = 'skipped'
    UNKNOWN = ''
    BROKEN = 'broken'  # 未使用


class MethodEnum(Text, Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"
    PATCH = "PATCH"
    CALL = "CALL"


class TConfig(BaseModel):
    """测试配置模型"""
    name: Name
    description: Desc = ''
    department_name: Text = ''  # 部门名称
    suite_name: Text = ''  # 用例集名称
    case_id: int = 0  # 用例ID
    case_name: Text = ''  # 用例名称
    verify: Verify = False
    base_url: BaseUrl = ""
    variables: Union[VariablesMapping, Text] = {}
    parameters: Union[VariablesMapping, Text] = {}
    export: Export = []
    path: Text = None
    weight: int = 1


class TRequest(BaseModel):
    """测试请求模型"""

    method: MethodEnum
    url: Url
    params: Dict[Text, Text] = {}
    headers: Headers = {}
    req_json: Union[Dict, List, Text] = Field(None, alias="json")
    data: Union[Text, Dict[Text, Any]] = None
    cookies: Cookies = {}
    timeout: float = 120
    allow_redirects: bool = True
    verify: Verify = False
    upload: Dict = {}  # used for upload files


class TStep(BaseModel):
    """测试步骤模型"""
    name: Name
    id: int = 0  # 步骤表ID
    sid: int = 0  # 步骤表执行顺序
    description: Desc = ''  # 步骤描述
    api_id: int = 0  # 接口ID
    api_description: Desc = ''  # 接口描述
    is_skip: bool = False  # 是否跳过改测试步骤
    is_api_valid: bool = True  # 步骤请求的接口是否 有效，如无效则跳过
    is_api_updated: bool = True  # 步骤请求的接口是否有更新，标记
    skipif: Union[Text, None] = None  # 条件表达式，是否跳过当前步骤
    depends: List[int] = []  # 依赖的测试步骤sid，如果依赖步骤失败，跳过当前步骤
    base_url: BaseUrl = ""  # 指定 base_url，如未指定则使用TConfig里的base_url
    request: Union[TRequest, None] = None
    testcase: Union[Text, Callable, None] = None
    variables: VariablesMapping = {}
    setup_hooks: Hooks = []
    teardown_hooks: Hooks = []
    # used to extract request's response field
    extract: VariablesMapping = {}
    # used to export session variables from referenced testcase
    export: Export = []
    validators: Validators = Field([], alias="validate")
    validate_script: List[Text] = []


class TestCase(BaseModel):
    """测试用例模型 = 测试配置 + 测试步骤"""
    id: int = 0
    config: TConfig
    test_type: Text = ''  # allure.feature
    tags: List[Text] = []  # allure.tag
    teststeps: List[TStep]
    setups: List[Text] = []  # setup 类名列表
    teardowns: List[Text] = []  # teardown 类名列表


class ProjectMeta(BaseModel):
    """项目配置模型"""
    debugtalk_py: Text = ""  # debugtalk.py file content
    debugtalk_path: Text = ""  # debugtalk.py file path
    dot_env_path: Text = ""  # .env file path
    functions: FunctionsMapping = {}  # functions defined in debugtalk.py
    env: Env = {}
    RootDir: Text = os.getcwd()  # project root directory (ensure absolute), the path debugtalk.py located


class TestsMapping(BaseModel):
    """测试集合 = 项目配置 + 测试用例"""
    project_meta: ProjectMeta
    testcases: List[TestCase]


class TestCaseTime(BaseModel):
    """测试用例时间"""
    start_at: float = 0
    start_at_iso_format: Text = ""
    duration: float = 0


class TestCaseInOut(BaseModel):
    """测试用例输入输出"""
    config_vars: VariablesMapping = {}
    export_vars: Dict = {}


class RequestStat(BaseModel):
    """请求状态"""
    content_size: float = 0
    response_time_ms: float = 0
    elapsed_ms: float = 0


class AddressData(BaseModel):
    """地址数据"""
    client_ip: Text = "N/A"
    client_port: int = 0
    server_ip: Text = "N/A"
    server_port: int = 0


class RequestData(BaseModel):
    """请求数据模型"""
    method: MethodEnum = MethodEnum.GET
    url: Url
    headers: Headers = {}
    cookies: Cookies = {}
    body: Union[Text, bytes, List, Dict, None] = {}


class ResponseData(BaseModel):
    """响应数据模型"""
    status_code: int
    headers: Dict
    cookies: Cookies
    encoding: Union[Text, None] = None
    content_type: Text
    body: Union[Text, bytes, List, Dict]


class ReqRespData(BaseModel):
    """请求响应数据模型"""
    request: RequestData
    response: ResponseData


class SessionData(BaseModel):
    """请求会话数据，请求+响应、请求状态、地址、校验器"""

    success: bool = False
    # in most cases, req_resps only contains one request & response
    # while when 30X redirect occurs, req_resps will contain multiple request & response
    req_resps: List[ReqRespData] = []
    stat: RequestStat = RequestStat()
    address: AddressData = AddressData()
    validators: Dict = {}


class StepData(BaseModel):
    """步骤数据模型, each step maybe corresponding to one request or one testcase"""

    step_id: int = 0
    success: bool = False
    stat: TestStatusEnum = TestStatusEnum.UNKNOWN
    blocker: List = []  # ['404', 'GET', '/api/path/1']
    sid: int = 0  # teststep sid
    name: Text = ""  # teststep name
    description: Desc = ""  # teststep description
    data: Union[SessionData, List['StepData']] = None
    export_vars: VariablesMapping = {}


StepData.update_forward_refs()


class PlatformInfo(BaseModel):
    runner_version: Text
    python_version: Text
    platform: Text


class TestCaseRef(BaseModel):
    name: Text
    base_url: Text = ""
    testcase: TestCase
    variables: VariablesMapping = {}


class TestSuite(BaseModel):
    """测试套件"""
    config: TConfig
    testcases: List[TestCaseRef]
    setup_tcs: List[TestCaseRef] = []
    teardown_tcs: List[TestCaseRef] = []
    setup_class_tcs: List[TestCaseRef] = []
    teardown_class_tcs: List[TestCaseRef] = []


class TestDept(BaseModel):
    """部门测试套件"""
    name: Name
    testsuites: List[TestSuite]


class Stat(BaseModel):
    """结果集状态"""
    total: int = 0
    passed: int = 0
    failed: int = 0
    error: int = 0
    skipped: int = 0


class TestCaseSummary(BaseModel):
    """测试用例结果"""
    name: Text
    success: bool
    stat: TestStatusEnum = TestStatusEnum.UNKNOWN
    case_id: Text
    time: TestCaseTime
    in_out: TestCaseInOut = {}
    log: Text = ""
    step_datas: List[StepData] = []


class TestSuiteSummary(BaseModel):
    """测试套件结果收集"""
    success: bool = False
    stat: Stat = Stat()
    time: TestCaseTime = TestCaseTime()
    platform: PlatformInfo
    testcases: List[TestCaseSummary]


class ReportSummary(BaseModel):
    """总测试报告概要收集"""
    success: bool = True
    stat: TestStatusEnum = TestStatusEnum.UNKNOWN
    testcases_stat: Stat = Stat()
    teststeps_stat: Stat = Stat()
    broken_apis: List[Dict] = []  # [{},{}]
    time: TestCaseTime = TestCaseTime()
    log_path: Text = ''
    allure_xml_path: Text = ''
    html_report_path: Text = ''


if __name__ == '__main__':
    pass
