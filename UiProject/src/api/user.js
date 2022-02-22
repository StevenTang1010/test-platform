import request from '@/utils/request'

// JWT
export function jwtLogin(data) {
  return request({
    url: '/api/user_auth/jwt/user/login/',
    method: 'post',
    data
  })
}

export function getjwtUserInfo(token) {
  return request({
    url: '/api/user_auth/jwt/user/info',
    method: 'get',
    params: { token }
  })
}

export function jwtLogout() {
  return request({
    url: '/api/user_auth/jwt/user/logout',
    method: 'post'
  })
}

// LDAP
export function login(data) {
  return request({
    url: '/api/user_auth/ldap/user/login/',
    method: 'post',
    data
  })
}

export function getUserInfo(token) {
  return request({
    url: '/api/user_auth/ldap/user/info',
    method: 'get',
    params: { token }
  })
}

export function logout() {
  return request({
    url: '/api/user_auth/ldap/user/logout',
    method: 'post'
  })
}

export function checkLogin(params) {
  return request({
    url: '/api/user_auth/ldap/user/check_login/',
    method: 'get',
    params
  })
}
