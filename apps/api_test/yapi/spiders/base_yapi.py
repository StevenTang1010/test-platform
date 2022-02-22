#!/usr/bin/python
# -*- coding:utf-8 _*- 
"""
@author:TXU
@file:yapi_client.py
@time:2021/11/04
@email:tao.xu2008@outlook.com
@description:
"""
import urllib3
import requests

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

YAPI_BASE_URL = 'https://yapi.dustess.com'
YAPI_USER = 'tangxy'
YAPI_PASSWORD = 'dustess#2021'


class BaseYApi(object):
    """yapi获取接口信息"""

    _session = None
    _groups = None

    def __init__(self, host=YAPI_BASE_URL, user=YAPI_USER, password=YAPI_PASSWORD):
        self.host = host
        self.user = user
        self.password = password

    def _get_session(self):
        """
        登录yapi
        :return:
        """
        login_url = self.host + '/api/user/login_by_ldap'
        login_json = {'email': self.user, 'password': self.password}
        login_header = {'Content-Type': 'application/json;charset=UTF-8'}
        session = requests.session()
        session.post(url=login_url, headers=login_header, json=login_json, verify=False)
        return session

    @property
    def session(self):
        if self._session is None:
            self._session = self._get_session()
        return self._session

    @property
    def groups(self) -> dict:
        """
        获取分组信息: {名称：ID}
        :return: {name:id}
        """
        if self._groups is None:
            url = self.host + '/api/group/list'
            res = self.session.get(url=url, verify=False)
            self._groups = {}
            for group in res.json().get('data'):
                if group.get('type') == 'private':
                    continue
                self._groups[group.get('group_name')] = group.get('_id')
        return self._groups

    def get_project_list(self, group_id):
        """
        获取分组下项目列表
        :return:
        """
        url = self.host + '/api/project/list'
        params = {'group_id': group_id, 'page': '1', 'limit': '9999'}
        res = self.session.get(url=url, params=params, verify=False)
        return res.json().get('data').get('list')

    def get_project_detail(self, prj_id: int):
        """
        获取项目详情: name/basepath/接口分类列表
        :return:
        """
        url = self.host + '/api/project/list'
        params = {'id': prj_id}
        res = self.session.get(url=url, params=params, verify=False)
        return res.json().get('data')

    def get_cat_list(self, prj_id: int) -> list:
        """
        获取接口分类目录
        :param prj_id:
        :return:
        """
        url = self.host + '/api/interface/list_menu'
        params = {'page': 1, 'limit': 999, 'project_id': prj_id}
        res = self.session.get(url=url, params=params, verify=False)
        return res.json().get("data")

    def get_cat_interface_list(self, prj_id: int) -> dict:
        menu_interface = {}
        menu_list = self.get_cat_list(prj_id)
        for menu in menu_list:
            # menu_id = menu.get('_id')
            menu_name = menu.get('name')
            interface_list = menu.get('list')
            menu_interface[menu_name] = interface_list
        return menu_interface

    def get_interface_list(self, prj_id: int):
        """
        获取项目下接口列表
        :param prj_id:
        :return:
        """
        url = self.host + '/api/interface/list'
        params = {'page': 1, 'limit': 9999, 'project_id': prj_id}
        res = self.session.get(url=url, params=params, verify=False)
        return res.json().get("data").get("list")

    def get_interface_detail(self, api_id: int, token: str):
        """
        获取接口数据（有详细接口数据定义文档）
        :param api_id:
        :param token:
        :return:
        """
        url = self.host + '/api/interface/get'
        params = {'id': api_id, 'token': token}
        res = requests.request(method='get', url=url, params=params)
        return res.json().get('data')

    def get_project_token(self, prj_id: int) -> str:
        """
        获取项目token，每个项目都有唯一的标识token，用户可以使用这个token值来请求项目openapi.
        :param prj_id:
        :return:
        """
        url = self.host + '/api/project/token'
        res = self.session.get(url=url, params={'project_id': prj_id})
        return res.json().get('data')


if __name__ == '__main__':
    yapi = BaseYApi()
    print(yapi.groups)
    # print(yapi.get_project_list(35))
    # print(yapi.get_interface_list(1461))
    # print(yapi.get_interface_detail(336116, yapi.get_project_token(1461)))
