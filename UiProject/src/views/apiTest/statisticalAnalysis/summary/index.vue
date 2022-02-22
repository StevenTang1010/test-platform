<template>
  <div class="main">
    <tabs-menu :tab-pane-list="tabPaneList" />
  </div>
</template>

<script>
import TabsMenu from '@/views/apiTest/components/TabsMenu'
import Statistic from '@/views/apiTest/statisticalAnalysis/summary/Statistic'
import AddTrend from '@/views/apiTest/statisticalAnalysis/summary/AddTrend'

export default {
  name: 'Index',
  components: { TabsMenu },
  data() {
    return {
      pageHeight: window.innerHeight - 275,
      tabPaneList: [
        {
          name: 'summary',
          label: '概览',
          components: [Statistic, AddTrend]
        }
      ]
    }
  },
  mounted() {
  }
}
</script>

<style scoped>

</style>
