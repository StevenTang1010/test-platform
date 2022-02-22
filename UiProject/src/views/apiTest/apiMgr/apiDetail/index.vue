<template>
  <div class="main" :style="{height: showPageHeader?'100%':innerHeight}">
    <el-page-header v-if="showPageHeader" title="返回" content="接口详情" style="padding: 10px" @back="goBack" />
    <tabs-menu :tab-pane-list="tabPaneList" style="padding-top: 0" />
  </div>
</template>

<script>
import TabsMenu from '@/views/apiTest/components/TabsMenu'
import ApiBaseInfo from '@/views/apiTest/apiMgr/apiDetail/ApiBaseInfo'
import ApiUpdateHistory from '@/views/apiTest/apiMgr/apiDetail/ApiUpdateHistory'
import StepList from '@/views/apiTest/caseMgr/StepList'

export default {
  name: 'Index',
  components: { TabsMenu },
  props: {
    showPageHeader: {
      type: Boolean,
      default() {
        return true
      }
    },
    innerHeight: {
      type: String,
      default() {
        return document.body.clientHeight - 130 + 'px'
      }
    }
  },
  data() {
    return {
      tabPaneList: [
        {
          name: 'ApiBaseInfo',
          label: '接口信息',
          components: [ApiBaseInfo]
        },
        {
          name: 'ApiUpdateHistory',
          label: '变更历史',
          components: [ApiUpdateHistory]
        },
        {
          name: 'StepList',
          label: '步骤列表',
          components: [StepList]
        }
      ]
    }
  },
  mounted() {},
  methods: {
    goBack() {
      this.$router.back()
    }
  }
}
</script>

<style scoped>

</style>
