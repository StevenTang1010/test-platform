import request from '@/utils/request'

// 获取全局Header配置列表
export function getGlobalHeaderList(params) {
  return request({
    url: '/api_test/global/header/list',
    method: 'get',
    params: params
  })
}

// 获取全局Header详情
export function getGlobalHeaderDetail(pk, params) {
  return request({
    url: '/api_test/global/header/detail/' + pk + '/',
    method: 'get',
    params
  })
}

// 新增全局Header
export function addGlobalHeader(data) {
  return request({
    url: '/api_test/global/header/add/',
    method: 'post',
    data: data
  })
}

// 更新全局Header
export function updateGlobalHeader(pk, data) {
  return request({
    url: '/api_test/global/header/update/' + pk + '/',
    method: 'patch',
    data
  })
}

// 批量 局部更新
export function bulkUpdateGlobalHeader(dataArr) {
  return request({
    url: '/api_test/global/header/bulk/',
    method: 'patch',
    data: dataArr
  })
}

// 删除全局Header
export function deleteGlobalHeader(pk) {
  return request({
    url: '/api_test/global/header/del/' + pk + '/',
    method: 'delete'
  })
}

// 批量 删除
export function bulkDeleteGlobalHeader(params) {
  return request({
    url: '/api_test/global/header/bulk/',
    method: 'delete',
    params
  })
}
