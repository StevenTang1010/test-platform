<template>
  <test-env-monitor :test-comments="comments" :build-type="build_type" />
</template>

<script>
import TestEnvMonitor from '@/views/apiTest/workbench/TestEnvMonitor'
export default {
  name: 'EnvSmoke',
  components: { TestEnvMonitor },
  data() {
    return {
      comments: '注：默认执行 = 单接口用例（P0:核心接口正向测试）',
      build_type: '环境验证'
    }
  }
}
</script>

<style scoped>

</style>
