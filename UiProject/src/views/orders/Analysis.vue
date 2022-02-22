<template>
  <div>
    <br>
    <div>
      <div>
        <el-radio-group v-model="teamValue" style="margin-left: 5px" @change="changeTeam">
          <el-radio-button :label="1">汇总</el-radio-button>
          <el-radio-button v-for="(item, index) in teamList" :key="index" :label="item" />
        </el-radio-group>
      </div>
      <br>
      <div id="week_box" style="height: 350%; width: 99%" />
      <hr>
      <br>
      <div id="month_box" style="height: 350%; width: 99%" />
      <hr>
      <br>
      <div id="bug_trend_box" style="height: 550%; width: 99%" />
      <!--      <p v-model="reportData" type="textarea" placeholder="暂无结论"></p>-->
    </div>
  </div>
</template>

<script>
import * as echarts from 'echarts'
import { GetAnalysisData, GetBugTrendData } from '@/api/orders'

export default {
  components: {},
  data() {
    return {
      weekData: {},
      monthData: {},
      // 日期数据
      teamList: ['CRM', '营销', '商城', '客服', '运营', '业务中台', '技术中台', '数据中台'],
      teamValue: 1

    }
  },
  created() {
  },
  mounted() {
    this.getAnalysisData()
    this.getBugTrendData()
  },
  methods: {
    // 获取趋势折线图数据
    getAnalysisData() {
      if (this.teamValue === 1) {
        this.team = ''
      } else {
        this.team = this.teamValue
      }
      const week_params = {
        is_bug: '是',
        domain: this.team,
        time_unit: 'week',
        group_by: 'pub_date'
      }
      GetAnalysisData(week_params).then(response => {
        this.weekData = response.data
        // 提取返回值对象的每个元素，拆分成2个数组
        const [weekList, weekCountList] = this.weekData.reduce(([l1, l2], { pub_date, count }) => {
          l1.push(pub_date)
          l2.push(count)
          return [l1, l2]
        }, [[], []])
        // const [dateList, countList] = [[], []]
        // for (var i = 0; i < this.weekData.length; i++) {
        //   dateList.push(this.weekData[i].pub_date)
        //   countList.push(this.weekData[i].count)
        // }
        // console.log(dateList)
        // 周趋势
        const week_line = echarts.init(document.getElementById('week_box'))
        const weekOptions = {
          title: {
            text: '总数量趋势（周）'
          },
          tooltip: {
            trigger: 'axis'
          },
          legend: {
            data: ['BUG工单']
          },
          xAxis: {
            type: 'category',
            boundaryGap: false,
            data: weekList
          },
          axisLabel: {
            interval: 0,
            rotate: 40
          },
          yAxis: {
            type: 'value'
          },
          series: {
            'name': 'BUG工单',
            'type': 'line',
            'data': weekCountList
          }
        }
        week_line.setOption(weekOptions)
        week_line.resize()
      })
      const month_params = {
        is_bug: '是',
        domain: this.team,
        time_unit: 'month',
        group_by: 'pub_date'
      }
      GetAnalysisData(month_params).then(response => {
        this.monthData = response.data
        // 提取返回值对象的每个元素，拆分成2个数组
        const [monthList, monthCountList] = this.monthData.reduce(([l1, l2], { pub_date, count }) => {
          l1.push(pub_date)
          l2.push(count)
          return [l1, l2]
        }, [[], []])
        // 月趋势
        const month_line = echarts.init(document.getElementById('month_box'))
        const monthOptions = {
          title: {
            text: '总数量趋势（月）'
          },
          tooltip: {
            trigger: 'axis'
          },
          legend: {
            data: [this.team + 'BUG工单']
          },
          xAxis: {
            type: 'category',
            boundaryGap: false,
            data: monthList
          },
          yAxis: {
            type: 'value'
          },
          series: {
            'name': 'BUG工单',
            'type': 'line',
            data: monthCountList
          }
        }
        month_line.setOption(monthOptions)
        month_line.resize()
      })
    },
    // 获取bug分类趋势数据
    getBugTrendData() {
      const params = {
        is_bug: '是',
        domain: this.team
      }
      GetBugTrendData(params).then(response => {
        this.bugtrendData = response.data
        // 漏测原因
        const bug_trend_bar = echarts.init(document.getElementById('bug_trend_box'))
        let bugTrendOptions
        setTimeout(() => {
          bugTrendOptions = {
            title: {
              text: 'BUG分类',
              left: 'left'
            },
            tooltip: {
              trigger: 'axis',
              showContent: false
            },
            dataset: {
              source: this.bugtrendData.missing_reasion_count_month_list
            },
            xAxis: { type: 'category' },
            yAxis: { gridIndex: 0 },
            grid: { top: '55%' },
            series: this.bugtrendData.missing_reasion_series
          }
          bug_trend_bar.on('updateAxisPointer', function(event) {
            const xAxisInfo = event.axesInfo[0]
            if (xAxisInfo) {
              const dimension = xAxisInfo.value + 1
              bug_trend_bar.setOption({
                series: {
                  id: 'pie',
                  label: {
                    formatter: '{b}: {@[' + dimension + ']} ({d}%)'
                  },
                  encode: {
                    value: dimension,
                    tooltip: dimension
                  }
                }
              })
            }
          })
          bug_trend_bar.setOption(bugTrendOptions)
          bug_trend_bar.resize()
        })
        bugTrendOptions && bug_trend_bar.setOption(bugTrendOptions)
      })
    },
    // 触发切换数据
    changeTeam() {
      this.getAnalysisData()
    }
  }
}
</script>

<style>
</style>
