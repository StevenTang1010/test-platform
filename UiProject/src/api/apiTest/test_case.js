import request from '@/utils/request'

// 获取用例列表
export function getTestCaseList(params) {
  return request({
    url: '/api_test/test/case/list/',
    method: 'get',
    params
  })
}

// 获取用例详情
export function getTestCaseDetail(pk, params) {
  return request({
    url: '/api_test/test/case/detail/' + pk + '/',
    method: 'get',
    params
  })
}

// 新增用例
export function addTestCase(data) {
  return request({
    url: '/api_test/test/case/add/',
    method: 'post',
    data: data
  })
}

// 局部更新用例
export function updateTestCase(pk, data) {
  return request({
    url: '/api_test/test/case/update/' + pk + '/',
    method: 'patch',
    data
  })
}

// 批量 局部更新用例
export function bulkUpdateTestCase(dataArr) {
  return request({
    url: '/api_test/test/case/bulk/',
    method: 'patch',
    data: dataArr
  })
}

// 删除用例
export function deleteTestCase(pk) {
  return request({
    url: '/api_test/test/case/del/' + pk + '/',
    method: 'delete'
  })
}

// 批量 删除用例
export function bulkDeleteTestCase(params) {
  return request({
    url: '/api_test/test/case/bulk/',
    method: 'delete',
    params
  })
}

// 获取用例统计数据
export function getTestCaseTotal(params) {
  return request({
    url: '/api_test/case/total',
    method: 'get',
    params
  })
}

export function getTestCaseCount(params) {
  return request({
    url: '/api_test/test/case/count/',
    method: 'get',
    params
  })
}
