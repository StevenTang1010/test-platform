import request from '@/utils/request'

// 获取比较器列表
export function getComparatorList(params) {
  return request({
    url: '/api_test/help/comparator/list/',
    method: 'get',
    params
  })
}
