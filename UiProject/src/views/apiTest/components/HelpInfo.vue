<template />

<script>
export default {
  name: 'HelpInfo',
  data() {
    return {
      // 支持的比较器
      comparatorList: [
        { name: '相等', keys: ['eq', 'equals', 'equal'] },
        { name: '不相等', keys: ['ne', 'not_equal'] },
        { name: '小于', keys: ['lt', 'less_than'] },
        { name: '小于等于', keys: ['le', 'less_or_equals'] },
        { name: '大于', keys: ['gt', 'greater_than'] },
        { name: '大于等于', keys: ['ge', 'greater_or_equals'] },
        { name: '字符等于', keys: ['str_eq', 'string_equals'] },
        { name: '长度等于', keys: ['len_eq', 'length_equal'] },
        { name: '长度大于', keys: ['len_gt', 'length_greater_than'] },
        { name: '长度大于等于', keys: ['len_ge', 'length_greater_or_equals'] },
        { name: '长度小于', keys: ['len_lt', 'length_less_than'] },
        { name: '长度小于等于', keys: ['len_le', 'length_less_or_equals'] },
        { name: '长度小于等于', keys: ['len_le', 'length_less_or_equals'] },
        { name: '长度小于等于', keys: ['len_le', 'length_less_or_equals'] },
        { name: '长度小于等于', keys: ['len_le', 'length_less_or_equals'] },
        { name: '长度小于等于', keys: ['len_le', 'length_less_or_equals'] },
        { name: '长度小于等于', keys: ['len_le', 'length_less_or_equals'] },
        { name: '长度小于等于', keys: ['len_le', 'length_less_or_equals'] },
        { name: '其他待完善', keys: ['len_le', 'length_less_or_equals'] }
      ]
    }
  }
}
</script>

<style scoped>

</style>
