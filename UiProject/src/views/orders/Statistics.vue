<template>
  <div>
    <el-row :gutter="20">
      <el-col :span="20">
        <el-date-picker
          v-model="datevalue"
          type="daterange"
          unlink-panels
          range-separator="至"
          start-placeholder="开始日期"
          end-placeholder="结束日期"
          value-format="yyyy-MM-dd"
          :picker-options="pickerOptions"
          @change="dateChange"
        />
      </el-col>
    </el-row>
    <br>
    <div>
      <div class="flex-box">
        <div id="category_box" style="height: 350%; width: 50%" />
        <div id="missing_box" style="height: 350%; width: 50%" />
      </div>
      <hr>
      <br>
      <div class="flex-box">
        <div id="team_box" style="height: 340%; width: 50%" />
        <div id="module_box" style="height: 350%; width: 50%" />
      </div>
    </div>
  </div>
</template>

<script>
import * as echarts from 'echarts'
import { GetStatisticsData } from '@/api/orders'
import BScroll from 'better-scroll'

export default {
  components: {},
  data() {
    return {
      // 是否是bug
      isBugData: {},
      // bug原因
      bugReasonData: {},
      // 归属架构域
      domainData: [],
      // 技术归属
      technicalData: {},
      foodScroll: '',
      // 加载
      statisticsLoading: false,
      // 图表接口请求参数
      statisticsParams: {},
      // 日期数组
      datevalue: [],
      // 日期选项
      pickerOptions: {
        shortcuts: [{
          text: '最近一周',
          onClick(picker) {
            const end = new Date()
            const start = new Date()
            start.setTime(start.getTime() - 3600 * 1000 * 24 * 7)
            picker.$emit('pick', [start, end])
          }
        }, {
          text: '最近一个月',
          onClick(picker) {
            const end = new Date()
            const start = new Date()
            start.setTime(start.getTime() - 3600 * 1000 * 24 * 30)
            picker.$emit('pick', [start, end])
          }
        }, {
          text: '最近三个月',
          onClick(picker) {
            const end = new Date()
            const start = new Date()
            start.setTime(start.getTime() - 3600 * 1000 * 24 * 90)
            picker.$emit('pick', [start, end])
          }
        }]
      }
    }
  },
  created() {
    this.initScroll()
  },
  mounted() {
    this.defaultDate()
    this.getStatisticsData()
  },
  methods: {
    // 滚动设置
    initScroll() {
      this.foodScroll = new BScroll(this.$refs.foodswrapper, { probeType: 3, click: true })
    },
    // 渲染图表
    randerData() {
      // 获取当前时间区间
      const timeParam = this.dateValueParse()
      // 工单分类
      const category_pie = echarts.init(document.getElementById('category_box'))
      let categoryOptions
      // 提取返回值对象的每个元素，重组数据
      const [bugTotal, bugDataList] = this.isBugData.reduce(([total, data], { bug_state, count }) => {
        total += parseInt(count)
        data.push({ value: count, name: bug_state })
        // console.log(total)
        return [total, data]
      }, [0, []])
      setTimeout(() => {
        categoryOptions = {
          title: {
            text: '是否是BUG',
            left: 'center',
            subtext: bugTotal,
            subtextStyle: {
              fontWeight: 'bolder'
            }
          },
          legend: {
            orient: 'vertical%',
            left: 'right'
          },
          series: [
            {
              name: '是否是BUG',
              type: 'pie',
              radius: ['30%', '70%'],
              center: ['50%', '50%'],
              emphasis: {
                label: {
                  show: true,
                  fontSize: '20',
                  fontWeight: 'bold'
                }
              },
              data: bugDataList,
              itemStyle: {
                normal: {
                  label: {
                    show: true,
                    formatter: '{b}: {c} ({d}%)'
                  },
                  labelLine: {
                    show: true
                  }
                }
              }
            }
          ]
        }
        category_pie.setOption(categoryOptions)
      })
      categoryOptions && category_pie.setOption(categoryOptions)
      category_pie.on(
        'click', (param) => {
          const bugStateParam = Object.assign({
            bug_state: param.name
          }, timeParam)
          // console.log(bugStateParam)
          this.$router.push({
            name: 'order',
            query: bugStateParam
          })
        }
      )
      // 漏测原因
      const missing_pie = echarts.init(document.getElementById('missing_box'))
      let missingOptions
      // 提取返回值对象的每个元素，重组数据
      const [missingTotal, missingDataList] = this.bugReasonData.reduce(([total, data], { bug_reason, count }) => {
        total += parseInt(count)
        data.push({ value: count, name: bug_reason })
        console.log(total)
        return [total, data]
      }, [0, []])
      setTimeout(() => {
        missingOptions = {
          title: {
            text: 'BUG原因',
            left: 'center',
            subtext: missingTotal,
            subtextStyle: {
              fontWeight: 'bolder'
            }
          },
          legend: {
            orient: 'vertical%',
            left: 'right'
          },
          series: [
            {
              name: 'BUG原因',
              type: 'pie',
              radius: ['30%', '70%'],
              center: ['50%', '50%'],
              emphasis: {
                label: {
                  show: true,
                  fontSize: '20',
                  fontWeight: 'bold'
                }
              },
              data: missingDataList,
              itemStyle: {
                normal: {
                  label: {
                    show: true,
                    formatter: '{b}: {c} ({d}%)'
                  },
                  labelLine: {
                    show: true
                  }
                }
              }
            }
          ]
        }
        missing_pie.setOption(missingOptions)
      })
      missingOptions && missing_pie.setOption(missingOptions)
      missing_pie.on(
        'click', (param) => {
          const bugStateParam = Object.assign({
            bug_reason: param.name,
            bug_state: '是'
          }, timeParam)
          // console.log(bugStateParam)
          this.$router.push({
            name: 'order',
            query: bugStateParam
          })
        }
      )
      // 归属团队
      const team_pie = echarts.init(document.getElementById('team_box'))
      let teamOptions
      // 提取返回值对象的每个元素，重组数据
      const [teamTotal, teamDataList] = this.domainData.reduce(([total, data], { domain, count }) => {
        total += parseInt(count)
        data.push({ value: count, name: domain })
        console.log(total)
        return [total, data]
      }, [0, []])
      setTimeout(() => {
        teamOptions = {
          title: {
            text: '归属架构域',
            left: 'center',
            subtext: teamTotal,
            subtextStyle: {
              fontWeight: 'bolder'
            }
          },
          legend: {
            orient: 'vertical%',
            left: 'right'
          },
          series: [
            {
              name: '归属架构域',
              type: 'pie',
              radius: ['30%', '70%'],
              center: ['50%', '50%'],
              emphasis: {
                label: {
                  show: true,
                  fontSize: '20',
                  fontWeight: 'bold'
                }
              },
              data: teamDataList,
              itemStyle: {
                normal: {
                  label: {
                    show: true,
                    formatter: '{b}: {c} ({d}%)'
                  },
                  labelLine: {
                    show: true
                  }
                }
              }
            }
          ]
        }
        team_pie.setOption(teamOptions)
      })
      teamOptions && team_pie.setOption(teamOptions)
      team_pie.on(
        'click', (param) => {
          const bugStateParam = Object.assign({
            domain: param.name,
            bug_state: '是'
          }, timeParam)
          // console.log(bugStateParam)
          this.$router.push({
            name: 'order',
            query: bugStateParam
          })
        }
      )
      // 所属技术域
      const module_pie = echarts.init(document.getElementById('module_box'))
      let moduleOptions
      // 提取返回值对象的每个元素，重组数据
      const [technicalTotal, technicalDataList] = this.technicalData.reduce(([total, data], { technical, count }) => {
        total += parseInt(count)
        data.push({ value: count, name: technical })
        console.log(total)
        return [total, data]
      }, [0, []])
      setTimeout(() => {
        moduleOptions = {
          title: {
            text: '技术归属',
            left: 'center',
            subtext: technicalTotal,
            subtextStyle: {
              fontWeight: 'bolder'
            }
          },
          legend: {
            orient: 'vertical%',
            left: 'right'
          },
          series: [
            {
              name: '技术归属',
              type: 'pie',
              radius: ['30%', '70%'],
              center: ['50%', '50%'],
              emphasis: {
                label: {
                  show: true,
                  fontSize: '20',
                  fontWeight: 'bold'
                }
              },
              data: technicalDataList,
              itemStyle: {
                normal: {
                  label: {
                    show: true,
                    formatter: '{b}: {c} ({d}%)'
                  },
                  labelLine: {
                    show: true
                  }
                }
              }
            }
          ]
        }
        module_pie.setOption(moduleOptions)
        module_pie.resize()
      })
      moduleOptions && module_pie.setOption(moduleOptions)
      module_pie.on(
        'click', (param) => {
          const bugStateParam = Object.assign({
            technical: param.name,
            bug_state: '是'
          }, timeParam)
          // console.log(bugStateParam)
          this.$router.push({
            name: 'order',
            query: bugStateParam
          })
        }
      )
    },
    // 时间解析
    dateValueParse() {
      if (this.datevalue) {
        return {
          start: this.datevalue[0],
          end: this.datevalue[1]
        }
      } else {
        return {}
      }
    },
    // 获取图表数据
    getStatisticsData() {
      // 获取是否是BUG数据
      const timeParams = this.dateValueParse()
      const bugParams = Object.assign({
        group_by: 'bug_state'
      }, timeParams)
      GetStatisticsData(bugParams).then(response => {
        this.isBugData = response.data
        this.randerData()
      })
      // 获取BUG原因数据
      const bugReasonParams = Object.assign({
        is_bug: '是',
        group_by: 'bug_reason',
        bug_reason_isnull: false
      }, timeParams)
      GetStatisticsData(bugReasonParams).then(response => {
        this.bugReasonData = response.data
        this.randerData()
      })
      // 获取归属架构域数据
      const domainParams = Object.assign({
        is_bug: '是',
        domain_isnull: false,
        group_by: 'domain'
      }, timeParams)
      GetStatisticsData(domainParams).then(response => {
        this.domainData = response.data
        this.randerData()
      })
      // 获取技术归属数据
      const technicalParams = Object.assign({
        is_bug: '是',
        technical_isnull: false,
        group_by: 'technical'
      }, timeParams)
      GetStatisticsData(technicalParams).then(response => {
        this.technicalData = response.data
        this.randerData()
      })
    },
    // 日期触发事件
    dateChange() {
      console.log('dateClear') // for debug
      this.statisticsLoading = true
      this.getStatisticsData()
      this.statisticsLoading = false
    },
    // 获取默认日期
    defaultDate() {
      // 日期运算
      const start_date = new Date().getTime() - 24 * 60 * 60 * 1000
      const end_date = start_date - 6 * 24 * 60 * 60 * 1000
      const start_time = new Date(start_date)
      const end_time = new Date(end_date)
      // 日期格式化
      const start_year = start_time.getFullYear()
      const start_month = start_time.getMonth() + 1 < 10 ? '0' + (start_time.getMonth() + 1) : start_time.getMonth() + 1
      const start_day = start_time.getDate() < 10 ? '0' + (start_time.getDate()) : start_time.getDate()
      const end_year = end_time.getFullYear()
      const end_month = end_time.getMonth() + 1 < 10 ? '0' + (end_time.getMonth() + 1) : end_time.getMonth() + 1
      const end_day = end_time.getDate() < 10 ? '0' + (end_time.getDate()) : end_time.getDate()
      const end = start_year + '-' + start_month + '-' + start_day
      const start = end_year + '-' + end_month + '-' + end_day
      this.datevalue = [start, end]
    }
  }
}
</script>

<style scoped>
.flex-box{
  display: flex;
  width: 100%;
}

</style>
