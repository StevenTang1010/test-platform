<template>
  <div class="main" style="padding:10px;">
    <!--工具条-->
    <el-col :span="24" class="toolbar">
      <el-form :inline="true" :model="filters" :size="themeSize" @submit.native.prevent>
        <el-form-item>
          <el-input v-model.trim="filters.name" placeholder="名称" clearable @keyup.enter.native="fetchData" />
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
      <el-table-column type="selection" min-width="50" />
      <el-table-column prop="name" label="名称" sortable show-overflow-tooltip min-width="150" />
      <el-table-column prop="description" label="描述" show-overflow-tooltip min-width="200" />
      <el-table-column prop="config" label="公司ID" sortable show-overflow-tooltip min-width="150">
        <template slot-scope="scope">
          {{ scope.row.config['company_id']['value'] }}
        </template>
      </el-table-column>
      <el-table-column prop="config" label="配置详情" min-width="100">
        <template slot-scope="scope">
          <el-popover
            placement="right"
            width="800"
            trigger="click"
          >
            <el-card class="box-card" shadow="never">
              <div slot="header" class="clearfix">环境配置({{ scope.row.name }}：{{ scope.row.description }})</div>
              <el-table :data="dictConfigToArray(scope.row.config, scope.row.qw_external_contact_config)" style="width: 100%" :size="themeSize">
                <el-table-column label="名称" prop="key" sortable show-overflow-tooltip />
                <el-table-column label="值" prop="value" sortable show-overflow-tooltip />
                <el-table-column label="描述" prop="description" sortable show-overflow-tooltip />
              </el-table>
            </el-card>
            <el-button slot="reference" :size="themeSize" type="text">详情</el-button>
          </el-popover>
        </template>
      </el-table-column>
      <el-table-column prop="data" label="环境数据" min-width="100">
        <template slot-scope="scope">
          <el-popover
            placement="right"
            width="600"
            trigger="click"
          >
            <el-row>
              <el-button style="float: right; padding: 3px 0" type="text" @click="clearData(scope.row)">清除数据</el-button>
              <el-button style="padding-left: 10px" type="primary" :size="themeSize" @click="toggleExpanded">{{ expanded ? '收起' : '展开' }}</el-button>
              环境数据({{ scope.row.name }}：{{ scope.row.description }})
            </el-row>
            <json-viewer
              :key="expanded"
              :value="scope.row.data"
              :expand-depth="1"
              :expanded="expanded"
              copyable
              boxed
              sort
            />
            <el-button slot="reference" :size="themeSize" type="text">详情</el-button>
          </el-popover>
        </template>
      </el-table-column>
      <el-table-column prop="mock" label="Mock数据" min-width="100">
        <template slot-scope="scope">
          <el-popover
            placement="right"
            width="500"
            trigger="click"
          >
            <el-row>
              <el-button style="float: right;" type="text" :size="themeSize" @click="clearMock(scope.row)">清除数据</el-button>
              <el-button style="padding-left: 10px" type="primary" :size="themeSize" @click="toggleExpanded">{{ expanded ? '收起' : '展开' }}</el-button>
              Mock数据，执行时自动更新({{ scope.row.name }}：{{ scope.row.description }})
            </el-row>
            <json-viewer
              :key="expanded"
              :value="scope.row.mock"
              :expand-depth="1"
              :expanded="expanded"
              copyable
              boxed
              sort
            />
            <el-button slot="reference" :size="themeSize" type="text">详情</el-button>
          </el-popover>
        </template>
      </el-table-column>
      <el-table-column prop="status" label="状态" sortable min-width="70">
        <template slot-scope="scope">
          <img v-show="scope.row.status" src="@/assets/icon-yes.svg" alt="">
          <img v-show="!scope.row.status" src="@/assets/icon-no.svg" alt="">
        </template>
      </el-table-column>
      <el-table-column label="操作" min-width="180">
        <template slot-scope="scope">
          <el-button type="info" icon="el-icon-edit" circle :size="themeSize" title="编辑" @click="handleEdit(scope.$index, scope.row)" />
          <el-button type="warning" icon="el-icon-refresh" circle :size="themeSize" title="更新环境数据" @click="handleUpdateEnvData(scope.$index, scope.row)" />
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
          <!--  基本信息  -->
          <el-collapse value="1">
            <el-collapse-item name="1">
              <span slot="title" style="font-weight:bold;font-size:14px;color:#2C8DF4;">基本信息</span>
              <el-form-item label="名称" prop="name">
                <el-input v-model.trim="editForm.name" auto-complete="off" />
              </el-form-item>
              <el-form-item v-for="(k,index) in editForm.config" :key="index" :label="k.description" :prop="index">
                <el-input v-model.trim="editForm.config[index].value" auto-complete="off" />
              </el-form-item>
              <el-form-item label="描述" prop="description">
                <el-input v-model.trim="editForm.description" type="textarea" :rows="2" />
              </el-form-item>
            </el-collapse-item>
          </el-collapse>

          <!--  企微客户联系配置  -->
          <el-collapse value="1">
            <el-collapse-item name="1">
              <span slot="title" style="font-weight:bold;font-size:14px;color:#2C8DF4;">企微客户联系配置</span>
              <el-form-item v-for="(k,index) in editForm.qw_external_contact_config" :key="index" :label="k.description" :prop="index">
                <el-input v-model.trim="editForm.qw_external_contact_config[index].value" auto-complete="off" />
              </el-form-item>
            </el-collapse-item>
          </el-collapse>

          <!--  设置  -->
          <el-collapse value="1">
            <el-collapse-item name="1">
              <span slot="title" style="font-weight:bold;font-size:14px;color:#2C8DF4;">设置</span>
              <el-form-item label="动态更新mock" prop="mock_dynamic">
                <el-switch
                  v-model="editForm.mock_dynamic"
                  active-color="#13ce66"
                />
              </el-form-item>
              <el-form-item label="默认环境" prop="is_default">
                <el-switch
                  v-model="editForm.is_default"
                  active-color="#13ce66"
                />
              </el-form-item>
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
      title="编辑"
      :with-header="true"
      :wrapper-closable="false"
      :visible.sync="addFormVisible"
      direction="rtl"
      size="50%"
    >
      <div class="demo-drawer__content">
        <el-form ref="addForm" :size="themeSize" :model="addForm" label-width="160px" :rules="addFormRules">
          <!--  基本信息  -->
          <el-collapse value="1">
            <el-collapse-item name="1">
              <span slot="title" style="font-weight:bold;font-size:14px;color:#2C8DF4;">基本信息</span>
              <el-form-item label="名称" prop="name">
                <el-input v-model.trim="addForm.name" auto-complete="off" />
              </el-form-item>
              <el-form-item v-for="(k,index) in addForm.config" :key="index" :label="k.description" :prop="'config.'+index">
                <el-input v-model.trim="addForm.config[index].value" auto-complete="off" />
              </el-form-item>
              <el-form-item label="环境描述" prop="description">
                <el-input v-model.trim="addForm.description" type="textarea" :rows="2" />
              </el-form-item>
            </el-collapse-item>
          </el-collapse>

          <!--  企微客户联系配置  -->
          <el-collapse value="1">
            <el-collapse-item name="1">
              <span slot="title" style="font-weight:bold;font-size:14px;color:#2C8DF4;">企微客户联系配置</span>
              <el-form-item v-for="(k,index) in addForm.qw_external_contact_config" :key="index" :label="k.description" :prop="'qw_external_contact_config.'+index">
                <el-input v-model.trim="addForm.qw_external_contact_config[index].value" auto-complete="off" />
              </el-form-item>
            </el-collapse-item>
          </el-collapse>

          <!--  设置  -->
          <el-collapse value="1">
            <el-collapse-item name="1">
              <span slot="title" style="font-weight:bold;font-size:14px;color:#2C8DF4;">设置</span>
              <el-form-item label="动态更新mock" prop="mock_dynamic">
                <el-switch
                  v-model="addForm.mock_dynamic"
                  active-color="#13ce66"
                />
              </el-form-item>
              <el-form-item label="默认环境" prop="is_default">
                <el-switch
                  v-model="addForm.is_default"
                  active-color="#13ce66"
                />
              </el-form-item>
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
import JsonViewer from 'vue-json-viewer'
import {
  addGlobalEnv,
  bulkDeleteGlobalEnv,
  deleteGlobalEnv,
  getGlobalEnvConfigDefault,
  getGlobalEnvQWExternalContactConfigDefault,
  getGlobalEnvData,
  getGlobalEnvList,
  updateGlobalEnv
} from '@/api/apiTest/global_env'

export default {
  name: 'GlobalEnv',
  components: { JsonViewer },
  data() {
    return {
      themeSize: this.$store.state.settings.themeSize,
      tableConfig: {
        isLoading: false,
        height: window.innerHeight - 230 // 下面剩余多少空白部分（即最下面距离底部有多少距离）
      },
      editLoading: false,
      addLoading: false,
      syncLoading: false,
      delLoading: false,
      batchDelLoading: false,
      expanded: true,

      filters: {
        name: ''
      },
      dataList: null,
      total: 0,
      page: 1,
      page_size: 20,
      page_count: 0,
      sels: [], // 列表选中列
      envDefaultConfig: {},

      editFormVisible: false, // 编辑界面是否显示
      // 编辑界面数据规则
      editFormRules: {
        name: [
          { required: true, message: '请输入名称', trigger: 'blur' },
          { min: 1, max: 50, message: '长度在 1 到 50 个字符', trigger: 'blur' }
        ],
        config: [
          { required: true, message: '请输入配置信息', trigger: 'blur' }
        ],
        description: [
          { required: false, message: '请输入描述', trigger: 'blur' },
          { max: 1024, message: '不能超过1024个字符', trigger: 'blur' }
        ]
      },
      // 编辑界面数据
      editForm: {
        name: '',
        config: {},
        mock_dynamic: false,
        is_default: false,
        description: ''
      },

      addFormVisible: false, // 新增界面是否显示
      // 新增界面数据规则
      addFormRules: {
        name: [
          { required: true, message: '请输入名称', trigger: 'blur' },
          { min: 1, max: 50, message: '长度在 1 到 50 个字符', trigger: 'blur' }
        ],
        // config: [
        //   { required: true, message: '请输入配置信息', trigger: 'blur' }
        // ],
        description: [
          { required: false, message: '请输入描述', trigger: 'blur' },
          { max: 1024, message: '不能超过1024个字符', trigger: 'blur' }
        ]
      },
      // 新增界面数据
      addForm: {
        name: '',
        config: {},
        qw_external_contact_config: {},
        data: {},
        mock: {},
        mock_dynamic: false,
        is_default: false,
        description: ''
      }

    }
  },
  created() {
  },
  mounted() {
    this.fetchEnvConfigDefault()
    this.fetchEnvQWExternalContactConfigDefault()
    this.fetchData()
  },
  methods: {
    // 获取ENV列表
    fetchData() {
      this.tableConfig.isLoading = true
      const params = {
        page: this.page,
        page_size: this.page_size,
        name: this.filters.name
      }
      getGlobalEnvList(params).then(response => {
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
    fetchEnvConfigDefault() {
      this.syncLoading = true
      getGlobalEnvConfigDefault({}).then(response => {
        const { msg, code } = response
        this.syncLoading = false
        if (code === 2) {
          this.addForm.config = response.data
          for (const k in response.data) {
            this.addFormRules['config.' + k] = [{ required: true, message: '请输入配置信息' + k, trigger: 'blur' }]
          }
        } else {
          this.$message.error({
            message: msg,
            center: true
          })
        }
      })
    },
    fetchEnvQWExternalContactConfigDefault() {
      this.syncLoading = true
      getGlobalEnvQWExternalContactConfigDefault({}).then(response => {
        const { msg, code } = response
        this.syncLoading = false
        if (code === 2) {
          this.addForm.qw_external_contact_config = response.data
          for (const k in response.data) {
            this.addFormRules['qw_external_contact_config.' + k] = [{ required: true, message: '请输入配置信息' + k, trigger: 'blur' }]
          }
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
        updateGlobalEnv(row.id, { status: false }).then(response => {
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
        updateGlobalEnv(row.id, { status: true }).then(response => {
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
            updateGlobalEnv(Number(this.editForm.id), this.editForm).then(response => {
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
            addGlobalEnv(this.addForm).then(response => {
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
        deleteGlobalEnv(row.id).then(response => {
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
        bulkDeleteGlobalEnv(params).then(response => {
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
    // 获取环境数据并更新到数据库
    handleUpdateEnvData: function(index, row) {
      this.$confirm('确认提交吗？', '提示', {}).then(() => {
        this.syncLoading = true
        getGlobalEnvData(Number(row.id), {}).then(response => {
          const { msg, code } = response
          this.syncLoading = false
          if (code === 2) {
            updateGlobalEnv(Number(row.id), response.data).then(response => {
              const { msg, code } = response
              if (code === 2) {
                this.$message({
                  message: '更新成功',
                  center: true,
                  type: 'success'
                })
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
          } else {
            this.$message.error({
              message: msg,
              center: true
            })
          }
        })
      })
    },
    // 清除env.data
    clearData: function(row) {
      this.$confirm('确认清除env.data数据吗？', '提示', {}).then(() => {
        updateGlobalEnv(Number(row.id), { data: {}}).then(response => {
          const { msg, code } = response
          if (code === 2) {
            this.$message({
              message: '清除成功',
              center: true,
              type: 'success'
            })
            this.fetchData()
          } else if (code === 3) {
            this.$message.error({
              message: msg,
              center: true
            })
          }
        })
      })
    },
    clearMock: function(row) {
      this.$confirm('确认清除env.mock数据吗？', '提示', {}).then(() => {
        updateGlobalEnv(Number(row.id), { mock: {}}).then(response => {
          const { msg, code } = response
          if (code === 2) {
            this.$message({
              message: '清除成功',
              center: true,
              type: 'success'
            })
            this.fetchData()
          } else if (code === 3) {
            this.$message.error({
              message: msg,
              center: true
            })
          }
        })
      })
    },
    // env.data/env.mock 字典key-value 转Array[{key:key, value:value}]
    dictKVToArray: function(src) {
      const dst = []
      for (const k in src) {
        const v = src[k]
        dst.push({ key: k, value: JSON.stringify(v) })
      }
      return dst
    },
    // env.config/env.qw_external_contact_config 字典key:{value:'', description:''} 转Array[{key:key, value:value, description:description}]
    dictConfigToArray: function(src1, src2) {
      const dst = []
      for (const k in src1) {
        const v = src1[k]
        dst.push({ key: k, value: JSON.stringify(v.value), description: v.description })
      }
      for (const k in src2) {
        const v = src2[k]
        dst.push({ key: k, value: JSON.stringify(v.value), description: v.description })
      }
      return dst
    },
    toggleExpanded() {
      this.expanded = !this.expanded
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
