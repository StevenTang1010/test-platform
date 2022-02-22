#!/usr/bin/python
# -*- coding:utf-8 _*- 
"""
@author:TXU
@file:get_api_from_mongo.py
@time:2021/11/12
@email:tao.xu2008@outlook.com
@description:
"""
import json

# from apps.api_test import logger
from loguru import logger
from common.mongodb import MongoDBOperation


MONGODB_HOST = '192.168.0.128'  # 47.96.184.58
MONGODB_PORT = 7211
MONGODB_USER = 'dustess'
MONGODB_PWD = 'dustesssetsud'
MONGODB_DATABASE = 'yapi'


class YapiMongoDB(MongoDBOperation):
    """从mongodb数据库获取yapi数据"""
    def __init__(self,
                 db_host=MONGODB_HOST,
                 db_port=MONGODB_PORT,
                 db_user=MONGODB_USER,
                 db_password=MONGODB_PWD,
                 db_name=MONGODB_DATABASE):
        super(YapiMongoDB, self).__init__(db_host, db_port, db_user, db_password, db_name, logger=logger)
        pass

    def get_projects_by_api_full_path(self, api_full_path):
        # 根据full path查找项目: fullpath.startswith(project.basepath)
        match_projects = []
        projects = self.read_table('project')
        if len(projects) == 0:
            raise Exception("YAPI中没找到project")
        for p in projects:
            if api_full_path.startswith(p.get('basepath')):
                match_projects.append(p)
        return match_projects

    def get_api_by_method_fullpath(self, method, fullpath):
        # 根据full path查找项目: 项目.basepath in fullpath
        match_projects = self.get_projects_by_api_full_path(fullpath)
        # 排序：basepath长度从大到小：优先检索basepath不为空的项目
        for p in sorted(match_projects, key=lambda x: x.get('basepath'), reverse=True):
            basepath = p.get('basepath')
            p_id = p.get('_id')
            path = fullpath.replace(basepath, '')
            query_filter = {'project_id': p_id, 'method': method.upper(), 'path': path}
            apis = self.read_table('interface', query_filter)
            if len(apis) == 0:
                continue
            return apis[0]
        return None

    def get_api_by_id(self, api_id):
        query_filter = {'_id': api_id}
        apis = self.read_table('interface', query_filter)
        if len(apis) == 0:
            raise Exception("YAPI中没找到对应接口, {}".format(query_filter))
        return apis[0]

    def get_project_by_id(self, project_id):
        query_filter = {'_id': project_id}
        projects = self.read_table('project', query_filter)
        if len(projects) == 0:
            raise Exception("YAPI中没找到对应project:{}".format(query_filter))
        return projects[0]

    def get_api_cat_by_id(self, cat_id):
        query_filter = {'_id': cat_id}
        cats = self.read_table('interface_cat', query_filter)
        if len(cats) == 0:
            raise Exception("YAPI中没找到对应接口分类:{}".format(query_filter))
        return cats[0]

    def pop_data_id(self, data_list):
        """
        去掉data中ObjectId类型字段，如 '_id': ObjectId('607d377f9f23fd3457e2f1ff')
        req_headers | req_query | yapi_req_body_form
        :param data_list:
        :return:
        """
        for data in data_list:
            data.pop('_id')
        return data_list

    def parse_api(self, api):
        """
        解析yapi原始数据
        :param api:
        :return:
        """
        api_name = api.get("title")
        api_path = api.get("path")
        if api_path.startswith('/internal'):
            # logger.warning('{}->{}(内部接口，跳过!!！)'.format(api_name, api_path))
            raise Exception('{}->{}(内部接口，跳过!!！)'.format(api_name, api_path))
        api_project_id = api.get("project_id"),
        api_project = self.get_project_by_id(api_project_id[0])
        prj_basepath = api_project.get("basepath")
        req_body_other_src = api.get('req_body_other', '{}')
        res_body_src = api.get('res_body', '{}')
        try:
            req_body_other = json.loads(req_body_other_src)
        except Exception as e:
            req_body_other = {"JSONDecodeError": str(e), "body": req_body_other_src}
        try:
            res_body = json.loads(api.get('res_body', '{}'))
        except Exception as e:
            res_body = {"JSONDecodeError": str(e), "body": res_body_src}

        api_info = {
            "name": api_name,
            "description": api.get("desc"),
            "yapi_id": api.get("_id"),
            "yapi_project_id": api.get("project_id"),  # 本地接口表无此字段
            "yapi_cat_id": api.get("catid"),  # 本地接口表无此字段
            "method": api.get("method"),
            "path": prj_basepath + api_path,
            "yapi_req_headers": self.pop_data_id(api.get('req_headers', [])),
            "yapi_req_params": self.pop_data_id(api.get('req_params', [])),
            "yapi_req_query": self.pop_data_id(api.get('req_query', [])),
            "yapi_req_body_form": self.pop_data_id(api.get('req_body_form', [])),
            "yapi_req_body_other": req_body_other,
            "yapi_res_body": res_body
        }
        return api_info

    def get_api_info_by_id(self, yapi_id):
        """
        根据yapi id获取yapi接口详情，并解析
        :param yapi_id:
        :return:
        """
        yapi = self.get_api_by_id(yapi_id)
        return self.parse_api(yapi)

    def get_api_info_by_method_path(self, method, api_full_path):
        """
        根据api_full_path获取yapi接口详情，并解析
        :param method: 请求方法
        :param api_full_path: 请求path，全路径
        :return:
        """
        yapi = self.get_api_by_method_fullpath(method, api_full_path)
        if not yapi:
            raise Exception("YAPI中没找到对应接口, {} {}".format(method, api_full_path))
        return self.parse_api(yapi)


if __name__ == '__main__':
    yapi_db = YapiMongoDB()
    yapi_info = yapi_db.get_api_by_method_fullpath('GET', '/mall/order/v1/mall_setting/get_order_trade_setting')
    print(yapi_info)
