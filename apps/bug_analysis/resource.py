# # --------------------------------------
# # Date: 2021/12/6
# # @Author: Steven_Tang
# # FileName: resource.py
# # Description: 导出序列化
# # --------------------------------------
# from io import BytesIO
#
# from import_export import resources
# from import_export.fields import Field
# from .models import Orders
# import xlwt
# from pathlib import Path
#
#
# class OrderResource(resources.ModelResource):
#     ticket_number = Field(attribute='ticket_number', column_name='工单编号')
#     priority = Field(attribute='priority', column_name='优先级')
#     severity = Field(attribute='severity', column_name='严重程度')
#     content = Field(attribute='content', column_name='问题描述')
#     bug_state = Field(attribute='bug_state', column_name='是否是BUG')
#     category = Field(attribute='category', column_name='分类')
#     bug_reason = Field(attribute='bug_reason', column_name='BUG原因')
#     reason = Field(attribute='reason', column_name='问题根源')
#     solver = Field(attribute='solver', column_name='解决人')
#     solution = Field(attribute='solution', column_name='解决方案')
#     thorough = Field(attribute='thorough', column_name='是否彻底解决')
#     domain = Field(attribute='domain', column_name='归属业务域')
#     edition = Field(column_name='归属版本')
#     technical = Field(attribute='technical', column_name='技术归属')
#     module = Field(attribute='module', column_name='所属模块')
#
#     class Meta:
#         model = Orders
#         fields = (
#             'ticket_number', 'priority', 'severity', 'content', 'bug_state', 'category', 'bug_reason', 'reason',
#             'solver',
#             'solution', 'thorough', 'domain', 'technical', 'module')
#         import_id_fields = ['ticket_number']
#
#
# def write_excel(dataset):
#     ws = xlwt.Workbook(encoding='utf8')
#     sheet1 = ws.add_sheet('sheet1')
#     headers = dataset.headers
#     # 写入表头
#     for i in range(len(headers)):
#         sheet1.write(0, i, headers[i])
#     # 写入数据
#     for i in range(len(headers)):
#         data = dataset.get_col(i)
#         for j in range(len(data)):
#             sheet1.write(j + 1, i, data[j])
#     export_dir = Path(__file__).parent.parent.parent.joinpath('static/export/')
#     export_dir.mkdir(parents=True, exist_ok=True)
#     file_name = export_dir.joinpath('export.xls')
#     # print(type(file_name.__str__()))
#     with open(file_name, 'wb+') as f:
#         ws.save(f)
#     return file_name
#
#
# if __name__ == '__main__':
#     pass
