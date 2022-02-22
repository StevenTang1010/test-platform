<template>
  <span>TODO</span>
</template>

<script>
export default {
  name: 'ReportStatistics',
  props: {
    resultType: {
      type: String,
      default() {
        return 'teststep'
      }
    }
  },
  data() {
    return {
      activeName: '' // 默认选中
    }
  }
}
</script>

<style scoped>

</style>
