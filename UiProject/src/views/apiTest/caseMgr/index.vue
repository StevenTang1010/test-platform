<template>
  <tabs-menu :tab-pane-list="tabPaneList" />
</template>

<script>
import TabsMenu from '@/views/apiTest/components/TabsMenu'
import CaseManager from '@/views/apiTest/caseMgr/CaseManager'
import analysis from '@/views/apiTest/caseMgr/CaseAnalysis'

export default {
  name: 'CaseMgr',
  components: { TabsMenu },
  data() {
    return {
      tabPaneList: [
        {
          name: 'CaseManager',
          label: '用例管理',
          components: [CaseManager]
        },
        {
          name: 'analysis',
          label: '统计分析',
          components: [analysis]
        }
      ]
    }
  }
}
</script>

<style scoped>

</style>
