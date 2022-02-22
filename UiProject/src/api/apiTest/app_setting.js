import request from '@/utils/request'

// 获取App系统配置列表
export function getAppSettingList(params) {
  return request({
    url: '/api_test/global/app_setting/list',
    method: 'get',
    params: params
  })
}

// 获取App系统配置详情
export function getAppSettingDetail(pk, params) {
  return request({
    url: '/api_test/global/app_setting/detail/' + pk + '/',
    method: 'get',
    params
  })
}

// 新增App系统配置
export function addAppSetting(data) {
  return request({
    url: '/api_test/global/app_setting/add/',
    method: 'post',
    data: data
  })
}

// 更新App系统配置
export function updateAppSetting(pk, data) {
  return request({
    url: '/api_test/global/app_setting/update/' + pk + '/',
    method: 'patch',
    data
  })
}

// 批量 局部更新
export function bulkUpdateAppSetting(dataArr) {
  return request({
    url: '/api_test/global/app_setting/bulk/',
    method: 'patch',
    data: dataArr
  })
}

// 删除App系统配置
export function deleteAppSetting(pk) {
  return request({
    url: '/api_test/global/app_setting/del/' + pk + '/',
    method: 'delete'
  })
}

// 批量 删除
export function bulkDeleteAppSetting(params) {
  return request({
    url: '/api_test/global/app_setting/bulk/',
    method: 'delete',
    params
  })
}

// 获取App系统配置默认数据
export function getAppSettingDataDefault(params) {
  return request({
    url: '/api_test/global/app_setting/data/default',
    method: 'get',
    params
  })
}
