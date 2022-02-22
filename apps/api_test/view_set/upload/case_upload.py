"""@author:sh
@file:update.py
@time:2021/11/27
@email:
@description: file upload and download
"""
from rest_framework.views import APIView
from apps.api_test import logger
from apps.api_test.view_set.base import JsonResponse
from apps.api_test.xmind.case_upload import FileImportHandle, DataInsertHandle


class UploadFileView(APIView):

    def post(self, request, *args, **kwargs):
        try:
            file_req = request.FILES.get('file')
            data_type = request.POST.get("data_type")
            load_type = request.POST.get("load_type")
            department = request.POST.get("department")
            fileN = file_req.name.split(".")
        except Exception as e:
            return JsonResponse(code=500200, success=False, msg="服务器内部错误,error: " + str(e))

        try:
            file_path = FileImportHandle(file_req=file_req, file_type=fileN[-1]).handle_file()
            logger.info("文件上传成功！")
        except Exception as e:
            return JsonResponse(data=str(e), code=500200, success=False, msg="文件上传失败")

        try:
            response = DataInsertHandle(file_path, file_type=fileN[-1], file_name=fileN[0],
                                        data_type=data_type, load_type=load_type, department=department).insert()
            logger.info("数据插入成功！")
            return JsonResponse(data=response, success=True, msg="文件上传入库成功")
        except Exception as e:
            return JsonResponse(data=str(e), code=500200, success=False, msg="数据插入失败")

    def get(self, request, *args, **kwargs):
        return JsonResponse(code=2, success=True, msg="测试成功", data="xxx")
