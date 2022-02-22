import request from '@/utils/request'

// 获取环境监控配置列表
export function getTestEnvMonitorList(params) {
  return request({
    url: '/api_test/test/env_monitor/list',
    method: 'get',
    params: params
  })
}

// 获取环境监控详情
export function getTestEnvMonitorDetail(pk, params) {
  return request({
    url: '/api_test/test/env_monitor/detail/' + pk + '/',
    method: 'get',
    params
  })
}

// 新增环境监控
export function addTestEnvMonitor(data) {
  return request({
    url: '/api_test/test/env_monitor/add/',
    method: 'post',
    data: data
  })
}

// 更新环境监控
export function updateTestEnvMonitor(pk, data) {
  return request({
    url: '/api_test/test/env_monitor/update/' + pk + '/',
    method: 'patch',
    data
  })
}

// 批量 局部更新
export function bulkUpdateTestEnvMonitor(dataArr) {
  return request({
    url: '/api_test/test/env_monitor/bulk/',
    method: 'patch',
    data: dataArr
  })
}

// 删除环境监控
export function deleteTestEnvMonitor(pk) {
  return request({
    url: '/api_test/test/env_monitor/del/' + pk + '/',
    method: 'delete'
  })
}

// 批量 删除
export function bulkDeleteTestEnvMonitor(params) {
  return request({
    url: '/api_test/test/env_monitor/bulk/',
    method: 'delete',
    params
  })
}
