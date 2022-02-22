#!/usr/bin/python
# -*- coding:utf-8 _*- 
"""
@author:TXU
@file:mock_data.py
@time:2021/07/21
@email:tao.xu2008@outlook.com
@description: 获取/爬取环境数据
"""
from apps.api_test.models import GlobalEnv
from loguru import logger
from runner.common.spiders.employee import EmployeeSpider
from runner.common.spiders.department import DepartmentSpider


class GetEnvData(object):
    """获取/爬取环境数据"""

    def __init__(self, env_id):
        self.env_data_id = env_id
        self.emp = EmployeeSpider(env_id)
        self.dept = DepartmentSpider(env_id)
        try:
            self.login_session_data = self.dept.get_login_session()
        except Exception as e:
            logger.error(e)
            self.login_session_data = {}

    @classmethod
    def get_props(cls):
        return [x for x in dir(cls) if isinstance(getattr(cls, x), property)]

    @property
    def env_id(self):
        return self.env_data_id

    @property
    def session_id(self):
        return self.dept.Authorization

    @property
    def bill_session_id(self):
        """计费系统token"""
        return self.dept.get_bill_session()

    @property
    def sesId(self):
        """计费系统token"""
        return self.dept.get_bill_session()

    @property
    def login_sid(self):
        return self.login_session_data.get("sid")

    @property
    def login_uid(self):
        return self.login_session_data.get("uid")

    @property
    def login_name(self):
        return self.login_session_data.get("name")

    @property
    def login_account(self):
        return self.login_session_data.get("account")

    @property
    def login_qw_user_id(self):
        return self.login_session_data.get("qwUserId")  # 如'alex'

    @property
    def login_agent_id(self):
        return self.login_session_data.get("agentId")  # 如'1000002'

    @property
    def login_qw_department_id(self):
        return self.login_session_data.get("qwDepartmentId")[0]

    @property
    def department_ids(self):
        return self.dept.departments_ids

    @property
    def department_names(self):
        return self.dept.departments_names

    @property
    def employee_names(self):
        return self.emp.employees_names

    @property
    def employee_ids(self):
        return self.emp.employees_ids

    @property
    def employees_roles(self):
        return self.emp.employees_roles

    @property
    def employees_department_ids(self):
        return self.emp.employees_department_ids

    # ==================== data for callback ====================
    @property
    def external_contact_access_token(self):
        corp_secret = self.dept.env.qw_external_contact_config.get('external_contact_corp_secret').get('value')
        return self.dept.get_access_token(corp_secret)


class ValidateSession(object):
    """校验session有效性"""
    def __init__(self, env_id):
        self.session_id = GlobalEnv.objects.get(id__exact=env_id).data.get('session_id')
        logger.warning(self.session_id)
        self.dept = DepartmentSpider(env_id)

    @property
    def login(self):
        """校验登录session有效性"""
        logger.info("{0} 校验登录session有效性 {0}".format("="*10))
        try:
            login_session = self.dept.get_login_session()
            if login_session.get('sid'):
                logger.info("校验登录session有效性 => PASS.")
                return True
            logger.info("校验登录session有效性 => FAIL，需要重新获取session_id")
            return False
        except Exception as e:
            logger.warning(e)
            logger.info("校验登录session有效性 => FAIL，需要重新获取session_id")
            return False

    @property
    def bill(self):
        """校验计费session有效性"""
        return True


def update_env_data(env_id):
    vs = ValidateSession(env_id)
    if vs.session_id and vs.login and vs.bill:
        # 如果环境数据中login session_id有效，跳过更新
        return

    logger.info("更新测试环境env数据...")
    new_env_data = {}
    GlobalEnv.objects.filter(id__exact=env_id).update(data={})  # 先清空data，避免无效session被取到
    env_data_obj = GetEnvData(env_id)
    for k in env_data_obj.get_props():
        try:
            v = env_data_obj.__getattribute__(k)
            logger.debug("环境数据：{}:{}".format(k, v))
            new_env_data.update({k: v})
        except Exception as e:
            logger.error(e)

    # 更新data数据到env
    GlobalEnv.objects.filter(id__exact=env_id).update(data=new_env_data)
    return


if __name__ == '__main__':
    mock = GetEnvData(1)
    # print(mock.get_props())
    # for p in mock.get_props():
    #     print(mock.__getattribute__(p))
