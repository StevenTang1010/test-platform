# --------------------------------------
# Date: 2021/8/5
# @Author: Steven_Tang
# FileName: orders.py
# Description: 工单数据统计清洗
# --------------------------------------
import datetime
import json
# import time
from collections import defaultdict

import requests
import yaml
# from dateutil.relativedelta import relativedelta
# from django.db.models import Count
from rest_framework.serializers import Serializer

from apps.bug_analysis.models import Orders


class OrderList:

    # 通过计费获取超管session
    def get_session(self) -> str:
        '''
        通过计费获取超管sessionid
        '''
        data = {
            'method': 'get',
            'url': f'https://bill.dustess.com/api/v1/public/account/backServiceAddress?id=W00000000001',
            'headers': {
                'Authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJ3cGJpbGwiLCJzdWIiOiJ0ZXN0X2RlcHQifQ.bd0HKqB-LV7xYIk_9N8SqmUAhwe4uzZplkJlRSTvWL4'}
        }
        res = requests.request(**data).json()
        return res.get('data', {}).get('url').split('sessionId=')[1]

    # 获取研发中心成员信息
    def get_department_info(self, num=None) -> None:
        session = self.get_session()
        url = 'https://mk.dustess.com/qw-scrm-svc/action/department/allList'
        headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36',
            'authorization': session
        }
        res = requests.request('post', url, headers=headers)
        id_mapping = {}
        member_dict = {}
        dev_lst = ['CRM测试组', '营销测试组', '商城测试组', '客服测试组', '运营测试组', '私有云测试组', '数据与智能化测试组', '平台测试组']
        dep_mapping = {'营销测试组': '营销', '客服测试组': '客服', '商城测试组': '商城', 'CRM测试组': 'CRM', '运营测试组': '运营',
                       '私有云测试组': '私有云', '平台测试组': '平台', '数据与智能化测试组': '数据中台'}
        for d in res.json().get('data').get('list'):
            if d.get('name') in dev_lst:
                id_mapping.setdefault(d.get('id'), dep_mapping.get(d.get('name'), d.get('name')))
        for did, dep in id_mapping.items():
            url = f'https://mk.dustess.com/biz/v1/qw_account/address-book/user/list?deptId={did}&page=1&pageSize=100'
            headers = {
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36',
                'authorization': session
            }
            res = requests.request('get', url, headers=headers).json()

            member_list = []
            for member in res.get('data').get('list'):
                member_list.append(member.get('name').replace(' ', ''))
            # if dep in ['CRM组', '营销组', '商城组', '客服/智能获客组', '运营计费组', '医美组', '项目管理组', '大数据组', '私有化组', '产业互联组']:
            #     member_dict['产品'].extend(member_list)
            # else:
            member_dict[dep] = member_list
        if num:
            with open('dep_member.yaml', 'w', encoding='utf8') as f:
                yaml.safe_dump(member_dict, f, allow_unicode=True)

    # 获取工单详情
    def get_order_info(self, status=None) -> list:
        f = open('tools/dep_member.yaml', encoding='utf8')
        deps = yaml.safe_load(f)
        end_time = datetime.datetime.now() + datetime.timedelta(days=1)
        end = end_time.strftime("%Y-%m-%d")
        f.close()
        session = self.get_session()
        start = Orders.objects.first().pub_date
        url = 'https://mk.dustess.com/java-work-service/api/v1/ticket_query/page-list'
        headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36',
            'authorization': session
        }
        data = {
            'pageIndex': 1,
            'pageSize': 100,
            'templateNodeMap': {
                "default_W00000000001": {
                    "61cbf966ea3b0f780ec4cd4e": [
                        "3a7fb916-8d6d-41cc-9583-e5f2827b253f",
                        "a7438fdd-dd17-4cf2-9d1d-379d8f17f4f8",
                        "cd472554-272a-43da-b8e1-9a5752fc3513",
                        "4ff2ad30-89f7-4423-ae89-6a4a5962d966",
                        "5cc1b664-7a31-44c8-ad3e-e9427f3b7592",
                        "677db502-358e-4171-9d6b-f571a83bac6f",
                        "7ff661ac-d1f5-48f2-be46-e8eab22b06fd",
                        "9a5f19d8-169d-4af1-9a90-0f0a82502713",
                        "e3082418-f6d3-43a9-a957-6f1d391886c2"
                    ]
                }
            },
            'tagIds': [],
            'pageType': 'ALL',
            'beginTime': f'{start} 00:00:00' if start else '',
            'endTime': f'{end} 23:59:59' if start else '',
            'states': [status] if status else [],
            'orderBy': 'updateTime'
        }  # 请求工单列表参数
        import loguru
        loguru.logger.info(data)
        # print(data)
        response = requests.request('post', url, headers=headers, json=data).json()
        res = response.get('data').get('list')
        data_list = []

        # 转换优先级
        def set_value(data):
            if data == 'VERY_URGENT':
                return '非常紧急'
            elif data == 'URGENT':
                return '紧急'
            elif data == 'NORMAL':
                return '一般'
            else:
                return '低'

        # 获取工单详情的类型、状态、工单号
        def get_ticket_detail1(ticketid: str) -> dict:
            url = f'https://mk.dustess.com/java-work-service/api/v1/ticket_operate/detail?id={ticketid}'
            headers = {
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36',
                'authorization': session
            }
            response = json.loads(requests.request('get', url, headers=headers).text)
            res = response.get('data')
            severities = ['P0', 'P1', 'P2', 'P3']
            severity = {}
            for tag in res.get('tags'):
                for tag_name in tag.get('tagList'):
                    if tag_name.get('name') in severities:
                        severity['severity'] = tag_name.get('name')
            ticket_msg = {
                # 'stateName': res.get('stateName', ''),  # 提取工单状态
                'ticketNumber': res.get('ticketNumber', ''),  # 提取工单号
                'priority': set_value(res.get('priority', ''))}  # 提取优先级
            ticket_msg.update(severity)
            return ticket_msg

        # 获取工单详情的解决人、问题原因
        def get_ticket_detail(ticketid: str):
            ticket_msg = get_ticket_detail1(ticketid)
            if not ticket_msg:
                return False
            url = f'https://mk.dustess.com/java-work-service/api/v1/ticket_record/list?ticketId={ticketid}'
            headers = {
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36',
                'authorization': session
            }
            response = json.loads(requests.request('get', url, headers=headers).text)
            res = response.get('data').get('list')  # 拿到流转和回复详情
            # if ticket_msg.get('stateName') == '已完结':
            #     step = res[1]
            team_member = ''
            for item in res:
                if item.get('nodeName') == 'bug处理':
                    team_member = item.get('fromAcceptorName')  # 提取测试人员

            # 解决人
            ticket_msg.setdefault('team_member', team_member.replace(' ', ''))
            for dept, names in deps.items():
                if ticket_msg.get('team_member') in names:
                    ticket_msg.setdefault('domain', dept)  # 判断归属团队
                    break
            ticket_msg.setdefault('domain', '')
            return ticket_msg

        # 将时间秒转换为时间
        def math_time(seconds):
            if seconds:
                m, s = divmod(seconds, 60)
                h, m = divmod(m, 60)
                return h
            return 0

        for ticket in res:
            order_detail = {}
            tid = ticket.get('id')
            ticket_msg = get_ticket_detail(tid)
            if not ticket_msg:
                continue
            order_detail['ticket_number'] = ticket_msg.get('ticketNumber')
            order_detail['priority'] = ticket_msg.get('priority')
            order_detail['severity'] = ticket_msg.get('severity')
            order_detail['content'] = ticket.get('content')
            # order_detail['team_member'] = ticket_msg.get('team_member')  # 当前解决人
            # order_detail['handling_time'] = math_time(ticket.get('totalAcceptorSeconds'))  # 解决时长
            order_detail['domain'] = ticket_msg.get('domain')
            date_list = list(ticket_msg.get('ticketNumber')[:8])
            date_list.insert(4, '-')
            date_list.insert(7, '-')
            pub_date = datetime.datetime.strptime(''.join(date_list), '%Y-%m-%d').date()
            order_detail['pub_date'] = pub_date
            data_list.append(order_detail)
            # time.sleep(3)
        return data_list

    # 获取工单更新数据
    def get_orders_data(self) -> list:
        return self.get_order_info()


class EchartsDataAnalysis:

    def __init__(self, data: Serializer = None):
        self.data = OrderData(data)

    # 获取BUG分类趋势
    def bug_trend(self) -> dict:
        """
        BUG分类统计趋势
        :param
        :return:
        """
        # 获取各个图表X轴、Y轴数据
        # 漏测原因
        missing_reasion_count_dict = self.data.count_date_missing_values_list(self.data.data)
        missing_reasion_count_month_list = []
        title_list = ['日期']
        missing_list = ['漏测']
        influence_list = ['影响范围']
        entrainment_list = ['夹带']
        nothing_list = ['无法模拟场景']
        history_list = ['环境问题']
        design_list = ['人为操作']
        nodo_list = ['已知BUG']
        third = ['第三方']
        missing_reasion_series = []
        for date, count in missing_reasion_count_dict:
            title_list.append(date)
            missing_list.append(count.get('漏测', 0))
            influence_list.append(count.get('影响范围', 0))
            entrainment_list.append(count.get('夹带', 0))
            nothing_list.append(count.get('无法模拟场景', 0))
            history_list.append(count.get('环境问题', 0))
            design_list.append(count.get('人为操作', 0))
            nodo_list.append(count.get('已知BUG', 0))
            third.append(count.get('第三方', 0))
            missing_reasion_series.append({'type': 'line',
                                           'smooth': True,
                                           'seriesLayoutBy': 'row',
                                           'emphasis': {'focus': 'series'}})
        missing_reasion_count_month_list.append(title_list)
        missing_reasion_count_month_list.append(missing_list)
        missing_reasion_count_month_list.append(influence_list)
        missing_reasion_count_month_list.append(entrainment_list)
        missing_reasion_count_month_list.append(nothing_list)
        missing_reasion_count_month_list.append(history_list)
        missing_reasion_count_month_list.append(design_list)
        missing_reasion_count_month_list.append(nodo_list)
        missing_reasion_count_month_list.append(third)
        missing_reasion_series.append({
            'type': 'pie',
            'id': 'pie',
            'radius': '50%',
            'center': ['50%', '26%'],
            'emphasis': {
                'focus': 'self'
            },
            'encode': {
                'itemName': title_list[0],
                'value': title_list[1],
                'tooltip': title_list[1]
            }
        })
        return {
            # 漏测原因 PIE
            'missing_reasion_count_month_list': list(missing_reasion_count_month_list),
            'missing_reasion_series': missing_reasion_series,
        }

    # 按列分组统计
    def count_column_values_lst(self, filter_data, column_name, sort=False) -> tuple:
        """
        统计指定列数据中每个值出现的次数
        :param column_name:
        :param sort:
        :param ignore_none:
        :return:
        """
        total = 0
        value_count_dict = defaultdict(int)
        values_list = filter_data.values_list(column_name)
        if column_name == 'bug_state':
            for v in values_list:
                total += 1
                if v[0]:
                    value_count_dict['是'] += 1
                else:
                    value_count_dict['否'] += 1
        else:
            for v in values_list:
                if not v[0] or v[0] == 'None':
                    continue
                else:
                    value_count_dict[v[0]] += 1
                    total += 1
        value_list = []
        if sort:
            sorted_tuple = sorted(value_count_dict.items(), key=lambda x: x[1], reverse=True)
            for k, v in sorted_tuple:
                value_list.append({'value': v, 'name': k})
        else:
            for v in value_list:
                value_list.append({'value': v[1], 'name': v[0]})
        return value_list, total


class OrderData:
    """order表数据查询封装"""

    def __init__(self, data: Serializer = None):
        self.data = data

    # 计算每月漏测的数量和
    def count_date_missing_values_list(self, data):
        """
        :return:
        """
        year_count = {}
        for item in data.instance:
            month = item.pub_date.month
            year = item.pub_date.year
            month_count = year_count.setdefault(f'{str(year)}-{str(month)}', {})
            if item.bug_reason:
                if month_count.get(item.bug_reason):
                    month_count[item.bug_reason] += 1
                else:
                    month_count[item.bug_reason] = 1
        count_list = list(year_count.items())
        count_list.reverse()
        return count_list


if __name__ == '__main__':
    od = OrderList()
    od.get_department_info()
    pass
