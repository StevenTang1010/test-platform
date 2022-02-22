export function isOjbect(param) {
  return Object.prototype.toString.call(param) === '[object Object]'
}

export function isFunction(param) {
  return Object.prototype.toString.call(param) === '[object Function]'
}
