<template>
  <tabs-menu :tab-pane-list="tabPaneList" />
</template>

<script>
import tabsMenu from '@/views/apiTest/components/TabsMenu'
import Theme from '@/views/system-manage/config-center/Theme/ThemeConfig'

export default {
  name: 'Index',
  components: { tabsMenu },
  data() {
    return {
      tabPaneList: [
        {
          name: 'Theme',
          label: '主题',
          component: Theme
        }
      ]
    }
  }
}
</script>

<style scoped>

</style>
