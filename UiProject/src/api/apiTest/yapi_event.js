import request from '@/utils/request'

// 获取YAPI变更事件列表
export function getYapiEventList(params) {
  return request({
    url: '/api_test/api/yapi_event/list/',
    method: 'get',
    params
  })
}

// 获取YAPI变更事件详情
export function getYapiEventDetail(pk, params) {
  return request({
    url: '/api_test/api/yapi_event/detail/' + pk + '/',
    method: 'get',
    params
  })
}

// 新增YAPI变更事件
export function addYapiEvent(data) {
  console.log(data)
  return request({
    url: '/api_test/api/yapi_event/add/',
    method: 'post',
    data: data
  })
}

// 更新-YAPI变更事件
export function updateYapiEvent(pk, data) {
  return request({
    url: '/api_test/api/yapi_event/update/' + pk + '/',
    method: 'patch',
    data
  })
}

// 批量 局部更新
export function bulkUpdateYapiEvent(dataArr) {
  return request({
    url: '/api_test/api/yapi_event/bulk/',
    method: 'patch',
    data: dataArr
  })
}

// 删除-YAPI变更事件
export function deleteYapiEvent(pk) {
  return request({
    url: '/api_test/api/yapi_event/del/' + pk + '/',
    method: 'delete'
  })
}

// 批量 删除
export function bulkDeleteYapiEvent(params) {
  return request({
    url: '/api_test/api/yapi_event/bulk/',
    method: 'delete',
    params
  })
}

// ==============
// 同步-YAPI变更事件
export function dataSyncYapiEvent(data) {
  return request({
    url: '/api_test/api/yapi_event/data_sync',
    method: 'post',
    data: data
  })
}
