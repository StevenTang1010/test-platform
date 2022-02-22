import request from '@/utils/request'

// 获取系统列表
export function getSystemList() {
  const obj = {
    url: '/api/precise/system/',
    method: 'get'
  }
  return request(obj)
}

// 获取一级菜单列表
export function getPrimaryList(params = null) {
  const obj = {
    url: '/api/precise/primary/',
    method: 'get',
    params
  }
  return request(obj)
}

// 获取二级菜单列表
export function getSecondaryList(params = null) {
  const obj = {
    url: '/api/precise/second/',
    method: 'get',
    params
  }
  return request(obj)
}

// 获取三级菜单列表
export function getThirdList(params = null) {
  const obj = {
    url: '/api/precise/third/',
    method: 'get',
    params
  }
  return request(obj)
}

// 模块搜索
export function ModelSearch(params) {
  return request({
    url: '/api/precise/search/',
    method: 'get',
    params
  })
}

// 查询关联
export function GetDetail(params) {
  return request({
    url: '/api/precise/detail/',
    method: 'get',
    params
  })
}

// match功能
export function MatchFunc(params) {
  return request({
    url: '/api/precise/func/match/',
    method: 'get',
    params
  })
}

// 新增功能
export function CreateFunc(data) {
  return request({
    url: '/api/precise/func/create/',
    method: 'post',
    data
  })
}

// 编辑功能
export function UpdateFunc(data) {
  return request({
    url: '/api/precise/func/update/',
    method: 'post',
    data
  })
}
