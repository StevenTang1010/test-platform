<template>
  <div class="main">
    <!--  接口基本信息  -->
    <el-collapse v-loading="apiLoading" value="1" style="padding-left: 10px" accordion>
      <el-collapse-item name="1">
        <span slot="title" style="font-weight:bold;font-size:14px;color:#2C8DF4;">接口名：{{ apiInfo.name }}</span>
        <el-container>
          <el-main>
            <el-divider class="blue-line" direction="vertical" />
            <span style="font-weight:bold;font-size:14px;color:#2C8DF4;">基本信息</span>
            <el-card class="box-card" shadow="never">
              <el-row :span="24">
                <el-col :span="4">状态：</el-col>
                <el-col :span="20">
                  <el-tag v-if="apiInfo.status" :size="themeSize" type="success">启用</el-tag>
                  <el-tag v-if="!apiInfo.status" :size="themeSize" type="danger">禁用</el-tag>
                </el-col>
              </el-row>
              <el-row :span="24">
                <el-col :span="4">更新状态：</el-col>
                <el-col :span="20">
                  <el-tag v-if="apiInfo.update_status===0" :size="themeSize" type="danger">待处理</el-tag>
                  <el-tag v-if="apiInfo.update_status===1" :size="themeSize" type="warning">待验证</el-tag>
                  <el-tag v-if="apiInfo.update_status===2" :size="themeSize" type="success">已处理</el-tag>
                </el-col>
              </el-row>
              <el-row :span="24">
                <el-col :span="4">接口路径：</el-col>
                <el-col :span="20">
                  <el-tag v-if="apiInfo.method==='POST'" :size="themeSize">{{ apiInfo.method }}</el-tag>
                  <el-tag v-if="apiInfo.method==='GET'" :size="themeSize" type="success">{{ apiInfo.method }}</el-tag>
                  <el-tag v-if="apiInfo.method==='PUT'" :size="themeSize" type="warning">{{ apiInfo.method }}</el-tag>
                  <el-tag v-if="apiInfo.method==='CALL'" :size="themeSize" type="warning">{{ apiInfo.method }}</el-tag>
                  <el-tag v-if="apiInfo.method==='DELETE'" :size="themeSize" type="danger">{{ apiInfo.method }}</el-tag>
                  {{ apiInfo.path }}
                  <el-button id="copyBtn" :size="themeSize" type="text" class="el-icon-document-copy" :data-clipboard-text="apiInfo.path" @click="copyText($event)" />
                </el-col>
              </el-row>
              <el-row :span="24">
                <el-col :span="4">请求Body：</el-col>
                <el-col :span="20">
                  <span>{{ apiInfo.parameter }}</span>
                </el-col>
              </el-row>
              <el-row :span="24">
                <el-col :span="4">请求Header：</el-col>
                <el-col :span="20">
                  <span>{{ apiInfo.header }}</span>
                </el-col>
              </el-row>
              <el-row :span="24">
                <el-col :span="4">Response：</el-col>
                <el-col :span="20">
                  <span>{{ apiInfo.response }}</span>
                </el-col>
              </el-row>
              <el-row :span="24">
                <el-col :span="4">描述：</el-col>
                <el-col :span="20">{{ apiInfo.description }}</el-col>
              </el-row>
              <el-row :span="24">
                <el-col :span="4">所属部门：</el-col>
                <el-col :span="20">{{ apiInfo.project? (apiInfo.project.department?apiInfo.project.department.name:''):'' }}</el-col>
              </el-row>
              <el-row :span="24">
                <el-col :span="4">所属项目：</el-col>
                <el-col :span="20">{{ apiInfo.project? apiInfo.project.name:'' }}</el-col>
              </el-row>
              <el-row :span="24">
                <el-col :span="4">接口分组：</el-col>
                <el-col :span="20">{{ apiInfo.api_group? apiInfo.api_group.name:'' }}</el-col>
              </el-row>
              <el-row :span="24">
                <el-col :span="4">safe_name：</el-col>
                <el-col :span="20">{{ apiInfo.safe_name }}</el-col>
              </el-row>
              <el-row :span="24">
                <el-col :span="4">上次更新时间：</el-col>
                <el-col :span="20">{{ apiInfo.lastUpdateTime }}</el-col>
              </el-row>
            </el-card>

            <el-row>
              <el-divider class="blue-line" direction="vertical" />
              <span style="font-weight:bold;font-size:14px;color:#2C8DF4;">原始数据</span>
            </el-row>
            <json-viewer
              :key="expanded"
              :value="apiInfo"
              :expand-depth="0"
              :expanded="expanded"
              copyable
              boxed
              sort
            />
          </el-main>
          <!-- 取消、提交 -->
          <el-footer style="align: center">
            <el-button :size="themeSize" type="warning" :loading="editBaseLoading" @click.native="handleEditBase">修改信息</el-button>
          </el-footer>
        </el-container>
      </el-collapse-item>
    </el-collapse>

    <!--编辑接口基本信息界面-->
    <el-drawer
      title="编辑接口"
      :with-header="true"
      :wrapper-closable="false"
      :visible.sync="editBaseFormVisible"
      direction="rtl"
      size="50%"
    >
      <!-- 接口详情 -->
      <div class="demo-drawer__content">
        <el-form ref="editBaseForm" :size="themeSize" :model="editBaseForm" label-width="120px" :rules="editBaseFormRules">
          <!--  基本信息  -->
          <span slot="title" style="font-weight:bold;font-size:14px;color:#2C8DF4;">基本信息</span>
          <el-form ref="editForm" :size="themeSize" :model="editBaseForm" label-width="100px" :rules="editBaseFormRules">
            <el-form-item label="接口名称" prop="name">
              <el-input v-model="editBaseForm.name" auto-complete="off" />
            </el-form-item>
            <el-form-item label="标签">
              <el-select v-model="editBaseForm.labels" value-key="id" placeholder="标签" multiple clearable style="width: 100%">
                <el-option-group v-for="group in globalLabel_options" :key="group.label" :label="group.label">
                  <el-option v-for="item in group.options" :key="item.id" :label="item.name" :value="item" />
                </el-option-group>
              </el-select>
            </el-form-item>
            <el-form-item label="接口路径" prop="path">
              <el-input v-model="editBaseForm.path" auto-complete="off">
                <el-select slot="prepend" v-model="editBaseForm.method" style="width:100px" value-key="id" placeholder="请选择">
                  <el-option v-for="item in method_options" :key="item.id" :label="item.name" :value="item.value" />
                </el-select>
              </el-input>
            </el-form-item>
            <el-form-item label="接口分组" prop="api_group1">
              <el-cascader
                placeholder="搜索：项目/接口分组名"
                :props="{lazy: true, lazyLoad (node, resolve) {deptApiTreeLoad(node, resolve, 2, false)}}"
                style="width: 50%"
                filterable
                clearable
                @change="handleEditCascaderChange"
              >
                <template slot-scope="{ node, data }">
                  <span>{{ data.label }}</span>
                </template>
              </el-cascader>
              <el-button v-if="editBaseForm.api_group" type="text">
                {{ editBaseForm.api_group.name }}->{{ editBaseForm.api_group.name }}
              </el-button>
            </el-form-item>
            <el-row :gutter="24">
              <el-col :span="12">
                <el-form-item label="host_tag" prop="host_tag">
                  <el-select v-model="editBaseForm.host_tag" value-key="value" placeholder="默认mk" clearable style="width: 100%">
                    <el-option v-for="item in host_tag_options" :key="item.id" :label="item.name" :value="item.value" />
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="更新状态" prop="name">
                  <el-select v-model="editBaseForm.update_status" value-key="id" placeholder="请选择">
                    <el-option label="待处理" :value="0" />
                    <el-option label="待验证" :value="1" />
                    <el-option label="已处理" :value="2" />
                  </el-select>
                </el-form-item>
              </el-col>
            </el-row>
            <el-row>
              <el-col :span="24">
                <el-form-item label="状态" prop="status">
                  <el-switch
                    v-model="editBaseForm.status"
                    active-color="#13ce66"
                  />
                </el-form-item>
              </el-col>
            </el-row>
            <el-form-item label="描述" prop="description">
              <el-input v-model="editBaseForm.description" type="textarea" :rows="2" />
            </el-form-item>
          </el-form>
        </el-form>
        <!-- 取消、提交 -->
        <div class="demo-drawer__footer">
          <el-button :size="themeSize" @click.native="editBaseFormVisible = false; editBaseLoading = false">取消</el-button>
          <el-button :size="themeSize" type="primary" :loading="editBaseLoading" @click.native="editBaseSubmit">提交</el-button>
        </div>
      </div>
    </el-drawer>

    <!--YAPI参数定义-->
    <el-collapse v-loading="apiLoading" value="1" style="padding-left: 10px" accordion>
      <el-collapse-item name="2">
        <span slot="title" style="font-weight:bold;font-size:14px;color:#2C8DF4;">YAPI参数定义</span>
        <yapi-parameters-desc :api-info="apiInfo" />
      </el-collapse-item>
    </el-collapse>

    <!--用例模板-->
    <el-collapse v-loading="apiLoading" value="1" style="padding-left: 10px" accordion>
      <el-collapse-item name="3">
        <span slot="title" style="font-weight:bold;font-size:14px;color:#2C8DF4;">用例模板</span>
        <el-container>
          <el-main>
            <el-divider class="blue-line" direction="vertical" />
            <span style="font-weight:bold;font-size:14px;color:#2C8DF4;">请求参数</span>
            <div>
              <el-tabs v-model="requestTabsActiveName">
                <!--  请求参数Body  -->
                <el-tab-pane label="Body" name="body">
                  <request-parameters v-model="apiInfo" />
                </el-tab-pane>
                <!--  请求头 Header -->
                <el-tab-pane label="Header" name="req_headers">
                  <request-headers v-model="apiInfo.req_headers" />
                </el-tab-pane>
              </el-tabs>
            </div>
            <div>
              <el-divider class="blue-line" direction="vertical" />
              <span style="font-weight:bold;font-size:14px;color:#2C8DF4;">期望输出</span>
              <response-validate v-model="apiInfo.validator" />
            </div>
          </el-main>
          <!-- 取消、提交 -->
          <el-footer style="align: center">
            <el-button :size="themeSize" type="primary" :loading="editLoading" @click.native="editSubmit">提交修改</el-button>
            <el-button :size="themeSize" type="warning" :loading="applyLoading" @click.native="handleApply">模板推送</el-button>
          </el-footer>
        </el-container>
      </el-collapse-item>
    </el-collapse>

    <!--用例模板推送-->
    <el-drawer
      title="测试模板数据推送"
      :with-header="true"
      :wrapper-closable="false"
      :visible.sync="applyTemplateVisible"
      direction="rtl"
      size="50%"
    >
      <!-- 接口详情 -->
      <div class="demo-drawer__content">
        <!-- 选择需要推送的数据 -->
        <el-divider class="blue-line" direction="vertical" />
        <span style="font-weight:bold;font-size:14px;color:#2C8DF4;">选择需要推送的数据</span>
        <el-container>
          <el-main>
            <el-checkbox v-model="checkAll" :indeterminate="isIndeterminate" @change="handleCheckAllChange">全选</el-checkbox>
            <div style="margin: 15px 0;" />
            <el-checkbox-group v-model="checkedTemplate" @change="handleCheckedTemplatesChange">
              <el-checkbox v-for="template in templateOptions" :key="template" :label="template">{{ template }}</el-checkbox>
            </el-checkbox-group>
          </el-main>
        </el-container>
        <!-- 选择接收数据的步骤 -->
        <step-list ref="stepListRef" table-name="推送到测试步骤" :show-top-tools="false" :show-bottom-tools="false" />
        <!-- 取消、提交 -->
        <div class="demo-drawer__footer">
          <el-button :size="themeSize" @click.native="applyTemplateVisible = false">取消</el-button>
          <el-button :size="themeSize" type="primary" :loading="applyLoading" @click.native="applySubmit">提交</el-button>
        </div>
      </div>
    </el-drawer>
  </div>

</template>

<script>
import Clipboard from 'clipboard'
import JsonViewer from 'vue-json-viewer'
import { getApiInfoDetail, updateApiInfo } from '@/api/apiTest/api_info'
import YapiParametersDesc from '@/views/apiTest/components/YapiParametersDesc'
import StepList from '@/views/apiTest/caseMgr/StepList'
import { updateTestStep } from '@/api/apiTest/test_step'
import RequestHeaders from '@/views/apiTest/components/RequestHeaders'
import RequestParameters from '@/views/apiTest/components/RequestParameters'
import ResponseValidate from '@/views/apiTest/components/ResponseValidate'
import get_base_data from '@/api/apiTest/get_base_data'

export default {
  name: 'ApiBaseInfo',
  components: { JsonViewer, YapiParametersDesc, RequestHeaders, RequestParameters, ResponseValidate, StepList },
  mixins: [get_base_data],
  data() {
    return {
      themeSize: this.$store.state.settings.themeSize,
      apiLoading: false,
      editLoading: false,
      editBaseLoading: false,
      applyLoading: false,
      expanded: false,
      method_options: [
        { id: 0, name: 'GET', value: 'GET' },
        { id: 1, name: 'POST', value: 'POST' },
        { id: 2, name: 'PUT', value: 'PUT' },
        { id: 3, name: 'DELETE', value: 'DELETE' },
        { id: 4, name: 'CALL', value: 'CALL' }
      ],
      update_status_options: [
        { id: 0, name: '待处理' },
        { id: 1, name: '待验证' },
        { id: 2, name: '已处理' }
      ],
      host_tag_options: [
        { id: 0, name: '服务商后台地址', value: 'mk' },
        { id: 1, name: '企微端地址', value: 'qw' },
        { id: 2, name: '运营计费地址', value: 'oss_bill' },
        { id: 3, name: '运营官方地址', value: 'oss_official' },
        { id: 4, name: '企业微信API', value: 'qyapi' }
      ],

      requestTabsActiveName: 'body',
      apiId: '',
      apiInfo: {
        api_group: null,
        // 用例模板参数
        req_headers: '',
        req_params: '',
        req_json: '',
        req_data: '',
        validator: ''
      },
      suite: [
        {
          tc_list: []
        }
      ],

      // 编辑接口基本信息
      dialogTableVisible: false,
      editBaseFormVisible: false, // 编辑界面是否显示
      // 编辑界面数据规则
      editBaseFormRules: {
        name: [
          { required: true, message: '请输入名称', trigger: 'blur' },
          { min: 1, max: 50, message: '长度在 1 到 50 个字符', trigger: 'blur' }
        ],
        api_group: [
          { required: true, message: '请选择项目分组名称', trigger: 'blur' }
        ],
        description: [
          { required: false, message: '请输入描述', trigger: 'blur' },
          { max: 1024, message: '不能超过1024个字符', trigger: 'blur' }
        ]
      },
      editBaseForm: {},

      // 模板推送
      applyTemplateVisible: false,

      // 选择需要推送的数据
      templateOptions: ['req_headers', 'req_params', 'req_json', 'req_data'],
      checkAll: false,
      checkedTemplate: [],
      isIndeterminate: true
    }
  },
  created() {
    // this.fetchData()
  },
  mounted() {
    if (typeof (this.$route.params.api_id) !== 'undefined') {
      this.fetchData()
    }
  },
  methods: {
    copyText(event) {
      const btnID = '#' + event.currentTarget.id
      console.log(btnID)
      const clipboard = new Clipboard(btnID)
      clipboard.on('success', e => {
        this.$message({
          type: 'success',
          message: '复制成功',
          showClose: true
        })
        clipboard.destroy() // 清楚缓存
      })
      clipboard.on('error', e => {
        this.$message({
          type: 'error',
          message: '复制失败',
          showClose: true
        })
        clipboard.destroy() // 清楚缓存
      })
    },
    fetchData() {
      this.apiLoading = true
      getApiInfoDetail(this.$route.params.api_id).then(response => {
        const { msg, code } = response
        this.apiLoading = false
        if (code === 2) {
          this.apiInfo = response.data
        } else {
          this.$message.error({
            message: msg,
            center: true
          })
        }
      })
    },

    // 显示编辑基础信息界面
    handleEditBase: function() {
      this.getLabel()
      this.editBaseFormVisible = true
      this.editBaseForm = Object.assign({}, this.apiInfo)
    },
    // 接口编辑级联
    handleEditCascaderChange(val) {
      // console.log(val)
      if (val.length > 2) {
        this.editBaseForm.project = val[1]
        this.editBaseForm.api_group = val[2]
      }
    },
    editBaseSubmit() {
      this.$confirm('确认提交吗？', '提示', {}).then(() => {
        this.editBaseLoading = true
        const lablel_ids = []
        for (let j = 0; j < this.editBaseForm.labels.length; j++) {
          lablel_ids.push(this.editBaseForm.labels[j].id)
        }
        const params = {
          name: this.editBaseForm.name,
          description: this.editBaseForm.description,
          project: this.editBaseForm.project ? this.editBaseForm.project.id : null,
          api_group: this.editBaseForm.api_group ? this.editBaseForm.api_group.id : null,
          host_tag: this.editBaseForm.host_tag,
          method: this.editBaseForm.method,
          path: this.editBaseForm.path,
          status: this.editBaseForm.status,
          update_status: this.editBaseForm.update_status,
          labels: lablel_ids
        }
        updateApiInfo(this.editBaseForm.id, params).then(_data => {
          const { msg, code } = _data
          this.editBaseLoading = false
          if (code === 2) {
            this.$message({
              message: '修改成功',
              center: true,
              type: 'success'
            })
            this.editBaseFormVisible = false
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
          }
        }).then(() => {
          this.fetchData()
        })
      })
    },

    editSubmit() {
      this.$confirm('确认提交吗？', '提示', {}).then(() => {
        this.editLoading = true
        const params = {
          req_headers: this.apiInfo.req_headers,
          req_params: this.apiInfo.req_params,
          req_json: this.apiInfo.req_json,
          req_data: this.apiInfo.req_data,
          validator: this.apiInfo.validator
        }
        updateApiInfo(this.apiInfo.id, params).then(_data => {
          const { msg, code } = _data
          this.editLoading = false
          if (code === 2) {
            this.$message({
              message: '修改成功',
              center: true,
              type: 'success'
            })
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
          }
        }).then(() => {
          this.fetchData()
        })
      })
    },

    // 显示模板推送到测试步骤的窗口
    handleApply() {
      this.applyTemplateVisible = true
    },
    handleCheckAllChange(val) {
      this.checkedTemplate = val ? this.templateOptions : []
      this.isIndeterminate = false
    },
    handleCheckedTemplatesChange(value) {
      const checkedCount = value.length
      this.checkAll = checkedCount === this.templateOptions.length
      this.isIndeterminate = checkedCount > 0 && checkedCount < this.templateOptions.length
    },
    applySubmit() {
      const params = {}
      for (let i = 0; i < this.checkedTemplate.length; i++) {
        const k = this.checkedTemplate[i]
        const v = this.apiInfo[k]
        params[k] = v ? JSON.stringify(JSON.parse(v)) : ''
      }
      const step_list = this.$refs.stepListRef.sels
      for (let j = 0; j < step_list.length; j++) {
        const step = step_list[j]
        this.editLoading = true
        updateTestStep(step.id, params).then(_data => {
          const { msg, code } = _data
          this.editLoading = false
          if (code === 2) {
            this.$message({
              message: '修改成功',
              center: true,
              type: 'success'
            })
            this.$refs.stepListRef.fetchData()
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
            this.$refs.stepListRef.fetchData()
          }
        })
      }
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
