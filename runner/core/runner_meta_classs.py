#!/usr/bin/python
# -*- coding:utf-8 _*- 
"""
@author:TXU
@file:step_meta_classs.py
@time:2021/11/12
@email:tao.xu2008@outlook.com
@description:
"""
import allure
import pytest
import types
import builtins
import jinja2
from loguru import logger

from runner.core.utils import merge_variables
from runner.core.parser import parse_variables_mapping
from runner.core.loader import load_project_meta


# test_xx.py 模板
__TEST_STEP_TEMPLATE__ = jinja2.Template(
    """
def {{ test_step_func_name }}(self, step):    
    # override variables
    # step variables > extracted variables from previous steps
    step.variables = merge_variables(step.variables, self.extracted_variables)
    # step variables > testcase config variables
    step.variables = merge_variables(step.variables, self._config.variables)

    # parse variables
    step.variables = parse_variables_mapping(
        step.variables, self._project_meta.functions
    )

    # run step
    # with allure.step(f"step{step.idx}: {step.name}"):
    # allure.dynamic.title(f"step{step.idx}: {step.name}")
    allure.dynamic.description(step.description or step.name)
    step_data = self.run_step(step)
    extract_mapping = step_data.export_vars

    # save extracted variables to session variables
    self.extracted_variables.update(extract_mapping)
"""
)


class RunnerMetaClass(type):
    """根据teststeps生成测试用例代码 test_step_xxx"""

    def __new__(cls, name, bases, attrs):
        teststeps = attrs.get('teststeps')
        tmp_teststeps = []
        for step in teststeps:
            tmp_teststeps.append(step.perform())
            allure.dynamic.title

        test_step_func_name = 'test_step'
        function = create_function(
            __TEST_STEP_TEMPLATE__.render(
                {
                    "test_step_func_name": test_step_func_name
                }
            ),
            namespace={
                'pytest': pytest,
                'allure': allure,
                'logger': logger,
                'merge_variables': merge_variables,
                'parse_variables_mapping': parse_variables_mapping,
                'load_project_meta': load_project_meta,
            })
        ids = [str(step.idx).zfill(3) for step in tmp_teststeps]
        attrs[test_step_func_name] = pytest.mark.parametrize('step', tmp_teststeps, ids=ids)(function)
        return super().__new__(cls, name, bases, attrs)


def create_function(function_express, namespace=None):
    """动态生成函数对象"""
    if namespace is not None:
        builtins.__dict__.update(namespace)
    module_code = compile(function_express, '', 'exec')  # 根据模板生成可执行的代码
    function_code = [x for x in module_code.co_consts if isinstance(x, types.CodeType)][0]
    return types.FunctionType(function_code, builtins.__dict__)


if __name__ == '__main__':
    pass
