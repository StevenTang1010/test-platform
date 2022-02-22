<template>
  <tabs-menu :tab-pane-list="tabPaneList" />
</template>

<script>
import TabsMenu from '@/views/apiTest/components/TabsMenu'
import ApiManager from '@/views/apiTest/apiMgr/ApiManager'
import apiAnalysis from '@/views/apiTest/apiMgr/apiAnalysis'
import apiDataSync from '@/views/apiTest/apiMgr/apiDataSync'
// import DuplicateChecking from '@/views/apiTest/apiMgr/duplicateChecking/DuplicateChecking'

export default {
  name: 'CaseMgr',
  components: { TabsMenu },
  data() {
    return {
      tabPaneList: [
        {
          name: 'ApiManager',
          label: '接口管理',
          components: [ApiManager]
        },
        {
          name: 'apiAnalysis',
          label: '统计分析',
          components: [apiAnalysis]
        },
        {
          name: 'apiDataSync',
          label: '数据同步',
          components: [apiDataSync]
        }
        // {
        //   name: 'DuplicateChecking',
        //   label: '查重工具',
        //   components: [DuplicateChecking]
        // }
      ]
    }
  }
}
</script>

<style scoped>

</style>
