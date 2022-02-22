<template>
  <system-logs-view log-name="message" :tail-num="100" />
</template>

<script>
import SystemLogsView from '@/views/system-manage/components/SystemLogsView'

export default {
  name: 'Message',
  components: { SystemLogsView }
}
</script>

<style scoped>

</style>
