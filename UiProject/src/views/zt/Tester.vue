<!--todo: 无筛选项则展示总体数据，展示内容为有效率、关闭率、漏测率、bug/pd率-->
<!--todo: 支持团队筛选-->
<!--todo: 支持级联团队单人筛选-->
<template>
  <div>
    <el-row style="padding-left: 1px; padding-top: 1px">
      <el-col :span="25">
        <el-form :model="modelForm">
          <el-form-item>
            <el-select v-model="systemValue" clearable placeholder="请选择系统" size="mini" @change="getPrimaryList">
              <el-option v-for="(item, index) in modelForm.system" :key="index" :label="item.system_name" :value="item.system_id" />
            </el-select>
            <el-select v-model="firstModelValue" clearable placeholder="请选择一级模块" size="mini" @change="getSecondaryList">
              <el-option v-for="(item, index) in modelForm.first" :key="index" :label="item.primary_module_name" :value="item.primary_module_id" />
            </el-select>
            <el-select v-model="secondModelValue" clearable placeholder="请选择二级模块" size="mini" @change="getThirdList">
              <el-option v-for="(item, index) in modelForm.second" :key="index" :label="item.secondary_module_name" :value="item.secondary_module_id" />
            </el-select>
            <el-select v-model="thirdModelValue" clearable placeholder="请选择三级模块" size="mini">
              <el-option v-for="(item, index) in modelForm.third" :key="index" :label="item.third_module_name" :value="item.third_module_id" />
            </el-select>
            <el-button type="primary" icon="el-icon-search" size="small" style="margin-left: 10px" circle @click.native="getSearchData" />
            <el-button type="default" icon="el-icon-refresh-left" size="small" style="margin-left: 10px" circle @click.native="filterClear" />
          </el-form-item>
        </el-form>
      </el-col>
      <el-button type="primary" icon="el-icon-plus" size="small" style="float: right; margin-right: 20px; margin-top: 2px" circle @click="addDialog" />
      <el-button type="primary" icon="el-icon-upload2" size="small" style="float: right; margin-right: 20px; margin-top: 2px" circle @click="dialogVisible = true" />
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
      domainData: {},
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
      // 工单分类
      const category_pie = echarts.init(document.getElementById('category_box'))
      let categoryOptions
      // 提取返回值对象的每个元素，重组数据
      const [bugTotal, bugDataList] = this.isBugData.reduce(([total, data], { bug_state, count }) => {
        let bug_name
        total += parseInt(count)
        if (bug_state) {
          bug_name = '是'
        } else {
          console.log(bug_state)
          bug_name = '否'
        }
        data.push({ value: count, name: bug_name })
        console.log(total)
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
        group_by: 'bug_reason'
      }, timeParams)
      GetStatisticsData(bugReasonParams).then(response => {
        this.bugReasonData = response.data
        this.randerData()
      })
      // 获取归属架构域数据
      const domainParams = Object.assign({
        is_bug: true,
        group_by: 'domain'
      }, timeParams)
      GetStatisticsData(domainParams).then(response => {
        this.domainData = response.data
        this.randerData()
      })
      // 获取技术归属数据
      const technicalParams = Object.assign({
        is_bug: true,
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
      const start_date = new Date().getTime() - 24 * 60 * 60 * 1000
      const end_date = start_date - 8 * 24 * 60 * 60 * 1000
      const start_time = new Date(start_date)
      const end_time = new Date(end_date)
      const start_year = start_time.getFullYear()
      const start_month = start_time.getMonth() + 1 < 10 ? '0' + (start_time.getMonth() + 1) : start_time.getMonth() + 1
      const start_day = start_time.getDate() < 10 ? '0' + (start_time.getDate()) : start_time.getDate()
      const end_year = end_time.getFullYear()
      const end_month = end_time.getMonth() + 1 < 10 ? '0' + (end_time.getMonth() + 1) : end_time.getMonth() + 1
      const end_day = end_time.getDate() < 10 ? '0' + (end_time.getDate()) : end_time.getDate()
      const end = start_year + '-' + start_month + '-' + start_day
      const start = end_year + '-' + end_month + '-' + end_day
      // console.log(start)
      // console.log(end)
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
