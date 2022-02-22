<template>
  <div class="main">
    <!--  用例集基本信息  -->
    <suite-base-info ref="suiteBaseInfoRef" />

    <!-- 用例列表 -->
    <case-list ref="caseListRef" />
  </div>
</template>

<script>
import SuiteBaseInfo from '@/views/apiTest/caseMgr/suiteDetail/SuiteBaseInfo'
import CaseList from '@/views/apiTest/caseMgr/CaseList'
export default {
  name: 'Index',
  components: { SuiteBaseInfo, CaseList },
  data() {
    return {}
  },
  mounted() {
    // this.fetchData()
  },
  methods: {
    fetchData(suiteID) {
      this.$refs.suiteBaseInfoRef.fetchData(suiteID)
      this.$refs.caseListRef.filters.test_suite = [{ id: suiteID }]
      this.$refs.caseListRef.fetchData()
    }
  }
}
</script>

<style scoped>

</style>
