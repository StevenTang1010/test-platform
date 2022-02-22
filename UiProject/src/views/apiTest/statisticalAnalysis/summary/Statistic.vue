<template>
  <div class="main">
    <!--  用例统计  -->
    <el-divider class="blue-line" direction="vertical" />
    <span style="font-weight:bold;font-size:14px;color:#2C8DF4;">用例统计</span>
    <el-container style="padding: 0">
      <el-main v-loading="caseLoading" element-loading-text="Loading">
        <statistic-desc :statistic-list="caseStatisticList" />
      </el-main>
    </el-container>

    <!--  接口统计  -->
    <el-divider class="blue-line" direction="vertical" />
    <span style="font-weight:bold;font-size:14px;color:#2C8DF4;">接口统计</span>
    <el-container style="padding: 0">
      <el-main v-loading="apiLoading" element-loading-text="Loading">
        <statistic-desc :statistic-list="apiStatisticList" />
      </el-main>
    </el-container>
  </div>
</template>

<script>
import StatisticDesc from '@/views/apiTest/components/StatisticDesc'
import get_count_data from '@/api/apiTest/get_count_data'

export default {
  name: 'Statistic',
  components: { StatisticDesc },
  mixins: [get_count_data],
  data() {
    return {
      caseLoading: false,
      apiLoading: false
    }
  },
  mounted() {
    this.fetchData()
  },
  methods: {
    fetchData() {
      this.fetchCaseData()
      this.fetchApiData()
    },
    // 顺序执行获取用例统计数据
    async fetchCaseData() {
      this.caseLoading = true
      await this.getTestCaseCount()
      await this.getTestStepCount()
      this.caseLoading = false
    },
    // 顺序执行获取接口统计数据
    async fetchApiData() {
      this.apiLoading = true
      await this.getApiTotalData()
      await this.getNoCaseApiCountData()
      await this.getToDoApiCount()
      this.apiLoading = false
    }
  }
}
</script>

<style scoped>

</style>
