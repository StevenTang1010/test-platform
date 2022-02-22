<template>
  <div class="main">
    <!--无用例的接口统计-->
    <div id="noCaseApiChart" v-loading="dataLoading" style="width: 500px; height:300px" />
  </div>

</template>

<script>
import * as echarts from 'echarts'
import { getNoCaseApiCount } from '@/api/apiTest/api_info'

export default {
  name: 'NoCaseApi',
  props: {
    groupByField: {
      type: String,
      default() {
        return 'project__name'
      }
    }
  },
  data() {
    return {
      dataLoading: false,
      noCaseApiCountData: [],

      myChart: null
    }
  },
  watch: {
    groupByField(val) {}
  },
  mounted() {
    // 获取接口统计数据
    this.fetchData()
  },
  methods: {
    clearData() {
      this.noCaseApiCountData = []
    },

    // 获取未覆盖接口数据 -- 按项目分组
    getNoCaseApiCountData() {
      const params = {
        group_by_field: this.groupByField
      }
      return getNoCaseApiCount(params).then((res) => {
        const { msg, code } = res
        if (code === 2) {
          const countData = res.data
          for (let i = 0; i < countData.length; i++) {
            const data = countData[i]
            this.noCaseApiCountData.push({ value: data['count'], name: data[this.groupByField] })
          }
        } else {
          this.$message.error({
            message: msg
          })
        }
      })
    },
    // echarts Pie图表绘制
    drawPie() {
      // 基于准备好的dom，初始化echarts实例
      if (this.myChart != null && this.myChart !== '' && this.myChart !== undefined) {
        this.myChart.dispose() // 销毁
      }
      this.myChart = echarts.init(document.getElementById('noCaseApiChart'))
      // 绘制图表
      this.myChart.setOption({
        title: {
          text: '无用例接口',
          left: 'center'
        },
        tooltip: {
          trigger: 'item'
        },
        // legend: {
        //   orient: 'vertical',
        //   left: 'left'
        // },
        series: [
          {
            type: 'pie',
            radius: ['40%', '70%'],
            avoidLabelOverlap: false,
            itemStyle: {
              borderRadius: 10,
              borderColor: '#fff',
              borderWidth: 2
            },
            label: {
              show: false,
              position: 'center',
              formatter: '{d}%'
            },
            emphasis: {
              label: {
                show: true,
                fontSize: '30',
                fontWeight: 'bold'
              }
            },
            labelLine: {
              show: false
            },
            data: this.noCaseApiCountData
          }
        ]
      })
    },

    async fetchData() {
      this.dataLoading = true
      await this.getNoCaseApiCountData()
      await this.drawPie()
      this.dataLoading = false
    }
  }
}
</script>

<style scoped>

</style>
