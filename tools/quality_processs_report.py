#!/usr/bin/pytho
# -*-encoding: utf-8 -*-
import os
import json
import xlwt

json_path = r"D:\work\code\MyAuto\script\zt_bug_new.json"
save_path = r"D:\work\code\MyAuto\script\zt_tmp.xlsx"

# 数据保存为插入excel的数据格式
insert_data = {"version_data": [], "tester_data": [], "solver_data": []}


class operate_excel():
    def __init__(self):
        self.workbook = xlwt.Workbook(encoding="utf-8")

    def creat_tmplate(self):
        self.version_sheet = self.workbook.add_sheet("版本数据")
        version_titles = ["版本", "BUG数量", "严重数", "有效数", "解决数", "reopen数", "关闭数", "遗留数", "平均解决时间(h)", "最大解决时间(h)", "平均关闭时间(h)",
                          "最大关闭时间(h)", "严重率", "有效率", "解决率", "reopen率", "关闭率", "遗留率"]
        for i, t in enumerate(version_titles):
            self.version_sheet.write(0, i, t)
        self.version_sheet.col(0).width = 6000
        self.version_sheet.col(8).width = 3000
        self.version_sheet.col(9).width = 3000
        self.version_sheet.col(10).width = 3000
        self.version_sheet.col(11).width = 3000

        self.tester_sheet = self.workbook.add_sheet("测试个人数据")
        tester_titles = ["人员", "PD", "BUG数量", "严重数", "有效数", "关闭数", "遗留数", "BUG/PD比", "严重率", "有效率", "关闭率", "遗留率"]
        for i, t in enumerate(tester_titles):
            self.tester_sheet.write(0, i, t)
        self.tester_sheet.col(0).width = 3000

        self.solver_sheet = self.workbook.add_sheet("解决人数据")
        solver_titles = ["人员", "BUG数量", "严重数", "解决数", "reopen数", "严重率", "解决率", "reopen率"]
        for i, t in enumerate(solver_titles):
            self.solver_sheet.write(0, i, t)
        self.solver_sheet.col(0).width = 3000

    def add_data(self, sheet_name):
        print("%s start insert data" % sheet_name)
        if sheet_name == "版本数据":
            vdata = insert_data.get("version_data")
            for row in range(0, len(vdata)):
                for i, v in enumerate(vdata[row]):
                    self.version_sheet.write(row + 1, i, v)
        elif sheet_name == "测试个人数据":
            tdata = insert_data.get("tester_data")
            for row in range(0, len(tdata)):
                value = list(tdata[row].values())
                for i in range(12):
                    self.tester_sheet.write(row + 1, i, value[i])
        elif sheet_name == "解决人数据":
            sdata = insert_data.get("solver_data")
            for row in range(0, len(sdata)):
                value = list(sdata[row].values())
                for i in range(8):
                    self.solver_sheet.write(row + 1, i, value[i])
        print("%s finish insert data" % sheet_name)

    def save_data(self):
        file = 'zt_tmp.xlsx'
        if os.path.exists(file):
            os.remove(file)
        self.workbook.save(file)
        print("save_data success")


# 读取json文件数据
def read_json():
    path = 'zt_bug.json'
    try:
        print("start read json file...")
        with open(path, encoding="utf-8") as f:
            res_json = json.load(f)
            print("finish read json file...")
            return res_json
    except Exception as e:
        print("read_json err: ", e)


# 处理读取出来的json数据
def handle_json(data: list):
    print("start handle json...")
    for d in data:
        vlist = []  # 获取原始的版本数据
        vlist.append(d.get("name"))
        total = d.get("bug_total")
        vlist.append(total)
        vlist.append(d.get("severity", 0))
        vlist.append(d.get("usage", 0))
        vlist.append(d.get("solve", 0))
        vlist.append(d.get("reopen", 0))
        vlist.append(d.get("close", 0))
        vlist.append(d.get("active", 0))
        vlist.append(d.get("solve_avg", 0))
        vlist.append(d.get("solve_max", 0))
        vlist.append(d.get("close_avg", 0))
        vlist.append(d.get("close_max", 0))
        vlist.append("{:.2f}%".format(d.get("severity") / total * 100))
        vlist.append("{:.2f}%".format(d.get("usage") / total * 100))
        vlist.append("{:.2f}%".format(d.get("solve") / total * 100))
        vlist.append("{:.2f}%".format(d.get("reopen") / total * 100))
        vlist.append("{:.2f}%".format(d.get("close") / total * 100))
        vlist.append("{:.2f}%".format(d.get("active") / total * 100))
        insert_data.get("version_data").append(vlist)
        # 获取原始的opened数据
        for k, total in d.get("opened_person").items():
            opened = {"person": "", "pd": 0, "bug": 0, "severity": 0, "usage": 0, "close": 0, "active": 0, "pd_rate": 0,
                      "severity_rate": 0, "usage_rate": 0, "close_rate": 0, "active_rate": 0}

            opened["person"] = k
            opened["bug"] = total
            opened["severity"] = d.get("opened_severity").get(k, 0)
            opened["usage"] = d.get("opened_usage").get(k, 0)
            opened["close"] = d.get("opened_close").get(k, 0)
            opened["active"] = d.get("solver_active").get(k, 0)
            insert_data.get("tester_data").append(opened)
        # 获取原始的solver数据
        for k, total in d.get("solver_person").items():
            solver = {"person": "", "bug": 0, "severity": 0, "solve": 0, "reopen": 0, "severity_rate": 0,
                      "solve_rate": 0, "reopen_rate": 0}
            solver["person"] = k
            solver["bug"] = total
            solver["severity"] = d.get("solver_severity").get(k, 0)
            solver["solve"] = d.get("solver_slove").get(k, 0)
            solver["reopen"] = d.get("solver_reopen").get(k, 0)
            insert_data.get("solver_data").append(solver)
    print("finish handle json...")
    try:
        handle_data_to_excel()
    except Exception as e:
        print("handle_data_to_excel err: ", e)


# 处理成可直接插入excel的数据
def handle_data_to_excel():
    # 处理版本数据汇总
    vdata = insert_data.get("version_data")
    total = ["统计"]
    for i in range(7):
        t = 0
        for v in vdata:
            t = t + v[i + 1]
        total.append(t)
    num = len(vdata)
    for i in range(8, 12):
        t = 0
        for v in vdata:
            t = t+v[i]
        total.append(round(t/num,2))
    total.append("{:.2f}%".format(total[2] / total[1] * 100))
    total.append("{:.2f}%".format(total[3] / total[1] * 100))
    total.append("{:.2f}%".format(total[4] / total[1] * 100))
    total.append("{:.2f}%".format(total[5] / total[1] * 100))
    total.append("{:.2f}%".format(total[6] / total[1] * 100))
    total.append("{:.2f}%".format(total[7] / total[1] * 100))
    insert_data.get("version_data").append(total)
    # 处理opened数据 去重
    tdata = insert_data.get("tester_data")
    len_num = len(tdata)
    new_tdata = []  # 保存新的opened数据
    for i, p in enumerate(tdata):
        if i + 1 > len_num:
            break
        for new in new_tdata:
            if p.get("person") == new.get("person"):
                break
        else:
            for k in range(i + 1, len_num):
                if p.get("person") == tdata[k].get("person"):
                    dup = tdata[k]
                    p["pd"] = p.get("pd", 0) + dup.get("pd", 0)
                    p["bug"] = p.get("bug", 0) + dup.get("bug", 0)
                    p["severity"] = p.get("severity", 0) + dup.get("severity", 0)
                    p["usage"] = p.get("usage", 0) + dup.get("usage", 0)
                    p["close"] = p.get("close", 0) + dup.get("close", 0)
                    p["active"] = p.get("active", 0) + dup.get("active", 0)
            new_tdata.append(p)
    # 计算opened总计数据
    t_total = {"person": "总数", "pd": 0}
    for i in ["bug", "severity", "usage", "close", "active"]:
        num = 0
        for t in new_tdata:
            num = num + t.get(i, 0)
        t_total[i] = num
    t_total["pd_rate"] = 0
    t_total["severity_rate"] = "{:.2f}%".format(t_total.get("severity", 0) / t_total.get("bug", 0) * 100)
    t_total["usage_rate"] = "{:.2f}%".format(t_total.get("usage", 0) / t_total.get("bug", 0) * 100)
    t_total["close_rate"] = "{:.2f}%".format(t_total.get("close", 0) / t_total.get("bug", 0) * 100)
    t_total["active_rate"] = "{:.2f}%".format(t_total.get("active", 0) / t_total.get("bug", 0) * 100)
    new_tdata.append(t_total)
    # 计算opened数据的效能
    for p in new_tdata:
        total = p.get("bug")
        p["severity_rate"] = "{:.2f}%".format(p.get("severity") / total * 100)
        p["usage_rate"] = "{:.2f}%".format(p.get("usage") / total * 100)
        p["close_rate"] = "{:.2f}%".format(p.get("close") / total * 100)
        p["active_rate"] = "{:.2f}%".format(p.get("active") / total * 100)
    insert_data["tester_data"] = new_tdata
    # 处理solver数据去重
    sdata = insert_data.get("solver_data")
    len_num = len(sdata)
    new_sdata = []
    for i, p in enumerate(sdata):
        if i + 1 > len_num:
            break
        for new in new_sdata:
            if p.get("person") == new.get("person"):
                break
        else:
            for k in range(i + 1, len_num):
                if p.get("person") == sdata[k].get("person"):
                    dup = sdata[k]
                    p["bug"] = p.get("bug", 0) + dup.get("bug", 0)
                    p["severity"] = p.get("severity", 0) + dup.get("severity", 0)
                    p["solve"] = p.get("solve", 0) + dup.get("solve", 0)
                    p["reopen"] = p.get("reopen", 0) + dup.get("reopen", 0)
            new_sdata.append(p)
    # 处理solver数据总计
    s_total = {"person": "总数"}
    for i in ["bug", "severity", "solve", "reopen"]:
        num = 0
        for t in new_sdata:
            num = num + t.get(i, 0)
        s_total[i] = num
    s_total["severity_rate"] = "{:.2f}%".format(s_total.get("severity", 0) / s_total.get("bug", 0) * 100)
    s_total["solve_rate"] = "{:.2f}%".format(s_total.get("solve", 0) / s_total.get("bug", 0) * 100)
    s_total["reopen_rate"] = "{:.2f}%".format(s_total.get("reopen", 0) / s_total.get("bug", 0) * 100)
    new_sdata.append(s_total)
    # 计算solver的效能数据
    for solver in new_sdata:
        total = solver.get("bug")
        solver["severity_rate"] = "{:.2f}%".format(solver.get("severity") / total * 100)
        solver["solve_rate"] = "{:.2f}%".format(solver.get("solve") / total * 100)
        solver["reopen_rate"] = "{:.2f}%".format(solver.get("reopen") / total * 100)
    insert_data["solver_data"] = new_sdata


if __name__ == "__main__":
    from zt_bug import BugReport
    br = BugReport()
    br.get_bug_data()
    handle_json(read_json())
    myworkbook = operate_excel()
    myworkbook.creat_tmplate()
    myworkbook.add_data("版本数据")
    myworkbook.add_data("测试个人数据")
    myworkbook.add_data("解决人数据")
    myworkbook.save_data()
