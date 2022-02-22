<template>
  <div class="main">
    <!--接口、用例统计信息-->
    <statistic />
    <!--接口覆盖率统计信息-->
    <el-divider class="blue-line" direction="vertical" />
    <span slot="title" style="font-weight:bold;font-size:14px;color:#2C8DF4;">覆盖率统计</span>
    <el-description v-if="apiCount >0" style="padding-top: 10px">
      <el-description-item :label="'覆盖率（'+(apiCount-noCaseApiCount)+'/'+apiCount+'）'" :span-map="{md:12}">
        <template slot="content">
          <el-progress
            :text-inside="true"
            :stroke-width="26"
            status="success"
            :percentage="Math.round(((apiCount-noCaseApiCount)/apiCount)*100)"
          />
        </template>
      </el-description-item>
    </el-description>

    <!-- 显示接口列表信息 -->
    <api-list ref="apiListRef" table-name="未覆盖接口列表" fetch-data-method="getNoCaseApi" style="padding-top: 10px" />
  </div>

</template>

<script>
import ElDescriptionItem from '@/components/Description/ElDescriptionItem'
import ElDescription from '@/components/Description/ElDescription'
import Statistic from '@/views/apiTest/statisticalAnalysis/summary/Statistic'
import ApiList from '@/views/apiTest/apiMgr/ApiList'
import get_count_data from '@/api/apiTest/get_count_data'

export default {
  name: 'Coverage',
  components: { ElDescription, ElDescriptionItem, Statistic, ApiList },
  mixins: [get_count_data],
  mounted() {
    this.$refs.apiListRef.fetchData()
    this.getApiTotalData()
    this.getNoCaseApiCountData()
    this.getTestCaseCount()
    this.getTestStepCount()
  },
  methods: {
  }
}
</script>

<style scoped>

</style>
