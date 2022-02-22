<template>
  <div class="main">
    <el-divider class="blue-line" direction="vertical" />
    <span slot="title" style="font-weight:bold;font-size:14px;color:#2C8DF4;">任务列表</span>

    <!--顶部工具条-->
    <el-col :span="24" class="toolbar" style="padding-bottom: 0;padding-top: 10px">
      <el-form ref="filters" :inline="true" :v-model="filters" :size="themeSize" @submit.native.prevent>
        <el-form-item style="width: 150px">
          <el-select v-model="filters.id" placeholder="任务ID" value-key="id" multiple filterable allow-create clearable @keyup.enter.native="fetchData">
            <span slot="empty" class="el-select-dropdown__empty">请输入任务ID</span>
            <el-option v-for="item in []" :key="item.value" :label="item.label" :value="item.value.replace(/[^\d]/g,'')" />
          </el-select>
        </el-form-item>
        <el-form-item style="width: 150px">
          <el-input v-model="filters.name" placeholder="任务名称" clearable @keyup.enter.native="fetchData" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="fetchData">查询</el-button>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleAdd">新增任务</el-button>
        </el-form-item>
        <el-form-item>
          <el-button type="default" @click.native="filterClear">重置</el-button>
        </el-form-item>
      </el-form>
    </el-col>

    <!--列表-->
    <el-table
      ref="suiteTable"
      v-loading="tableConfig.isLoading"
      :data="dataList"
      element-loading-text="Loading"
      border
      fit
      highlight-current-row
      :size="themeSize"
      :height="tableConfig.height"
      style="width: 100%"
      @cell-mouse-enter="cellMouseEnter"
      @cell-mouse-leave="cellMouseLeave"
      @selection-change="selsChange"
    >
      <el-table-column fixed type="selection" />
      <el-table-column prop="id" label="ID" sortable width="70" />
      <el-table-column prop="name" label="任务名称" sortable show-overflow-tooltip width="150" />
      <el-table-column prop="cron" label="cron" sortable show-overflow-tooltip width="150" />
      <el-table-column prop="priority" label="优先级" show-overflow-tooltip width="70">
        <template slot-scope="scope">
          <el-tag :size="themeSize">P{{ scope.row.priority }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="status" label="状态" sortable show-overflow-tooltip width="100">
        <template slot-scope="scope">
          <el-tag :size="themeSize" :type="status_display[scope.row.status].type">{{ status_display[scope.row.status].display }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="next_run" label="下次执行" sortable show-overflow-tooltip width="200" />
      <el-table-column prop="test_env.name" label="执行环境" sortable show-overflow-tooltip width="150">
        <template slot-scope="scope">
          {{ scope.row.test_env.name }} ({{ scope.row.test_env.description }})
        </template>
      </el-table-column>
      <el-table-column prop="test_validate.name" label="校验规则" sortable show-overflow-tooltip width="150">
        <template slot-scope="scope">
          {{ scope.row.test_validate.name }} ({{ scope.row.test_validate.description }})
        </template>
      </el-table-column>
      <el-table-column prop="test_level" label="类型" sortable show-overflow-tooltip width="150" />
      <el-table-column prop="test_filters" label="筛选器" sortable show-overflow-tooltip width="100">
        <template slot-scope="scope">
          <el-popover
            placement="right"
            width="600"
            trigger="click"
          >
            <el-card class="box-card" shadow="never">
              <div slot="header" class="clearfix">筛选列表 ({{ scope.row.name }}: {{ scope.row.test_level }})</div>
              <el-table :data="dictConfigToArray(scope.row.test_filters)" style="width: 100%" :size="themeSize">
                <el-table-column label="名称" prop="key" sortable show-overflow-tooltip width="200" />
                <el-table-column label="值" prop="value" sortable show-overflow-tooltip />
              </el-table>
            </el-card>
            <el-button slot="reference" :size="themeSize" type="text">详情</el-button>
          </el-popover>
        </template>
      </el-table-column>
      <el-table-column prop="job_state" label="任务详情" sortable show-overflow-tooltip width="100">
        <template slot-scope="scope">
          <el-popover
            placement="right"
            width="600"
            trigger="click"
          >
            <el-card class="box-card" shadow="never">
              <div slot="header" class="clearfix">任务详情 ({{ scope.row.name }})</div>
              <el-table :data="dictConfigToArray(scope.row.job_state)" style="width: 100%" :size="themeSize">
                <el-table-column label="名称" prop="key" sortable show-overflow-tooltip width="150" />
                <el-table-column label="值" prop="value" sortable show-overflow-tooltip />
              </el-table>
            </el-card>
            <el-button slot="reference" :size="themeSize" type="text">详情</el-button>
          </el-popover>
        </template>
      </el-table-column>
      <el-table-column fixed="right" label="操作" width="180">
        <template slot-scope="scope">
          <!-- v-show="currentRow === scope.row" -->
          <el-row>
            <el-button type="info" icon="el-icon-edit" circle :size="themeSize" title="编辑任务" @click="handleEdit(scope.$index, scope.row)" />
            <el-button type="danger" icon="el-icon-delete" circle :size="themeSize" title="删除任务" @click="handleDelTestTask(scope.$index, scope.row)" />
            <el-button type="warning" icon="el-icon-s-flag" circle :size="themeSize" :title="scope.row.status===false?'启用':'禁用'" @click="handleChangeStatus(scope.$index, scope.row)" />
          </el-row>
        </template>
      </el-table-column>
    </el-table>

    <!--底部工具条-->
    <el-row class="toolbar">
      <!--分页-->
      <el-col class="pagination-toolbar" :span="24">
        <el-pagination
          background
          style="float:right;"
          :current-page.sync="page"
          layout="total, sizes, prev, pager, next, jumper"
          :page-size="page_size"
          :page-sizes="[20, 50, 100, 1000]"
          :total="total"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </el-col>
      <!--批量处理-->
      <el-col v-show="sels.length>0" class="bulk-toolbar" :span="24">
        <span style="font-weight:bold;font-size:14px;color:#2C8DF4;">批量处理: </span>
        <el-button type="warning" plain :disabled="sels.length===0" :size="themeSize" @click="bulkEnable">启用</el-button>
        <el-button type="warning" plain :disabled="sels.length===0" :size="themeSize" @click="bulkDisable">禁用</el-button>
        <el-button type="danger" plain :disabled="sels.length===0" :size="themeSize" @click="bulkRemove">删除</el-button>
        <span style="font-size: 14px; padding-right: 30px;"> 选中{{ sels.length }}条</span>
        <el-button type="text" plain :size="themeSize" @click="sels = []">取消</el-button>
      </el-col>
    </el-row>

    <!--编辑界面-->
    <el-drawer
      title="编辑"
      :with-header="true"
      :wrapper-closable="false"
      :visible.sync="editFormVisible"
      direction="rtl"
      size="50%"
    >
      <div class="demo-drawer__content">
        <el-form ref="editForm" :size="themeSize" :model="editForm" :rules="editFormRules" label-width="160px">
          <!-- 基本信息 -->
          <el-collapse value="1">
            <el-collapse-item name="1">
              <span slot="title" style="font-weight:bold;font-size:14px;color:#2C8DF4;">基本信息</span>
              <el-form-item label="名称" prop="name">
                <el-input v-model.trim="editForm.name" auto-complete="off" />
              </el-form-item>
              <el-form-item label="cron" prop="cron">
                <el-input v-model.trim="editForm.cron" />
              </el-form-item>
              <el-form-item label="执行环境" prop="test_env">
                <el-select v-model="editForm.test_env" value-key="id" placeholder="请选择环境配置" style="width:100%" clearable>
                  <el-option v-for="item in globalEnv_options" :key="item.id" :label="'环境配置:'+item.name" :value="item" />
                </el-select>
              </el-form-item>
              <el-form-item label="校验规则" prop="test_validate">
                <el-select v-model="editForm.test_validate" value-key="id" placeholder="请选择校验规则" style="width:100%" clearable>
                  <el-option v-for="item in globalValidate_options" :key="item.id" :label="item.name" :value="item" />
                </el-select>
              </el-form-item>
              <el-form-item label="优先级" prop="priority">
                <el-input-number v-model="editForm.priority" controls-position="right" :min="0" :max="3" />
              </el-form-item>
            </el-collapse-item>
          </el-collapse>

          <!-- 数据筛选 -->
          <el-collapse value="1">
            <el-collapse-item name="1">
              <span slot="title" style="font-weight:bold;font-size:14px;color:#2C8DF4;">数据筛选</span>
              <el-form-item label="测试级别" prop="test_level">
                <el-select v-model="editForm.test_level" value-key="id" placeholder="请选择level" style="width:100%" clearable>
                  <el-option v-for="(item, index) in test_level_options" :key="index" :label="item" :value="item" />
                </el-select>
              </el-form-item>
              <el-form-item label="ID" prop="test_filters.id">
                <el-select v-model="editForm.test_filters.id" placeholder="ID筛选" value-key="id" style="width: 100%" multiple filterable allow-create clearable>
                  <span slot="empty" class="el-select-dropdown__empty">请输入ID</span>
                  <el-option v-for="item in []" :key="item.value" :label="item.label" :value="item.value.replace(/[^\d]/g,'')" />
                </el-select>
              </el-form-item>
              <el-form-item label="名称" prop="test_filters.name">
                <el-input v-model="editForm.test_filters.name" placeholder="名称筛选" clearable />
              </el-form-item>
              <div v-show="editForm.test_level==='test_suite'">
                <el-form-item label="所属部门" prop="department">
                  <el-select v-model="editForm.test_filters.department__id" value-key="id" placeholder="所属部门" style="width: 100%;" multiple filterable clearable>
                    <el-option v-for="item in department_options" :key="item.id" :label="item.name" :value="item.id" />
                  </el-select>
                </el-form-item>
              </div>
            </el-collapse-item>
          </el-collapse>

        </el-form>
        <!-- 取消、提交 -->
        <div class="demo-drawer__footer">
          <el-button :size="themeSize" @click.native="editFormVisible = false; editLoading = false">取消</el-button>
          <el-button :size="themeSize" type="primary" :loading="editLoading" @click.native="editSubmit">提交</el-button>
        </div>
      </div>
    </el-drawer>

    <!--新增界面-->
    <el-drawer
      title="新增"
      :with-header="true"
      :wrapper-closable="false"
      :visible.sync="addFormVisible"
      direction="rtl"
      size="50%"
    >
      <div class="demo-drawer__content">
        <el-form ref="addForm" :size="themeSize" :model="addForm" label-width="160px" :rules="addFormRules">
          <!-- 基本信息 -->
          <el-collapse value="1">
            <el-collapse-item name="1">
              <span slot="title" style="font-weight:bold;font-size:14px;color:#2C8DF4;">基本信息</span>
              <el-form-item label="名称" prop="name">
                <el-input v-model.trim="addForm.name" auto-complete="off" />
              </el-form-item>
              <el-form-item label="cron" prop="cron">
                <el-input v-model="addForm.cron" />
              </el-form-item>
              <el-form-item label="执行环境" prop="test_env">
                <el-select v-model="addForm.test_env" value-key="id" placeholder="请选择环境配置" style="width:100%" clearable>
                  <el-option v-for="item in globalEnv_options" :key="item.id" :label="'环境配置:'+item.name" :value="item" />
                </el-select>
              </el-form-item>
              <el-form-item label="校验规则" prop="test_validate">
                <el-select v-model="addForm.test_validate" value-key="id" placeholder="请选择校验规则" style="width:100%" clearable>
                  <el-option v-for="item in globalValidate_options" :key="item.id" :label="item.name" :value="item" />
                </el-select>
              </el-form-item>
              <el-form-item label="优先级" prop="priority">
                <el-input-number v-model="addForm.priority" controls-position="right" :min="0" :max="3" />
              </el-form-item>
            </el-collapse-item>
          </el-collapse>

          <!-- 数据筛选 -->
          <el-collapse value="1">
            <el-collapse-item name="1">
              <span slot="title" style="font-weight:bold;font-size:14px;color:#2C8DF4;">数据筛选</span>
              <el-form-item label="测试级别" prop="test_level">
                <el-select v-model="addForm.test_level" value-key="id" placeholder="请选择level" style="width:100%" clearable>
                  <el-option v-for="(item, index) in test_level_options" :key="index" :label="item" :value="item" />
                </el-select>
              </el-form-item>
              <el-form-item label="ID" prop="test_filters.id">
                <el-select v-model="addForm.test_filters.id" placeholder="ID筛选" value-key="id" style="width: 100%" multiple filterable allow-create clearable>
                  <span slot="empty" class="el-select-dropdown__empty">请输入ID</span>
                  <el-option v-for="item in []" :key="item.value" :label="item.label" :value="item.value.replace(/[^\d]/g,'')" />
                </el-select>
              </el-form-item>
              <el-form-item label="名称" prop="test_filters.name">
                <el-input v-model="addForm.test_filters.name" placeholder="名称筛选" clearable />
              </el-form-item>
              <div v-show="addForm.test_level==='test_suite'">
                <el-form-item label="所属部门" prop="department">
                  <el-select v-model="addForm.test_filters.department__id" value-key="id" placeholder="所属部门" style="width: 100%;" multiple filterable clearable>
                    <el-option v-for="item in department_options" :key="item.id" :label="item.name" :value="item.id" />
                  </el-select>
                </el-form-item>
              </div>
            </el-collapse-item>
          </el-collapse>
        </el-form>
        <!-- 取消、提交 -->
        <div class="demo-drawer__footer">
          <el-button :size="themeSize" @click.native="addFormVisible = false; addLoading = false">取消</el-button>
          <el-button :size="themeSize" type="primary" :loading="addLoading" @click.native="addSubmit">提交</el-button>
        </div>
      </div>
    </el-drawer>
  </div>
</template>

<script>
import get_base_data from '@/api/apiTest/get_base_data'
import { getTestTaskList, addTestTask, updateTestTask } from '@/api/apiTest/test_task'

export default {
  name: 'TaskSchedule',
  mixins: [get_base_data],
  data() {
    return {
      themeSize: this.$store.state.settings.themeSize,
      tableConfig: {
        isLoading: false,
        height: window.innerHeight - 225 // 下面剩余多少空白部分（即最下面距离底部有多少距离）
      },
      editLoading: false,
      addLoading: false,
      delLoading: false,

      total: 0,
      page: 1,
      page_size: 20,
      dataList: [],
      filters: {
        id: [],
        name: ''
      },
      sels: [], // 用例列表选中列
      currentRow: '', // 用例列表当前行
      status_display: [
        { type: 'info', display: '等待中' },
        { type: 'success', display: '运行中' },
        { type: 'success', display: '已完成' },
        { type: 'warning', display: '暂停' },
        { type: 'danger', display: '无效' },
        { type: 'danger', display: '异常' }
      ],
      test_level_options: [
        'test_suite',
        'test_case',
        'test_step'
      ],

      editFormVisible: false, // 编辑界面是否显示
      // 编辑界面数据规则
      editFormRules: {
        name: [
          { required: true, message: '请输入名称', trigger: 'blur' },
          { min: 1, max: 50, message: '长度在 1 到 50 个字符', trigger: 'blur' }
        ],
        cron: [
          { required: true, message: '请选配置cron', trigger: 'blur' }
        ],
        test_env: [
          { required: true, message: '请选择环境配置', trigger: 'blur' }
        ],
        test_validate: [
          { required: true, message: '请选择校验规则', trigger: 'blur' }
        ],
        test_level: [
          { required: true, message: '请选择测试level', trigger: 'blur' }
        ]
      },
      // 编辑界面数据
      editForm: {
        name: '',
        priority: 0,
        cron: '',
        test_env: null,
        test_validate: null,
        test_level: 'test_suite',
        test_filters: {
          id: null,
          name: null,
          department: null,
          department__id: null
        }
      },

      addFormVisible: false, // 新增界面是否显示
      // 新增界面数据规则
      addFormRules: {
        name: [
          { required: true, message: '请输入名称', trigger: 'blur' },
          { min: 1, max: 50, message: '长度在 1 到 50 个字符', trigger: 'blur' }
        ],
        cron: [
          { required: true, message: '请选配置cron', trigger: 'blur' }
        ],
        test_env: [
          { required: true, message: '请选择环境配置', trigger: 'blur' }
        ],
        test_validate: [
          { required: true, message: '请选择校验规则', trigger: 'blur' }
        ],
        test_level: [
          { required: true, message: '请选择测试level', trigger: 'blur' }
        ]
      },
      // 新增界面数据
      addForm: {
        name: '',
        priority: 0,
        cron: '',
        test_env: null,
        test_validate: null,
        test_level: 'test_suite',
        test_filters: {
          id: null,
          name: null,
          department: null,
          department__id: null
        }
      }
    }
  },
  mounted() {
    this.fetchData()
  },
  methods: {
    filterClear() {
      this.filters.id = []
      this.filters.name = ''
    },
    fetchData() {
      const params = {
        page: this.page,
        page_size: this.page_size,
        id_in: this.filters.id ? this.filters.id.join(',') : null,
        name: this.filters.name ? this.filters.name : null
      }
      this.tableConfig.isLoading = true
      getTestTaskList(params).then(response => {
        this.dataList = response.data.list
        this.total = response.data.count
        this.tableConfig.isLoading = false
      })
    },
    // 选中用例列表行
    selsChange: function(sels) {
      this.sels = sels
    },
    cellMouseEnter(row) {
      this.currentRow = row
    },
    cellMouseLeave(row) {
      this.currentRow = ''
    },

    // 刷新每页数据条数
    handleSizeChange(val) {
      console.log(`每页 ${val} 条`)
      this.page_size = val
      this.fetchData()
    },
    // 刷新指定页数据
    handleCurrentChange(val) {
      console.log(`当前页: ${val}`)
      this.page = val
      this.fetchData()
    },
    // job_state 字典key:valve 转Array[{key:key, value:value}]
    dictConfigToArray: function(src) {
      const dst = []
      if (!src) {
        return dst
      }
      for (const k in src) {
        const v = src[k]
        dst.push({ key: k, value: v })
      }
      return dst
    },

    handleAdd() {
      this.getEnv()
      this.getValidate()
      this.getDepartment()
      this.addFormVisible = true
    },
    // 显示编辑界面
    handleEdit: function(index, row) {
      this.getEnv()
      this.getValidate()
      this.getDepartment()
      this.editFormVisible = true
      this.editForm = Object.assign({}, row)
    },
    handleDelTestTask() {
      this.$message.warning('TODO')
    },
    handleChangeStatus() {
      this.$message.warning('TODO')
    },

    addSubmit() {
      this.$refs.addForm.validate((valid) => {
        if (valid) {
          this.$confirm('确认提交吗？', '提示', {}).then(() => {
            // NProgress.start();
            const test_filters = {}
            for (const k in this.addForm.test_filters) {
              const v = this.addForm.test_filters[k]
              if (v === null) {
                //
              } else {
                test_filters[k] = v
              }
            }
            const data = {
              name: this.addForm.name,
              priority: this.addForm.priority,
              cron: this.addForm.cron,
              test_env: this.addForm.test_env.id,
              test_validate: this.addForm.test_validate.id,
              test_level: this.addForm.test_level,
              test_filters: test_filters
            }
            this.editLoading = true
            addTestTask(data).then(_data => {
              const { msg, code } = _data
              this.editLoading = false
              if (code === 2) {
                this.$message({
                  message: '添加成功',
                  center: true,
                  type: 'success'
                })
                this.$refs['addForm'].resetFields()
                this.addFormVisible = false
                this.fetchData()
              } else if (code === 400) { // 参数错误或数据库不允许的输入
                this.$message.error({
                  message: msg,
                  center: true
                })
              } else {
                this.$message.error({
                  message: msg,
                  center: true
                })
                this.addFormVisible = false
                this.fetchData()
              }
            })
          })
        }
      })
    },
    editSubmit() {
      this.$refs.editForm.validate((valid) => {
        if (valid) {
          this.$confirm('确认提交吗？', '提示', {}).then(() => {
            // NProgress.start();
            const test_filters = {}
            for (const k in this.editForm.test_filters) {
              const v = this.editForm.test_filters[k]
              if (v === null) {
                //
              } else {
                test_filters[k] = v
              }
            }
            const params = {
              name: this.editForm.name,
              priority: this.editForm.priority,
              cron: this.editForm.cron,
              test_env: this.editForm.test_env.id,
              test_validate: this.editForm.test_validate.id,
              test_level: this.editForm.test_level,
              test_filters: test_filters
            }
            this.editLoading = true
            updateTestTask(this.editForm.id, params).then(_data => {
              const { msg, code } = _data
              this.editLoading = false
              if (code === 2) {
                this.$message({
                  message: '修改成功',
                  center: true,
                  type: 'success'
                })
                this.$refs['editForm'].resetFields()
                this.editFormVisible = false
                this.fetchData()
              } else if (code === 400) { // 参数错误或数据库不允许的输入
                this.$message.error({
                  message: msg,
                  center: true
                })
              } else {
                this.$message.error({
                  message: msg,
                  center: true
                })
                this.editFormVisible = false
                this.fetchData()
              }
            })
          })
        }
      })
    },

    bulkEnable() {
      this.$message.warning('TODO')
    },
    bulkDisable() {
      this.$message.warning('TODO')
    },
    bulkRemove() {
      this.$message.warning('TODO')
    }
  }
}
</script>

<style lang="scss" scoped>
  ::v-deep .el-drawer__body {
      overflow: auto;
    }
  ::v-deep .demo-drawer__content {
    margin-bottom: 2px;
    padding: 10px 20px 20px;
    overflow: auto;
  }
  ::v-deep .demo-drawer__footer{
    width: 100%;
    position: absolute;
    bottom: 0;
    left: 0;
    border-top: 1px solid #e8e8e8;
    padding: 10px 16px;
    text-align: center;
    background-color: white;
  }
</style>
