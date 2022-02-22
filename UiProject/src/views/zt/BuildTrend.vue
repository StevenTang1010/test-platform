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
          @input="dateChange"
        />
        <el-button-group>
          <el-button
            icon="el-icon-refresh"
            size="small"
            style="margin-left: 10px"
            type="primary"
            :loading="getBottonLoading"
            @click="getNewData"
          >拉取新数据
          </el-button>
          <!--          todo: 暂时先注释掉导出按钮，解决问题后恢复-->
          <!--          <el-button-->
          <!--            icon="el-icon-download"-->
          <!--            size="small"-->
          <!--            style="margin-left: 10px"-->
          <!--            type="success"-->
          <!--            :loading="exportBottonLoading"-->
          <!--            @click="orderExport"-->
          <!--          >结果导出-->
          <!--          </el-button>-->
        </el-button-group>
      </el-col>
      <br>
      <el-col :span="30">
        <el-form :model="selectForm">
          <el-form-item>
            <el-input v-model="selectForm.ticketNumber" clearable placeholder="工单编号" size="mini" style="width: 12%" />
            <el-select
              v-model="selectForm.bug_state"
              clearable
              placeholder="是否BUG"
              size="mini"
              value-key="id"
              @visible-change="handleChangeFlag"
            >
              <el-option
                v-for="(item, index) in bugStateFilterList"
                :key="index"
                :label="item.text"
                :value="item.value"
              />
            </el-select>
            <el-select
              v-model="selectForm.category"
              clearable
              placeholder="分类"
              size="mini"
              @visible-change="handleChangeFlag"
            >
              <el-option
                v-for="(item, index) in categoryFilterList"
                :key="index"
                :label="item.text"
                :value="item.value"
              />
            </el-select>
            <el-select
              v-model="selectForm.bug_reason"
              clearable
              placeholder="BUG原因"
              size="mini"
              value-key="id"
              @visible-change="handleChangeFlag"
            >
              <el-option
                v-for="(item, index) in bugReasonFilterList"
                :key="index"
                :label="item.text"
                :value="item.value"
              />
            </el-select>
            <el-select
              v-model="selectForm.domain__contains"
              clearable
              placeholder="归属业务域"
              size="mini"
              value-key="id"
              @visible-change="handleChangeFlag"
            >
              <el-option v-for="(item, index) in domainFilterList" :key="index" :label="item.text" :value="item.value" />
            </el-select>
            <el-select
              v-model="selectForm.technical"
              clearable
              placeholder="技术归属"
              size="mini"
              value-key="id"
              @visible-change="handleChangeFlag"
            >
              <el-option
                v-for="(item, index) in technicalFilterList"
                :key="index"
                :label="item.text"
                :value="item.value"
              />
            </el-select>
            <el-button
              type="primary"
              icon="el-icon-search"
              size="small"
              style="margin-left: 10px"
              @click.native="handleFilterChange"
            >查询
            </el-button>
            <el-button
              type="default"
              icon="el-icon-circle-close"
              size="small"
              style="margin-left: 10px"
              @click.native="filterClear"
            >重置
            </el-button>
          </el-form-item>
        </el-form>
      </el-col>
    </el-row>
    <div class="table-container">
      <el-table
        ref="table"
        v-loading="listLoading"
        element-loading-text="拼命加载中"
        :data="list.results"
        border
        :max-height="tableHeight"
      >
        <el-table-column align="center" label="工单编号" prop="ticket_number" width="150px" />
        <el-table-column label="严重程度" align="center" prop="severity" width="80px" />
        <el-table-column label="详情" align="center" prop="content" :show-overflow-tooltip="true" />
        <el-table-column label="分类" prop="category" align="center" width="100px" />
        <el-table-column align="center" prop="bug_reason" label="BUG原因" width="150px" />
        <el-table-column align="center" prop="domain" label="归属业务域" width="120px" />
        <el-table-column align="center" prop="module" label="功能模块" width="150px" />
        <el-table-column align="center" prop="technical" label="技术归属" width="100px" />
        <el-table-column align="center" label="操作" width="100px">
          <template slot-scope="scope">
            <el-button type="primary" icon="el-icon-edit" circle @click="openDialog(scope.$index, scope.row)" />
          </template>
        </el-table-column>
      </el-table>
      <br>
      <el-pagination
        :current-page="currentPage"
        layout="total, prev, pager, next"
        background
        :page-size="50"
        :total="list.count"
        @current-change="CurrentChange"
        @prev-click="pervious"
        @next-click="next"
      />
    </div>
    <el-drawer
      ref="drawer"
      title="编辑工单详情"
      destroy-on-close="true"
      modal="true"
      wrapper-closable="false"
      size="50%"
      :visible.sync="dialogFormVisible"
    >
      <el-form ref="editForm" :model="editForm" :rules="formRules" style="margin: 20px;" label-width="100px">
        <el-form-item label="工单编号" prop="ticket_number">
          <el-input v-model="editForm.ticket_number" autocomplete="off" :disabled="true" />
        </el-form-item>
        <el-form-item label="严重程度" prop="severity">
          <el-select v-model="editForm.severity" autocomplete="off" clearable>
            <el-option label="P0" value="P0" />
            <el-option label="P1" value="P1" />
            <el-option label="P2" value="P2" />
            <el-option label="P3" value="P3" />
          </el-select>
        </el-form-item>
        <el-form-item label="工单详情" prop="content">
          <el-input v-model="editForm.content" autocomplete="off" :disabled="true" :show-overflow-tooltip="true" />
        </el-form-item>
        <el-form-item label="问题原因" prop="reason">
          <el-input v-model="editForm.reason" autocomplete="off" :show-overflow-tooltip="true" />
        </el-form-item>
        <el-form-item label="解决方案" prop="solution">
          <el-input v-model="editForm.solution" autocomplete="off" :show-overflow-tooltip="true" clearable />
        </el-form-item>
        <el-form-item label="是否是BUG" prop="bug_state">
          <el-select v-model="editForm.bug_state" placeholder="请选择活动区域" @change="BugShow">
            <el-option label="是" value="是" />
            <el-option label="否" value="否" />
            <el-option label="老系统" value="老系统" />
          </el-select>
        </el-form-item>
        <el-form-item label="分类" prop="category">
          <el-select v-model="editForm.category" placeholder="请选择活动区域">
            <el-option label="穿透" value="穿透" />
            <el-option label="运维问题" value="运维问题" />
            <el-option label="需求" value="需求" />
            <el-option label="使用配置" value="使用配置" />
          </el-select>
        </el-form-item>
        <template v-if="bugShow">
          <el-form-item label="BUG原因" prop="bug_reason">
            <el-select v-model="editForm.bug_reason" placeholder="请选择活动区域" clearable>
              <el-option label="漏测" value="漏测" />
              <el-option label="影响范围" value="影响范围" />
              <el-option label="夹带" value="夹带" />
              <el-option label="无法模拟场景" value="无法模拟场景" />
              <el-option label="环境问题" value="环境问题" />
              <el-option label="人为操作" value="人为操作" />
              <el-option label="已知BUG" value="已知BUG" />
              <el-option label="第三方" value="第三方" />
            </el-select>
          </el-form-item>
          <el-form-item label="归属架构域" prop="domain">
            <el-select v-model="editForm.domain" placeholder="请选择活动区域" clearable>
              <el-option label="CRM" value="CRM" />
              <el-option label="营销" value="营销" />
              <el-option label="商城" value="商城" />
              <el-option label="客服" value="客服" />
              <el-option label="运营" value="运营" />
              <el-option label="私有云" value="私有云" />
              <el-option label="业务中台" value="业务中台" />
              <el-option label="数据中台" value="数据中台" />
              <el-option label="技术中台" value="技术中台" />
            </el-select>
          </el-form-item>
          <el-form-item label="技术归属" prop="technical">
            <el-select v-model="editForm.technical" placeholder="请选择活动区域" clearable>
              <el-option label="前端" value="前端" />
              <el-option label="后端" value="后端" />
              <el-option label="性能" value="性能" />
              <el-option label="产品设计" value="产品设计" />
            </el-select>
          </el-form-item>
          <el-form-item label="是否彻底解决" prop="domain">
            <el-select v-model="editForm.thorough" placeholder="请选择活动区域" clearable>
              <el-option label="是" :value="true" />
              <el-option label="否" :value="false" />
            </el-select>
          </el-form-item>
          <el-form-item label="功能模块" prop="module">
            <el-input v-model="editForm.module" autocomplete="off" clearable />
          </el-form-item>
        </template>
      </el-form>
      <div class="drawer__footer" style="padding-left: 20px">
        <el-button style="width: 100px" @click="$refs.drawer.closeDrawer()">取消</el-button>
        <el-button
          style="width: 100px"
          type="primary"
          :loading="buttonLoading"
          :disabled="buttonDisable"
          @click.native="updateForm"
        >{{ loading ? '提交中 ...' : '更新' }}
        </el-button>
      </div>
    </el-drawer>
  </div>
</template>

<style>
.el-drawer__body {
  overflow: auto;
}

.main-container {
  height: 100%;
}
</style>
<script>
import { getOrderList, updateOrder, OrderExport } from '@/api/orders'
import { Message } from 'element-ui'
// import XLSX from 'xlsx'
export default {
  filters: {
    statusFilter(status) {
      const statusMap = {
        published: 'success',
        draft: 'gray',
        deleted: 'danger'
      }
      return statusMap[status]
    }
  },
  data() {
    return {
      getBottonLoading: false,
      exportBottonLoading: false,
      dialogFormVisible: false,
      buttonLoading: false,
      buttonDisable: false,
      // 显示或隐藏分类
      bugShow: false,
      // 表单提交验证信息
      formRules: {
        category: [{ required: true, message: '亲，必填！', trigger: 'blur' }],
        reason: [{ required: true, message: '亲，必填！', trigger: 'blur' }],
        team: [{ required: true, message: '亲，必填！', trigger: 'blur' }]
      },
      // 筛选条件
      selectForm: {
        ticketNumber: null,
        bug_state: null,
        category: null,
        bug_reason: null,
        thorough: null,
        domain: null,
        domain__contains: null,
        module: null
      },
      // 更新表单
      editForm: {
        index: 0,
        severity: 0,
        ticket_number: null,
        content: null,
        reason: null,
        solution: null,
        bug_state: null,
        category: null,
        bug_reason: null,
        domain: null,
        module: null,
        thorough: null,
        technical: null
      },
      // 表格数据
      list: {
        results: []
      },
      listLoading: true,
      // 日期数组
      datevalue: [],
      tableHeight: '',
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
      },
      currentPage: 1,
      // 是否是BUG筛选列表
      bugStateFilterList: [
        { text: '是', value: '是' },
        { text: '否', value: '否' },
        { text: '老系统', value: '老系统' }
      ],
      // 分类筛选列表
      categoryFilterList: [
        { text: '穿透', value: '穿透' },
        { text: '运维问题', value: '运维问题' },
        { text: '需求', value: '需求' },
        { text: '产品设计', value: '产品设计' }
      ],
      // 技术维度筛选列表
      technicalFilterList: [
        { text: '前端', value: '前端' },
        { text: '后端', value: '后端' },
        { text: '性能', value: '性能' },
        { text: '产品设计', value: '产品设计' }
      ],
      // 漏测原因筛选列表
      bugReasonFilterList: [
        { text: '漏测', value: '漏测' },
        { text: '影响范围', value: '影响范围' },
        { text: '夹带', value: '夹带' },
        { text: '无法模拟场景', value: '无法模拟场景' },
        { text: '环境问题', value: '环境问题' },
        { text: '人为操作', value: '人为操作' },
        { text: '已知BUG', value: '已知BUG' },
        { text: '第三方', value: '第三方' }
      ],
      // 归属筛选列表
      domainFilterList: [
        { text: 'CRM', value: 'CRM' },
        { text: '营销', value: '营销' },
        { text: '商城', value: '商城' },
        { text: '客服', value: '客服' },
        { text: '运营', value: '运营' },
        { text: '私有云', value: '私有云' },
        { text: '业务中台', value: '业务中台' },
        { text: '数据中台', value: '数据中台' },
        { text: '技术中台', value: '技术中台' }
      ]
    }
  },
  created() {
    const { start, end, domain, bug_reason, bug_state, technical } = this.$route.query
    // console.log(bug_state)
    if (start) {
      this.datevalue = [start, end]
    }
    this.selectForm.domain = domain
    this.selectForm.bug_reason = bug_reason
    this.selectForm.bug_state = bug_state
    this.selectForm.technical = technical
  },
  mounted() {
    this.fetchData()
    this.tableHeight = window.innerHeight * 0.75
    // 监听浏览器窗口大小变化改变高度
    window.onresize = () => {
      this.$nextTick(() => {
        this.tableHeight = window.innerHeight * 0.75
      })
    }
  },
  methods: {
    // 下拉框变化
    handleChangeFlag(type) {
      console.log(type)
      this.changeFlag = type
    },
    // 显示或隐藏bug编辑列表
    BugShow() {
      this.bugShow = this.editForm.bug_state === '是'
    },
    // 获取全量列表接口
    fetchData() {
      console.log('fetchData')
      this.listLoading = true
      this.currentPage = 1
      const firstParams = Object.assign({
        start: this.datevalue[0],
        end: this.datevalue[1]
      }, this.selectForm)
      getOrderList(firstParams).then(response => {
        this.list = response.data
        this.listLoading = false
      }).catch(err => {
        console.log(err)
      })
    },
    // 表格筛选
    handleFilterChange() {
      this.listLoading = true
      // 填充参数
      this.selectForm.p = this.currentPage
      this.selectForm.start = this.datevalue[0]
      this.selectForm.end = this.datevalue[1]
      // if (this.selectForm.ticketNumber != null) {
      //   this.selectForm.ticketNumber = this.selectForm.ticketNumber
      // }
      // if (this.selectForm.domain != null) {
      //   if (this.selectForm.domain === '') {
      //     this.selectForm.domain = null
      //   } else {
      //     this.selectForm.domain = this.selectForm.domain
      //   }
      // }
      // if (this.selectForm.bug_state != null) {
      //   if (this.selectForm.bug_state === '') {
      //     this.selectForm.bug_state = null
      //   } else {
      //     this.selectForm.bug_state = this.selectForm.bug_state
      //   }
      // }
      // if (this.selectForm.bug_reason != null) {
      //   if (this.selectForm.bug_reason === '') {
      //     this.selectForm.bug_reason = null
      //   } else {
      //     this.selectForm.bug_reason = this.selectForm.bug_reason
      //   }
      // }
      // if (this.selectForm.category != null) {
      //   if (this.selectForm.category === '') {
      //     this.selectForm.category = null
      //   } else {
      //     this.selectForm.category = this.selectForm.category
      //   }
      // }
      // if (this.selectForm.technical != null) {
      //   if (this.selectForm.technical === '') {
      //     this.selectForm.technical = null
      //   } else {
      //     this.selectForm.technical = this.selectForm.technical
      //   }
      // }
      this.currentPage = 1
      getOrderList(this.selectForm).then(response => {
        this.list = response.data
        this.listLoading = false
      })
    },
    // 导出筛选内容
    orderExport() {
      this.exportBottonLoading = true
      delete this.selectForm.p
      OrderExport(this.selectForm).then(response => {
        this.exportBottonLoading = false
        this.exportData(response)
        // console.log(response)
      }).catch(err => {
        console.log(err)
      })
    },
    // 解析导出数据逻辑
    exportData(response) {
      console.log(response)
      const a = document.createElement('a') // 创建a标签
      a.style.display = 'none'
      a.href = response
      // a.download = 'export.xlsx'
      a.click()
      a.parentNode.removeChild(a)
      // 不创建a标签直接下载
      // window.open(href)
    },
    // 筛选清空
    filterClear() {
      this.selectForm.ticketNumber = null
      this.selectForm.domain = null
      this.selectForm.technical = null
      this.selectForm.category = null
      this.selectForm.bug_state = null
      this.selectForm.bug_reason = null
      this.datevalue = []
      this.currentPage = 1
      this.fetchData()
    },
    // 拉取新数据
    getNewData() {
      this.getBottonLoading = true
      this.listLoading = true
      console.log('getNewData')
      getOrderList(null, 'post').then(response => {
        this.getBottonLoading = false
        this.fetchData()
        console.log({ response })
        switch (response.code) {
          case 2:
            Message.success({
              message: '恭喜你，更新成功',
              duration: 2 * 1000
            })
            break
          case 0:
            Message.error({
              message: '更新失败，原因么有深究',
              duration: 5 * 1000
            })
            break
        }
      })
      this.listLoading = false
    },
    // 改变page触发事件
    CurrentChange(val) {
      this.listLoading = true
      // 填充参数
      this.selectForm.p = val
      let pageParams
      if (this.datevalue) {
        pageParams = Object.assign({
          start: this.datevalue[0],
          end: this.datevalue[1]
        }, this.selectForm)
      } else {
        pageParams = this.selectForm
      }
      getOrderList(pageParams).then(
        response => {
          this.list = response.data
          this.listLoading = false
        }
      )
    },
    // 上一页
    pervious() {
      this.currentPage = this.list.page - 1
    },
    // 下一页
    next() {
      this.currentPage = this.list.page + 1
    },
    // 日期触发事件
    dateChange() {
      // console.log('dateClear') // for debug
      if (this.datevalue != null) {
        // this.listLoading = true
        this.selectForm.start = this.datevalue[0]
        this.selectForm.end = this.datevalue[1]
        this.selectForm.p = this.currentPage
      } else {
        this.datevalue = []
      }
    },
    // 打开编辑窗口
    openDialog(index, row) {
      this.dialogFormVisible = true // 打开窗口
      this.editForm = Object.assign({}, row) // 将数据传入当前dialog
      this.editForm.index = index // 传index
    },
    // 提交表单数据
    updateForm() {
      this.$refs.editForm.validate((valid) => {
        if (valid) {
          this.buttonLoading = true
          this.buttonDisable = true
          let data
          if (this.bugShow) {
            data = {
              bug_state: this.editForm.bug_state,
              category: this.editForm.category,
              severity: this.editForm.severity,
              reason: this.editForm.reason,
              solution: this.editForm.solution,
              bug_reason: this.editForm.bug_reason,
              technical: this.editForm.technical,
              domain: this.editForm.domain,
              module: this.editForm.module,
              thorough: this.editForm.thorough
            }
          } else {
            data = {
              bug_state: this.editForm.bug_state,
              category: this.editForm.category,
              reason: this.editForm.reason,
              solution: this.editForm.solution,
              bug_reason: null,
              technical: null,
              domain: this.editForm.domain,
              module: null,
              thorough: null
            }
          }
          updateOrder(this.editForm.ticket_number, data).then(response => {
            this.listLoading = true
            this.selectForm.p = this.list.page
            // console.log(this.selectForm)
            if (this.datevalue) {
              var updateParams = Object.assign({
                start: this.datevalue[0],
                end: this.datevalue[1]
              }, this.selectForm)
            }
            getOrderList(updateParams).then(response => {
              const { code, data, errors } = response
              if (code === 2) {
                this.list = data
                this.$message.success({
                  message: '修改成功',
                  center: true
                })
              } else if (code === 0) {
                this.$message.error({
                  message: '修改失败' + errors,
                  center: true
                })
              }
              this.listLoading = false
              this.dialogFormVisible = false
            })
          })
          this.buttonLoading = false
          this.buttonDisable = false
        }
      })
    }
  }
}
</script>
