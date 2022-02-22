<template>
  <tabs-menu :tab-pane-list="tabPaneList" />
</template>

<script>
import TabsMenu from '@/views/apiTest/components/TabsMenu'
import ProjectManager from '@/views/apiTest/projectMgr/ProjectManager'
import organization from '@/views/apiTest/projectMgr/organization'

export default {
  name: 'Index',
  components: { TabsMenu },
  data() {
    return {
      tabPaneList: [
        {
          name: 'ProjectManager',
          label: '项目管理',
          components: [ProjectManager]
        },
        {
          name: 'organization',
          label: '部门组织',
          components: [organization]
        }
      ]
    }
  }
}
</script>

<style scoped>

</style>
