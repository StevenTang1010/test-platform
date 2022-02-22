<template>
  <div class="main">
    <tabs-menu v-if="!this.$route.params.report_id" :tab-pane-list="tabPaneList" />
    <router-view v-if="this.$route.params.report_id" />
  </div>
</template>

<script>
import TabsMenu from '@/views/apiTest/components/TabsMenu'
import ReportHistory from '@/views/apiTest/reportMgr/ReportHistory'

export default {
  name: 'ReportMgrIndex',
  components: { TabsMenu },
  data() {
    return {
      tabPaneList: this.$route.params.report_id ? [] : [
        {
          name: 'ReportHistory',
          label: '历史报告',
          components: [ReportHistory]
        }
      ]
    }
  }
}
</script>

<style scoped>

</style>
