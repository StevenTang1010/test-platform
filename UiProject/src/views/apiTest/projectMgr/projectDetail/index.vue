<template>
  <tabs-menu :tab-pane-list="tabPaneList" />
</template>

<script>
import TabsMenu from '@/views/apiTest/components/TabsMenu'
import projectSummary from '@/views/apiTest/projectMgr/projectDetail/projectSummary'
import apiAnalysis from '@/views/apiTest/apiMgr/apiAnalysis'
import memberMgr from '@/views/apiTest/projectMgr/projectDetail/memberMgr'
import projectDynamic from '@/views/apiTest/projectMgr/projectDetail/projectDynamic'

export default {
  name: 'Index',
  components: { TabsMenu },
  data() {
    return {
      activeName: 'projectDetail',
      tabPaneList: [
        {
          name: 'projectSummary',
          label: '项目概况',
          components: [projectSummary]
        },
        {
          name: 'apiAnalysis',
          label: '统计分析',
          components: [apiAnalysis]
        },
        {
          name: 'memberMgr',
          label: '成员管理',
          components: [memberMgr]
        },
        {
          name: 'projectDynamic',
          label: '项目动态',
          components: [projectDynamic]
        }
      ]
    }
  },
  watch: {
    activeName(val) {
      this.activeName = val
    }
  }
}
</script>

<style scoped>

</style>
