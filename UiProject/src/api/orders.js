import request from '@/utils/request'

// 获取/新增工单
export function getOrderList(q_data = null, method = 'get', url = '/api/order/list/') {
  const obj = {
    url: url,
    method: method
  }
  if (q_data) {
    // 获取
    if (obj.method === 'get') {
      obj.params = q_data
      // 新增
    } else if (obj.method === 'post') {
      obj.data = q_data
    }
  }
  return request(obj)
}

// 单条数据更新
export function updateOrder(pk, data) {
  return request({
    url: '/api/order/update/' + pk + '/',
    method: 'patch',
    data
  })
}

// 获取statistics图表数据
export function GetStatisticsData(params) {
  return request({
    url: '/api/order/statistics/',
    method: 'get',
    params
  })
}

// 获取analysis折线趋势数据
export function GetAnalysisData(params) {
  return request({
    url: '/api/order/analysis/',
    method: 'get',
    params
  })
}

// 获取bug分类趋势数据
export function GetBugTrendData(params) {
  return request({
    url: '/api/order/trend/',
    method: 'get',
    params
  })
}

// 导出
export function OrderExport(params) {
  return request({
    url: '/api/order/export/',
    method: 'get',
    params
  })
}
