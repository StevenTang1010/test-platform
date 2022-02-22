import request from '@/utils/request'

// 获取接口变更列表
export function getApiUpdateHistoryList(params) {
  return request({
    url: '/api_test/api/update_history/list/',
    method: 'get',
    params
  })
}

// 获取待处理接口变更列表
export function getToDoApiUpdateHistoryList(params) {
  return request({
    url: '/api_test/api/update_history/todo/list/',
    method: 'get',
    params
  })
}

// 获取接口变更详情
export function getApiUpdateHistoryDetail(pk, params) {
  return request({
    url: '/api_test/api/update_history/detail/' + pk + '/',
    method: 'get',
    params
  })
}

// 新增接口变更
export function addApiUpdateHistory(data) {
  console.log(data)
  return request({
    url: '/api_test/api/update_history/add/',
    method: 'post',
    data: data
  })
}

// 更新-接口变更
export function updateApiUpdateHistory(pk, data) {
  return request({
    url: '/api_test/api/update_history/update/' + pk + '/',
    method: 'patch',
    data
  })
}

// 删除-接口变更
export function deleteApiUpdateHistory(pk) {
  return request({
    url: '/api_test/api/update_history/del/' + pk + '/',
    method: 'delete'
  })
}

// 接口update_status同步到接口变更历史表
export function syncUpdateStatusToApiUpdateHistory(data) {
  return request({
    url: '/api_test/api/sync/update_history/update_status',
    method: 'put',
    data
  })
}
