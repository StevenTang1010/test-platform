<template>
  <div class="main">
    <!--测试用例集 选择执行-->
    <run-test-suite />

    <!--测试用例集 选择执行-->
    <run-test-case style="padding-top: 20px" />
  </div>
</template>

<script>
import RunTestSuite from '@/views/apiTest/workbench/FastTest/RunTestSuite'
import RunTestCase from '@/views/apiTest/workbench/FastTest/RunTestCase'

export default {
  name: 'Index',
  components: { RunTestSuite, RunTestCase },
  data() {
    return {
      themeSize: this.$store.state.settings.themeSize,
      caseOrSuite: 'suite'
    }
  },
  methods: {
    fetchData() {
      switch (this.caseOrSuite) {
        case 'case':
          this.$refs.caseListRef.showMoreFilters = true
          this.$refs.caseListRef.fetchFiltersData()
          this.$refs.caseListRef.fetchData()
          break
        case 'suite':
          this.$refs.suiteListRef.filters.department = []
          this.$refs.suiteListRef.filters.department__isnull = null
          this.$refs.suiteListRef.fetchData()
          break
        default:
          // dd
      }
    }
  }
}
</script>

<style scoped>

</style>
