import request from '@/utils/request'

// 获取全局ENV（环境配置）配置列表
export function getGlobalEnvList(params) {
  return request({
    url: '/api_test/global/env/list',
    method: 'get',
    params: params
  })
}

// 获取全局ENV（环境配置）详情
export function getGlobalEnvDetail(pk, params) {
  return request({
    url: '/api_test/global/env/detail/' + pk + '/',
    method: 'get',
    params
  })
}

// 新增全局ENV（环境配置）
export function addGlobalEnv(data) {
  return request({
    url: '/api_test/global/env/add/',
    method: 'post',
    data: data
  })
}

// 更新全局ENV（环境配置）
export function updateGlobalEnv(pk, data) {
  return request({
    url: '/api_test/global/env/update/' + pk + '/',
    method: 'patch',
    data
  })
}

// 批量 局部更新
export function bulkUpdateGlobalEnv(dataArr) {
  return request({
    url: '/api_test/global/env/bulk/',
    method: 'patch',
    data: dataArr
  })
}

// 删除全局ENV（环境配置）
export function deleteGlobalEnv(pk) {
  return request({
    url: '/api_test/global/env/del/' + pk + '/',
    method: 'delete'
  })
}

// 批量 删除
export function bulkDeleteGlobalEnv(params) {
  return request({
    url: '/api_test/global/env/bulk/',
    method: 'delete',
    params
  })
}

// 爬取/获取全局ENV对应环境的数据
export function getGlobalEnvData(pk, params) {
  return request({
    url: '/api_test/global/env/data/' + pk + '/',
    method: 'get',
    params
  })
}

// 获取全局env.config默认数据
export function getGlobalEnvConfigDefault(params) {
  return request({
    url: '/api_test/global/env/config/default',
    method: 'get',
    params
  })
}

// 获取全局env.qw_external_contact_config默认数据
export function getGlobalEnvQWExternalContactConfigDefault(params) {
  return request({
    url: '/api_test/global/env/qw_external_contact_config/default',
    method: 'get',
    params
  })
}
