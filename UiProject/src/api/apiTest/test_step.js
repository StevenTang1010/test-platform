import request from '@/utils/request'

// 获取用例步骤列表
export function getTestStepList(params) {
  return request({
    url: '/api_test/test/step/list/',
    method: 'get',
    params
  })
}

// 获取用例步骤详情
export function getTestStepDetail(pk, params) {
  return request({
    url: '/api_test/test/step/detail/' + pk + '/',
    method: 'get',
    params
  })
}

// 新增用例步骤
export function addTestStep(data) {
  return request({
    url: '/api_test/test/step/add/',
    method: 'post',
    data: data
  })
}

// 局部更新用例步骤
export function updateTestStep(pk, data) {
  return request({
    url: '/api_test/test/step/update/' + pk + '/',
    method: 'patch',
    data
  })
}

// 批量局部更新用例步骤
export function bulkUpdateTestStep(dataArr) {
  return request({
    url: '/api_test/test/step/bulk/',
    method: 'patch',
    data: dataArr
  })
}

// 删除用例步骤
export function deleteTestStep(pk) {
  return request({
    url: '/api_test/test/step/del/' + pk + '/',
    method: 'delete'
  })
}

// 批量 删除用例步骤
export function bulkDeleteTestStep(params) {
  return request({
    url: '/api_test/test/step/bulk/',
    method: 'delete',
    params
  })
}

// 获取测试步骤统计数据
export function getTestStepTotal(params) {
  return request({
    url: '/api_test/step/total',
    method: 'get',
    params
  })
}

export function getTestStepCount(params) {
  return request({
    url: '/api_test/test/step/count/',
    method: 'get',
    params
  })
}
