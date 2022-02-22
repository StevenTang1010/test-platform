<template>
  <div class="main">
    <tabs-menu :tab-pane-list="tabPaneList" />
  </div>
</template>

<script>
import TabsMenu from '@/views/apiTest/components/TabsMenu'

export default {
  name: 'WorkAnalysis',
  components: { TabsMenu },
  data() {
    return {
      themeSize: this.$store.state.settings.themeSize,
      tabPaneList: [
        {
          name: 'WorkAnalysis',
          label: '进度分析',
          components: []
        }
      ]
    }
  }
}
</script>

<style scoped>

</style>
