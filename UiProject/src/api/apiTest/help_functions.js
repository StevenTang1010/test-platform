import request from '@/utils/request'

// 获取 内建 方法列表
export function getBuiltinFunctionList(params) {
  return request({
    url: '/api_test/help/builtin_functions/list/',
    method: 'get',
    params
  })
}

// 获取 回调 方法列表
export function getCallBackFunctionList(params) {
  return request({
    url: '/api_test/help/callback_functions/list/',
    method: 'get',
    params
  })
}

// 获取自定义 商城 方法列表
export function getMallFunctionList(params) {
  return request({
    url: '/api_test/help/mall_functions/list/',
    method: 'get',
    params
  })
}

// 获取自定义 配置中心 方法列表
export function getSettingsFunctionList(params) {
  return request({
    url: '/api_test/help/settings_functions/list/',
    method: 'get',
    params
  })
}
