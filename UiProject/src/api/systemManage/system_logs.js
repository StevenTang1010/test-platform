import request from '@/utils/request'

// 系统日志 - pk： message | error | api_test
export function getSystemLogs(pk, params) {
  return request({
    url: '/api/system_manage/logs/' + pk + '/',
    method: 'get',
    params: params
  })
}
