import request from '@/utils/request'

// 获取项目成员列表
export function getProjectMemberList(params) {
  return request({
    url: '/api_test/project/member/list/',
    method: 'get',
    params
  })
}

// 获取项目成员详情
export function getProjectMemberDetail(pk, params) {
  return request({
    url: '/api_test/project/member/detail/' + pk + '/',
    method: 'get',
    params
  })
}

// 新增项目成员
export function addProjectMember(data) {
  return request({
    url: '/api_test/project/member/add/',
    method: 'post',
    data: data
  })
}

// 更新项目成员
export function updateProjectMember(pk, data) {
  return request({
    url: '/api_test/project/member/update/' + pk + '/',
    method: 'patch',
    data
  })
}

// 删除项目成员
export function deleteProjectMember(pk) {
  return request({
    url: '/api_test/project/member/del/' + pk + '/',
    method: 'delete'
  })
}
