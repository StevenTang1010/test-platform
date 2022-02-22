<template>
  <div class="main">
    <el-divider class="blue-line" direction="vertical" />
    <span slot="title" style="font-weight:bold;font-size:14px;color:#2C8DF4;">用例集列表</span>

    <!--顶部工具条-->
    <el-col :span="24" class="toolbar" style="padding-bottom: 0;padding-top: 10px">
      <el-form ref="filters" :inline="true" :v-model="filters" :size="themeSize" @submit.native.prevent>
        <el-form-item style="width: 150px">
          <el-select v-model="filters.id" placeholder="用例集ID" value-key="id" multiple filterable allow-create clearable @keyup.enter.native="fetchData">
            <span slot="empty" class="el-select-dropdown__empty">请输入用例集ID</span>
            <el-option v-for="item in []" :key="item.value" :label="item.label" :value="item.value.replace(/[^\d]/g,'')" />
          </el-select>
        </el-form-item>
        <el-form-item style="width: 150px">
          <el-input v-model="filters.name" placeholder="用例集名称" clearable @keyup.enter.native="fetchData" />
        </el-form-item>
        <el-form-item v-if="showMoreFilters">
          <el-select v-model="filters.department" value-key="id" multiple placeholder="所属部门" filterable clearable>
            <el-option v-for="item in department_options" :key="item.id" :label="item.name" :value="item" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="fetchData">查询</el-button>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleAddSuite">新增用例集</el-button>
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

      :default-sort="{prop: 'id', order: 'ascending'}"
      @cell-mouse-enter="cellMouseEnter"
      @cell-mouse-leave="cellMouseLeave"
      @selection-change="selsChange"
    >
      <el-table-column fixed type="selection" />
      <el-table-column prop="id" label="ID" sortable width="100" />
      <el-table-column prop="name" label="用例集名称" sortable show-overflow-tooltip width="150">
        <template slot-scope="scope">
          <img v-show="scope.row.status" src="@/assets/icon-yes.svg" alt="">
          <img v-show="!scope.row.status" src="@/assets/icon-no.svg" alt="">
          {{ scope.row.name }}
        </template>
      </el-table-column>
      <el-table-column prop="description" label="用例集描述" sortable show-overflow-tooltip width="200" />
      <el-table-column prop="department.name" label="部门" sortable show-overflow-tooltip width="150" />
      <el-table-column prop="labels" label="标签" show-overflow-tooltip width="200">
        <template slot-scope="scope">
          <el-tag v-for="item in scope.row.labels" :key="item.id" :size="themeSize">{{ item.name }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="setup" label="setup" show-overflow-tooltip width="100">
        <template slot-scope="scope">
          <el-popover
            placement="right"
            width="600"
            trigger="click"
          >
            <el-card class="box-card" shadow="never">
              <div slot="header" class="clearfix">
                setup({{ scope.row.setup.length }})
              </div>
              <el-table :size="themeSize" :data="scope.row.setup">
                <el-table-column prop="id" label="CaseID" sortable min-width="100" />
                <el-table-column prop="name" label="CaseName" sortable min-width="200" />
              </el-table>
            </el-card>
            <span slot="reference" type="text">共{{ scope.row.setup.length }}条</span>
          </el-popover>
        </template>
      </el-table-column>
      <el-table-column prop="setup_class" label="setup_class" show-overflow-tooltip width="100">
        <template slot-scope="scope">
          <el-popover
            placement="right"
            width="600"
            trigger="click"
          >
            <el-card class="box-card" shadow="never">
              <div slot="header" class="clearfix">
                setup_class({{ scope.row.setup_class.length }})
              </div>
              <el-table :size="themeSize" :data="scope.row.setup_class">
                <el-table-column prop="id" label="CaseID" sortable min-width="100" />
                <el-table-column prop="name" label="CaseName" sortable min-width="200" />
              </el-table>
            </el-card>
            <span slot="reference" type="text">共{{ scope.row.setup_class.length }}条</span>
          </el-popover>
        </template>
      </el-table-column>
      <el-table-column prop="teardown" label="teardown" show-overflow-tooltip width="100">
        <template slot-scope="scope">
          <el-popover
            placement="right"
            width="600"
            trigger="click"
          >
            <el-card class="box-card" shadow="never">
              <div slot="header" class="clearfix">
                teardown({{ scope.row.teardown.length }})
              </div>
              <el-table :size="themeSize" :data="scope.row.teardown">
                <el-table-column prop="id" label="CaseID" sortable min-width="100" />
                <el-table-column prop="name" label="CaseName" sortable min-width="200" />
              </el-table>
            </el-card>
            <span slot="reference" type="text">共{{ scope.row.teardown.length }}条</span>
          </el-popover>
        </template>
      </el-table-column>
      <el-table-column prop="teardown_class" label="teardown_class" show-overflow-tooltip width="120">
        <template slot-scope="scope">
          <el-popover
            placement="right"
            width="600"
            trigger="click"
          >
            <el-card class="box-card" shadow="never">
              <div slot="header" class="clearfix">
                teardown_class({{ scope.row.teardown_class.length }})
              </div>
              <el-table :size="themeSize" :data="scope.row.teardown_class">
                <el-table-column prop="id" label="CaseID" sortable min-width="100" />
                <el-table-column prop="name" label="CaseName" sortable min-width="200" />
              </el-table>
            </el-card>
            <span slot="reference" type="text">共{{ scope.row.teardown_class.length }}条</span>
          </el-popover>
        </template>
      </el-table-column>
      <el-table-column fixed="right" label="操作" width="180">
        <template slot-scope="scope">
          <!-- v-show="currentRow === scope.row" -->
          <el-row>
            <el-button type="info" icon="el-icon-edit" circle :size="themeSize" title="编辑用例集" @click="handleEditTestSuite(scope.$index, scope.row)" />
            <el-button :loading="scope.row.runLoading" type="primary" icon="el-icon-caret-right" circle :size="themeSize" title="运行用例" @click="runTest(scope.row)" />
            <el-button type="danger" icon="el-icon-delete" circle :size="themeSize" title="删除用例" @click="handleDelTestSuite(scope.$index, scope.row)" />
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
        <el-button :loading="bulkRunLoading" type="primary" plain :disabled="sels.length===0" :size="themeSize" @click="bulkRunTest">运行</el-button>
        <el-button type="info" plain :disabled="sels.length===0" :size="themeSize" @click="bulkEditFormVisible = true">编辑</el-button>
        <el-button type="warning" plain :disabled="sels.length===0" :size="themeSize" @click="bulkEnable">启用</el-button>
        <el-button type="warning" plain :disabled="sels.length===0" :size="themeSize" @click="bulkDisable">禁用</el-button>
        <el-button type="danger" plain :disabled="sels.length===0" :size="themeSize" @click="bulkRemove">删除</el-button>
        <span style="font-size: 14px; padding-right: 30px;"> 选中{{ sels.length }}条</span>
        <el-button type="text" plain :size="themeSize" @click="sels = []">取消</el-button>
      </el-col>
    </el-row>

    <!--批量编辑 弹窗界面-->
    <el-dialog
      title="批量编辑"
      :visible.sync="bulkEditFormVisible"
      :close-on-click-modal="false"
      :append-to-body="true"
      style="width: 75%; left: 12.5%"
    >
      <el-form ref="bulkEditForm" :model="bulkEditForm" :size="themeSize" label-width="100px">
        <el-form-item label="所属部门" prop="department">
          <el-select v-model="bulkEditForm.department" value-key="id" placeholder="请选择所属部门" style="width:100%" clearable>
            <el-option v-for="item in department_options" :key="item.id" :label="item.name" :value="item.id" />
          </el-select>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button :size="themeSize" @click.native="bulkEditFormVisible = false">取消</el-button>
        <el-button :size="themeSize" type="primary" @click.native="bulkEdit()">确定</el-button>
      </div>
    </el-dialog>

    <!--新增用例集界面-->
    <el-drawer
      title="新增用例集"
      :with-header="true"
      :wrapper-closable="false"
      :visible.sync="addSuiteFormVisible"
      direction="rtl"
      size="50%"
    >
      <!-- 新增用例集 -->
      <div class="demo-drawer__content">
        <el-form ref="addSuiteForm" :size="themeSize" :model="addSuiteForm" label-width="120px" :rules="addSuiteFormRules">
          <el-collapse value="1" @change="handleChange">
            <el-collapse-item name="1">
              <span slot="title" style="font-weight:bold;font-size:14px;color:#2C8DF4;">基本信息</span>
              <el-form-item label="名称" prop="name">
                <el-input v-model="addSuiteForm.name" auto-complete="off" />
              </el-form-item>
              <el-form-item label="SafeName" prop="safe_name">
                <el-input v-model="addSuiteForm.safe_name" auto-complete="off" placeholder="pytest目录名" />
              </el-form-item>
              <el-form-item label="所属部门" prop="department">
                <el-select v-model="addSuiteForm.department" value-key="id" placeholder="请选择所属部门" style="width:100%" clearable>
                  <el-option v-for="item in department_options" :key="item.id" :label="item.name" :value="item" />
                </el-select>
              </el-form-item>
              <el-form-item label="标签">
                <el-select v-model="addSuiteForm.labels" value-key="id" placeholder="标签" multiple clearable style="width: 100%">
                  <el-option-group v-for="group in globalLabel_options" :key="group.label" :label="group.label">
                    <el-option v-for="item in group.options" :key="item.id" :label="item.name" :value="item" />
                  </el-option-group>
                </el-select>
              </el-form-item>
              <el-form-item label="描述" prop="description">
                <el-input v-model="addSuiteForm.description" type="textarea" :rows="2" />
              </el-form-item>

            </el-collapse-item>
          </el-collapse>

          <!-- 全局请求头 -->
          <!--          <global-headers />-->

          <!-- 前置/后置 -->
          <el-collapse value="1" @change="handleChange">
            <el-collapse-item name="1">
              <span slot="title" style="font-weight:bold;font-size:14px;color:#2C8DF4;">前置/后置</span>
              <setup-teardown v-model="addSuiteForm" />
            </el-collapse-item>
          </el-collapse>
        </el-form>
        <!-- 取消、提交 -->
        <div class="demo-drawer__footer">
          <el-button :size="themeSize" @click.native="addSuiteFormVisible = false; addLoading = false">取消</el-button>
          <el-button :size="themeSize" type="primary" :loading="addLoading" @click.native="addSuiteSubmit">提交</el-button>
        </div>
      </div>
    </el-drawer>

    <!--编辑用例集界面-->
    <el-drawer
      title="编辑用例集"
      :with-header="true"
      :wrapper-closable="false"
      :visible.sync="editSuiteFormVisible"
      direction="rtl"
      size="50%"
    >
      <!-- 编辑用例集 -->
      <div class="demo-drawer__content">
        <el-form ref="editSuiteForm" :model="editSuiteForm" label-width="120px" :size="themeSize" :rules="editSuiteFormRules">
          <el-collapse value="编辑用例集" @change="handleChange">
            <el-collapse-item name="编辑用例集">
              <span slot="title" style="font-weight:bold;font-size:14px;color:#2C8DF4;">基本信息</span>
              <el-form-item label="所属部门" prop="department">
                <el-select v-model="editSuiteForm.department" value-key="id" placeholder="请选择" style="width: 100%">
                  <el-option v-for="item in department_options" :key="item.id" :label="item.name" :value="item" />
                </el-select>
              </el-form-item>
              <el-form-item label="用例集名称" prop="name">
                <el-input v-model="editSuiteForm.name" auto-complete="off" />
              </el-form-item>
              <el-form-item label="SafeName" prop="safe_name">
                <el-input v-model="editSuiteForm.safe_name" auto-complete="off" placeholder="pytest目录名" />
              </el-form-item>
              <el-form-item label="标签">
                <el-select v-model="editSuiteForm.labels" value-key="id" placeholder="标签" multiple clearable style="width: 100%">
                  <el-option-group v-for="group in globalLabel_options" :key="group.label" :label="group.label">
                    <el-option v-for="item in group.options" :key="item.id" :label="item.name" :value="item" />
                  </el-option-group>
                </el-select>
              </el-form-item>
              <el-form-item label="描述" prop="description">
                <el-input v-model="editSuiteForm.description" type="textarea" :rows="2" />
              </el-form-item>
            </el-collapse-item>
          </el-collapse>
          <!-- 全局请求头 -->
          <!--          <global-headers />-->

          <!-- 前置/后置 -->
          <el-collapse value="1" @change="handleChange">
            <el-collapse-item name="1">
              <span slot="title" style="font-weight:bold;font-size:14px;color:#2C8DF4;">前置/后置</span>
              <setup-teardown v-model="editSuiteForm" />
            </el-collapse-item>
          </el-collapse>

        </el-form>
        <!-- 取消、提交 -->
        <div class="demo-drawer__footer">
          <el-button :size="themeSize" @click.native="editSuiteFormVisible = false; editLoading = false">取消</el-button>
          <el-button :size="themeSize" type="primary" :loading="editLoading" @click.native="editSuiteSubmit">提交</el-button>
        </div>
      </div>
    </el-drawer>

    <!-- 执行测试-->
    <run-test ref="runTestRef" />
  </div>
</template>

<script>
import { addTestSuite, bulkUpdateTestSuite, getTestSuiteList, updateTestSuite } from '@/api/apiTest/test_suite'
import get_base_data from '@/api/apiTest/get_base_data'
// import GlobalHeaders from '@/views/apiTest/components/GlobalHeaders'
import SetupTeardown from '@/views/apiTest/components/SetupTeardown'
import RunTest from '@/views/apiTest/components/RunTest'

export default {
  name: 'SuiteList',
  components: { SetupTeardown, RunTest },
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
      // delLoading: false,
      // bulkDelLoading: false,
      bulkRunLoading: false, // 批量执行按钮loading
      showMoreFilters: false,
      headerModel: [],

      filters: {
        id: '',
        name: '',
        department: [],
        department__isnull: null
      },
      total: 0,
      page: 1,
      page_size: 20,
      dataList: [],
      sels: [], // 用例集列表选中列

      // 新增
      addSuiteFormVisible: false, // 新增用例集界面是否显示
      // 新增界面数据规则
      addSuiteFormRules: {
        department: [
          { required: true, message: '请选择所属部门', trigger: 'blur' }
        ],
        name: [
          { required: true, message: '请输入名称', trigger: 'blur' },
          { min: 1, max: 50, message: '长度在 1 到 50 个字符', trigger: 'blur' }
        ],
        safe_name: [
          { required: true, message: '请输入名称用作pytest目录名', trigger: 'blur' },
          { min: 1, max: 50, message: '长度在 1 到 50 个字符', trigger: 'blur' }
        ],
        description: [
          { required: false, message: '请输入描述', trigger: 'blur' },
          { max: 1024, message: '不能超过1024个字符', trigger: 'blur' }
        ]
      },
      // 新增数据
      addSuiteForm: {
        department: { name: '' },
        name: '',
        safe_name: '',
        headers: '',
        customHeader: '{}',
        description: '',
        labels: [],
        setup: [],
        setup_class: [],
        teardown: [],
        teardown_class: []
      },

      editSuiteFormVisible: false, // 编辑用例集界面是否显示
      editSuiteFormRules: {
        name: [
          { required: true, message: '请输入名称', trigger: 'blur' },
          { min: 1, max: 50, message: '长度在 1 到 50 个字符', trigger: 'blur' }
        ],
        safe_name: [
          { required: true, message: '请输入SafeName名称用作py类名', trigger: 'blur' },
          { min: 1, max: 50, message: '长度在 1 到 50 个字符', trigger: 'blur' }
        ],
        type: [
          { required: true, message: '请选择测试环境', trigger: 'blur' }
        ],
        description: [
          { required: false, message: '请输入描述', trigger: 'blur' },
          { max: 1024, message: '不能超过1024个字符', trigger: 'blur' }
        ]
      },
      editSuiteForm: {
        department: '',
        name: '',
        safe_name: '',
        headers: '',
        type: 'ping',
        description: '',
        labels: [],
        setup: [],
        setup_class: [],
        teardown: [],
        teardown_class: []
      },
      // 批量处理
      bulkEditFormVisible: false,
      bulkEditForm: {
        department: null
      },
      bulkStatus: true
    }
  },
  mounted() {
    this.getTestSuite()
    this.getDepartment()
    this.getEnv()
  },
  methods: {
    // 折叠版 click
    handleChange(val) {
      // console.log(val)
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
    // 顶部工具条 重置（清空所有下拉框）
    filterClear() {
      this.filters.id = []
      this.filters.name = ''
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
    // 查询 用例集列表
    fetchData() {
      const department_ids = []
      for (let i = 0; i < this.filters.department.length; i++) {
        department_ids.push(this.filters.department[i].id)
      }
      const params = {
        page: this.page,
        page_size: this.page_size,
        id_in: this.filters.id.join(','),
        name: this.filters.name,
        department__in: department_ids.join(','),
        department__isnull: this.filters.department__isnull
      }
      this.tableConfig.isLoading = true
      getTestSuiteList(params).then((res) => {
        const { msg, code } = res
        this.tableConfig.isLoading = false
        if (code === 2) {
          this.dataList = res.data.list
          this.total = res.data.count
        } else {
          this.$message.error({
            message: msg,
            center: true
          })
        }
      })
    },
    // 显示新增用例集界面
    handleAddSuite: function() {
      // this.getHeader()
      this.getLabel(['优先级', '测试集类型'])
      this.addSuiteFormVisible = true
    },
    // 新增用例集
    addSuiteSubmit: function() {
      // this.parseHeader()
      this.$refs.addSuiteForm.validate((valid) => {
        if (valid) {
          this.$confirm('确认提交吗？', '提示', {}).then(() => {
            this.addLoading = true
            // NProgress.start();
            let _headers = {}
            for (let i = 0; i < this.headerModel.length; i++) {
              const v = this.headerModel[i]['value']
              if (v) {
                _headers = Object.assign(_headers, JSON.parse(v))
              }
            }
            _headers = Object.assign(_headers, JSON.parse(this.addSuiteForm.customHeader))
            const label_ids = []
            for (let i = 0; i < this.addSuiteForm.labels.length; i++) {
              label_ids.push(this.addSuiteForm.labels[i].id)
            }
            const addData = {
              name: this.addSuiteForm.name,
              department: this.addSuiteForm.department.id,
              safe_name: this.addSuiteForm.safe_name,
              headers: JSON.stringify(_headers),
              description: this.addSuiteForm.description,
              labels: label_ids,
              setup: this.addSuiteForm.setup,
              setup_class: this.addSuiteForm.setup_class,
              teardown: this.addSuiteForm.teardown,
              teardown_class: this.addSuiteForm.teardown_class
            }
            addTestSuite(addData).then(_data => {
              const { msg, code } = _data
              this.addLoading = false
              if (code === 2) {
                this.$message({
                  message: '添加成功',
                  center: true,
                  type: 'success'
                })
                this.$refs['addSuiteForm'].resetFields()
                this.addSuiteFormVisible = false
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
                this.$refs['addSuiteForm'].resetFields()
                this.addSuiteFormVisible = false
              }
            }).then(() => { this.fetchData() })
          })
        }
      })
    },
    // 显示编辑用例集界面
    handleEditTestSuite: function(index, row) {
      // this.getHeader()
      this.getLabel(['优先级', '测试集类型'])
      this.editSuiteForm = Object.assign({}, row)
      this.editSuiteFormVisible = true
    },
    // 修改测试用例集
    editSuiteSubmit: function() {
      this.$refs.editSuiteForm.validate((valid) => {
        if (valid) {
          this.$confirm('确认提交吗？', '提示', {}).then(() => {
            this.editLoading = true
            // NProgress.start();
            let _headers = {}
            for (let i = 0; i < this.headerModel.length; i++) {
              const v = this.headerModel[i]['value']
              if (v) {
                _headers = Object.assign(_headers, JSON.parse(v))
              }
            }
            if (typeof (this.editSuiteForm.header) !== 'undefined') {
              _headers = Object.assign(_headers, JSON.parse(this.editSuiteForm.header))
            }
            const lablel_ids = []
            for (let j = 0; j < this.editSuiteForm.labels.length; j++) {
              lablel_ids.push(this.editSuiteForm.labels[j].id)
            }
            const params = {
              name: this.editSuiteForm.name,
              department: this.editSuiteForm.department.id,
              safe_name: this.editSuiteForm.safe_name,
              headers: JSON.stringify(_headers),
              labels: lablel_ids,
              description: this.editSuiteForm.description,
              setup: this.editSuiteForm.setup,
              setup_class: this.editSuiteForm.setup_class,
              teardown: this.editSuiteForm.teardown,
              teardown_class: this.editSuiteForm.teardown_class
            }
            updateTestSuite(this.editSuiteForm.id, params).then(_data => {
              const { msg, code } = _data
              this.editLoading = false
              if (code === 2) {
                this.$message({
                  message: '修改成功',
                  center: true,
                  type: 'success'
                })
                this.$refs['editSuiteForm'].resetFields()
                this.editSuiteFormVisible = false
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
                this.editSuiteFormVisible = false
              }
            }).then(() => { this.fetchData() })
          })
        }
      })
    },
    // 删除测试用例集
    handleDelTestSuite: function() {
      if (this.total > 0) {
        this.$notify.error({
          title: '错误',
          message: '用例集下面存在用例，不能删除！！！'
        })
      } else {
        this.$notify.warning({
          title: 'TODO',
          message: '暂时不支持删除！！！'
        })
      }
    },

    // 批量处理
    // 编辑（局部更新）
    bulkEdit: function() {
      this.$confirm('确认修改选中记录吗？', '提示', {
        type: 'warning'
      }).then(() => {
        const validData = {}
        for (const key in this.bulkEditForm) {
          const value = this.bulkEditForm[key]
          if (value) {
            validData[key] = value
          }
        }
        const dataArr = this.sels.map(item => Object.assign({ id: item.id }, validData))
        bulkUpdateTestSuite(dataArr).then(response => {
          const { code, msg } = response
          if (code === 2) {
            this.$message({
              message: '批量修改成功',
              center: true,
              type: 'success'
            })
          } else {
            this.$message.error({
              message: msg,
              center: true
            })
          }
        }).then(() => {
          this.bulkEditFormVisible = false
          this.fetchData()
        })
      })
    },
    // 批量修改状态
    bulkChangeStatus: function(bulkStatus) {
      let params, opt
      if (bulkStatus) {
        opt = '启用'
        params = { status: true }
      } else {
        opt = '禁用'
        params = { status: false }
      }
      const dataArr = this.sels.map(item => Object.assign({ id: item.id }, params))
      bulkUpdateTestSuite(dataArr).then(response => {
        const { code, msg } = response
        if (code === 2) {
          this.$message({
            message: opt + '成功',
            center: true,
            type: 'success'
          })
        } else {
          this.$message.error({
            message: msg,
            center: true
          })
        }
      }).then(() => { this.fetchData() })
    },
    // 批量启用
    bulkEnable: function() {
      this.bulkChangeStatus(true)
    },
    // 批量禁用
    bulkDisable: function() {
      this.bulkChangeStatus(false)
    },
    // 批量删除用例
    bulkRemove: function() {
      this.$notify.warning({
        title: 'TODO',
        message: '暂时不支持删除！！！'
      })
    },

    // 运行用例步骤
    runTest(row) {
      this.$refs.runTestRef.handleRunTest('test_suite', [row])
      this.$set(row, 'runLoading', false)
    },
    // 批量运行用例步骤
    bulkRunTest() {
      this.$refs.runTestRef.handleRunTest('test_suite', this.sels)
      this.bulkRunLoading = false
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
