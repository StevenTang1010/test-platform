import request from '@/utils/request'

// 获取User列表
export function getUserList(params) {
  return request({
    url: '/api_test/user/list',
    method: 'get',
    params: params
  })
}
