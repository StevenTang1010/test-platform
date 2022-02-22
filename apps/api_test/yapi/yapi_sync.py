#!/usr/bin/python
# -*- coding:utf-8 _*- 
"""
@author:TXU
@file:yapi_sync.py
@time:2021/12/14
@email:tao.xu2008@outlook.com
@description:
"""
import json
from dictdiffer import diff
from concurrent.futures import ThreadPoolExecutor, as_completed

from apps.api_test import logger
from apps.api_test.yapi.get_api_from_mongo import YapiMongoDB
from apps.api_test.models import ApiInfo, ApiGroup, ApiUpdateHistory, YApiEvent, Project, TestStep


class APICaseTemplate(object):
    """根据yapi原始数据解析生成接口请求模板数据"""
    def __json_loads(self, src_string):
        try:
            body = json.loads(src_string)
        except Exception as e:
            body = {"JSONDecodeError": str(e), "body": src_string}
        return body

    def __vaild_json(self, src_string):
        if not isinstance(src_string, (list, dict)):
            src_string = self.__json_loads(src_string)
        return src_string

    def __serilaize_req_headers(self, headers_string: list) -> dict:
        """
        序列化请求headers
        :param headers_string:需要序列化的headers_string
        :return:
        """
        a_dict = {}
        for x in headers_string:
            header_name = x.get('name')
            if header_name == 'Authorization':
                # Authorization 统一添加到所有接口请求头
                continue
            a_dict[header_name] = x.get('value') or x.get('desc')
        return a_dict

    def __serilaize_req_params(self, params_string: list) -> dict:
        """
        序列化params类型body
        :param params_string:需要序列化的params_string
        :return:
        """
        a_dict = {}
        for x in params_string:
            a_dict[x.get('name')] = x.get('desc')
        return a_dict

    def __serilaize_req_query(self, query_string: list) -> dict:
        """
        序列化query类型参数
        :param query_string: 需要序列化的query_string
        :return:
        """
        a_dict = {}
        for x in query_string:
            a_dict[x.get('name')] = x.get('desc')
        return a_dict

    def __serilaize_req_form(self, form_string: list) -> dict:
        """
        序列化form类型body
        :param form_string: 需要序列化的form_string
        :return:
        """
        a_dict = {}
        for x in form_string:
            a_dict[x.get('name')] = x.get('desc')
        return a_dict

    def __serilaize_json_body(self, src_data: dict, dst_data: dict):
        """
        递归序列化字典(json.loads(json格式字符串))， res_body | req_body_other
        :param src_data: 需要递归序列化的 data
        :param dst_data: 序列化后的data
        :return:
        """
        for k, v in src_data.items():
            if k in ['items', 'properties'] and isinstance(v, dict):
                dst_data = self.__serilaize_json_body(v, dst_data)
            elif isinstance(v, dict):
                dst_data[k] = {}
                if v.get('properties'):
                    dst_data[k] = self.__serilaize_json_body(v, dst_data[k])
                elif v.get('items'):
                    dst_data[k] = [self.__serilaize_json_body(v, dst_data[k])]
                else:
                    dst_data[k] = v.get('description')
            else:
                # dst_data[k] = v
                pass
        return dst_data

    def __serilaize_res_body(self, res_body: dict) -> dict:
        res = {}
        try:
            properties = res_body.get('properties')
        except Exception as e:
            logger.error(e)
            return {}
        if not properties:
            return {}
        for k, v in properties.items():
            # if keys and k in keys:
            v_type = v.get('type')
            example = v.get('example')
            if example:
                res[k] = example
            elif v_type == 'object':
                res[k] = {}
            elif v_type == 'array':
                res[k] = []
            elif v_type == 'integer':
                res[k] = 0
            elif v_type == 'string':
                res[k] = ''
            elif v_type == 'boolean':
                res[k] = False
            else:
                res[k] = v_type
        return res

    def parse_to_req_template(self, yapi_info):
        req_data = {
            "req_headers": {},
            "req_params": {},
            "req_data": {},
            "req_json": {},
            "validator": {},
        }
        req_headers = self.__vaild_json(yapi_info.get('yapi_req_headers'))
        req_params = self.__vaild_json(yapi_info.get('yapi_req_params'))
        req_query = self.__vaild_json(yapi_info.get('yapi_req_query'))
        req_body_form = self.__vaild_json(yapi_info.get('yapi_req_body_form'))
        req_body_other = self.__vaild_json(yapi_info.get('yapi_req_body_other'))
        res_body = self.__vaild_json(yapi_info.get('yapi_res_body'))

        if len(req_headers) != 0:
            req_data.update({'req_headers': json.dumps(self.__serilaize_req_headers(req_headers), indent=2, ensure_ascii=False)})
        if len(req_params) != 0:
            req_data.update({'req_params': json.dumps(self.__serilaize_req_params(req_params), indent=2, ensure_ascii=False)})
        if len(req_query) != 0:
            req_data.update({'req_json': json.dumps(self.__serilaize_req_query(req_query), indent=2, ensure_ascii=False)})
        if len(req_body_form) != 0:
            req_data.update({'req_data': json.dumps(self.__serilaize_req_form(req_body_form), indent=2, ensure_ascii=False)})
        if req_body_other and req_body_other.get("JSONDecodeError", '') == '':
            req_data.update({'req_json': json.dumps(self.__serilaize_json_body(req_body_other, {}), indent=2, ensure_ascii=False)})
        if res_body and res_body.get("JSONDecodeError", '') == '':
            req_data.update({'validator': json.dumps(self.__serilaize_res_body(res_body), indent=2, ensure_ascii=False)})
        return req_data

    def update_template(self, api_dict: dict):
        api_id = api_dict.get('id')
        api_name = api_dict.get('name')
        logger.info("更新接口模板：{} -> {}".format(api_id, api_name))
        template = self.parse_to_req_template(api_dict)
        ApiInfo.objects.filter(id__exact=api_id).update(**template)
        response = {"msg": "用例模板更新成功！", "api_id": api_id}
        return response

    def bulk_update_template(self, api_list=None, max_workers=2):
        """
        批量更新用例模板
        :param api_list: 接口信息列表，list[dict1,dict2]
        :param max_workers: 多线程执行-最大线程数
        :return:
        """
        if api_list is None:
            api_list = []
        response_list = []
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_api = {executor.submit(self.update_template, api): api for api in api_list}
            for future in as_completed(future_to_api):
                try:
                    response_list.append(future.result())
                except Exception as e:
                    logger.error(e)
                    api_id = future_to_api[future]
                    response = {"msg": '用例模板更新失败！', "api_id": api_id, 'exception': str(e)}
                    response_list.append(response)
        return response_list

    def update_all(self):
        api_objs = ApiInfo.objects.all()
        api_list = [api.__dict__ for api in api_objs]
        return self.bulk_update_template(api_list, max_workers=4)


# 接口数据同步处理 -- YApiEvent表事件
class YAPIEventDataSync(object):
    """接口数据同步处理 -- YApiEvent表事件
        diff_contents = [
            {
                "change": '',
                "node": a.b,
                "value": [1, 2],
            }
        ]
    """

    def __parse_yapi_to_api(self, yapi_info):
        """
        解析yapi_info为 api_info
        1. api表存储req_* res_* 为text类型， yapi_info数据源为字典
        2. 删除yapi_info中无效字段： cat_id
        :param yapi_info:
        :return:
        """
        api_info = {}

        # 删除无效字段
        yapi_info.pop('yapi_cat_id')
        yapi_info.pop('yapi_project_id')

        # 转换 dict -> json text
        for k, v in yapi_info.items():
            if isinstance(v, (dict, list)):
                api_info[k] = json.dumps(v, ensure_ascii=False)
            else:
                api_info[k] = v
        return api_info

    def __insert_yapi_project_cat_info(self, yapi_info):
        """
        插入接口 项目+分组 信息，数据源为yapi_info
        1. 查找yapi所属项目名，本地数据库如不存在，创建新项目
        2. 查找yapi所属分组名，本地数据库如不存在，创建新分组
        :param yapi_info:
        :return:
        """
        yapi_db = YapiMongoDB()

        # 查找yapi所属项目名，本地数据库如不存在，创建新项目
        yapi_project = yapi_db.get_project_by_id(yapi_info['yapi_project_id'])
        yapi_project_name = yapi_project.get('name')
        prj_list = Project.objects.filter(name__exact=yapi_project_name).all()
        if prj_list:
            project_id = prj_list[0].id
        else:
            # 创建新项目
            yapi_project_desc = yapi_project.get('desc')
            Project.objects.create(
                **{
                    "name": yapi_project_name,
                    "description": yapi_project_desc
                }
            )
            project_id = Project.objects.get(name__exact=yapi_project_name).id

        # 查找yapi所属分组名，本地数据库如不存在，创建新分组
        yapi_cat = yapi_db.get_api_cat_by_id(yapi_info['yapi_cat_id'])
        yapi_cat_name = yapi_cat.get('name')
        group_list = ApiGroup.objects.filter(project__id__exact=project_id, name__exact=yapi_cat_name).all()
        if group_list:
            api_group_id = group_list[0].id
        else:
            # 创建新分组
            yapi_cat_desc = yapi_cat.get('desc')
            ApiGroup.objects.create(
                **{
                    "name": yapi_cat_name,
                    "project_id": project_id,
                    "description": yapi_cat_desc
                }
            )
            api_group_id = ApiGroup.objects.get(project__id__exact=project_id, name__exact=yapi_cat_name).id

        return project_id, api_group_id

    def __insert_yapi_info(self, yapi_info):
        """
        插入接口，数据源为yapi_info
        1. 查找yapi所属项目名，本地数据库如不存在，创建新项目
        2. 查找yapi所属分组名，本地数据库如不存在，创建新分组
        3. 插入接口表，指定项目、分组，接口更新状态：1 - 待验证
        :param yapi_info:
        :return:
        """

        project_id, api_group_id = self.__insert_yapi_project_cat_info(yapi_info)

        # 解析、新增待插入接口数据元素
        yapi_info.update(APICaseTemplate().parse_to_req_template(yapi_info))
        api_info = self.__parse_yapi_to_api(yapi_info)
        api_info.update({'project_id': project_id})
        api_info.update({'api_group_id': api_group_id})
        api_info.update({'update_status': 1})  # 新插入的接口，默认状态为待验证（即需要新建case并执行验证）
        api_info.update({'origin': 'yapi'})
        ApiInfo.objects.create(**api_info)
        return True

    def __update_yapi_info(self, yapi_info, api_define_changed=True):
        """
        更新YAPI数据变更到本地接口表对应接口：method+path
        :param yapi_info:
        :return:
        """
        method = yapi_info.get('method')
        path = yapi_info.get('path')
        yapi_info.update(APICaseTemplate().parse_to_req_template(yapi_info))
        api_info = self.__parse_yapi_to_api(yapi_info)
        if api_define_changed:
            api_info.update({'update_status': 0})
        api_info.update({'origin': 'yapi'})
        ApiInfo.objects.filter(method__exact=method, path__exact=path).update(**api_info)

    def insert(self, event, yapi_info: dict, update_time: str = None):
        """
        本地接口不存在，插入接口数据->插入接口变更记录（新增）
        :param event:
        :param yapi_info:
        :param update_time: 事件时间
        :return:
        """
        logger.info("本地接口不存在，插入数据...")
        self.__insert_yapi_info(yapi_info)
        yapi_id = yapi_info['yapi_id']
        new_api = ApiInfo.objects.get(yapi_id__exact=yapi_id)
        diff_contents = [{'change': 'interface_add', 'node': '', 'value': ''}]

        logger.info("插入接口变更记录（新增）...")
        history = {
            "api": new_api,
            "event": event,
            "content": json.dumps(diff_contents, ensure_ascii=False),
            "update_status": 0
        }
        if update_time:
            history.update({"update_time": update_time})
        ApiUpdateHistory.objects.create(**history)
        return True

    # diff
    def update(self, event, yapi_info: dict, api_obj, update_time: str = None):
        """
        本地接口已存在， Diff(yapi_info, api_obj->info)
            1. diff 无变更 -> 退出
            2. diff 有变更 -> 插入接口变更记录（更新）-> 更新变更内容
        :param event:
        :param yapi_info: YAPI接口内容 -- 待比较
        :param api_obj: 本地接口obj
        :param update_time: 更新事件时间
        :return:
        """

        # 准备本地接口数据 - 待比较
        api_info = {
            "name": api_obj.name,
            "description": api_obj.description,
            "yapi_id": api_obj.yapi_id,
            "method": api_obj.method,
            "path": api_obj.path,
            "yapi_req_headers": json.loads(api_obj.yapi_req_headers or "[]", strict=False),
            "yapi_req_params": json.loads(api_obj.yapi_req_params or "[]", strict=False),
            "yapi_req_query": json.loads(api_obj.yapi_req_query or "[]", strict=False),
            "yapi_req_body_form": json.loads(api_obj.yapi_req_body_form or "[]", strict=False),
            "yapi_req_body_other": json.loads(api_obj.yapi_req_body_other or "{}", strict=False),
            "yapi_res_body": json.loads(api_obj.yapi_res_body or "{}", strict=False),
        }

        yapi_id = yapi_info['yapi_id']
        logger.info("diff接口变更：yapi({})===>api({}:{})".format(yapi_id, api_obj.id, api_obj.name))
        diff_result = diff(
            api_info, yapi_info,
            ignore={'yapi_project_id', 'yapi_cat_id'}
        )
        # 转换diff_result:  tuple --> dict，方便前端解析
        diff_contents = []
        for df in diff_result:
            diff_content = {
                "change": df[0],
                "node": df[1],
                "value": df[2],
            }
            diff_contents.append(diff_content)

        # diff 无变更 -> 退出
        if len(diff_contents) == 0:
            logger.info("diff结果：接口无变更...")
            if api_obj.api_group:
                # 接口无分组信息，仍然拉取数据更新
                return True

        api_define_changed = True
        if len(diff_contents) == 1 and diff_contents[0]['node'] == 'yapi_id':
            # 接口变更内容仅 yapi_id，只更新内容，不修改变更状态
            api_define_changed = False
        # diff 有变更 -> 插入接口变更记录（更新）-> 更新变更内容
        logger.info("插入接口变更记录（更新）...")
        history = {
            "api": api_obj,
            "event": event,
            "content": json.dumps(diff_contents, ensure_ascii=False),
            "update_status": 0
        }
        if update_time:
            history.update({"update_time": update_time})
        ApiUpdateHistory.objects.create(**history)

        # 更新yapi_info到api
        logger.info("更新接口变更内容...")
        if not api_obj.api_group:
            # api无project+api_group信息，更新添加
            project_id, api_group_id = self.__insert_yapi_project_cat_info(yapi_info)
            yapi_info.update({'project_id': project_id})
            yapi_info.update({'api_group_id': api_group_id})

        self.__update_yapi_info(yapi_info, api_define_changed)

    def delete(self, event, api_obj, update_time: str = None):
        logger.info("YAPI删除接口，删除/禁用本地接口...")
        if TestStep.objects.filter(apiInfo_id=api_obj.id).count() > 0:
            api_obj.status = False
            api_obj.save()
        else:
            api_obj.status = False
            api_obj.delete()
            api_obj.save()

        logger.info("插入接口变更记录（新增）...")
        diff_contents = [{'change': 'interface_del', 'node': '', 'value': ''}]
        history = {
            "api": api_obj,
            "event": event,
            "content": json.dumps(diff_contents, ensure_ascii=False),
            "update_status": 0
        }
        if update_time:
            history.update({"update_time": update_time})
        ApiUpdateHistory.objects.create(**history)
        return True

    def get_api_list(self, yapi_info):
        """
        根据yapi_info查找本地接口表对应的接口列表
        查找本地接口表，条件：yapi_id
            1. 找到，返回
            2. 未找到：查找本地接口，条件: method+path
        :param yapi_info:
        :return: 本地接口查找结果（list[obj]）
        """
        yapi_id = yapi_info['yapi_id']
        api_objs = ApiInfo.objects.filter(yapi_id__exact=yapi_id)
        if api_objs.count() == 0:
            method = yapi_info.get('method')
            path = yapi_info.get('path')
            api_objs = ApiInfo.objects.filter(method__exact=method, path__exact=path)
        return api_objs

    def data_sync(self, yapi_event: dict):
        """
        根据收到的yapi事件信息，同步YAPI数据到本地数据库
        YAPI事件处理，类型：
            1. 客户端更新接口成功后触发： interface_update
                {'_id': 365459, 'YApiEvent': 'yapi_interface_update'}
            2. 客户端新增接口成功后触发：interface_add
                TODO
            3. 客户端删除接口成功后触发
                TODO
        :param yapi_event:
        :return:
        """
        logger.debug(yapi_event)
        yapi_event_id = yapi_event.get('id')
        yapi_event_content = yapi_event.get('content')
        yapi_event_time = yapi_event.get('update_time', '')
        event = yapi_event.get('event')
        yapi_id = yapi_event.get('yapi_id')
        # 主动拉取yapi时，如果本地无yapi_id信息，使用method+path检索
        method = yapi_event.get('method', '')
        api_full_path = yapi_event.get('path')
        yapi_db = YapiMongoDB()

        if yapi_id:
            # 根据yapi_id获取yapi_info，如找不到yapi对应信息，删除本地YapiEvent
            try:
                yapi_info = yapi_db.get_api_info_by_id(yapi_id)
            except Exception as e:
                logger.error(e)
                YApiEvent.objects.filter(id__exact=yapi_event_id).delete()
                response = {
                    "msg": str(e),
                    "yapi_event": yapi_event_content
                }
                return response
        elif method and api_full_path:
            # 根据api method+path获取yapi info  -- 模拟构造的yapi_event
            try:
                yapi_info = yapi_db.get_api_info_by_method_path(method, api_full_path)
            except Exception as e:
                logger.error(e)
                YApiEvent.objects.filter(id__exact=yapi_event_id).delete()
                response = {
                    "msg": str(e),
                    "yapi_event": yapi_event_content
                }
                return response
        else:
            response = {
                "msg": "无效的参数，找不到yapi信息",
                "yapi_event": yapi_event_content
            }
            return response

        if event == 'pull_yapi_info':
            # 主动拉取，直接更新本地接口
            api_id = yapi_event.get('api_id')
            api = ApiInfo.objects.filter(id__exact=api_id).first()
            # 是否更新api 项目+分组信息
            self.update(event, yapi_info, api, yapi_event_time)
        else:
            # yapi web hook 事件
            # 获取api_info --> 更新处理
            api_objs = self.get_api_list(yapi_info)
            api_count = api_objs.count()
            # yapi事件 - del - 删除本地接口
            if event == 'yapi_interface_del' and api_count > 0:
                for api_obj in api_objs.all():
                    self.delete(event, api_obj, yapi_event_time)
                YApiEvent.objects.filter(id__exact=yapi_event_id).delete()
                response = {
                    "msg": "本地接口删除/禁用完成",
                    "yapi_event": yapi_event_content
                }
                return response
            else:
                # yapi_interface_add || yapi_interface_update
                if api_count == 0:
                    # 本地无该接口，插入数据
                    self.insert(event, yapi_info, yapi_event_time)
                else:
                    api = api_objs.first()
                    self.update(event, yapi_info, api, yapi_event_time)

        # 处理完成，删除本地YapiEvent
        logger.info("数据同步更新处理成功，删除已同步事件id:{},yapi_id:{},event:{}...".format(
            yapi_event_id, yapi_id, event))
        YApiEvent.objects.filter(id__exact=yapi_event_id).delete()

        response = {
            "msg": "更新处理成功！",
            "yapi_event": yapi_event_content
        }
        return response

    def data_sync_bulk(self, yapi_events=None, max_workers=2):
        """
        批量数据同步
        :param yapi_events: 列表，list[dict1,dict2]
        :param max_workers: 多线程执行-最大线程数
        :return:
        """
        if yapi_events is None:
            yapi_events = []
        response_list = []
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_event = {executor.submit(self.data_sync, yapi_event): yapi_event for yapi_event in yapi_events}
            for future in as_completed(future_to_event):
                try:
                    response_list.append(future.result())
                except Exception as e:
                    logger.error(e)
                    yapi_event = future_to_event[future]
                    response = {"msg": str(e), "yapi_event": yapi_event.get('content')}
                    response_list.append(response)
        return response_list

    def data_sync_all(self):
        """
        查询本地YApiEvent表，遍历所有事件并做更新处理
        :return:
        """
        yapi_events = YApiEvent.objects.values()
        return self.data_sync_bulk(yapi_events, max_workers=4)


if __name__ == '__main__':
    pass
