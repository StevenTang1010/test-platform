<template>
  <tabs-menu :tab-pane-list="tabPaneList" />
</template>

<script>
import TabsMenu from '@/views/apiTest/components/TabsMenu'
import TaskSchedule from "@/views/apiTest/taskMgr/TaskSchedule";
import TaskQueue from "@/views/apiTest/taskMgr/TaskQueue";

export default {
  name: 'Workbench',
  components: { TabsMenu },
  data() {
    return {
      tabPaneList: [
        {
          name: 'TaskSchedule',
          label: '定时任务',
          components: [TaskSchedule]
        },
        {
          name: 'TaskQueue',
          label: '任务队列',
          components: [TaskQueue]
        }
      ]
    }
  }
}
</script>

<style scoped>

</style>
