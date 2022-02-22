<template>
  <div class="main" style="padding:10px;">
    <!--工具条-->
    <el-col :span="24" class="toolbar" style="padding-bottom: 0;">
      <el-form :inline="true" :model="filters" :size="themeSize" @submit.native.prevent>
        <el-form-item>
          <el-input v-model.trim="filters.name" placeholder="名称" clearable @keyup.enter.native="fetchData" />
        </el-form-item>
        <el-form-item>
          <el-select v-model.trim="filters.type" value-key="type" placeholder="请选择类型" clearable>
            <el-option v-for="item in label_type_options" :key="item.type" :label="item.type_name" :value="item.type" />
          </el-select>
        </el-form-item>
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
      v-loading="tableConfig.isLoading"
      :data="dataList"
      highlight-current-row
      :size="themeSize"
      :height="tableConfig.height"
      style="width: 100%;"
      @selection-change="selsChange"
    >
      <el-table-column type="selection" min-width="2%" />
      <el-table-column prop="name" label="名称" min-width="10%" sortable show-overflow-tooltip />
      <el-table-column prop="type_name" label="类型" min-width="10%" sortable show-overflow-tooltip />
      <el-table-column prop="description" label="描述" min-width="15%" sortable show-overflow-tooltip />
      <el-table-column prop="status" label="状态" min-width="6%" sortable>
        <template slot-scope="scope">
          <img v-show="scope.row.status" src="@/assets/icon-yes.svg" alt="">
          <img v-show="!scope.row.status" src="@/assets/icon-no.svg" alt="">
        </template>
      </el-table-column>
      <el-table-column label="操作" min-width="18%">
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
    <el-dialog title="编辑" :visible.sync="editFormVisible" :close-on-click-modal="false" style="width: 100%; left: 0">
      <el-form ref="editForm" :size="themeSize" :model="editForm" :rules="editFormRules" label-width="100px">
        <el-row :span="24">
          <el-col :span="14">
            <el-form-item label="名称" prop="name">
              <el-input v-model.trim="editForm.name" auto-complete="off" />
            </el-form-item>
          </el-col>
          <el-col :span="10">
            <el-form-item label="类型" prop="type">
              <el-select v-model="editForm.type" value-key="type" placeholder="请选择">
                <el-option v-for="item in label_type_options" :key="item.type" :label="item.type_name" :value="item.type" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="描述" prop="description">
          <el-input v-model.trim="editForm.description" type="textarea" :rows="5" />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button :size="themeSize" @click.native="editFormVisible = false; editLoading = false">取消</el-button>
        <el-button :size="themeSize" type="primary" :loading="editLoading" @click.native="editSubmit">提交</el-button>
      </div>
    </el-dialog>

    <!--新增界面-->
    <el-dialog title="新增" :visible.sync="addFormVisible" :close-on-click-modal="false" style="width: 100%; left: 0">
      <el-form ref="addForm" :size="themeSize" :model="addForm" label-width="100px" :rules="addFormRules">
        <el-row :span="24">
          <el-col :span="14">
            <el-form-item label="名称" prop="name">
              <el-input v-model.trim="addForm.name" auto-complete="off" />
            </el-form-item>
          </el-col>
          <el-col :span="10">
            <el-form-item label="类型" prop="type">
              <el-select v-model="addForm.type" value-key="type" placeholder="请选择">
                <el-option v-for="item in label_type_options" :key="item.type" :label="item.type_name" :value="item.type" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="描述" prop="description">
          <el-input v-model.trim="addForm.description" type="textarea" :rows="5" />
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
import {
  addGlobalLabel,
  bulkDeleteGlobalLabel,
  deleteGlobalLabel,
  getGlobalLabelList,
  updateGlobalLabel
} from '@/api/apiTest/global_label'

export default {
  name: 'GlobalLabel',
  data() {
    return {
      themeSize: this.$store.state.settings.themeSize,
      tableConfig: {
        isLoading: false,
        height: window.innerHeight - 230 // 下面剩余多少空白部分（即最下面距离底部有多少距离）
      },
      editLoading: false,
      addLoading: false,
      delLoading: false,
      batchDelLoading: false,

      label_type_options: [
        { type: 'priority', type_name: '优先级' },
        { type: 'severity', type_name: '严重等级' },
        { type: 'function', type_name: '业务功能' },
        { type: 'testsuite_type', type_name: '测试集类型' },
        { type: 'other', type_name: '其他' }
      ],
      filters: {
        name: '',
        type: ''
      },
      dataList: null,
      total: 0,
      page: 1,
      page_size: 20,
      page_count: 0,
      sels: [], // 列表选中列

      editFormVisible: false, // 编辑界面是否显示
      // 编辑界面数据规则
      editFormRules: {
        name: [
          { required: true, message: '请输入名称', trigger: 'blur' },
          { min: 1, max: 50, message: '长度在 1 到 50 个字符', trigger: 'blur' }
        ],
        type: [
          { required: true, message: '请选择标签类型', trigger: 'blur' }
        ],
        description: [
          { required: false, message: '请输入描述', trigger: 'blur' },
          { max: 1024, message: '不能超过1024个字符', trigger: 'blur' }
        ]
      },
      // 编辑界面数据
      editForm: {
        name: '',
        type: '',
        description: ''
      },

      addFormVisible: false, // 新增界面是否显示
      // 新增界面数据规则
      addFormRules: {
        name: [
          { required: true, message: '请输入名称', trigger: 'blur' },
          { min: 1, max: 50, message: '长度在 1 到 50 个字符', trigger: 'blur' }
        ],
        type: [
          { required: true, message: '请选择标签类型', trigger: 'blur' }
        ],
        description: [
          { required: false, message: '请输入描述', trigger: 'blur' },
          { max: 1024, message: '不能超过1024个字符', trigger: 'blur' }
        ]
      },
      // 新增界面数据
      addForm: {
        name: '',
        type: '',
        description: ''
      }

    }
  },
  created() {
  },
  mounted() {
    this.fetchData()
  },
  methods: {
    // 获取HOST列表
    fetchData() {
      this.tableConfig.isLoading = true
      const params = {
        page: this.page,
        page_size: this.page_size,
        name: this.filters.name,
        type: this.filters.type
      }
      getGlobalLabelList(params).then(response => {
        const { msg, code } = response
        this.tableConfig.isLoading = false
        if (code === 2) {
          this.total = response.data.count
          this.dataList = response.data.list
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
    // 显示编辑界面
    handleEdit: function(index, row) {
      this.editFormVisible = true
      this.editForm = Object.assign({}, row)
    },
    // 显示新增界面
    handleAdd: function() {
      this.addFormVisible = true
    },
    // 改变状态: enable/disable
    handleChangeStatus: function(index, row) {
      if (row.status) {
        // 禁用
        updateGlobalLabel(row.id, { status: false }).then(response => {
          const { code, msg } = response
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
        updateGlobalLabel(row.id, { status: true }).then(response => {
          const { msg, code } = response
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
            const params = {
              id: Number(this.editForm.id),
              name: this.editForm.name,
              type: this.editForm.type,
              description: this.editForm.description
            }
            updateGlobalLabel(Number(this.editForm.id), params).then(response => {
              const { msg, code } = response
              this.editLoading = false
              if (code === 2) {
                this.$message({
                  message: '修改成功',
                  center: true,
                  type: 'success'
                })
                this.$refs['editForm'].resetFields()
                this.editFormVisible = false
              } else if (code === 3) {
                this.$message.error({
                  message: msg,
                  center: true
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
              name: this.addForm.name,
              type: this.addForm.type,
              description: this.addForm.description
            }
            addGlobalLabel(params).then(response => {
              const { msg, code } = response
              this.addLoading = false
              if (code === 2) {
                this.$message({
                  message: '添加成功',
                  center: true,
                  type: 'success'
                })
                this.$refs['addForm'].resetFields()
                this.addFormVisible = false
              } else if (code === 3) {
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
        deleteGlobalLabel(row.id).then(response => {
          const { msg, code } = response
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
        bulkDeleteGlobalLabel(params).then(response => {
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

<style scoped>

</style>
