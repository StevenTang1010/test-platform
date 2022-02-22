<template>
  <div class="main">
    <tabs-menu :tab-pane-list="tabPaneList" />
    <el-container>
      <el-aside style="width:420px; padding-left: 5px">
        <upload-data />
      </el-aside>
      <el-aside style="width:420px; padding-left: 5px">
        <download-data />
      </el-aside>
    </el-container>
  </div>
</template>

<script>
import TabsMenu from '@/views/apiTest/components/TabsMenu'
import uploadData from '@/views/apiTest/dataMgr/uploadData/index'
import downloadData from '@/views/apiTest/dataMgr/downloadData/index'

export default {
  name: 'DataMgrIndex',
  components: { TabsMenu, uploadData, downloadData },
  data() {
    return {
      tabPaneList: [
        {
          name: 'dataMgr',
          label: '数据管理',
          components: []
        }
      ]
    }
  }
}
</script>

<style scoped>

</style>
