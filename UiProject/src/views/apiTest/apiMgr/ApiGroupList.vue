<template>
  <div class="main">
    <el-divider class="blue-line" direction="vertical" />
    <span slot="title" style="font-weight:bold;font-size:14px;color:#2C8DF4;">接口分组</span>

    <!--顶部工具条-->
    <el-col :span="24" class="toolbar" style="padding-bottom: 0;padding-top: 10px;">
      <el-form :inline="true" :model="filters" :size="themeSize" @submit.native.prevent>
        <el-form-item>
          <el-input v-model="filters.name" placeholder="名称" clearable @keyup.enter.native="fetchData" />
        </el-form-item>
        <el-form-item>
          <el-select v-model="filters.project" value-key="id" multiple placeholder="所属项目" filterable clearable>
            <el-option v-for="item in project_options" :key="item.id" :label="item.name" :value="item" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="fetchData">查询</el-button>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleAddApiGroup">新增</el-button>
        </el-form-item>
        <el-form-item>
          <el-button type="default" @click.native="filterClear">重置</el-button>
        </el-form-item>
      </el-form>
    </el-col>

    <!--列表-->
    <el-table
      :data="dataList"
      v-loading="tableConfig.isLoading"
      element-loading-text="Loading"
      border
      fit
      highlight-current-row
      :size="themeSize"
      :height="tableConfig.height"
      style="width: 100%"
      :default-sort="{prop: 'id', order: 'descending'}"
      @cell-mouse-enter="cellMouseEnter"
      @cell-mouse-leave="cellMouseLeave"
      @selection-change="selsChange"
    >
      <el-table-column type="selection" min-width="10%" />
      <el-table-column prop="name" label="分组名称" sortable show-overflow-tooltip min-width="20%">
        <template slot-scope="scope">
          <el-icon name="name" />
          <router-link
            v-if="scope.row.status"
            :to="{ name: '接口详情', params: {api_id: scope.row.id}}"
            style="cursor:pointer;color: #0000ff"
          >
            {{ scope.row.name }}
          </router-link>
          {{ !scope.row.status?scope.row.name:"" }}
        </template>
      </el-table-column>
      <el-table-column prop="description" label="描述" sortable show-overflow-tooltip min-width="20%" />
      <el-table-column prop="project.name" label="项目" sortable min-width="20%" />
      <el-table-column label="操作" min-width="20%">
        <template slot-scope="scope">
          <el-row>
            <el-button type="info" icon="el-icon-edit" circle :size="themeSize" title="编辑接口" @click="handleEditApiGroup(scope.$index, scope.row)" />
            <el-button type="danger" icon="el-icon-delete" circle :size="themeSize" title="删除接口" @click="handleDeleteApiGroup(scope.$index, scope.row)" />
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
        <el-button type="danger" plain :disabled="sels.length===0" :size="themeSize" @click="bulkRemove">删除</el-button>
        <span style="font-size: 14px; padding-right: 30px;"> 选中{{ sels.length }}条</span>
        <el-button type="text" plain :size="themeSize" @click="sels = []">取消</el-button>
      </el-col>
    </el-row>

    <!--新增分组界面-->
    <el-drawer
      title="新增分组"
      :with-header="true"
      :wrapper-closable="false"
      :visible.sync="addFormVisible"
      direction="rtl"
      size="50%"
    >
      <div class="demo-drawer__content">
        <el-form ref="addApiGroupForm" :size="themeSize" :model="addForm" label-width="120px" :rules="addFormRules">
          <el-form-item label="所属项目" prop="project">
            <el-cascader
              placeholder="搜索：部门/项目名"
              :props="{lazy: true, lazyLoad (node, resolve) {deptApiTreeLoad(node, resolve, 1, false)}}"
              style="width: 100%"
              filterable
              clearable
              @change="handleAddCascaderChange"
            >
              <template slot-scope="{ node, data }">
                <span>{{ data.label }}</span>
              </template>
            </el-cascader>
          </el-form-item>
          <el-form-item label="分组名称" prop="name">
            <el-input v-model.trim="addForm.name" auto-complete="off" />
          </el-form-item>
          <el-form-item label="描述" prop="description">
            <el-input v-model="addForm.description" type="textarea" :rows="6" />
          </el-form-item>
        </el-form>
        <!-- 取消、提交 -->
        <div class="demo-drawer__footer">
          <el-button :size="themeSize" @click.native="addFormVisible = false; addLoading = false">取消</el-button>
          <el-button :size="themeSize" type="primary" :loading="addLoading" @click.native="addGroupSubmit">提交</el-button>
        </div>
      </div>
    </el-drawer>

    <!--编辑接口分组界面-->
    <el-drawer
      title="编辑接口分组"
      :with-header="true"
      :wrapper-closable="false"
      :visible.sync="editFormVisible"
      direction="rtl"
      size="50%"
    >
      <!-- 编辑接口分组 -->
      <div class="demo-drawer__content">
        <el-form ref="editApiGroupForm" :size="themeSize" :model="editForm" label-width="120px" :rules="editFormRules">
          <el-collapse value="1" @change="handleChange">
            <el-collapse-item name="1">
              <span slot="title" style="font-weight:bold;font-size:14px;color:#2C8DF4;">基本信息</span>
              <el-form-item label="分组名称" prop="name">
                <el-input v-model="editForm.name" auto-complete="off" />
              </el-form-item>
              <el-form-item label="描述" prop="description">
                <el-input v-model="editForm.description" type="textarea" :rows="2" />
              </el-form-item>
            </el-collapse-item>
          </el-collapse>
        </el-form>

        <!-- 取消、提交 -->
        <div class="demo-drawer__footer">
          <el-button :size="themeSize" @click.native="editFormVisible = false; editLoading = false">取消</el-button>
          <el-button :size="themeSize" type="primary" :loading="editLoading" @click.native="editApiGroupSubmit">提交</el-button>
        </div>
      </div>
    </el-drawer>
  </div>
</template>

<script>

import { addApiGroup, getApiGroupList, updateApiGroup } from '@/api/apiTest/api_group'
import get_base_data from '@/api/apiTest/get_base_data'

export default {
  name: 'ApiGroupList',
  mixins: [get_base_data],
  data() {
    return {
      themeSize: this.$store.state.settings.themeSize,
      tableConfig: {
        isLoading: false,
        height: window.innerHeight - 225 // 下面剩余多少空白部分（即最下面距离底部有多少距离）
      },

      // 分组列表
      total: 0,
      page_count: 0,
      page: 1,
      page_size: 20,
      dataList: null,
      filters: {
        name: '',
        project: []
      },
      sels: [], // 列表选中列

      // 新增分组
      addFormVisible: false, // 新增分组界面是否显示
      addLoading: false,
      // 新增界面数据规则
      addFormRules: {
        name: [
          { required: true, message: '请输入名称', trigger: 'blur' },
          { min: 1, max: 50, message: '长度在 1 到 50 个字符', trigger: 'blur' }
        ],
        project: [
          { required: true, message: '请选择所属项目', trigger: 'blur' }
        ],
        description: [
          { required: false, message: '请输入描述', trigger: 'blur' },
          { max: 1024, message: '不能超过1024个字符', trigger: 'blur' }
        ]
      },
      // 新增数据
      addForm: {
        department: { name: '' },
        name: '',
        project: '',
        host: {},
        header: '',
        customHeader: '{}',
        description: '',
        labels: []
      },

      // 编辑
      editLoading: false,
      editFormVisible: false, // 编辑接口分组界面是否显示
      editFormRules: {
        name: [
          { required: true, message: '请输入名称', trigger: 'blur' },
          { min: 1, max: 50, message: '长度在 1 到 50 个字符', trigger: 'blur' }
        ],
        description: [
          { required: false, message: '请输入描述', trigger: 'blur' },
          { max: 1024, message: '不能超过1024个字符', trigger: 'blur' }
        ]
      },
      editForm: {
        name: '',
        description: ''
      }
    }
  },
  mounted() {
  },
  methods: {
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
    // 选中行
    selsChange: function(sels) {
      this.sels = sels
    },
    cellMouseEnter(row) {
      this.currentRow = row
    },
    cellMouseLeave(row) {
      this.currentRow = ''
    },
    // 清空所有下拉框
    filterClear() {
      this.filters.name = ''
      this.filters.project = ''
    },
    fetchData() {
      const params = {
        page: this.page,
        page_size: this.page_size,
        name: this.filters.name,
        project: this.filters.project.id
      }
      this.tableConfig.isLoading = true
      getApiGroupList(params).then((res) => {
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
    // 新增接口分组事件
    handleAddApiGroup() {
      this.addFormVisible = true
    },
    handleAddCascaderChange(val) {
      this.addForm.project = val[1]
    },
    // 新增分组
    addGroupSubmit: function() {
      this.$refs.addApiGroupForm.validate((valid) => {
        if (valid) {
          this.$confirm('确认提交吗？', '提示', {}).then(() => {
            this.addLoading = true
            // NProgress.start();
            const addData = {
              name: this.addForm.name,
              project: this.addForm.project.id,
              description: this.addForm.description
            }
            addApiGroup(addData).then(_data => {
              const { msg, code } = _data
              if (code === 2) {
                this.$message({
                  message: '添加成功',
                  center: true,
                  type: 'success'
                })
                this.$refs['addApiGroupForm'].resetFields()
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
                this.$refs['addApiGroupForm'].resetFields()
                this.addFormVisible = false
              }
            }).then(() => { this.fetchData() })
          })
        }
      })
    },

    // 编辑接口分组事件
    handleEditApiGroup(index, row) {
      this.editForm = Object.assign({}, row)
      this.editFormVisible = true
    },
    // 修改接口分组
    editApiGroupSubmit() {
      this.$refs.editApiGroupForm.validate((valid) => {
        if (valid) {
          this.$confirm('确认提交吗？', '提示', {}).then(() => {
            this.editLoading = true
            // NProgress.start();
            const params = {
              name: this.editForm.name,
              description: this.editForm.description
            }
            updateApiGroup(this.editForm.id, params).then(_data => {
              const { msg, code } = _data
              this.editLoading = false
              if (code === 2) {
                this.$message({
                  message: '修改成功',
                  center: true,
                  type: 'success'
                })
                this.$refs['editApiGroupForm'].resetFields()
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
            }).then(_res => {
              this.fetchGroupDetail()
            })
          })
        }
      })
    },

    // 删除接口分组事件
    handleDeleteApiGroup() {
      if (this.total > 0) {
        this.$notify.error({
          title: '错误',
          message: '接口分组中存在API，不能删除！！！'
        })
      } else {
        this.$notify.warning({
          title: 'TODO',
          message: '暂时不支持删除！！！'
        })
      }
    },
    bulkRemove: function() {
      this.$notify.warning({
        title: 'TODO',
        message: '暂时不支持删除！！！'
      })
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
