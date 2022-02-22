<template>
  <div class="main">
    <el-divider class="blue-line" direction="vertical" />
    <span style="font-weight:bold;font-size:14px;color:#2C8DF4;">用例列表</span>

    <!--顶部工具条-->
    <el-col :span="24" class="toolbar">
      <el-form ref="filters" :inline="true" :v-model="filters" :size="themeSize" @submit.native.prevent>
        <el-form-item style="width: 150px">
          <el-select v-model="filters.id" placeholder="用例ID" value-key="id" multiple filterable allow-create clearable @keyup.enter.native="fetchData">
            <span slot="empty" class="el-select-dropdown__empty">请输入用例ID</span>
            <el-option v-for="item in []" :key="item.value" :label="item.label" :value="item.value.replace(/[^\d]/g,'')" />
          </el-select>
        </el-form-item>
        <el-form-item style="width: 150px">
          <el-input v-model="filters.name" placeholder="用例名称" clearable @keyup.enter.native="fetchData" />
        </el-form-item>
        <el-form-item style="width: 150px">
          <el-select v-model="filters.result" value-key="id" multiple clearable placeholder="测试结果">
            <el-option label="passed" value="passed" />
            <el-option label="failed" value="failed" />
            <el-option label="skipped" value="skipped" />
            <el-option label="error" value="error" />
            <el-option label="未执行" value="null" />
          </el-select>
        </el-form-item>
        <el-form-item v-if="showMoreFilters">
          <el-select v-model="filters.test_suite" value-key="id" multiple clearable placeholder="所属用例集">
            <el-option v-for="item in test_suite_options" :key="item.id" :label="item.name" :value="item" />
          </el-select>
        </el-form-item>
        <el-form-item v-if="showMoreFilters">
          <el-select v-model="filters.department" value-key="id" multiple clearable placeholder="所属部门">
            <el-option v-for="item in department_options" :key="item.id" :label="item.name" :value="item" />
          </el-select>
        </el-form-item>
        <el-form-item v-if="showMoreFilters">
          <el-select v-model="filters.label" value-key="id" placeholder="标签" clearable style="width: 100%">
            <el-option-group v-for="group in globalLabel_options" :key="group.label" :label="group.label">
              <el-option v-for="item in group.options" :key="item.id" :label="item.name" :value="item" />
            </el-option-group>
          </el-select>
        </el-form-item>
        <el-form-item v-if="showMoreFilters">
          <el-select v-model="filters.type" style="width:100%" value-key="id" multiple clearable placeholder="测试用例类型">
            <el-option v-for="(item, index) in test_case_type_options" :key="index" :label="item" :value="item" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="fetchData">查询</el-button>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleAdd">新增用例</el-button>
        </el-form-item>
        <el-form-item>
          <el-button type="default" @click.native="filterClear">重置</el-button>
        </el-form-item>
      </el-form>
    </el-col>

    <!--用例列表-->
    <el-table
      ref="caseTable"
      v-loading="tableConfig.isLoading"
      :data="dataList"
      element-loading-text="Loading"
      border
      fit
      highlight-current-row
      :size="themeSize"
      :height="tableConfig.height"
      style="width: 100%"
      :default-sort="{prop: 'step_id', order: 'ascending'}"
      :row-class-name="tableRowClassName"
      @cell-mouse-enter="cellMouseEnter"
      @cell-mouse-leave="cellMouseLeave"
      @selection-change="selsChange"
    >
      <el-table-column fixed type="selection" />
      <el-table-column prop="id" label="ID" sortable width="70" />
      <el-table-column prop="name" label="用例名称" sortable show-overflow-tooltip width="200">
        <template slot-scope="scope">
          <img v-show="scope.row.status" src="@/assets/icon-yes.svg" alt="">
          <img v-show="!scope.row.status" src="@/assets/icon-no.svg" alt="">
          <el-icon name="name" />
          <router-link
            v-if="scope.row.status"
            :to="{ name: '用例详情', params: {case_id: scope.row.id}}"
            style="cursor:pointer;color: #0000ff"
          >
            {{ scope.row.name }}
          </router-link>
          {{ !scope.row.status?scope.row.name:"" }}
        </template>
      </el-table-column>
      <el-table-column prop="description" label="用例描述" sortable show-overflow-tooltip width="200" />
      <el-table-column prop="test_suite.name" label="用例集" sortable show-overflow-tooltip width="150">
        <template slot-scope="scope">
          <el-popover
            placement="right"
            width="800"
            trigger="click"
          >
            <el-card class="box-card" shadow="never">
              <el-description>
                <el-description-item label="所属部门" :value="scope.row.test_suite.department?scope.row.test_suite.department.name:''" :span="24" :span-map="{md:8}" />
                <el-description-item label="SafeName" :value="scope.row.test_suite.safe_name" :span="24" :span-map="{md:8}" />
                <el-description-item label="类型" :value="scope.row.test_suite.type" :span="24" :span-map="{md:8}" />
                <el-description-item label="标签" :span-map="{md:24}">
                  <template slot="content">
                    <span v-for="label in scope.row.test_suite.labels" :key="label.id" style="margin:0 2px" :title="label" type="mini">
                      <el-tag :size="themeSize">{{ label.name }}</el-tag>
                    </span>
                  </template>
                </el-description-item>
                <el-description-item label="描述" :value="scope.row.test_suite.description" :span="24" :span-map="{md:24}" />
                <el-description-item label="请求头" :value="scope.row.test_suite.header" :span-map="{md:24}" />
              </el-description>
            </el-card>
            <el-button slot="reference" type="text" :size="themeSize">
              {{ scope.row.test_suite.department?scope.row.test_suite.department.name:'' }}->{{ scope.row.test_suite.name }}
            </el-button>
          </el-popover>
        </template>
      </el-table-column>
      <el-table-column prop="status" label="结果" sortable width="100">
        <template slot-scope="scope">
          <el-tag v-if="scope.row.result==='passed'" :size="themeSize" type="success">passed</el-tag>
          <el-tag v-if="scope.row.result==='failed'" :size="themeSize" type="danger">failed</el-tag>
          <el-tag v-if="scope.row.result==='skipped'" :size="themeSize" type="warning">skipped</el-tag>
          <el-tag v-if="scope.row.result==='error'" :size="themeSize" type="danger">error</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="type" label="类型" sortable show-overflow-tooltip width="100">
        <template slot-scope="scope">
          <el-tag :size="themeSize" type="success">{{ scope.row.type }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="labels" label="标签" show-overflow-tooltip width="200">
        <template slot-scope="scope">
          <el-tag v-for="item in scope.row.labels" :key="item.id" :size="themeSize">{{ item.name }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="safe_name" label="SafeName" show-overflow-tooltip width="200" />
      <el-table-column fixed="right" label="操作" width="180">
        <template slot-scope="scope">
          <!-- v-show="currentRow === scope.row" -->
          <el-row>
            <el-button type="info" icon="el-icon-edit" circle :size="themeSize" title="编辑用例" @click="handleEdit(scope.$index, scope.row)" />
            <el-button type="info" icon="el-icon-document-copy" circle :size="themeSize" title="复制用例" @click="handleCopy(scope.$index, scope.row)" />
            <el-button :loading="scope.row.runLoading" type="primary" icon="el-icon-caret-right" circle :size="themeSize" title="运行用例" @click="runTest(scope.row)" />
            <el-popover style="margin-left: 10px" trigger="hover">
              <div style="text-align: center">
                <el-button type="warning" icon="el-icon-s-flag" circle :size="themeSize" :title="scope.row.status===false?'启用':'禁用'" @click="handleChangeStatus(scope.$index, scope.row)" />
                <el-button type="danger" icon="el-icon-delete" circle :size="themeSize" :loading="delLoading" title="删除用例" @click="handleDel(scope.$index, scope.row)" />
              </div>
              <el-button slot="reference" icon="el-icon-more" title="更多" circle :size="themeSize" />
            </el-popover>
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
        <el-form-item label="所属用例集" prop="test_suite">
          <el-cascader
            placeholder="搜索：部门/用例集名称"
            :props="{lazy: true, lazyLoad (node, resolve) {deptCaseTreeLoad(node, resolve, 1, false)}}"
            style="width: 100%"
            filterable
            clearable
            @change="handleBulkEditFormCascaderSuite"
          >
            <template slot-scope="{ node, data }">
              <span>{{ data.label }}</span>
            </template>
          </el-cascader>
          <el-button :size="themeSize" type="text">{{ bulkEditForm.test_suite? bulkEditForm.test_suite.name: '' }}</el-button>
        </el-form-item>
        <el-form-item label="标签">
          <el-select v-model="bulkEditForm.labels" value-key="id" placeholder="标签" multiple clearable style="width: 100%">
            <el-option-group v-for="group in globalLabel_options" :key="group.label" :label="group.label">
              <el-option v-for="item in group.options" :key="item.id" :label="item.name" :value="item.id" />
            </el-option-group>
          </el-select>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button :size="themeSize" @click.native="bulkEditFormVisible = false">取消</el-button>
        <el-button :size="themeSize" type="primary" @click.native="bulkEdit()">确定</el-button>
      </div>
    </el-dialog>

    <!--编辑用例界面-->
    <el-drawer
      title="编辑用例"
      :with-header="true"
      :wrapper-closable="false"
      :visible.sync="editFormVisible"
      direction="rtl"
      size="50%"
    >
      <!-- 用例详情 -->
      <div class="demo-drawer__content">
        <el-form ref="editForm" :model="editForm" label-width="100px" :size="themeSize" :rules="editFormRules">
          <el-collapse value="1" @change="handleChange">
            <el-collapse-item name="1">
              <span slot="title" style="font-weight:bold;font-size:14px;color:#2C8DF4;">基本信息</span>
              <el-form-item label="用例名称" prop="name">
                <el-input v-model="editForm.name" auto-complete="off" />
              </el-form-item>
              <el-form-item label="SafeName" prop="safe_name">
                <el-input v-model="editForm.safe_name" auto-complete="off" placeholder="用作pytest类名" />
              </el-form-item>
              <el-form-item label="标签">
                <el-select v-model="editForm.labels" value-key="id" placeholder="标签" multiple clearable style="width: 100%">
                  <el-option-group v-for="group in globalLabel_options" :key="group.label" :label="group.label">
                    <el-option v-for="item in group.options" :key="item.id" :label="item.name" :value="item" />
                  </el-option-group>
                </el-select>
              </el-form-item>
              <el-form-item label="类型" prop="type">
                <el-select v-model="editForm.type" style="width:100%" value-key="id" placeholder="请选择">
                  <el-option v-for="(item, index) in test_case_type_options" :key="index" :label="item" :value="item" />
                </el-select>
              </el-form-item>
              <el-form-item label="描述" prop="description">
                <el-input v-model="editForm.description" type="textarea" :rows="2" />
              </el-form-item>
              <el-form-item label="所属用例集" prop="test_suite">
                <el-cascader
                  placeholder="搜索：部门/用例集名称"
                  :props="{lazy: true, lazyLoad (node, resolve) {deptCaseTreeLoad(node, resolve, 1, false)}}"
                  style="width: 50%"
                  filterable
                  clearable
                  @change="handleEditFormCascaderSuite"
                >
                  <template slot-scope="{ node, data }">
                    <span>{{ data.label }}</span>
                  </template>
                </el-cascader>
                <el-button :size="themeSize" type="text">{{ editForm.test_suite.name }}</el-button>
              </el-form-item>
            </el-collapse-item>
          </el-collapse>
          <!--  设置用例变量 -->
          <el-collapse value="1" @change="handleChange">
            <el-collapse-item name="1">
              <span slot="title" style="font-weight:bold;font-size:14px;color:#2C8DF4;">设置用例变量</span>
              <set-variables v-model="editForm.variables" />
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

    <!--新增用例界面-->
    <el-drawer
      :title="addCaseTitle"
      :with-header="true"
      :wrapper-closable="false"
      :visible.sync="addFormVisible"
      direction="rtl"
      size="50%"
      :before-close="closeAddForm"
    >
      <!-- 用例详情 -->
      <div class="demo-drawer__content">
        <el-form ref="addForm" :model="addForm" label-width="100px" :size="themeSize" :rules="addFormRules">
          <!--  基本信息  -->
          <el-collapse value="1" @change="handleChange">
            <el-collapse-item name="1">
              <span slot="title" style="font-weight:bold;font-size:14px;color:#2C8DF4;">基本信息</span>
              <el-form-item label="用例名称" prop="name">
                <el-input v-model="addForm.name" auto-complete="off" />
              </el-form-item>
              <el-form-item label="SafeName" prop="safe_name">
                <el-input v-model="addForm.safe_name" auto-complete="off" placeholder="用作pytest类名" />
              </el-form-item>
              <el-form-item label="标签">
                <el-select v-model="addForm.labels" value-key="id" placeholder="标签" multiple clearable style="width: 100%">
                  <el-option-group v-for="group in globalLabel_options" :key="group.label" :label="group.label">
                    <el-option v-for="item in group.options" :key="item.id" :label="item.name" :value="item" />
                  </el-option-group>
                </el-select>
              </el-form-item>
              <el-form-item label="类型" prop="type">
                <el-select v-model="addForm.type" style="width:100%" value-key="id" placeholder="请选择">
                  <el-option v-for="(item, index) in test_case_type_options" :key="index" :label="item" :value="item" />
                </el-select>
              </el-form-item>
              <el-form-item label="用例描述" prop="description">
                <el-input v-model="addForm.description" type="textarea" :rows="2" />
              </el-form-item>
              <el-form-item label="所属用例集" prop="test_suite">
                <el-cascader
                  placeholder="搜索：部门/用例集名称"
                  :props="{lazy: true, lazyLoad (node, resolve) {deptCaseTreeLoad(node, resolve, 1, false)}}"
                  style="width: 50%"
                  filterable
                  clearable
                  @change="handleAddFormCascaderSuite"
                >
                  <template slot-scope="{ node, data }">
                    <span>{{ data.label }}</span>
                  </template>
                </el-cascader>
                <el-button :size="themeSize" type="text">{{ addForm.test_suite.name }}</el-button>
              </el-form-item>
              <el-row :gutter="24">
                <el-col :span="12">
                  <el-form-item label="状态" prop="status">
                    <el-switch
                      v-model="addForm.status"
                      active-color="#13ce66"
                    />
                  </el-form-item>
                </el-col>
              </el-row>
            </el-collapse-item>
          </el-collapse>

          <!--  设置用例变量 -->
          <el-collapse value="1" @change="handleChange">
            <el-collapse-item name="1">
              <span slot="title" style="font-weight:bold;font-size:14px;color:#2C8DF4;">设置用例变量</span>
              <set-variables v-model="editForm.variables" />
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

    <!-- 执行测试-->
    <run-test ref="runTestRef" />
  </div>
</template>

<script>
import {
  addTestCase,
  bulkDeleteTestCase,
  bulkUpdateTestCase,
  deleteTestCase,
  getTestCaseList,
  updateTestCase
} from '@/api/apiTest/test_case'

import ElDescription from '@/components/Description/ElDescription'
import ElDescriptionItem from '@/components/Description/ElDescriptionItem'
import get_base_data from '@/api/apiTest/get_base_data'
import SetVariables from '@/views/apiTest/components/SetVariables'
import RunTest from '@/views/apiTest/components/RunTest'

export default {
  name: 'CaseList',
  components: { ElDescription, ElDescriptionItem, SetVariables, RunTest },
  mixins: [get_base_data],
  data() {
    return {
      // 公共var
      themeSize: this.$store.state.settings.themeSize,
      tableConfig: {
        isLoading: false,
        height: window.innerHeight - 275 // 下面剩余多少空白部分（即最下面距离底部有多少距离）
      },
      editLoading: false,
      addLoading: false,
      delLoading: false,
      bulkDelLoading: false,
      bulkRunLoading: false, // 批量执行按钮loading

      requestTabsActiveName: 'body',
      responseTabsActiveName: 'expect',
      showMoreFilters: false,
      test_case_type_options: [
        '单接口测试',
        '场景测试',
        '性能测试',
        'setup',
        'teardown'
      ],

      // 用例
      total: 0,
      page: 1,
      page_size: 20,
      dataList: [],
      filters: {
        id: [],
        name: '',
        result: [],
        project: [],
        test_suite: [],
        department: [],
        type: [],
        label: null
      },
      sels: [], // 用例列表选中列
      currentRow: '', // 用例列表当前行
      isShowColStep: false,
      isShowColSuite: false,

      // 编辑用例
      editFormVisible: false, // 编辑界面是否显示
      // 编辑界面数据规则
      editFormRules: {
        // name: [
        //   { required: true, message: '请输入名称', trigger: 'blur' },
        //   { min: 1, max: 50, message: '长度在 1 到 50 个字符', trigger: 'blur' }
        // ],
        safe_name: [
          { required: true, message: '请输入名称如safe_name用作类名', trigger: 'blur' },
          { min: 1, max: 50, message: '长度在 1 到 50 个字符', trigger: 'blur' }
        ],
        test_suite: [
          { required: true, message: '请选择项目分组名称', trigger: 'blur' }
        ],
        description: [
          { required: false, message: '请输入描述', trigger: 'blur' },
          { max: 1024, message: '不能超过1024个字符', trigger: 'blur' }
        ]
      },
      // 编辑界面数据
      editForm: {
        name: '',
        description: '',
        test_suite: '',
        type: '',
        status: true,
        updater: ''
      },
      cascaderEditVisible: false, // 编辑接口级联面板是否显示

      // 新增用例
      addCaseTitle: '新增用例',
      projectGroupApiTreeData: [], // 选择接口 Tree
      addFormVisible: false, // 新增界面是否显示
      // 新增界面数据规则
      addFormRules: {
        // name: [
        //   { required: true, message: '请输入名称', trigger: 'blur' },
        //   { min: 1, max: 50, message: '长度在 1 到 50 个字符', trigger: 'blur' }
        // ],
        safe_name: [
          { required: true, message: '请输入名称如safe_name用作类名', trigger: 'blur' },
          { min: 1, max: 50, message: '长度在 1 到 50 个字符', trigger: 'blur' }
        ],
        test_suite: [
          { required: true, message: '请选择所属用例集', trigger: 'blur' }
        ],
        description: [
          { required: false, message: '请输入版本号', trigger: 'blur' },
          { max: 1024, message: '不能超过1024个字符', trigger: 'blur' }
        ]
      },
      // 新增界面数据
      addForm: {
        name: '',
        safe_name: '',
        description: '',
        label: '',
        test_suite: '',
        type: '单接口测试',
        creator: '',
        status: true
      },

      // 批量处理
      bulkEditFormVisible: false,
      bulkEditForm: {
        test_suite: null
      },
      bulkStatus: true
    }
  },
  created() {
  },
  mounted() {
    // this.fetchData()
    this.getLabel(['优先级', '测试类型'])
  },
  methods: {
    // ========== 公共 ==========
    // 折叠版 click
    handleChange(val) {
      // console.log(val)
    },
    // 标签页 click
    handleClick(tab, event) {
      console.log(tab, event)
    },
    // 顶部工具条 重置（清空所有下拉框）
    filterClear() {
      this.filters.id = []
      this.filters.name = ''
      this.filters.department = []
      this.filters.test_suite = []
      this.filters.result = []
    },
    // 设置行 颜色
    tableRowClassName({ row }) {
      if (row.test_suite && row.test_suite.department) {
        // return 'success-row'
      } else {
        return 'error-row'
      }
    },
    // ========== 用例 ==========
    // 查询 filters data
    fetchFiltersData() {
      this.getDepartment()
      this.getTestSuite()
    },
    // 查询用例列表
    fetchData() {
      const test_suite_ids = []
      for (let i = 0; i < this.filters.test_suite.length; i++) {
        test_suite_ids.push(this.filters.test_suite[i].id)
      }
      const department_ids = []
      for (let i = 0; i < this.filters.department.length; i++) {
        department_ids.push(this.filters.department[i].id)
      }
      const params = {
        page: this.page,
        page_size: this.page_size,
        id_in: this.filters.id ? this.filters.id.join(',') : null,
        name: this.filters.name ? this.filters.name : null,
        result__in: this.filters.result.length > 0 ? this.filters.result.join(',') : null,
        test_suite__in: test_suite_ids.length > 0 ? test_suite_ids.join(',') : null,
        department__in: department_ids.length > 0 ? department_ids.join(',') : null,
        type__in: this.filters.type.length > 0 ? this.filters.type.join(',') : null,
        label__contains: this.filters.label ? this.filters.label.id : null
      }
      this.tableConfig.isLoading = true
      getTestCaseList(params).then(response => {
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
    // 级联面板
    handleAddFormCascaderSuite(val) {
      if (val.length > 1) {
        this.addForm.test_suite = val[1]
      }
    },
    handleEditFormCascaderSuite(val) {
      if (val.length > 1) {
        this.editForm.test_suite = val[1]
      }
    },
    handleBulkEditFormCascaderSuite(val) {
      if (val.length > 1) {
        this.bulkEditForm.test_suite = val[1].id
      }
    },
    // 显示编辑用例界面
    handleEdit: function(index, row) {
      this.getLabel(['优先级', '测试类型'])
      this.cascaderEditVisible = true
      this.editFormVisible = true
      this.editForm = Object.assign({}, row)
    },
    // 复制用例
    handleCopy: function(index, row) {
      this.getLabel(['优先级', '测试类型'])
      this.addCaseTitle = '复制用例'
      this.addFormVisible = true
      this.addForm = Object.assign({}, row)
      this.addForm.name += '-copy'
      this.addForm.description += '-copy'
      this.addForm.result = ''
      this.addForm.status = true
    },
    // 清空新增页面数据
    addFormClear() {
      this.addForm = {
        name: '',
        description: '',
        label: '',
        test_suite: '',
        variables: '',
        creator: '',
        status: true
      }
    },
    // 显示新增用例界面
    handleAdd: function() {
      // this.addFormClear()
      this.getLabel(['优先级', '测试类型'])
      this.addCaseTitle = '新增用例'
      this.addFormVisible = true
    },
    closeAddForm: function() {
      this.addFormVisible = false
    },
    // 改变用例状态
    handleChangeStatus: function(index, row) {
      let params, opt
      if (row.status) {
        opt = '禁用'
        params = { status: false }
      } else {
        opt = '启用'
        params = { status: true }
      }
      updateTestCase(row.id, params).then(response => {
        const { msg, code } = response
        if (code === 2) {
          this.$message({
            message: opt + '成功',
            center: true,
            type: 'success'
          })
          row.status = !row.status
        } else {
          this.$message.error({
            message: msg,
            center: true
          })
        }
      })
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

    // 编辑用例
    editSubmit: function() {
      this.$refs.editForm.validate((valid) => {
        if (valid) {
          this.$confirm('确认提交吗？', '提示', {}).then(() => {
            this.editLoading = true
            // NProgress.start();
            const lablel_ids = []
            for (let j = 0; j < this.editForm.labels.length; j++) {
              lablel_ids.push(this.editForm.labels[j].id)
            }
            const params = {
              name: this.editForm.name,
              safe_name: this.editForm.safe_name,
              description: this.editForm.description,
              test_suite: this.editForm.test_suite.id,
              type: this.editForm.type,
              variables: this.editForm.variables,
              status: this.editForm.status,
              labels: lablel_ids
            }
            updateTestCase(this.editForm.id, params).then(_data => {
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
              }
            }).then(() => { this.fetchData() })
          })
        }
      })
    },
    // 新增用例
    addSubmit: function() {
      this.$refs.addForm.validate((valid) => {
        if (valid) {
          this.$confirm('确认提交吗？', '提示', {}).then(() => {
            this.addLoading = true
            // NProgress.start();
            const lablel_ids = []
            for (let j = 0; j < this.addForm.labels.length; j++) {
              lablel_ids.push(this.addForm.labels[j].id)
            }
            Object.assign(this.addForm, {
              name: this.addForm.name,
              safe_name: this.addForm.safe_name,
              description: this.addForm.description,
              test_suite: this.addForm.test_suite.id,
              type: this.addForm.type,
              variables: this.addForm.variables,
              status: this.addForm.status,
              labels: lablel_ids
              // creator: this.addForm.creator.id
            })
            addTestCase(this.addForm).then(_data => {
              const { msg, code } = _data
              this.addLoading = false
              if (code === 2) {
                this.$message({
                  message: '添加成功',
                  center: true,
                  type: 'success'
                })
                this.$refs['addForm'].resetFields()
                this.addFormVisible = false
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
                this.$refs['addForm'].resetFields()
                this.addFormVisible = false
              }
            }).then(() => { this.fetchData() })
          })
        }
      })
    },
    // 删除用例
    handleDel: function(index, row) {
      this.$confirm('确认删除该记录吗?', '提示', {
        type: 'warning'
      }).then(() => {
        this.delLoading = true
        deleteTestCase(row.id).then(response => {
          const { code, msg } = response
          this.delLoading = false
          if (code === 2) {
            this.$message({
              message: '删除成功',
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
      })
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
        bulkUpdateTestCase(dataArr).then(response => {
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
      bulkUpdateTestCase(dataArr).then(response => {
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
      const ids = this.sels.map(item => item.id)
      this.$confirm('确认删除选中记录吗？', '提示', {
        type: 'warning'
      }).then(() => {
        const params = {
          id_in: ids.join(',')
        }
        bulkDeleteTestCase(params).then(response => {
          const { code, msg } = response
          if (code === 2) {
            this.$message({
              message: '删除成功',
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
      })
    },

    // 运行用例
    runTest(row) {
      this.$refs.runTestRef.handleRunTest('test_case', [row])
      this.$set(row, 'runLoading', false)
    },
    // 批量运行用例步骤
    bulkRunTest() {
      this.$refs.runTestRef.handleRunTest('test_case', this.sels)
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
  ::v-deep .el-table .success-row {
    background: #e8fcdf;
  }
  ::v-deep .el-table .error-row {
    background: #f8e1e1;
  }
  ::v-deep .el-table .warning-row {
    background: #fae9c9;
  }
</style>
