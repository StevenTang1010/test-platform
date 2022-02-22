<template>
  <div class="main">
    <tabs-menu :tab-pane-list="tabPaneList" tab-position="left" />
  </div>

</template>

<script>
import TabsMenu from '@/views/apiTest/components/TabsMenu'
import CallBackFunctions from '@/views/apiTest/help/CallBackFunctions'
import MallFunctions from '@/views/apiTest/help/MallFunctions'
import SettingsFunctions from '@/views/apiTest/help/SettingsFunctions'

export default {
  name: 'Index',
  components: { TabsMenu },
  data() {
    return {
      themeSize: this.$store.state.settings.themeSize,
      tabPaneList: [
        {
          name: 'CallBackFunctions',
          label: '企微回调',
          components: [CallBackFunctions]
        },
        {
          name: 'MallFunctions',
          label: '商城',
          components: [MallFunctions]
        },
        {
          name: 'SettingsFunctions',
          label: '配置中心',
          components: [SettingsFunctions]
        }
      ]
    }
  },
  methods: {}
}
</script>

<style scoped>

</style>
