import request from '@/utils/request'

// 获取TestSuite列表
export function getTestSuiteList(params) {
  return request({
    url: '/api_test/test/suite/list',
    method: 'get',
    params: params
  })
}

// 获取TestSuite详情
export function getTestSuiteDetail(pk, params) {
  return request({
    url: '/api_test/test/suite/detail/' + pk + '/',
    method: 'get',
    params
  })
}

// 新增TestSuite
export function addTestSuite(data) {
  return request({
    url: '/api_test/test/suite/add/',
    method: 'post',
    data: data
  })
}

// 局部更新TestSuite
export function updateTestSuite(pk, data) {
  return request({
    url: '/api_test/test/suite/update/' + pk + '/',
    method: 'patch',
    data
  })
}

// 批量 局部更新用例
export function bulkUpdateTestSuite(dataArr) {
  return request({
    url: '/api_test/test/suite/bulk/',
    method: 'patch',
    data: dataArr
  })
}

// 删除TestSuite
export function deleteTestSuite(pk) {
  return request({
    url: '/api_test/test/suite/del/' + pk + '/',
    method: 'delete'
  })
}

// 批量 删除用例
export function bulkDeleteTestSuite(params) {
  return request({
    url: '/api_test/test/suite/bulk/',
    method: 'delete',
    params
  })
}

// 获取用例集统计数据
export function getTestSuiteTotal(params) {
  return request({
    url: '/api_test/suite/total',
    method: 'get',
    params
  })
}

export function getTestSuiteCount(params) {
  return request({
    url: '/api_test/test/suite/count/',
    method: 'get',
    params
  })
}
