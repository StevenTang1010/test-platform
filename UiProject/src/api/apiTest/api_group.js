import request from '@/utils/request'

// 获取ApiGroup列表
export function getApiGroupList(params) {
  return request({
    url: '/api_test/api/group/list',
    method: 'get',
    params: params
  })
}

// 获取ApiGroup详情
export function getApiGroupDetail(pk, params) {
  return request({
    url: '/api_test/api/group/detail/' + pk + '/',
    method: 'get',
    params
  })
}

// 新增ApiGroup
export function addApiGroup(data) {
  return request({
    url: '/api_test/api/group/add/',
    method: 'post',
    data: data
  })
}

// 更新ApiGroup
export function updateApiGroup(pk, data) {
  return request({
    url: '/api_test/api/group/update/' + pk + '/',
    method: 'patch',
    data
  })
}

// 批量 局部更新
export function bulkUpdateApiGroup(dataArr) {
  return request({
    url: '/api_test/api/group/bulk/',
    method: 'patch',
    data: dataArr
  })
}

// 删除ApiGroup
export function deleteApiGroup(pk) {
  return request({
    url: '/api_test/api/group/del/' + pk + '/',
    method: 'delete'
  })
}

// 批量 删除
export function bulkDeleteApiGroup(params) {
  return request({
    url: '/api_test/api/group/bulk/',
    method: 'delete',
    params
  })
}
