<template>
  <div class="main">
    <tabs-menu :tab-pane-list="tabPaneList" />
  </div>
</template>

<script>
import TabsMenu from '@/views/apiTest/components/TabsMenu'

export default {
  name: 'CaseAnalysis',
  components: { TabsMenu },
  data() {
    return {
      themeSize: this.$store.state.settings.themeSize,
      tabPaneList: [
        {
          name: 'CaseAnalysis',
          label: '用例分析',
          components: []
        }
      ],
      group_by: ''
    }
  }
}
</script>

<style scoped>

</style>
