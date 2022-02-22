import { getApiCount, getApiTotal, getNoCaseApiCount } from '@/api/apiTest/api_info'
import { getTestCaseCount } from '@/api/apiTest/test_case'
import { getTestStepCount } from '@/api/apiTest/test_step'

export default {
  data() {
    return {
      // 统计数据
      apiCount: 0,
      noCaseApiCount: 0,
      caseStatisticList: [],
      apiStatisticList: []
    }
  },
  methods: {
    // 接口统计
    getApiTotalData() {
      return getApiTotal({}).then(response => {
        const { msg, code } = response
        if (code === 2) {
          this.apiCount = response.data.total
          this.apiStatisticList.push(
            {
              label: '接口总数',
              count: response.data.total
            }
          )
        } else {
          this.$message.error({
            message: msg,
            center: true
          })
        }
      })
    },
    getNoCaseApiCountData() {
      return getNoCaseApiCount({ group_by_field: 'project' }).then(response => {
        const { msg, code } = response
        if (code === 2) {
          const countData = response.data
          let count = 0
          for (let i = 0; i < countData.length; i++) {
            const data = countData[i]
            count += data['count']
          }
          this.noCaseApiCount = count
          this.apiStatisticList.push(
            {
              label: '无用例接口数',
              count: count
            }
          )
        } else {
          this.$message.error({
            message: msg,
            center: true
          })
        }
      })
    },
    getToDoApiCount() {
      return getApiCount({ group_by_field: 'update_status' }).then(response => {
        const { msg, code } = response
        this.listLoading = false
        if (code === 2) {
          const countData = response.data
          for (let i = 0; i < countData.length; i++) {
            const data = countData[i]
            const update_status = data['update_status']
            const count = data['count']
            if (update_status === 0) {
              this.apiStatisticList.push(
                {
                  label: '待处理接口',
                  count: count
                }
              )
            } else if (update_status === 1) {
              this.apiStatisticList.push(
                {
                  label: '待验证接口',
                  count: count
                }
              )
            } else if (update_status === 2) {
              this.apiStatisticList.push(
                {
                  label: '已验证接口',
                  count: count
                }
              )
            } else {
              // 无效的update_status
            }
          }
        } else {
          this.$message.error({
            message: msg,
            center: true
          })
        }
      })
    },
    // 用例统计
    getTestCaseCount() {
      return getTestCaseCount({ group_by_field: 'type' }).then(response => {
        const { msg, code } = response
        if (code === 2) {
          const countData = response.data
          let count = 0
          for (let i = 0; i < countData.length; i++) {
            const data = countData[i]
            count += data['count']
            this.caseStatisticList.push(
              {
                label: data['type'],
                count: data['count']
              }
            )
          }
          this.caseStatisticList.push(
            {
              label: '测试用例数',
              count: count
            }
          )
        } else {
          this.$message.error({
            message: msg,
            center: true
          })
        }
      })
    },
    getTestStepCount() {
      return getTestStepCount({ group_by_field: 'result' }).then(response => {
        const { msg, code } = response
        if (code === 2) {
          const countData = response.data
          let count = 0
          for (let i = 0; i < countData.length; i++) {
            const data = countData[i]
            count += data['count']
          }
          this.caseStatisticList.push(
            {
              label: '测试步骤数',
              count: count
            }
          )
        } else {
          this.$message.error({
            message: msg,
            center: true
          })
        }
      })
    }
  }
}
