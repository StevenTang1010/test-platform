<template>
  <tabs-menu :tab-pane-list="tabPaneList" />
</template>

<script>
import TabsMenu from '@/views/apiTest/components/TabsMenu'
// import jobBoard from '@/views/apiTest/workbench/jobBoard'
import FastTest from '@/views/apiTest/workbench/FastTest'
import EnvInspection from '@/views/apiTest/workbench/EnvInspection'
import EnvSmoke from '@/views/apiTest/workbench/EnvSmoke'
import EnvValidate from '@/views/apiTest/workbench/EnvValidate'
// import task from '@/views/apiTest/taskMgr/TaskSchedule'

export default {
  name: 'Workbench',
  components: { TabsMenu },
  data() {
    return {
      tabPaneList: [
        // {
        //   name: 'jobBoard',
        //   label: '工作看板',
        //   components: [jobBoard]
        // },
        {
          name: 'FastTest',
          label: '快速测试',
          components: [FastTest]
        },
        {
          name: 'EnvInspection',
          label: '业务巡检',
          components: [EnvInspection]
        },
        {
          name: 'EnvSmoke',
          label: '冒烟测试',
          components: [EnvSmoke]
        },
        {
          name: 'EnvValidate',
          label: '环境验证',
          components: [EnvValidate]
        }
      ]
    }
  }
}
</script>

<style scoped>

</style>
