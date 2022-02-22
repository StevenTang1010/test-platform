import request from '@/utils/request'

// 获取部门列表
export function getDepartmentList(params) {
  return request({
    url: '/api/system_manage/department/list/',
    method: 'get',
    params
  })
}

// 获取部门详情
export function getDepartmentDetail(pk, params) {
  return request({
    url: '/api/system_manage/department/detail/' + pk + '/',
    method: 'get',
    params
  })
}

// 新增部门
export function addDepartment(data) {
  return request({
    url: '/api/system_manage/department/add/',
    method: 'post',
    data: data
  })
}

// 局部更新部门
export function updateDepartment(pk, data) {
  return request({
    url: '/api/system_manage/department/update/' + pk + '/',
    method: 'patch',
    data
  })
}

// 批量 局部更新部门
export function bulkUpdateDepartment(dataArr) {
  return request({
    url: '/api/system_manage/department/bulk/',
    method: 'patch',
    data: dataArr
  })
}

// 删除部门
export function deleteDepartment(pk) {
  return request({
    url: '/api/system_manage/department/del/' + pk + '/',
    method: 'delete'
  })
}

// 批量 删除部门
export function bulkDeleteDepartment(params) {
  return request({
    url: '/api/system_manage/department/bulk/',
    method: 'delete',
    params
  })
}
