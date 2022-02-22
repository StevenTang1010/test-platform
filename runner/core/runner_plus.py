#!/usr/bin/python
# -*- coding:utf-8 _*- 
"""
@author:TXU
@file:runner.py
@time:2021/10/26
@email:tao.xu2008@outlook.com
@description:执行器 - 以测试步骤为test_*单位执行
"""

import os
import sys
import time
import uuid
from datetime import datetime
from typing import List, Dict, Text, NoReturn
from loguru import logger

from runner.config import cf
from runner.core import exceptions, utils
from runner.core.client import HttpSession
from runner.core.exceptions import ValidationFailure, ParamsError
from runner.core.ext.uploader import prepare_upload_step
from runner.core.loader import load_project_meta
from runner.core.parser import build_url, parse_data, parse_variables_mapping
from runner.core.response import ResponseObject
from runner.core.testcase import Config, Step
from runner.core.models import (
    TConfig,
    TStep,
    VariablesMapping,
    StepData,
    TestCaseSummary,
    TestCaseTime,
    TestCaseInOut,
    ProjectMeta,
    TestCase,
    Hooks,
)


class StepRequestRunner(object):
    config: Config
    teststeps: List[Step]

    success: bool = False  # indicate testcase execution result
    _config: TConfig
    _teststeps: List[TStep]
    _project_meta: ProjectMeta = None
    _case_id: Text = ""
    _export: List[Text] = []
    _step_datas: List[StepData] = []
    _session: HttpSession = None
    _session_variables: VariablesMapping = {}
    # time
    _start_at: float = 0
    _duration: float = 0
    _start_str: Text = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    # log
    _log_path: Text = ""
    _log_handlers: List = []
    extracted_variables: VariablesMapping = {}

    # 初始化config
    @classmethod
    def init_config(cls):
        cls._config = cls.config.perform()
        cls._project_meta = cls._project_meta or load_project_meta(cls._config.path)
        print('cls._config')
        print(cls._config)

    @classmethod
    def __parse_config(cls, config: TConfig) -> NoReturn:
        config.variables.update(cls._session_variables)
        config.variables = parse_variables_mapping(
            config.variables, cls._project_meta.functions
        )
        config.name = parse_data(
            config.name, config.variables, cls._project_meta.functions
        )
        config.base_url = parse_data(
            config.base_url, config.variables, cls._project_meta.functions
        )

    # 初始化用例
    @classmethod
    def init_testcase(cls):
        cls._config = cls.config.perform()
        cls._teststeps = []
        for step in cls.teststeps:
            cls._teststeps.append(step.perform())
        cls._project_meta = cls._project_meta or load_project_meta(cls._config.path)
        cls._case_id = cls._case_id or str(uuid.uuid4())
        cls._export = []
        cls._step_datas = []
        cls._session = HttpSession()
        cls._session_variables = {}
        # time
        cls._start_at = 0
        cls._duration = 0
        cls._start_str: Text = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        # logger
        cls._log_path = cls._log_path or os.path.join(
            cls._project_meta.RootDir,
            "test-platform/apps/api_test/runner/logs",
            f"{cls._start_str}-{cls._config.name}.run.log"
        )
        cls._log_handlers = []
        # logger.remove()
        cls._log_handlers.append(
            logger.add(
                cls._log_path,
                rotation='100 MB',
                retention='7 days',
                enqueue=True,
                encoding="utf-8",
                level=cf.get_str("LOGGER", "file_level") or "DEBUG"
            )
        )
        cls._log_handlers.append(logger.add(sys.stdout, level=cf.get_str("LOGGER", "console_level")))

        # parse config name
        config_variables = cls._config.variables
        config_variables.update(cls._session_variables)
        cls._config.name = parse_data(
            cls._config.name, config_variables, cls._project_meta.functions
        )

        # update allure report meta
        # allure.dynamic.title(cls._config.name + '-' + cls._config.description)
        # allure.dynamic.description(cls._config.description)

    @classmethod
    def setup_class(cls):
        cls.init_testcase()
        logger.info(f"Start to run testcase: {cls._config.name}, TestCase ID: {cls._case_id}")
        cls.__parse_config(cls._config)
        cls._start_at = time.time()
        cls._step_datas: List[StepData] = []
        cls._session = cls._session or HttpSession()
        # save extracted variables of teststeps
        cls.extracted_variables: VariablesMapping = {}

    @classmethod
    def teardown_class(cls):
        # self._session_variables.update(extracted_variables)
        cls._duration = time.time() - cls._start_at
        summary = cls.get_summary()
        # logger.info(summary)
        # 删除用例创建的logger
        logger.info(f"generate testcase log: {cls._log_path}")
        for log_handler in cls._log_handlers:
            logger.remove(log_handler)

    @property
    def raw_testcase(self) -> TestCase:
        return TestCase(config=self._config, teststeps=self._teststeps)

    def with_project_meta(self, project_meta: ProjectMeta) -> "StepRequestRunner":
        self._project_meta = project_meta
        return self

    def with_session(self, session: HttpSession) -> "StepRequestRunner":
        self._session = session
        return self

    def with_case_id(self, case_id: Text) -> "StepRequestRunner":
        self._case_id = case_id
        return self

    def with_variables(self, variables: VariablesMapping) -> "StepRequestRunner":
        self._session_variables = variables
        return self

    def with_export(self, export: List[Text]) -> "StepRequestRunner":
        self._export = export
        return self

    def __call_hooks(
            self, hooks: Hooks, step_variables: VariablesMapping, hook_msg: Text,
    ) -> NoReturn:
        """ call hook actions.

        Args:
            hooks (list): each hook in hooks list maybe in two format.

                format1 (str): only call hook functions.
                    ${func()}
                format2 (dict): assignment, the value returned by hook function will be assigned to variable.
                    {"var": "${func()}"}

            step_variables: current step variables to call hook, include two special variables

                request: parsed request dict
                response: ResponseObject for current response

            hook_msg: setup/teardown request/testcase

        """
        logger.info(f"call hook actions: {hook_msg}")

        if not isinstance(hooks, List):
            logger.error(f"Invalid hooks format: {hooks}")
            return

        for hook in hooks:
            if isinstance(hook, Text):
                # format 1: ["${func()}"]
                logger.debug(f"call hook function: {hook}")
                parse_data(hook, step_variables, self._project_meta.functions)
            elif isinstance(hook, Dict) and len(hook) == 1:
                # format 2: {"var": "${func()}"}
                var_name, hook_content = list(hook.items())[0]
                hook_content_eval = parse_data(
                    hook_content, step_variables, self._project_meta.functions
                )
                logger.debug(
                    f"call hook function: {hook_content}, got value: {hook_content_eval}"
                )
                logger.debug(f"assign variable: {var_name} = {hook_content_eval}")
                step_variables[var_name] = hook_content_eval
            else:
                logger.error(f"Invalid hook format: {hook}")

    def __run_step_request(self, step: TStep) -> StepData:
        """run teststep: request"""
        step_data = StepData(name=step.name)

        # parse
        prepare_upload_step(step, self._project_meta.functions)
        request_dict = step.request.dict()
        request_dict.pop("upload", None)
        parsed_request_dict = parse_data(
            request_dict, step.variables, self._project_meta.functions
        )
        parsed_request_dict["headers"].setdefault(
            "RUN-Request-ID",
            f"RUN-{self._case_id}-{str(int(time.time() * 1000))[-6:]}",
        )
        parsed_request_dict["headers"].setdefault(
            "Authorization", self._config.variables.get("session_id"),
        )
        step.variables["request"] = parsed_request_dict

        # setup hooks
        if step.setup_hooks:
            self.__call_hooks(step.setup_hooks, step.variables, "setup request")

        # prepare arguments
        method = parsed_request_dict.pop("method")
        url_path = parsed_request_dict.pop("url")
        url = build_url(self._config.base_url, url_path)
        parsed_request_dict["verify"] = self._config.verify
        parsed_request_dict["json"] = parsed_request_dict.pop("req_json", {})

        # request
        resp = self._session.request(method, url, **parsed_request_dict)
        resp_obj = ResponseObject(resp)
        step.variables["response"] = resp_obj

        # teardown hooks
        if step.teardown_hooks:
            self.__call_hooks(step.teardown_hooks, step.variables, "teardown request")

        def log_req_resp_details():
            err_msg = "\n{} DETAILED REQUEST & RESPONSE {}\n".format("*" * 32, "*" * 32)

            # log request
            err_msg += "====== request details ======\n"
            err_msg += f"url: {url}\n"
            err_msg += f"method: {method}\n"
            headers = parsed_request_dict.pop("headers", {})
            err_msg += f"headers: {headers}\n"
            for k, v in parsed_request_dict.items():
                v = utils.omit_long_data(v)
                err_msg += f"{k}: {repr(v)}\n"

            err_msg += "\n"

            # log response
            err_msg += "====== response details ======\n"
            err_msg += f"status_code: {resp.status_code}\n"
            err_msg += f"headers: {resp.headers}\n"
            err_msg += f"body: {repr(resp.text)}\n"
            logger.error(err_msg)

        # extract
        extractors = step.extract
        extract_mapping = resp_obj.extract(extractors)
        step_data.export_vars = extract_mapping

        self._config.variables.update(extract_mapping)  # 更新步骤变量到用例配置变量
        variables_mapping = step.variables
        variables_mapping.update(extract_mapping)

        # validate
        validators = step.validators
        session_success = False
        try:
            resp_obj.validate(
                validators, variables_mapping, self._project_meta.functions
            )
            session_success = True
        except ValidationFailure:
            session_success = False
            log_req_resp_details()
            # log testcase duration before raise ValidationFailure
            self._duration = time.time() - self._start_at
            raise
        finally:
            self.success = session_success
            step_data.success = session_success

            if hasattr(self._session, "data"):
                # runner.core.client.HttpSession, not locust.clients.HttpSession
                # save request & response meta data
                self._session.data.success = session_success
                self._session.data.validators = resp_obj.validation_results

                # save step data
                step_data.data = self._session.data

        return step_data

    def __run_step_testcase(self, step: TStep) -> StepData:
        """run teststep: referenced testcase"""
        step_data = StepData(name=step.name)
        step_variables = step.variables
        step_export = step.export

        # setup hooks
        if step.setup_hooks:
            self.__call_hooks(step.setup_hooks, step_variables, "setup testcase")

        if hasattr(step.testcase, "config") and hasattr(step.testcase, "teststeps"):
            testcase_cls = step.testcase
            case_result = (
                testcase_cls()
                    .with_session(self._session)
                    .with_case_id(self._case_id)
                    .with_variables(step_variables)
                    .with_export(step_export)
                    .run()
            )

        else:
            raise exceptions.ParamsError(
                f"Invalid teststep referenced testcase: {step.dict()}"
            )

        # teardown hooks
        if step.teardown_hooks:
            self.__call_hooks(step.teardown_hooks, step.variables, "teardown testcase")

        step_data.data = case_result.get_step_datas()  # list of step data
        step_data.export_vars = case_result.get_export_variables()
        step_data.success = case_result.success
        self.success = case_result.success

        if step_data.export_vars:
            logger.info(f"export variables: {step_data.export_vars}")

        return step_data

    def run_step(self, step: TStep) -> StepData:
        """run teststep, teststep maybe a request or referenced testcase"""
        logger.info(f"run step begin: {step.name} >>>>>>")

        if step.request:
            step_data = self.__run_step_request(step)
        elif step.testcase:
            step_data = self.__run_step_testcase(step)
        else:
            raise ParamsError(
                f"teststep is neither a request nor a referenced testcase: {step.dict()}"
            )

        self._step_datas.append(step_data)
        logger.info(f"run step end: {step.name} <<<<<<\n")
        # return step_data.export_vars
        return step_data

    def get_step_datas(self) -> List[StepData]:
        return self._step_datas

    @classmethod
    def get_export_variables(cls) -> Dict:
        # override testcase export vars with step export
        export_var_names = cls._export or cls._config.export
        export_vars_mapping = {}
        for var_name in export_var_names:
            if var_name not in cls._session_variables:
                raise ParamsError(
                    f"failed to export variable {var_name} from session variables {cls._session_variables}"
                )

            export_vars_mapping[var_name] = cls._session_variables[var_name]

        return export_vars_mapping

    @classmethod
    def get_summary(cls) -> TestCaseSummary:
        """get testcase result summary"""
        start_at_timestamp = cls._start_at
        start_at_iso_format = datetime.utcfromtimestamp(start_at_timestamp).isoformat()
        return TestCaseSummary(
            name=cls._config.name,
            success=cls.success,
            case_id=cls._case_id,
            time=TestCaseTime(
                start_at=cls._start_at,
                start_at_iso_format=start_at_iso_format,
                duration=cls._duration,
            ),
            in_out=TestCaseInOut(
                config_vars=cls._config.variables,
                export_vars=cls.get_export_variables(),
            ),
            log=cls._log_path,
            step_datas=cls._step_datas,
        )


if __name__ == '__main__':
    pass
