<template>
  <div class="main" style="padding:10px;">
    <el-divider class="blue-line" direction="vertical" />
    <span style="font-weight:bold;font-size:14px;color:#2C8DF4;">项目列表</span>

    <!--顶部工具条-->
    <el-col :span="24" class="toolbar">
      <el-form :inline="true" :model="filters" :size="themeSize" @submit.native.prevent>
        <el-form-item>
          <el-input v-model="filters.name" placeholder="名称" clearable @keyup.enter.native="fetchData" />
        </el-form-item>
        <el-form-item>
          <el-select v-model="filters.department" placeholder="所属部门" clearable>
            <el-option v-for="item in department_options" :key="item.id" :label="item.name" :value="item.id" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="fetchData">查询</el-button>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleAdd">新增</el-button>
        </el-form-item>
        <el-form-item>
          <el-button type="default" @click.native="filterClear">重置</el-button>
        </el-form-item>
      </el-form>
    </el-col>

    <!--列表-->
    <el-table
      v-loading="tableConfig.isLoading"
      :data="dataList"
      element-loading-text="Loading"
      border
      fit
      highlight-current-row
      :size="themeSize"
      :height="tableConfig.height"
      style="width: 100%"
      :default-sort="{prop: 'id', order: 'descending'}"
      @selection-change="selsChange"
    >
      <el-table-column fixed type="selection" />
      <el-table-column prop="name" label="项目名称" sortable show-overflow-tooltip width="200" >
        <template slot-scope="scope">
          <el-icon name="name" />
          <router-link
            v-if="scope.row.status"
            :to="{ name: '项目详情', params: {project_id: scope.row.id}}"
            style="cursor:pointer;color: #0000ff"
          >
            {{ scope.row.name }}
          </router-link>
          {{ !scope.row.status?scope.row.name:"" }}
        </template>
      </el-table-column>
      <el-table-column prop="department.name" label="部门" sortable width="100" />
      <el-table-column prop="creator.username" label="负责人" sortable width="100" />
      <el-table-column prop="version" label="版本" sortable width="100" />
      <el-table-column prop="update_time" label="最后修改时间" sortable show-overflow-tooltip width="150" />
      <el-table-column prop="status" label="状态" sortable width="80">
        <template slot-scope="scope">
          <img v-show="scope.row.status" src="@/assets/icon-yes.svg" alt="">
          <img v-show="!scope.row.status" src="@/assets/icon-no.svg" alt="">
        </template>
      </el-table-column>
      <el-table-column label="操作" width="150">
        <template slot-scope="scope">
          <el-button type="info" icon="el-icon-edit" circle :size="themeSize" title="编辑" @click="handleEdit(scope.$index, scope.row)" />
          <el-button type="warning" icon="el-icon-s-flag" circle :size="themeSize" :title="scope.row.status===false?'启用':'禁用'" @click="handleChangeStatus(scope.$index, scope.row)" />
          <el-button type="danger" icon="el-icon-delete" circle :size="themeSize" :loading="delLoading" title="删除" @click="handleDel(scope.$index, scope.row)" />
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

    <!--编辑界面-->
    <el-dialog title="编辑" :visible.sync="editFormVisible" :close-on-click-modal="false" style="width: 75%; left: 12.5%">
      <el-form ref="editForm" :size="themeSize" :model="editForm" label-width="120px" :rules="editFormRules">
        <el-form-item label="项目名称" prop="name">
          <el-input v-model="editForm.name" auto-complete="off" />
        </el-form-item>
        <el-row :gutter="24">
          <el-col :span="12">
            <el-form-item label="所属部门" prop="department">
              <el-select v-model="editForm.department" value-key="id" placeholder="请选择">
                <el-option v-for="item in department_options" :key="item.id" :label="item.name" :value="item" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="版本号" prop="version">
              <el-input v-model="editForm.version" auto-complete="off" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="负责人" prop="updater">
              <el-select v-model="editForm.updater" value-key="id" placeholder="请选择">
                <el-option v-for="item in user_options" :key="item.id" :label="item.username" :value="item" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="描述" prop="description">
          <el-input v-model="editForm.description" type="textarea" :rows="6" />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button :size="themeSize" @click.native="editFormVisible = false; editLoading = false">取消</el-button>
        <el-button :size="themeSize" type="primary" :loading="editLoading" @click.native="editSubmit">提交</el-button>
      </div>
    </el-dialog>

    <!--新增界面-->
    <el-dialog title="新增" :visible.sync="addFormVisible" :close-on-click-modal="false" style="width: 75%; left: 12.5%">
      <el-form ref="addForm" :size="themeSize" :model="addForm" label-width="120px" :rules="addFormRules">
        <el-form-item label="项目名称" prop="name">
          <el-input v-model.trim="addForm.name" auto-complete="off" />
        </el-form-item>
        <el-row :gutter="24">
          <el-col :span="12">
            <el-form-item label="所属部门" prop="department">
              <el-select v-model="addForm.department" value-key="id" placeholder="请选择">
                <el-option v-for="item in department_options" :key="item.id" :label="item.name" :value="item" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="版本号" prop="version">
              <el-input v-model="addForm.version" auto-complete="off" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="负责人" prop="creator">
              <el-select v-model="addForm.creator" value-key="id" placeholder="请选择">
                <el-option v-for="item in user_options" :key="item.id" :label="item.username" :value="item" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="描述" prop="description">
          <el-input v-model="addForm.description" type="textarea" :rows="6" />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button :size="themeSize" @click.native="addFormVisible = false; addLoading = false">取消</el-button>
        <el-button :size="themeSize" type="primary" :loading="addLoading" @click.native="addSubmit">提交</el-button>
      </div>
    </el-dialog>

  </div>
</template>

<script>
// import { getUserList } from '@/api/apiTest/user'
import { getDepartmentList } from '@/api/apiTest/department'
import { getProjectList, addProject, updateProject, deleteProject, bulkDeleteProject } from '@/api/apiTest/project'

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
      themeSize: this.$store.state.settings.themeSize,
      tableConfig: {
        isLoading: false,
        height: window.innerHeight - 245 // 下面剩余多少空白部分（即最下面距离底部有多少距离）
      },
      editLoading: false,
      addLoading: false,
      delLoading: false,
      batchDelLoading: false,

      total: 0,
      page_count: 0,
      page: 1,
      page_size: 20,
      dataList: null,
      filters: {
        name: '',
        department: '',
        department__isnull: null
      },
      sels: [], // 列表选中列
      department_options: [],
      user_options: [],

      editFormVisible: false, // 编辑界面是否显示
      // 编辑界面数据规则
      editFormRules: {
        name: [
          { required: true, message: '请输入名称', trigger: 'blur' },
          { min: 1, max: 50, message: '长度在 1 到 50 个字符', trigger: 'blur' }
        ],
        department: [
          { required: false, message: '请选择部门名称', trigger: 'blur' }
        ],
        updater: [
          { required: false, message: '请选择updater user', trigger: 'blur' }
        ],
        version: [
          { required: true, message: '请输入版本号', trigger: 'blur' },
          { min: 1, max: 20, message: '长度在 1 到 20 个字符', trigger: 'blur' }
        ],
        description: [
          { required: false, message: '请输入描述', trigger: 'blur' },
          { max: 1024, message: '不能超过1024个字符', trigger: 'blur' }
        ]
      },
      // 编辑界面数据
      editForm: {
        name: '',
        department: 0,
        version: '',
        updater: 0,
        description: ''
      },

      addFormVisible: false, // 新增界面是否显示
      // 新增界面数据规则
      addFormRules: {
        name: [
          { required: true, message: '请输入名称', trigger: 'blur' },
          { min: 1, max: 50, message: '长度在 1 到 50 个字符', trigger: 'blur' }
        ],
        department: [
          { required: false, message: '请选择部门名称', trigger: 'blur' }
        ],
        creator: [
          { required: false, message: '请选择creator user', trigger: 'blur' }
        ],
        version: [
          { required: true, message: '请输入版本号', trigger: 'blur' },
          { min: 1, max: 20, message: '长度在 1 到 20 个字符', trigger: 'blur' }
        ],
        description: [
          { required: false, message: '请输入版本号', trigger: 'blur' },
          { max: 1024, message: '不能超过1024个字符', trigger: 'blur' }
        ]
      },
      // 新增界面数据
      addForm: {
        name: '',
        department: '',
        version: '',
        creator: '',
        description: ''
      }
    }
  },
  created() {
  },
  mounted() {
    this.fechBaseData()
    // this.fetchData()
  },
  methods: {
    // 清空所有下拉框
    filterClear() {
      this.filters.name = ''
      this.filters.department = ''
    },
    // 查询 部门、项目分组、用户
    fechBaseData() {
      getDepartmentList({}).then((res) => {
        const { msg, code } = res
        if (code === 2) {
          this.department_options = res.data.list
        } else {
          this.$message.error({
            message: msg,
            center: true
          })
        }
      })
      // getUserList({}).then((res) => {
      //   const { msg, code } = res
      //   if (code === 2) {
      //     this.user_options = res.data.list
      //   } else {
      //     this.$message.error({
      //       message: msg,
      //       center: true
      //     })
      //   }
      // })
    },
    // 查询项目列表
    fetchData() {
      this.tableConfig.isLoading = true
      const params = {
        page: this.page,
        page_size: this.page_size,
        name: this.filters.name,
        department: this.filters.department,
        department__isnull: this.filters.department__isnull
      }
      getProjectList(params).then(response => {
        this.dataList = response.data.list
        this.total = response.data.count
        this.tableConfig.isLoading = false
      })
    },
    // 选中行
    selsChange: function(sels) {
      this.sels = sels
    },
    // 显示编辑界面
    handleEdit: function(index, row) {
      this.editFormVisible = true
      this.editForm = Object.assign({}, row)
    },
    // 显示新增界面
    handleAdd: function() {
      this.addFormVisible = true
    },
    // 改变项目状态
    handleChangeStatus: function(index, row) {
      let params, opt
      if (row.status) {
        opt = '禁用'
        params = { status: false }
      } else {
        opt = '启用'
        params = { status: true }
      }
      updateProject(row.id, params).then(response => {
        const { code, msg } = response
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
    // 编辑
    editSubmit: function() {
      this.$refs.editForm.validate((valid) => {
        if (valid) {
          this.$confirm('确认提交吗？', '提示', {}).then(() => {
            this.editLoading = true
            // NProgress.start();
            let params = {
              // id: this.editForm.id,
              name: this.editForm.name,
              // department: this.editForm.department.id,
              // updater: this.editForm.updater.id,
              version: this.editForm.version,
              description: this.editForm.description
            }
            if (this.editForm.department !== null) {
              params = Object.assign(params, { department: this.editForm.department.id })
            }
            console.log(params)
            updateProject(this.editForm.id, params).then(_data => {
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
    // 新增
    addSubmit: function() {
      this.$refs.addForm.validate((valid) => {
        if (valid) {
          this.$confirm('确认提交吗？', '提示', {}).then(() => {
            this.addLoading = true
            // NProgress.start();
            const addData = {
              name: this.addForm.name,
              department: this.addForm.department.id,
              creator: this.addForm.creator.id,
              version: this.addForm.version,
              description: this.addForm.description
            }
            addProject(addData).then(_data => {
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
    // 删除
    handleDel: function(index, row) {
      this.$confirm('确认删除该记录吗?', '提示', {
        type: 'warning'
      }).then(() => {
        this.delLoading = true
        // NProgress.start();
        deleteProject(row.id).then(response => {
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
    // 批量删除
    bulkRemove: function() {
      const ids = this.sels.map(item => item.id)
      this.$confirm('确认删除选中记录吗？', '提示', {
        type: 'warning'
      }).then(() => {
        const params = {
          id_in: ids.join(',')
        }
        bulkDeleteProject(params).then(response => {
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
    }
  }
}
</script>
