import request from '@/utils/request'

export function getList(params) {
  return request({
    url: '/UiProject/table/list',
    method: 'get',
    params
  })
}
