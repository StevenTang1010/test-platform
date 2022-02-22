<template>
  <div class="main">
    <el-page-header v-if="showPageHeader" title="返回" content="用例详情" style="padding: 10px" @back="goBack" />

    <!--  用例基本信息  -->
    <case-base-info ref="caseBaseInfoRef" />

    <!-- 用例步骤列表 -->
    <step-list ref="stepListRef" />
  </div>
</template>

<script>
import CaseBaseInfo from '@/views/apiTest/caseMgr/caseDetail/CaseBaseInfo'
import StepList from '@/views/apiTest/caseMgr/StepList'
export default {
  name: 'Index',
  components: { CaseBaseInfo, StepList },
  data() {
    return {
      showPageHeader: false
    }
  },
  mounted() {
    if (typeof (this.$route.params.case_id) !== 'undefined') {
      this.showPageHeader = true
      this.getCaseStepInfo(this.$route.params.case_id)
    }
  },
  methods: {
    getCaseStepInfo(caseID) {
      this.$refs.caseBaseInfoRef.getCaseInfo(caseID)
      this.$refs.stepListRef.filters.test_case = [{ id: caseID }]
      this.$refs.stepListRef.allowUpdateStepId = true
      this.$refs.stepListRef.fetchData()
    },
    goBack() {
      this.$router.back()
    }
  }
}
</script>

<style scoped>

</style>
