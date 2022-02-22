<template>
  <tabs-menu :tab-pane-list="tabPaneList" />
</template>

<script>
import TabsMenu from '@/views/apiTest/components/TabsMenu'
import GlobalEnv from '@/views/apiTest/globalMgr/environment'
import GlobalHeader from '@/views/apiTest/globalMgr/header'
import GlobalConst from '@/views/apiTest/globalMgr/const'
import GlobalLabel from '@/views/apiTest/globalMgr/label'
import GlobalValidate from '@/views/apiTest/globalMgr/response_validate'
import AppSetting from '@/views/apiTest/globalMgr/app_setting'

export default {
  name: 'Index',
  components: { TabsMenu },
  data() {
    return {
      tabPaneList: [
        {
          name: 'GlobalEnv',
          label: '环境配置',
          components: [GlobalEnv]
        },
        {
          name: 'GlobalHeader',
          label: '请求头配置',
          components: [GlobalHeader]
        },
        {
          name: 'GlobalConst',
          label: '全局变量',
          components: [GlobalConst]
        },
        {
          name: 'GlobalLabel',
          label: '标签配置',
          components: [GlobalLabel]
        },
        {
          name: 'GlobalValidate',
          label: '校验规则',
          components: [GlobalValidate]
        },
        {
          name: 'AppSetting',
          label: '系统配置',
          components: [AppSetting]
        }
      ]
    }
  }
}
</script>

<style scoped>

</style>
