<template>
  <system-logs-view log-name="api_test" :tail-num="200" />
</template>

<script>
import SystemLogsView from '@/views/system-manage/components/SystemLogsView'

export default {
  name: 'ApiTestLogs',
  components: { SystemLogsView }
}
</script>

<style scoped>

</style>
