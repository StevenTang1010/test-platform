<template>
  <div class="main">
    <el-radio-group v-model="activeName" :size="themeSize" style="margin-bottom: 10px;">
      <el-radio-button label="coverage">接口覆盖率</el-radio-button>
      <el-radio-button label="update">接口更新</el-radio-button>
    </el-radio-group>
    <!--显示接口覆盖率信息：覆盖率 页面-->
    <template v-if="activeName==='coverage'">
      <api-coverage />
    </template>
    <!--显示接口更新信息：更新 页面-->
    <template v-if="activeName==='update'">
      <api-update />
    </template>
  </div>
</template>

<script>
import ApiCoverage from '@/views/apiTest/apiMgr/apiAnalysis/ApiCoverage'
import ApiUpdate from '@/views/apiTest/apiMgr/apiAnalysis/ApiUpdate'

export default {
  name: 'ApiAnalysis',
  components: { ApiUpdate, ApiCoverage },
  data() {
    return {
      themeSize: this.$store.state.settings.themeSize,
      // 默认选中
      activeName: 'coverage'
    }
  },
  mounted() {
  },
  methods: {
  }
}
</script>

<style scoped>

</style>
