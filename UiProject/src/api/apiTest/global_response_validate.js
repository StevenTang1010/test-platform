import request from '@/utils/request'

// 获取全局ResponseValidate配置列表
export function getGlobalResponseValidateList(params) {
  return request({
    url: '/api_test/global/response_validate/list',
    method: 'get',
    params: params
  })
}

// 获取全局ResponseValidate详情
export function getGlobalResponseValidateDetail(pk, params) {
  return request({
    url: '/api_test/global/response_validate/detail/' + pk + '/',
    method: 'get',
    params
  })
}

// 新增全局ResponseValidate
export function addGlobalResponseValidate(data) {
  return request({
    url: '/api_test/global/response_validate/add/',
    method: 'post',
    data: data
  })
}

// 更新全局ResponseValidate
export function updateGlobalResponseValidate(pk, data) {
  return request({
    url: '/api_test/global/response_validate/update/' + pk + '/',
    method: 'patch',
    data
  })
}

// 批量 局部更新
export function bulkUpdateGlobalResponseValidate(dataArr) {
  return request({
    url: '/api_test/global/response_validate/bulk/',
    method: 'patch',
    data: dataArr
  })
}

// 删除全局ResponseValidate
export function deleteGlobalResponseValidate(pk) {
  return request({
    url: '/api_test/global/response_validate/del/' + pk + '/',
    method: 'delete'
  })
}

// 批量 删除
export function bulkDeleteGlobalResponseValidate(params) {
  return request({
    url: '/api_test/global/response_validate/bulk/',
    method: 'delete',
    params
  })
}
