import request from '@/utils/request'

// 获取接口列表
export function getApiInfoList(params) {
  return request({
    url: '/api_test/api/list/',
    method: 'get',
    params
  })
}

// 获取待处理接口列表
export function getNoCaseApiInfoList(params) {
  return request({
    url: '/api_test/api/nocase/list/',
    method: 'get',
    params
  })
}

// 获取待处理接口列表
export function getToDoApiInfoList(params) {
  return request({
    url: '/api_test/api/todo/list/',
    method: 'get',
    params
  })
}

// 获取重复接口列表
export function getDuplicateApiInfoList(params) {
  return request({
    url: '/api_test/api/duplicate/list/',
    method: 'get',
    params
  })
}

// 获取接口详情
export function getApiInfoDetail(pk, params) {
  return request({
    url: '/api_test/api/detail/' + pk + '/',
    method: 'get',
    params
  })
}

// 新增接口
export function addApiInfo(data) {
  return request({
    url: '/api_test/api/add/',
    method: 'post',
    data: data
  })
}

// 更新接口
export function updateApiInfo(pk, data) {
  return request({
    url: '/api_test/api/update/' + pk + '/',
    method: 'patch',
    data
  })
}

// 批量 局部更新
export function bulkUpdateApiInfo(dataArr) {
  return request({
    url: '/api_test/api/bulk/',
    method: 'patch',
    data: dataArr
  })
}

// 删除接口
export function deleteApiInfo(pk) {
  return request({
    url: '/api_test/api/del/' + pk + '/',
    method: 'delete'
  })
}

// 批量 删除
export function bulkDeleteApiInfo(params) {
  return request({
    url: '/api_test/api/bulk/',
    method: 'delete',
    params
  })
}

// 同步-YAPI数据
export function dataSyncYapi(data) {
  return request({
    url: '/api_test/api/data_sync',
    method: 'post',
    data: data
  })
}
// 本地接口用例模板更新
export function updateCaseTemplate(data) {
  return request({
    url: '/api_test/api/update/case_template',
    method: 'post',
    data: data
  })
}

// ================  统计数据  ================
// 获取接口统计数据 - total
export function getApiTotal(params) {
  return request({
    url: '/api_test/api/total',
    method: 'get',
    params
  })
}

// 获取接口统计数据
export function getApiCount(params) {
  return request({
    url: '/api_test/api/count',
    method: 'get',
    params
  })
}

// 获取接口统计数据 - 无用例
export function getNoCaseApiCount(params) {
  return request({
    url: '/api_test/api/count/no_case',
    method: 'get',
    params
  })
}

// 获取接口统计数据 - 有用例
export function getWithCaseApiCount(params) {
  return request({
    url: '/api_test/api/count/with_case',
    method: 'get',
    params
  })
}

// 获取接口统计数据 - 更新待处理
export function getToDoApiCount(params) {
  return request({
    url: '/api_test/api/count/todo',
    method: 'get',
    params
  })
}
