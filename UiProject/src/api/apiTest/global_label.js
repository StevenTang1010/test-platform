import request from '@/utils/request'

// 获取全局标签配置列表
export function getGlobalLabelList(params) {
  return request({
    url: '/api_test/global/label/list',
    method: 'get',
    params: params
  })
}

// 获取全局标签详情
export function getGlobalLabelDetail(pk, params) {
  return request({
    url: '/api_test/global/label/detail/' + pk + '/',
    method: 'get',
    params
  })
}

// 新增全局标签
export function addGlobalLabel(data) {
  return request({
    url: '/api_test/global/label/add/',
    method: 'post',
    data: data
  })
}

// 更新全局标签
export function updateGlobalLabel(pk, data) {
  return request({
    url: '/api_test/global/label/update/' + pk + '/',
    method: 'patch',
    data
  })
}

// 批量 局部更新
export function bulkUpdateGlobalLabel(dataArr) {
  return request({
    url: '/api_test/global/label/bulk/',
    method: 'patch',
    data: dataArr
  })
}

// 删除全局标签
export function deleteGlobalLabel(pk) {
  return request({
    url: '/api_test/global/label/del/' + pk + '/',
    method: 'delete'
  })
}

// 批量 删除
export function bulkDeleteGlobalLabel(params) {
  return request({
    url: '/api_test/global/label/bulk/',
    method: 'delete',
    params
  })
}
