<template>
  <div class="main">
    <!--趋势统计-->
    <el-divider class="blue-line" direction="vertical" />
    <span style="font-weight:bold;font-size:14px;color:#2C8DF4;">趋势统计</span>
    <!--数据统计条件-->
    <div style="padding: 10px 0 0 20px">
      <!--时间分组-->
      <el-radio-group v-model="timeUnit" :size="themeSize" @change="fetchData">
        <el-radio-button label="year">按年</el-radio-button>
        <el-radio-button label="month">按月</el-radio-button>
        <el-radio-button label="week">按周</el-radio-button>
        <el-radio-button label="day">按日</el-radio-button>
      </el-radio-group>
      <!--时间范围-->
      <span style="padding-left:10px;font-size:14px">创建时间:</span>
      <el-date-picker
        v-model="dateRange"
        type="daterange"
        align="right"
        :size="themeSize"
        unlink-panels
        range-separator="至"
        start-placeholder="开始日期"
        end-placeholder="结束日期"
        value-format="yyyy-MM-dd"
        :picker-options="pickerOptions"
        @change="fetchData"
      />
      <!--统计数据类型-->
      <span style="padding-left:10px;font-size:14px">统计类型:</span>
      <el-select
        v-model="dataType"
        :size="themeSize"
        style="width:100px"
        value-key="id"
        placeholder="请选择数据类型"
        @change="fetchData"
      >
        <el-option label="累计" value="sum" />
        <el-option label="新增" value="add" />
      </el-select>
    </div>
    <el-container style="min-height: 285px">
      <el-main v-loading="trendLoading" element-loading-text="Loading">
        <div id="addTrendChart" style="width:100%;height:100%" />
      </el-main>
    </el-container>
  </div>

</template>

<script>
import * as echarts from 'echarts'
import { getTestCaseCount } from '@/api/apiTest/test_case'
import { getTestStepCount } from '@/api/apiTest/test_step'
import { getApiCount, getWithCaseApiCount } from '@/api/apiTest/api_info'

export default {
  name: 'AddTrend',
  data() {
    return {
      themeSize: this.$store.state.settings.themeSize,
      trendLoading: false,
      timeUnit: 'day',
      dateRange: null,
      dataType: 'sum',

      pickerOptions: {
        shortcuts: [
          {
            text: '本月',
            onClick(picker) {
              picker.$emit('pick', [new Date(), new Date()])
            }
          },
          {
            text: '今年至今',
            onClick(picker) {
              const end = new Date()
              const start = new Date(new Date().getFullYear(), 0)
              picker.$emit('pick', [start, end])
            }
          },
          {
            text: '最近三个月',
            onClick(picker) {
              const end = new Date()
              const start = new Date()
              start.setMonth(start.getMonth() - 3)
              picker.$emit('pick', [start, end])
            }
          },
          {
            text: '最近六个月',
            onClick(picker) {
              const end = new Date()
              const start = new Date()
              start.setMonth(start.getMonth() - 6)
              picker.$emit('pick', [start, end])
            }
          }
        ]
      },

      timeData: {},
      time_str_list: [],
      api_num_list: [],
      case_num_list: [],
      step_num_list: [],
      coverage_num_list: [],

      myChart: null
    }
  },
  mounted() {
    // 获取统计数据并绘图
    this.fetchData()
  },
  methods: {
    clearData() {
      this.timeData = {}
      this.time_str_list = []
      this.api_num_list = []
      this.case_num_list = []
      this.step_num_list = []
      this.coverage_num_list = []
    },
    insertData(time_str, data) {
      if (!Object.prototype.hasOwnProperty.call(this.timeData, time_str)) {
        this.timeData[time_str] = {
          api_num: 0,
          api_sum: 0,
          withCaseApi_sum: 0,
          case_num: 0,
          step_num: 0
        }
      }
      this.timeData[time_str] = Object.assign(this.timeData[time_str], data)
    },
    // 获取Case数据 -- 按创建时间分组
    getTestCaseCountData() {
      const params = {
        group_by_field: 'create_time',
        time_unit: this.timeUnit,
        create_time__gte: this.dateRange ? this.dateRange[0] : this.dateRange,
        create_time__lte: this.dateRange ? this.dateRange[1] : this.dateRange
      }
      return getTestCaseCount(params).then(response => {
        const { msg, code } = response
        if (code === 2) {
          const countData = response.data
          let count = 0
          for (let i = 0; i < countData.length; i++) {
            const data = countData[i]
            const create_time = data['create_time']
            if (this.dataType === 'sum') {
              count += data['count']
            } else {
              count = data['count']
            }
            this.insertData(create_time, { case_num: count })
          }
        } else {
          this.$message.error({
            message: msg,
            center: true
          })
        }
      })
    },
    getTestStepCountData() {
      const params = {
        group_by_field: 'create_time',
        time_unit: this.timeUnit,
        create_time__gte: this.dateRange ? this.dateRange[0] : this.dateRange,
        create_time__lte: this.dateRange ? this.dateRange[1] : this.dateRange
      }
      return getTestStepCount(params).then(response => {
        const { msg, code } = response
        if (code === 2) {
          const countData = response.data
          let count = 0
          for (let i = 0; i < countData.length; i++) {
            const data = countData[i]
            const create_time = data['create_time']
            if (this.dataType === 'sum') {
              count += data['count']
            } else {
              count = data['count']
            }
            this.insertData(create_time, { step_num: count })
          }
        } else {
          this.$message.error({
            message: msg,
            center: true
          })
        }
      })
    },
    // 获取API数据 -- 按创建时间分组
    getApiCountData() {
      const params = {
        group_by_field: 'create_time',
        time_unit: this.timeUnit,
        create_time__gte: this.dateRange ? this.dateRange[0] : this.dateRange,
        create_time__lte: this.dateRange ? this.dateRange[1] : this.dateRange
      }
      return getApiCount(params).then(response => {
        const { msg, code } = response
        let count = 0
        let countSum = 0
        if (code === 2) {
          const countData = response.data
          for (let i = 0; i < countData.length; i++) {
            const data = countData[i]
            const create_time = data['create_time']
            countSum += data['count']
            count = this.dataType === 'sum' ? countSum : data['count']
            this.insertData(create_time, { api_num: count, api_sum: countSum })
          }
        } else {
          this.$message.error({
            message: msg,
            center: true
          })
        }
      })
    },
    getWithCaseApiCountData() {
      const params = {
        group_by_field: 'api_test_teststep.create_time',
        time_unit: this.timeUnit,
        create_time__gte: this.dateRange ? this.dateRange[0] : this.dateRange,
        create_time__lte: this.dateRange ? this.dateRange[1] : this.dateRange
      }
      return getWithCaseApiCount(params).then(response => {
        const { msg, code } = response
        let count = 0
        if (code === 2) {
          const countData = response.data
          for (let i = 0; i < countData.length; i++) {
            const data = countData[i]
            const create_time = data['api_test_teststep.create_time']
            count += data['count']
            this.insertData(create_time, { withCaseApi_sum: count })
          }
        } else {
          this.$message.error({
            message: msg,
            center: true
          })
        }
      })
    },

    // echarts Line Chart图表绘制
    drawLineChart() {
      const sortTime = Object.keys(this.timeData).sort()
      let last_v = {}
      let last_coverage = 0
      for (const idx in sortTime) {
        const time_str = sortTime[idx]
        const v = this.timeData[time_str]
        if (!last_v) {
          last_v = v
        }
        this.time_str_list.push(time_str)
        this.api_num_list.push(v.api_num === 0 && this.dataType === 'sum' ? last_v.api_num : v.api_num)
        this.case_num_list.push(v.case_num === 0 && this.dataType === 'sum' ? last_v.case_num : v.case_num)
        this.step_num_list.push(v.step_num === 0 && this.dataType === 'sum' ? last_v.step_num : v.step_num)
        const withCaseApi_sum = v.withCaseApi_sum === 0 ? last_v.withCaseApi_sum : v.withCaseApi_sum
        const coverage = Math.round(withCaseApi_sum / v.api_sum * 10000) / 100
        if (this.dataType === 'sum') {
          this.coverage_num_list.push(coverage)
        } else {
          this.coverage_num_list.push(coverage - last_coverage)
        }
        for (const key in v) {
          const value = v[key]
          if (value > 0) {
            last_v[key] = value
          }
        }
        last_coverage = coverage
      }
      // 基于准备好的dom，初始化echarts实例
      if (this.myChart != null && this.myChart !== '' && this.myChart !== undefined) {
        this.myChart.dispose() // 销毁
      }
      this.myChart = echarts.init(document.getElementById('addTrendChart'))
      // 自适应大小
      window.addEventListener('resize', () => {
        this.myChart.resize()
      })
      // 绘制图表
      const colors = ['#5470C6', '#e31515', '#91CC75']
      this.myChart.setOption({
        // title: {
        //   text: '新增趋势'
        // },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'cross'
          }
        },
        legend: {
          data: ['接口', '用例', '步骤', '覆盖率']
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        toolbox: {
          feature: {
            dataView: { show: true, readOnly: false },
            saveAsImage: { show: true }
          }
        },
        xAxis: {
          type: 'category',
          boundaryGap: false,
          axisTick: {
            alignWithLabel: true
          },
          data: JSON.parse(JSON.stringify(this.time_str_list))
        },
        yAxis: [
          {
            name: '数量',
            type: 'value',
            min: 0,
            position: 'left',
            axisLine: {
              show: true,
              lineStyle: {
                color: colors[0]
              }
            }
          },
          {
            name: '覆盖率',
            type: 'value',
            min: 0,
            max: 100,
            position: 'right',
            axisLine: {
              show: true,
              lineStyle: {
                color: colors[1]
              }
            },
            axisLabel: {
              formatter: '{value} %'
            }
          }
        ],
        series: [
          {
            name: '接口',
            type: 'line',
            stack: 'api',
            data: JSON.parse(JSON.stringify(this.api_num_list))
          },
          {
            name: '用例',
            type: 'line',
            stack: 'case',
            data: JSON.parse(JSON.stringify(this.case_num_list))
          },
          {
            name: '步骤',
            type: 'line',
            stack: 'step',
            data: JSON.parse(JSON.stringify(this.step_num_list))
          },
          {
            name: '覆盖率',
            type: 'line',
            stack: 'coverage',
            yAxisIndex: 1,
            data: JSON.parse(JSON.stringify(this.coverage_num_list))
          }
        ]
      })
    },

    async fetchData() {
      this.trendLoading = true
      await this.clearData()
      await this.getApiCountData()
      await this.getWithCaseApiCountData()
      await this.getTestCaseCountData()
      await this.getTestStepCountData()
      await this.drawLineChart()
      this.trendLoading = false
    }
  }
}
</script>

<style scoped>

</style>
