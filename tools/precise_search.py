# --------------------------------------
# Date: 2021/8/24
# @Author: Steven_Tang
# FileName: precise_search.py   
# Description: 
# --------------------------------------
import time

from apps.precise.models import *
from django.forms.models import model_to_dict


# 序列化搜索结果数据
def search_model(system: str, primary: str, secondary: str, third=None):
    system = System.objects.filter(system_id=system)
    primary_module = PrimaryModule.objects.filter(primary_module_id=primary)
    secondary_module = SecondaryModule.objects.filter(secondary_module_id=secondary)
    third = third
    system = [model_to_dict(item) for item in system][0].get('system_name')
    primary_data = [model_to_dict(item) for item in primary_module][0].get('primary_module_name')
    secondary_data = [model_to_dict(item) for item in secondary_module][0].get('secondary_module_name')
    results = []
    if third:
        third_modle = ThirdModule.objects.filter(third_module_id=third)
        func_modle = ModuleFunction.objects.filter(third_modle=third)
        for third_item in [model_to_dict(item) for item in third_modle]:
            for item in [model_to_dict(item) for item in func_modle]:
                data = {
                    'system': system,
                    'primary': primary_data,
                    'secondary': secondary_data,
                    'third': third_item.get('third_module_name'),
                    'func': item.get('module_function_name')
                }
                results.append(data)
    else:
        third_modle = ThirdModule.objects.filter(secondary_module_id=secondary)
        for third_item in [model_to_dict(item) for item in third_modle]:
            data = {
                'system': system,
                'primary': primary_data,
                'secondary': secondary_data,
                'third': third_item.get('third_module_name'),
                'func': ''
            }
            results.append(data)
    return results


# 产出三级模块关联结果
def search_third_elevance(model_name):
    # 通过三级模块名，查询id
    third_model = ThirdModule.objects.filter(third_module_name=model_name)
    third_id = third_model.values('third_module_id')[0].get(
        'third_module_id')
    # 通过三级模块id，查询所有包含功能id
    func_id_list = ModuleFunction.objects.filter(third_modle=third_id).values_list('module_function_id', flat=True)
    # 通过功能id，查询所有关联功能id
    indirect_func_list = list(FunctionalRelevance.objects.filter(direct_func__in=list(func_id_list)).values_list(
        'indirect_impact_func', flat=True))
    # 根据关联功能id，查出所有三级模块id
    third_id_list = [item.third_modle_id for item in
                     list(ModuleFunction.objects.in_bulk(id_list=list(indirect_func_list)).values())]
    # 根据id查三级模块
    third_model_data = ThirdModule.objects.filter(third_module_id__in=list(third_id_list))
    data_list = []
    for item in third_model_data:
        second_name = model_to_dict(
            SecondaryModule.objects.filter(secondary_module_id=item.secondary_module_id)[0]).get(
            'secondary_module_name')
        detail = model_to_dict(item)
        detail.setdefault('second_name', second_name)
        data_list.append(detail)
    return {'detail': data_list}


# 产出功能关联结果
def search_func_elevance(func_name):
    # 通过功能名，查询所有包含功能id
    func_id_list = ModuleFunction.objects.filter(module_function_name=func_name).values_list('module_function_id',
                                                                                             flat=True)
    # 通过功能id，查询所有关联功能id
    indirect_func_list = list(FunctionalRelevance.objects.filter(direct_func__in=list(func_id_list)).values_list(
        'indirect_impact_func', flat=True))
    # 根据关联功能id，查出所有关联功能信息
    func_list = [item for item in
                 list(ModuleFunction.objects.in_bulk(id_list=list(indirect_func_list)).values())]
    data_list = []
    for item in func_list:
        third_name = model_to_dict(ThirdModule.objects.filter(third_module_id=item.third_modle_id)[0]).get(
            'third_module_name')
        detail = model_to_dict(item)
        detail.setdefault('third_name', third_name)
        data_list.append(detail)
    return {'detail': data_list}


# 模糊匹配功能
def match_func(query_string):
    func_list = ModuleFunction.objects.filter(module_function_name__icontains=query_string).values_list(
        'module_function_name', flat=True)
    data = []
    for func in func_list:
        data.append({'value': func})
    return data


# 新增功能保存
def create_func(data):
    system = data.get('system')
    first = data.get('first')
    second = data.get('second')
    third = data.get('third')
    func = data.get('func')
    module_function_id = int(round(time.time() * 1000000))
    ModuleFunction.objects.create(module_function_name=func, module_function_id=module_function_id, third_modle_id=third)
    direct_func = ModuleFunction.objects.filter(module_function_name=func)[0]
    indirect_funcs = data.get('directFunc')
    try:
        for item in indirect_funcs:
            indirect_func = ModuleFunction.objects.filter(module_function_name=item)[0]
            FunctionalRelevance.objects.create(direct_func=direct_func, indirect_impact_func=indirect_func)
    except Exception as e:
        return e
    else:
        return True


# 编辑功能保存
def update_func(data):
    func = data.get('func')
    FunctionalRelevance.objects.filter(direct_func=func).delete()
    direct_func = ModuleFunction.objects.filter(module_function_name=func)[0]
    indirect_funcs = data.get('directFunc')
    try:
        for item in indirect_funcs:
            indirect_func = ModuleFunction.objects.filter(module_function_name=item)[0]
            FunctionalRelevance.objects.create(direct_func=direct_func, indirect_impact_func=indirect_func)
    except Exception as e:
        return e
    else:
        return True


if __name__ == '__main__':
    pass
