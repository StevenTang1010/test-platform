import request from '@/utils/request'

// 获取全局Const配置列表
export function getGlobalConstList(params) {
  return request({
    url: '/api_test/global/const/list',
    method: 'get',
    params: params
  })
}

// 获取全局Const详情
export function getGlobalConstDetail(pk, params) {
  return request({
    url: '/api_test/global/const/detail/' + pk + '/',
    method: 'get',
    params
  })
}

// 新增全局Const
export function addGlobalConst(data) {
  return request({
    url: '/api_test/global/const/add/',
    method: 'post',
    data: data
  })
}

// 更新全局Const
export function updateGlobalConst(pk, data) {
  return request({
    url: '/api_test/global/const/update/' + pk + '/',
    method: 'patch',
    data
  })
}

// 批量 局部更新
export function bulkUpdateGlobalConst(dataArr) {
  return request({
    url: '/api_test/global/const/bulk/',
    method: 'patch',
    data: dataArr
  })
}

// 删除全局Const
export function deleteGlobalConst(pk) {
  return request({
    url: '/api_test/global/const/del/' + pk + '/',
    method: 'delete'
  })
}

// 批量 删除
export function bulkDeleteGlobalConst(params) {
  return request({
    url: '/api_test/global/const/bulk/',
    method: 'delete',
    params
  })
}
