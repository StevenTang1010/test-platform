<template>
  <test-env-monitor :test-comments="comments" :build-type="build_type" />
</template>

<script>
import TestEnvMonitor from '@/views/apiTest/workbench/TestEnvMonitor'
export default {
  name: 'EnvInspection',
  components: { TestEnvMonitor },
  data() {
    return {
      comments: '注：默认执行 = 所有接口用例(场景用例+单接口用例：P0/P1/P2/P3)',
      build_type: '业务巡检'
    }
  }
}
</script>

<style scoped>

</style>
