import request from '@/utils/request'

// 获取TestTask列表
export function getTestTaskList(params) {
  return request({
    url: '/api_test/test/task/list',
    method: 'get',
    params: params
  })
}

// 获取TestTask详情
export function getTestTaskDetail(pk, params) {
  return request({
    url: '/api_test/test/task/detail/' + pk + '/',
    method: 'get',
    params
  })
}

// 新增TestTask
export function addTestTask(data) {
  return request({
    url: '/api_test/test/task/add/',
    method: 'post',
    data: data
  })
}

// 局部更新TestTask
export function updateTestTask(pk, data) {
  return request({
    url: '/api_test/test/task/update/' + pk + '/',
    method: 'patch',
    data
  })
}

// 批量 局部更新用例
export function bulkUpdateTestTask(dataArr) {
  return request({
    url: '/api_test/test/task/bulk/',
    method: 'patch',
    data: dataArr
  })
}

// 删除TestTask
export function deleteTestTask(pk) {
  return request({
    url: '/api_test/test/task/del/' + pk + '/',
    method: 'delete'
  })
}

// 批量 删除用例
export function bulkDeleteTestTask(params) {
  return request({
    url: '/api_test/test/task/bulk/',
    method: 'delete',
    params
  })
}

