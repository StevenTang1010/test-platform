# --------------------------------------
# Date: 2021/11/1
# @Author: Steven_Tang
# FileName: zt_bug.py   
# Description: 禅道BUG通告
# --------------------------------------

import datetime
import pymysql
import json
import requests


# from apps.bug_analysis.models import ZtBug, TesterZtBug, DeveloperZtBug


class BugReport:
    '''
    sql语句封装
    '''

    def __init__(self):
        self.db = pymysql.connect(host='192.168.0.20',
                                  port=3306,
                                  user='watcher',
                                  password='watcher@123456',
                                  database='zentao')
        # self.cursor = self.db.cursor(cursor=pymysql.cursors.DictCursor)
        self.cursor = self.db.cursor()
        self.today = datetime.datetime.now().strftime('%Y-%m-%d')  # 今天的日期

    def __del__(self):
        self.db.close()

    def test_bug_count(self):
        '''
        统计当天bug数据
        '''
        self.cursor.execute(f"select count(*) from zt_bug where deleted='0' and openedDate >= '{self.today}';")
        # bug总数
        today_bug = self.cursor.fetchall()[0]
        # 已解决的bug
        self.cursor.execute(
            f"select count(*) from zt_bug where deleted = '0' and status = 'resolved' and resolution = 'fixed' and openedDate >= '{self.today}';")
        resolved_bug = self.cursor.fetchall()[0]
        # 激活的bug
        self.cursor.execute(
            f"select count(*) from zt_bug where deleted = '0' and `status` =  'active' and openedDate >= '{self.today}'")
        active_bug = self.cursor.fetchall()[0]
        # reopen的bug
        self.cursor.execute(
            f"select count(*) from zt_bug where deleted = '0' and `activatedCount` > '0' and activatedDate >= '{self.today}'")
        reopen_bug = self.cursor.fetchall()[0]

        try:
            solution = round(resolved_bug[0] / today_bug[0] * 100, 2)
        except:
            solution = 0
        # active_detail = self.bug_detail()
        bug_str = f"每日质量晚报：\n今日新增Bug数: {today_bug[0]}\n今日Bug解决率: {solution}%\n今日剩余激活Bug: {active_bug[0]}\n今日reopen: {reopen_bug[0]}\n"
        return bug_str

    def bug_detail(self):
        '''
        获取未解决明细数据
        '''
        # bug_detail_sql = f"-- SELECT b.id,b.title,b.assignedTo,b.severity,b.type,b.status from zt_bug b where deleted = '0' and `status` !=  'resolved' and openedDate >= '2021-11-01';"
        bug_detail_sql = f"SELECT b.id,b.title,b.assignedTo,b.severity,b.type,b.status from zt_bug b where deleted = '0' and `status` !=  'resolved' and openedDate >= '{self.today}';"
        self.cursor.execute(bug_detail_sql)
        bug_detail = self.cursor.fetchall()
        return bug_detail

    def send_report(self):
        """
        发送企微群消息通知
        :return:
        """
        text = self.test_bug_count()
        url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=b3174458-ae4c-45f4-aa3d-fd09c38d60e4'
        data = {
            "msgtype": "text",
            "text": {
                "content": text
            }
        }
        headers = {'Content-Type': 'application/json'}
        res = requests.post(url, json=data, headers=headers)  # 群消息通知
        print(res.json())

    # 统计需要的BUG数据
    def get_bug_data(self):
        build_lst = ['商城1.7.7', 'CRM1.0', 'BI v1.1']
        build_dict = []
        # 获取版本id
        for build in build_lst:
            print(build)
            build_info = {'name': build}
            sql = f'select bug.openedBuild from zt_bug as bug join zt_build as b on b.id=bug.openedBuild where bug.deleted="0" and b.name="{build}" and b.deleted="0";'
            self.cursor.execute(sql)
            fetch_one = self.cursor.fetchall()[0]
            build_info['id'] = fetch_one[0]
            build_dict.append(build_info)

        for build in build_dict:
            print(build)
            # 获取单个版本的BUG总量
            sql = f'select COUNT(*) from zt_bug where openedBuild like "%{build.get("id")}%" and deleted="0";'
            self.cursor.execute(sql)
            build['bug_total'] = int(self.cursor.fetchall()[0][0])
            # 统计严重bug总数
            sql = f'select COUNT(*) from zt_bug where openedBuild like "%{build.get("id")}%" and deleted="0" and pri in (1,2);'
            self.cursor.execute(sql)
            build['severity'] = int(self.cursor.fetchall()[0][0])
            # 统计有效bug总数
            sql = f'select COUNT(*) from zt_bug where openedBuild like "%{build.get("id")}%" and deleted="0" and resolution NOT IN ("willnotfix","duplicate","notrepro");'
            self.cursor.execute(sql)
            build['usage'] = int(self.cursor.fetchall()[0][0])
            # 统计解决bug总数
            sql = f'select COUNT(*) from zt_bug where openedBuild like "%{build.get("id")}%" and deleted="0" and resolution = "fixed";'
            self.cursor.execute(sql)
            build['solve'] = int(self.cursor.fetchall()[0][0])
            # 统计reopenbug总数
            sql = f'select COUNT(*) from zt_bug where openedBuild like "%{build.get("id")}%" and deleted="0" and activatedCount  > "0";'
            self.cursor.execute(sql)
            build['reopen'] = int(self.cursor.fetchall()[0][0])
            # 统计关闭bug总数
            sql = f'select COUNT(*) from zt_bug where openedBuild like "%{build.get("id")}%" and deleted="0" and status = "closed";'
            self.cursor.execute(sql)
            build['close'] = int(self.cursor.fetchall()[0][0])
            # 统计遗留激活bug总数
            sql = f'select COUNT(*) from zt_bug where openedBuild like "%{build.get("id")}%" and deleted="0" and (status = "active" or resolution in ("bydesign", "postponed"));'
            self.cursor.execute(sql)
            build['active'] = int(self.cursor.fetchall()[0][0])
            # 统计bug平均解决时长
            sql = f'select avg((UNIX_TIMESTAMP(resolvedDate) - UNIX_TIMESTAMP(openedDate))/3600) as time from zt_bug where openedBuild like "%{build.get("id")}%" and deleted="0";'
            self.cursor.execute(sql)
            build['solve_avg'] = int(self.cursor.fetchall()[0][0])
            # 统计bug最大解决时长
            sql = f'select max((UNIX_TIMESTAMP(resolvedDate) - UNIX_TIMESTAMP(openedDate))/3600) as time from zt_bug where openedBuild like "%{build.get("id")}%" and deleted="0";'
            self.cursor.execute(sql)
            build['solve_max'] = int(self.cursor.fetchall()[0][0])
            # 统计bug平均关闭时长
            sql = f'select avg((UNIX_TIMESTAMP(closedDate) - UNIX_TIMESTAMP(resolvedDate))/3600) as time from zt_bug where openedBuild like "%{build.get("id")}%" and deleted="0";'
            self.cursor.execute(sql)
            build['close_avg'] = int(self.cursor.fetchall()[0][0])
            # 统计bug最大解决时长
            sql = f'select max((UNIX_TIMESTAMP(closedDate) - UNIX_TIMESTAMP(resolvedDate))/3600) as time from zt_bug where openedBuild like "%{build.get("id")}%" and deleted="0";'
            self.cursor.execute(sql)
            build['close_max'] = int(self.cursor.fetchall()[0][0])
            # 统计个人创建BUG数
            sql = f'select b.realname, count(b.id) from zt_bug as bug join zt_user as b on b.account=bug.openedBy where bug.deleted="0" and bug.openedBuild like "%{build.get("id")}%" GROUP BY bug.openedBy;'
            self.cursor.execute(sql)
            build['opened_person'] = dict(self.cursor.fetchall())
            # 统计个人解决BUG数
            sql = f'select b.realname, count(b.id) from zt_bug as bug join zt_user as b on b.account=bug.resolvedBy where bug.deleted="0" and openedBuild like "%{build.get("id")}%" GROUP BY bug.resolvedBy;'
            self.cursor.execute(sql)
            build['solver_person'] = dict(self.cursor.fetchall())
            # 统计创建人严重BUG数
            sql = f'select b.realname, count(b.id) from zt_bug as bug join zt_user as b on b.account=bug.openedBy where bug.pri IN (1,2) and bug.deleted="0" and openedBuild like "%{build.get("id")}%" GROUP BY b.realname;'
            self.cursor.execute(sql)
            build['opened_severity'] = dict(self.cursor.fetchall())
            # 统计解决人严重BUG数
            sql = f'select b.realname, count(b.id) from zt_bug as bug join zt_user as b on b.account=bug.resolvedBy where bug.pri IN (1,2) and bug.deleted="0" and openedBuild like "%{build.get("id")}%" GROUP BY b.realname;'
            self.cursor.execute(sql)
            build['solver_severity'] = dict(self.cursor.fetchall())
            # 统计创建人有效BUG数
            sql = f'select b.realname, count(b.id) from zt_bug as bug join zt_user as b on b.account=bug.openedBy where resolution NOT IN ("willnotfix","duplicate","notrepro") and bug.deleted="0" and openedBuild like "%{build.get("id")}%" GROUP BY b.realname;'
            self.cursor.execute(sql)
            build['opened_usage'] = dict(self.cursor.fetchall())
            # 统计解决人解决BUG数
            sql = f'select b.realname, count(b.id) from zt_bug as bug join zt_user as b on b.account=bug.resolvedBy where resolution = "fixed" and bug.deleted="0" and openedBuild like "%{build.get("id")}%" GROUP BY b.realname;'
            self.cursor.execute(sql)
            build['solver_slove'] = dict(self.cursor.fetchall())
            # 统计解决人reopenBUG数
            sql = f'select b.realname, count(b.id) from zt_bug as bug join zt_user as b on b.account=bug.resolvedBy where activatedCount  > "0" and bug.deleted="0" and openedBuild like "%{build.get("id")}%" GROUP BY b.realname;'
            self.cursor.execute(sql)
            build['solver_reopen'] = dict(self.cursor.fetchall())
            # 统计创建人关闭BUG数
            sql = f'select b.realname, count(b.id) from zt_bug as bug join zt_user as b on b.account=bug.openedBy where status = "closed" and bug.deleted="0" and openedBuild like "%{build.get("id")}%" GROUP BY b.realname;'
            self.cursor.execute(sql)
            build['opened_close'] = dict(self.cursor.fetchall())
            # 统计人遗留BUG数
            sql = f'select b.realname, count(b.id) from zt_bug as bug join zt_user as b on b.account=bug.openedBy where (bug.status = "active" or bug.resolution in ("bydesign", "postponed")) and bug.deleted="0" and openedBuild like "%{build.get("id")}%" GROUP BY b.realname;'
            self.cursor.execute(sql)
            build['solver_active'] = dict(self.cursor.fetchall())
        print(build_dict)
        with open('zt_bug.json', 'w', encoding='utf8') as f:
            json.dump(build_dict, f, ensure_ascii=False)

    # 提取创建者禅道数据
    def get_test_data(self, start_time='2021-01-01'):
        tester_list = []
        # 查询所有BUG创建者数据
        sql = 'select b.id as build_id, b.name as build_name,p.name as prj_name,bug.openedBy,u.id as user_id,u.realname,d.name,' \
              'count(bug.id) as total_create,' \
              'SUM(case when bug.pri in (1,2) then 1 else 0 end) as severity_total,' \
              'SUM(case when bug.resolution NOT IN ("willnotfix","duplicate","notrepro") then 1 else 0 end) as usage_total,' \
              'SUM(case when bug.status = "closed" then 1 else 0 end) as closed_total,' \
              'SUM(case when bug.status = "active" or bug.resolution in ("bydesign", "postponed") then 1 else 0 end) as active_total ' \
              f'from zt_bug as bug left join zt_build as b on b.id=bug.openedBuild left join zt_user as u on bug.openedBy=u.account ' \
              f'left join zt_dept as d on u.dept=d.id left join zt_product as p on b.product=p.id where b.deleted="0" and u.deleted="0" and b.date>="{start_time}" GROUP BY b.name,bug.openedBy;'
        self.cursor.execute(sql)
        testers = self.cursor.fetchall()
        for tester in testers:
            tester_info = {}
            tester_info['tester_id'] = tester.get('user_id')
            tester_info['tester_name'] = tester.get('realname')
            tester_info['prj_name'] = tester.get('prj_name')
            tester_info['edition_id_id'] = tester.get('build_id')
            tester_info['edition_name'] = tester.get('build_name')
            tester_info['bug_total'] = int(str(tester.get('total_create', 0)))
            tester_info['severity'] = int(str(tester.get('severity_total', 0)))
            tester_info['usages'] = int(str(tester.get('usage_total', 0)))
            tester_info['closed'] = int(str(tester.get('closed_total', 0)))
            tester_info['leave_over'] = int(str(tester.get('active_total', 0)))
            tester_info['update_time'] = self.today
            tester_list.append(tester_info)
        print(len(tester_list))
        return tester_list

# 按部门查bug总数和reopen总数
# '''
# select u.realname,count(bug.id) as total,
# 	SUM(case when bug.activatedCount  > "0" then 1 else 0 end) as reopen_total
#               from zt_bug as bug left join zt_user as u on bug.resolvedBy=u.account
#               left join zt_product as p on bug.product=p.id where u.deleted="0" and bug.openedDate>="2021-07-01" and p.id=26 GROUP by bug.resolvedBy;
# '''

    # 提取禅道解决者数据
    def get_dev_data(self, start_time='2021-01-01'):
        developer_list = []
        sql = 'select b.id as build_id, b.name as build_name,bug.resolvedBy,u.id as user_id,u.realname,d.name as dept_name,' \
              'count(bug.id) as total_solve, ' \
              'SUM(case when bug.pri in (1,2) then 1 else 0 end) as severity_total, ' \
              'SUM(case when bug.resolution = "fixed" then 1 else 0 end) as fixed_total, ' \
              'SUM(case when bug.activatedCount  > "0" then 1 else 0 end) as reopen_total ' \
              'from zt_bug as bug left join zt_build as b on b.id=bug.openedBuild left join zt_user as u on bug.resolvedBy=u.account ' \
              f'left join zt_dept as d on u.dept=d.id where b.deleted="0" and u.deleted="0" and b.date>="{start_time}" GROUP BY b.name,bug.resolvedBy;'
        self.cursor.execute(sql)
        developers = self.cursor.fetchall()
        for developer in developers:
            developer_info = {}
            developer_info['solve_id'] = developer.get('user_id')
            developer_info['solver_name'] = developer.get('realname')
            developer_info['dept'] = developer.get('dept_name')
            developer_info['edition_id_id'] = developer.get('build_id')
            developer_info['edition_name'] = developer.get('build_name')
            developer_info['bug_total'] = int(str(developer.get('total_solve')))
            developer_info['severity'] = int(str(developer.get('severity_total')))
            developer_info['solve'] = int(str(developer.get('fixed_total')))
            developer_info['reopen'] = int(str(developer.get('reopen_total')))
            developer_info['update_time'] = self.today
            developer_list.append(developer_info)
            # print(developer_info)
        print(len(developer_list))
        return developer_list


class ZtBugUpdate:
    '''
    禅道bug数据定时统计更新任务
    '''

    def __init__(self):
        self.db = pymysql.connect(host='localhost',
                                  port=3306,
                                  user='root',
                                  password='tangxiaoyu1.',
                                  database='apiplatform')
        self.cursor = self.db.cursor(cursor=pymysql.cursors.DictCursor)
        self.today = datetime.datetime.now().strftime('%Y-%m-%d')  # 今天的日期

    def __del__(self):
        self.db.close()

    def update(self):
        # 查询最后一次更新版本数据的时间
        sql = 'select date_format(update_time, "%Y-%m-%d") as day_time from bug_analysis_ztbug order by "update_time" desc;'
        print(sql)
        self.cursor.execute(sql)
        last_up_time = self.cursor.fetchall()
        try:
            last_time = last_up_time[0].get('day_time')
        except Exception as e:
            print('无数据，区今年全年数据')
            last_time = '2021-01-01'
        br = BugReport()

        # 写入tester表
        test_data = br.get_test_data(last_time)
        for row in test_data:
            prj_name = row.pop('prj_name')
            sql = f'select * from bug_analysis_testerztbug where tester_id={row.get("tester_id")} and edition_id_id={row.get("edition_id_id")};'
            self.cursor.execute(sql)
            row_data = self.cursor.fetchall()
            if len(row_data) > 0:
                sql = f'update bug_analysis_testerztbug set ' \
                      f'bug_total=bug_total+{row.get("bug_total", 0)},' \
                      f'severity=severity+{row.get("severity", 0)},' \
                      f'usages=usages+{row.get("usages", 0)},' \
                      f'closed=closed+{row.get("closed", 0)},' \
                      f'leave_over=leave_over+{row.get("leave_over", 0)},' \
                      f'update_time="{row.get("update_time")}" ' \
                      f'where id="{row_data[0].get("id")}";'
                try:
                    self.cursor.execute(sql)
                except Exception as e:
                    print(e)
                else:
                    print('success!')
            else:
                sql = f'insert into bug_analysis_testerztbug ' \
                      f'(tester_id, tester_name,edition_id_id, edition_name, bug_total, severity, usages, closed, leave_over,update_time) ' \
                      f'values {tuple(row.values())};'
                try:
                    self.cursor.execute(sql)
                except Exception as e:
                    print(e)
                else:
                    print('success!')

            # 写入bug表
            sql = f'select * from bug_analysis_ztbug where edition_id={row.get("edition_id_id")};'
            self.cursor.execute(sql)
            build_data = self.cursor.fetchall()
            if len(build_data) > 0:
                sql = f'update bug_analysis_ztbug set ' \
                      f'bug_total=bug_total+{row.get("bug_total")},' \
                      f'severity=severity+{row.get("severity", 0)},' \
                      f'usages=usages+{row.get("usages", 0)},' \
                      f'closed=closed+{row.get("closed", 0)},' \
                      f'leave_over=leave_over+{row.get("leave_over", 0)}, ' \
                      f'update_time="{row.get("update_time")}" ' \
                      f'where edition_id={row.get("edition_id_id")};'
                print(sql)
                self.cursor.execute(sql)
            else:
                sql = f'insert into bug_analysis_ztbug (edition_id,edition_name,project,bug_total,severity,usages,closed,leave_over,update_time)' \
                      f'values ({row.get("edition_id_id")},"{row.get("edition_name")}", "{prj_name}", {row.get("bug_total")},{row.get("severity")},' \
                      f'{row.get("usages")},{row.get("closed")},{row.get("leave_over")},"{self.today}");'
                self.cursor.execute(sql)
        self.db.commit()

        # 写入dev人员表
        dev_data = br.get_dev_data(last_time)
        for row in dev_data:
            sql = f'select * from bug_analysis_developerztbug where solve_id={row.get("solve_id")} and edition_id_id={row.get("edition_id_id")};'
            self.cursor.execute(sql)
            row_data = self.cursor.fetchall()
            if len(row_data) > 0:
                sql = f'update bug_analysis_developerztbug set ' \
                      f'bug_total=bug_total+{row.get("bug_total", 0)},' \
                      f'severity=severity+{row.get("severity", 0)},' \
                      f'solve=solve+{row.get("solve", 0)},' \
                      f'reopen=reopen+{row.get("reopen", 0)}, ' \
                      f'update_time="{row.get("update_time")}" ' \
                      f'where id="{row.get("id")}";'
                try:
                    self.cursor.execute(sql)
                except Exception as e:
                    print(e)
                else:
                    print('success!')
            else:
                print(row.get('dept'))
                sql = f'insert into bug_analysis_developerztbug ' \
                      f'(solve_id, solver_name, edition_id_id, edition_name, dept, bug_total, severity, solve, reopen,update_time) ' \
                      f'values {tuple(row.values())};'
                try:
                    self.cursor.execute(sql)
                except Exception as e:
                    print(e)
                else:
                    print('success!')

            # 写入bug表
            sql = f'update bug_analysis_ztbug set ' \
                  f'solve=(case when solve is null then {row.get("solve", 0)} else solve+{row.get("solve", 0)} end), ' \
                  f'reopen=(case when reopen is null then {row.get("reopen", 0)} else reopen+{row.get("reopen", 0)} end), ' \
                  f'update_time="{row.get("update_time")}" ' \
                  f'where edition_id="{row.get("edition_id_id")}";'
            print(sql)
            self.cursor.execute(sql)
        self.db.commit()


if __name__ == '__main__':
    br = BugReport()
    br.get_bug_data()
    # br.get_test_data()
    # br.get_dev_data()
    # br.send_report()
    # up = ZtBugUpdate()
    # up.update()
