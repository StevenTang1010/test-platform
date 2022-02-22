<template>
  <system-logs-view log-name="error" :tail-num="200" />
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
