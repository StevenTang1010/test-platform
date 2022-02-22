<template>
  <div class="main" style="padding:20px;">
    <!--工具条-->
    <el-col :span="24" class="toolbar" style="padding-bottom: 0; padding-left: 10px">
      <el-form :inline="true" :model="filters" :size="themeSize" @submit.native.prevent>
        <el-select v-model="filters.username" :size="themeSize" placeholder="成员名称" value-key="id" multiple filterable allow-create clearable @keyup.enter.native="fetchData">
          <el-option v-for="item in []" :key="item.value" :label="item.label" :value="item.value" />
        </el-select>
        <el-form-item>
          <el-button type="primary" @click="fetchData">查询</el-button>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleAdd">新增</el-button>
        </el-form-item>
      </el-form>
    </el-col>

    <!--列表-->
    <el-table
      v-loading="listLoading"
      :data="list"
      highlight-current-row
      :size="themeSize"
      style="width: 100%; padding-left: 10px"
      @selection-change="selsChange"
    >
      <el-table-column v-if="isSuperuser" type="selection" min-width="3%" />
      <el-table-column prop="id" label="ID" min-width="2%" sortable />
      <el-table-column prop="role" label="角色" min-width="6%" sortable />
      <el-table-column prop="user.username" label="username" min-width="10%" sortable />
      <el-table-column prop="user.email" label="email" min-width="10%" sortable />
      <el-table-column prop="status" label="状态" min-width="5%" sortable>
        <template slot-scope="scope">
          <img v-show="scope.row.status" src="@/assets/icon-yes.svg" alt="">
          <img v-show="!scope.row.status" src="@/assets/icon-no.svg" alt="">
        </template>
      </el-table-column>
      <el-table-column label="操作" min-width="5%">
        <template slot-scope="scope">
          <el-button type="info" icon="el-icon-edit" circle :size="themeSize" title="编辑成员" @click="handleEdit(scope.$index, scope.row)" />
          <el-button type="warning" icon="el-icon-s-flag" circle :size="themeSize" :title="scope.row.status===false?'启用':'禁用'" @click="handleChangeStatus(scope.$index, scope.row)" />
          <el-button v-if="isSuperuser" type="danger" :size="themeSize" @click="handleDel(scope.$index, scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!--底部工具条-->
    <el-col v-show="isSuperuser" :span="24" class="toolbar" style="padding: 5px 5px 5px 10px;">
      <el-button type="danger" :disabled="sels.length===0" @click="batchRemove">批量删除</el-button>
      <span style="font-size: 14px"> 选中{{ sels.length }}条</span>
      <el-pagination
        background
        style="float:right;"
        :current-page.sync="page"
        layout="total, sizes, prev, pager, next, jumper"
        :page-size="20"
        :page-sizes="[20, 50, 100]"
        :total="total"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </el-col>

    <!--编辑界面-->
    <el-dialog title="编辑项目成员" :visible.sync="editFormVisible" :close-on-click-modal="false" style="width: 75%; left: 12.5%">
      <el-form ref="editForm" :model="editForm" label-width="100px" :size="themeSize" :rules="editFormRules">
        <el-form-item label="角色" prop="role">
          <el-select v-model="editForm.role" value-key="id" placeholder="请选择" style="width: 100%">
            <el-option label="超级管理员" value="超级管理员" />
            <el-option label="开发人员" value="开发人员" />
            <el-option label="测试人员" value="测试人员" />
            <el-option label="测试开发" value="测试开发" />
            <el-option label="游客" value="游客" />
          </el-select>
        </el-form-item>
        <el-form-item label="user" prop="user">
          <el-select v-model="editForm.user" value-key="id" placeholder="请选择" style="width: 100%">
            <el-option v-for="item in user_options" :key="item.id" :label="item.username" :value="item" />
          </el-select>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click.native="editFormVisible = false; editLoading = false">取消</el-button>
        <el-button type="primary" :loading="editLoading" @click.native="editSubmit">确定</el-button>
      </div>
    </el-dialog>

    <!--新增界面-->
    <el-dialog title="新增项目成员" :visible.sync="addFormVisible" :close-on-click-modal="false" style="width: 75%; left: 12.5%">
      <el-form ref="addForm" :model="addForm" label-width="100px" :size="themeSize" :rules="addFormRules">
        <el-form-item label="角色" prop="role">
          <el-select v-model="addForm.role" value-key="id" placeholder="请选择" style="width: 100%">
            <el-option label="超级管理员" value="超级管理员" />
            <el-option label="开发人员" value="开发人员" />
            <el-option label="测试人员" value="测试人员" />
            <el-option label="测试开发" value="测试开发" />
            <el-option label="游客" value="游客" />
          </el-select>
        </el-form-item>
        <el-form-item label="user" prop="user">
          <el-select v-model="addForm.user" value-key="id" placeholder="请选择" style="width: 100%">
            <el-option v-for="item in user_options" :key="item.id" :label="item.username" :value="item" />
          </el-select>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button :size="themeSize" @click.native="addFormVisible = false; addLoading = false">取消</el-button>
        <el-button :size="themeSize" type="primary" :loading="addLoading" @click.native="addSubmit">确定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { getProjectMemberList, updateProjectMember, deleteProjectMember, addProjectMember } from '@/api/apiTest/project_member'
import { getUserList } from '@/api/apiTest/user'

export default {
  name: 'MemberList',
  data() {
    return {
      themeSize: this.$store.state.settings.themeSize,
      isSuperuser: false,
      user_options: [],
      filters: {
        username: ''
      },

      // 成员列表
      list: null,
      total: 0,
      page: 1,
      page_count: 0,
      listLoading: false,
      sels: [], // 列表选中列

      // 编辑页面
      editFormVisible: false,
      editLoading: false,
      // 编辑界面数据规则
      editFormRules: {
        role: [
          { required: true, message: '请选择role', trigger: 'blur' }
        ],
        'user.username': [
          { required: true, message: '请输入名称', trigger: 'blur' },
          { min: 1, max: 50, message: '长度在 1 到 50 个字符', trigger: 'blur' }
        ],
        'user.email': [
          { required: false, message: '请输入email', trigger: 'blur' },
          { max: 50, message: '不能超过50个字符', trigger: 'blur' }
        ]
      },
      // 编辑界面数据
      editForm: {
        role: '',
        user: {
          username: '',
          email: ''
        }
      },

      // 编辑页面
      addFormVisible: false,
      addLoading: false,
      // 编辑界面数据规则
      addFormRules: {
        role: [
          { required: true, message: '请选择role', trigger: 'blur' }
        ],
        'user.username': [
          { required: true, message: '请输入名称', trigger: 'blur' },
          { min: 1, max: 50, message: '长度在 1 到 50 个字符', trigger: 'blur' }
        ],
        'user.email': [
          { required: false, message: '请输入email', trigger: 'blur' },
          { max: 50, message: '不能超过50个字符', trigger: 'blur' }
        ]
      },
      // 编辑界面数据
      addForm: {
        role: '',
        user: {
          username: '',
          email: ''
        }
      }
    }
  },
  created() {
  },
  mounted() {
    this.fetchData()
  },
  methods: {
    // 获取member列表
    fetchData() {
      this.listLoading = true
      const params = {
        page: this.page,
        user__username: this.filters.username.join(','),
        project: this.$route.params.project_id
      }
      getProjectMemberList(params).then(response => {
        const { msg, code } = response
        this.listLoading = false
        if (code === 2) {
          this.total = response.data.count
          this.list = response.data.list
        } else {
          this.$message.error({
            message: msg,
            center: true
          })
        }
      })
    },
    getUser() {
      getUserList({}).then(response => {
        const { msg, code } = response
        this.listLoading = false
        if (code === 2) {
          this.user_options = response.data.list
        } else {
          this.$message.error({
            message: msg,
            center: true
          })
        }
      })
    },

    // 选中行
    selsChange: function(sels) {
      this.sels = sels
    },
    // 刷新每页数据条数
    handleSizeChange(val) {
      console.log(`每页 ${val} 条`)
    },
    // 刷新指定页数据
    handleCurrentChange(val) {
      console.log(`当前页: ${val}`)
      this.page = val
      this.fetchData()
    },
    // 显示编辑界面
    handleEdit: function(index, row) {
      this.getUser()
      this.editFormVisible = true
      this.editForm = Object.assign({}, row)
    },
    // 显示新增界面
    handleAdd: function() {
      this.getUser()
      this.addFormVisible = true
    },
    // 编辑
    editSubmit: function() {
      this.$refs.editForm.validate((valid) => {
        if (valid) {
          this.$confirm('确认提交吗？', '提示', {}).then(() => {
            this.editLoading = true
            // NProgress.start();
            const params = {
              role: this.editForm.role,
              user: this.editForm.user.id
            }
            updateProjectMember(this.editForm.id, params).then(_data => {
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
    // 新增
    addSubmit: function() {
      this.$refs.addForm.validate((valid) => {
        if (valid) {
          this.$confirm('确认提交吗？', '提示', {}).then(() => {
            this.addLoading = true
            // NProgress.start();
            const params = {
              role: this.addForm.role,
              project: this.$route.params.project_id,
              user: this.addForm.user.id,
              status: true
            }
            addProjectMember(params).then(_data => {
              const { msg, code } = _data
              this.addLoading = false
              if (code === 2) {
                this.$message({
                  message: '新增成功',
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
    // 改变状态
    handleChangeStatus: function(index, row) {
      this.listLoading = true
      if (row.status) {
        // 禁用
        updateProjectMember(row.id, { status: false }).then(response => {
          const { code, msg } = response
          this.listLoading = false
          if (code === 2) {
            this.$message({
              message: '禁用成功',
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
      } else {
        // 启用
        updateProjectMember(row.id, { status: true }).then(response => {
          const { msg, code } = response
          this.listLoading = false
          if (code === 2) {
            this.$message({
              message: '启用成功',
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
      }
    },
    // 删除
    handleDel: function(index, row) {
      this.$confirm('确认删除该记录吗?', '提示', {
        type: 'warning'
      }).then(() => {
        this.listLoading = true
        // NProgress.start();
        deleteProjectMember(row.id).then(response => {
          const { msg, code } = response
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
          this.fetchData()
        })
      })
    },
    // 批量删除
    batchRemove: function() {
      const ids = this.sels.map(item => item.id)
      this.$confirm('确认删除选中记录吗？', '提示', {
        type: 'warning'
      }).then(() => {
        this.listLoading = true
        // NProgress.start();
        for (let i = 0; i < ids.length; i++) {
          deleteProjectMember(ids[i]).then(response => {
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
          })
        }
      }).then(() => {
        this.fetchData()
      })
    }
  }
}
</script>

<style scoped>

</style>
