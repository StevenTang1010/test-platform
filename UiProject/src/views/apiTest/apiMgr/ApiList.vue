<template>
  <div class="main">
    <el-divider class="blue-line" direction="vertical" />
    <span slot="title" style="font-weight:bold;font-size:14px;color:#2C8DF4;">{{ tableName }}</span>

    <!--顶部工具条-->
    <el-col :span="24" class="toolbar" style="padding-bottom: 0;padding-top: 10px;">
      <el-form :inline="true" :model="filters" :size="themeSize" @submit.native.prevent>
        <el-form-item>
          <el-input v-model="filters.name" placeholder="名称" clearable @keyup.enter.native="fetchData" />
        </el-form-item>
        <el-form-item>
          <el-input v-model="filters.path" placeholder="path" clearable @keyup.enter.native="fetchData" />
        </el-form-item>
        <el-form-item>
          <el-select v-model="filters.project" value-key="id" style="min-width: 230px" multiple placeholder="所属项目" filterable clearable>
            <el-option v-for="item in project_options" :key="item.id" :label="item.name" :value="item" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-select v-model="filters.api_group" value-key="id" placeholder="所属接口分组" clearable>
            <el-option v-for="item in api_group_options" :key="item.id" :label="item.name" :value="item" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-select v-model="filters.update_status" value-key="id" multiple placeholder="更新状态" clearable>
            <el-option v-for="item in update_status_options" :key="item.id" :label="item.name" :value="item" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="fetchData">查询</el-button>
        </el-form-item>
        <el-form-item>
          <el-button type="default" @click.native="filterClear">重置</el-button>
        </el-form-item>
        <el-popover style="margin-left: 5px" trigger="click">
          <div style="text-align: left">
            <el-button type="primary" :size="themeSize" @click="handleAdd">新增</el-button>
            <el-button type="warning" :size="themeSize" :loading="syncLoading" @click="handleSyncYAPI(['all'])">同步YAPI</el-button>
            <el-button type="warning" :size="themeSize" :loading="updateTemplateLoading" @click="handleUpdateTemplate(['all'])">更新模板</el-button>
          </div>
          <el-button slot="reference" icon="el-icon-more" title="更多" circle :size="themeSize" />
        </el-popover>
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
      @cell-mouse-enter="cellMouseEnter"
      @cell-mouse-leave="cellMouseLeave"
      @selection-change="selsChange"
    >
      <el-table-column fixed type="selection" />
      <el-table-column prop="id" label="ID" sortable show-overflow-tooltip width="80" />
      <el-table-column prop="name" label="接口名称" sortable show-overflow-tooltip width="200">
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
      <el-table-column label="接口路径" sortable show-overflow-tooltip width="400">
        <template slot-scope="scope">
          <el-tag v-if="scope.row.method==='POST'" :size="themeSize">{{ scope.row.method }}</el-tag>
          <el-tag v-if="scope.row.method==='GET'" :size="themeSize" type="success">{{ scope.row.method }}</el-tag>
          <el-tag v-if="scope.row.method==='PUT'" :size="themeSize" type="warning">{{ scope.row.method }}</el-tag>
          <el-tag v-if="scope.row.method==='CALL'" :size="themeSize" type="warning">{{ scope.row.method }}</el-tag>
          <el-tag v-if="scope.row.method==='DELETE'" :size="themeSize" type="danger">{{ scope.row.method }}</el-tag>
          {{ scope.row.path }}
        </template>
      </el-table-column>
      <el-table-column prop="description" label="描述" sortable show-overflow-tooltip width="200" />
      <el-table-column prop="origin" label="数据来源" sortable show-overflow-tooltip width="100" />
      <el-table-column prop="project.department.name" label="部门" sortable show-overflow-tooltip width="100" />
      <el-table-column prop="project.name" label="项目" sortable show-overflow-tooltip width="200" />
      <el-table-column prop="api_group.name" label="分组" sortable show-overflow-tooltip width="200" />
      <el-table-column prop="test_case_count" label="用例" sortable show-overflow-tooltip width="70" />
      <el-table-column prop="labels" label="标签" show-overflow-tooltip width="200">
        <template slot-scope="scope">
          <el-tag v-for="item in scope.row.labels" :key="item.id" :size="themeSize">{{ item.name }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="update_status_name" label="更新" sortable width="100">
        <template slot-scope="scope">
          <el-tag v-if="scope.row.update_status===0" :size="themeSize" type="danger">待处理</el-tag>
          <el-tag v-if="scope.row.update_status===1" :size="themeSize" type="warning">待验证</el-tag>
          <el-tag v-if="scope.row.update_status===2" :size="themeSize" type="success">已处理</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="status" label="状态" sortable width="100">
        <template slot-scope="scope">
          <img v-show="scope.row.status" src="@/assets/icon-yes.svg" alt="">
          <img v-show="!scope.row.status" src="@/assets/icon-no.svg" alt="">
        </template>
      </el-table-column>
      <el-table-column prop="yapi_id" label="YAPI ID" sortable show-overflow-tooltip width="100" />
      <el-table-column fixed="right" label="操作" width="200">
        <template slot-scope="scope">
          <el-row>
            <el-button type="info" icon="el-icon-edit" circle :size="themeSize" title="编辑接口" @click="handleEdit(scope.$index, scope.row)" />
            <el-button type="info" icon="el-icon-document-copy" circle :size="themeSize" title="复制接口" @click="handleCopy(scope.$index, scope.row)" />
            <el-button type="primary" icon="el-icon-caret-right" circle :size="themeSize" title="运行接口" @click="handleRunAPI(scope.row.id, scope.row.name)" />
            <el-popover style="margin-left: 10px" trigger="hover">
              <div style="text-align: center">
                <el-button type="primary" icon="el-icon-refresh" circle :size="themeSize" :loading="syncLoading" title="同步YAPI" @click="handleSyncYAPI([scope.row])" />
                <el-button type="primary" icon="el-icon-magic-stick" circle :size="themeSize" :loading="updateTemplateLoading" title="更新模板" @click="handleUpdateTemplate([scope.row])" />
                <el-button type="warning" icon="el-icon-s-flag" circle :size="themeSize" :title="scope.row.status===false?'启用':'禁用'" @click="handleChangeStatus(scope.$index, scope.row)" />
                <el-button type="danger" icon="el-icon-delete" circle :size="themeSize" :loading="delLoading" title="删除接口" @click="handleDel(scope.$index, scope.row)" />
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
        <el-button :loading="bulkSyncLoading" type="primary" plain :disabled="sels.length===0" :size="themeSize" @click="handleSyncYAPI(sels)">同步YAPI</el-button>
        <el-button :loading="bulkUpdateLoading" type="primary" plain :disabled="sels.length===0" :size="themeSize" @click="handleUpdateTemplate(sels)">更新模板</el-button>
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
        <el-form-item label="所属分组" prop="api_group">
          <el-cascader
            placeholder="搜索：项目/接口分组名"
            :props="{lazy: true, lazyLoad (node, resolve) {deptApiTreeLoad(node, resolve, 2, false)}}"
            lazy
            style="width: 100%"
            filterable
            clearable
            @change="handleBulkEditCascaderChange"
          >
            <template slot-scope="{ node, data }">
              <span>{{ data.label }}</span>
            </template>
          </el-cascader>
        </el-form-item>
        <el-form-item label="host_tag" prop="host_tag">
          <el-select v-model="bulkEditForm.host_tag" value-key="value" placeholder="默认mk：服务商后台地址" clearable style="width: 100%">
            <el-option v-for="item in host_tag_options" :key="item.id" :label="item.name" :value="item.value" />
          </el-select>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button :size="themeSize" @click.native="bulkEditFormVisible = false">取消</el-button>
        <el-button :size="themeSize" type="primary" @click.native="bulkEdit()">确定</el-button>
      </div>
    </el-dialog>

    <!--编辑接口界面-->
    <el-drawer
      title="编辑接口"
      :with-header="true"
      :wrapper-closable="false"
      :visible.sync="editFormVisible"
      direction="rtl"
      size="50%"
    >
      <!-- 接口详情 -->
      <div class="demo-drawer__content">
        <el-form ref="editForm" :size="themeSize" :model="editForm" label-width="120px" :rules="editFormRules">
          <!--  基本信息  -->
          <el-collapse value="1" @change="handleChange">
            <el-collapse-item name="1">
              <span slot="title" style="font-weight:bold;font-size:14px;color:#2C8DF4;">基本信息</span>
              <el-form ref="editForm" :size="themeSize" :model="editForm" label-width="100px" :rules="editFormRules">
                <el-form-item label="接口名称" prop="name">
                  <el-input v-model="editForm.name" auto-complete="off" />
                </el-form-item>
                <el-form-item label="标签">
                  <el-select v-model="editForm.labels" value-key="id" placeholder="标签" multiple clearable style="width: 100%">
                    <el-option-group v-for="group in globalLabel_options" :key="group.label" :label="group.label">
                      <el-option v-for="item in group.options" :key="item.id" :label="item.name" :value="item" />
                    </el-option-group>
                  </el-select>
                </el-form-item>
                <el-form-item label="接口路径" prop="path">
                  <el-input v-model="editForm.path" auto-complete="off">
                    <el-select slot="prepend" v-model="editForm.method" style="width:100px" value-key="id" placeholder="请选择">
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
                  <el-button v-if="editForm.api_group" type="text">
                    {{ editForm.api_group.name }}->{{ editForm.api_group.name }}
                  </el-button>
                </el-form-item>
                <el-row :gutter="24">
                  <el-col :span="12">
                    <el-form-item label="HttpType" prop="http_type">
                      <el-select v-model="editForm.http_type" value-key="id" placeholder="请选择">
                        <el-option label="HTTP" value="HTTP" />
                        <el-option label="HTTPS" value="HTTPS" />
                      </el-select>
                    </el-form-item>
                  </el-col>
                </el-row>
                <el-row :gutter="24">
                  <el-col :span="12">
                    <el-form-item label="host_tag" prop="host_tag">
                      <el-select v-model="editForm.host_tag" value-key="value" placeholder="默认mk" clearable style="width: 100%">
                        <el-option v-for="item in host_tag_options" :key="item.id" :label="item.name" :value="item.value" />
                      </el-select>
                    </el-form-item>
                  </el-col>
                  <el-col :span="12">
                    <el-form-item label="更新状态" prop="name">
                      <el-select v-model="editForm.update_status" value-key="id" placeholder="请选择">
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
                        v-model="editForm.status"
                        active-color="#13ce66"
                      />
                    </el-form-item>
                  </el-col>
                </el-row>
                <el-form-item label="描述" prop="description">
                  <el-input v-model="editForm.description" type="textarea" :rows="2" />
                </el-form-item>
              </el-form>
            </el-collapse-item>
          </el-collapse>

          <!--  YAPI 参数定义  -->
          <el-collapse value="1" @change="handleChange">
            <el-collapse-item name="2">
              <span slot="title" style="font-weight:bold;font-size:14px;color:#2C8DF4;">YAPI参数定义</span>
              <yapi-parameters-desc :api-info="editForm" />
            </el-collapse-item>
          </el-collapse>

          <!--  用例模板  -->
          <el-collapse value="1" @change="handleChange">
            <el-collapse-item name="1">
              <span slot="title" style="font-weight:bold;font-size:14px;color:#2C8DF4;">用例模板</span>
              <el-divider class="blue-line" direction="vertical" />
              <span style="font-weight:bold;font-size:14px;color:#2C8DF4;">请求参数</span>
              <div>
                <el-tabs v-model="requestTabsActiveName" @tab-click="handleClick">
                  <!--  请求参数Body  -->
                  <el-tab-pane label="Body" name="body">
                    <request-parameters v-model="editForm" />
                  </el-tab-pane>
                  <!--  请求头 Header -->
                  <el-tab-pane label="Header" name="req_headers">
                    <request-headers v-model="editForm.req_headers" />
                  </el-tab-pane>
                </el-tabs>
              </div>
              <div>
                <el-divider class="blue-line" direction="vertical" />
                <span style="font-weight:bold;font-size:14px;color:#2C8DF4;">期望输出</span>
                <response-validate v-model="editForm.validator" />
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

    <!--新增接口界面-->
    <el-drawer
      title="新增接口"
      :with-header="true"
      :wrapper-closable="false"
      :visible.sync="addFormVisible"
      direction="rtl"
      size="50%"
    >
      <!-- 接口详情 -->
      <div class="demo-drawer__content">
        <el-form ref="addForm" :size="themeSize" :model="addForm" label-width="90px" :rules="addFormRules">
          <!--  基本信息  -->
          <el-collapse value="1" @change="handleChange">
            <el-collapse-item name="1">
              <span slot="title" style="font-weight:bold;font-size:14px;color:#2C8DF4;">基本信息</span>
              <el-form-item label="接口名称" prop="name">
                <el-input v-model="addForm.name" auto-complete="off" />
              </el-form-item>
              <el-form-item label="标签">
                <el-select v-model="addForm.labels" value-key="id" placeholder="标签" multiple clearable style="width: 100%">
                  <el-option-group v-for="group in globalLabel_options" :key="group.label" :label="group.label">
                    <el-option v-for="item in group.options" :key="item.id" :label="item.name" :value="item" />
                  </el-option-group>
                </el-select>
              </el-form-item>
              <el-form-item label="接口路径" prop="path">
                <el-input v-model="addForm.path" auto-complete="off">
                  <el-select slot="prepend" v-model="addForm.method" style="width:100px" value-key="id" placeholder="请选择">
                    <el-option v-for="item in method_options" :key="item.id" :label="item.name" :value="item.value" />
                  </el-select>
                </el-input>
              </el-form-item>
              <el-form-item label="接口分组" prop="api_group">
                <el-cascader
                  placeholder="搜索：项目/接口分组名"
                  :props="{lazy: true, lazyLoad (node, resolve) {deptApiTreeLoad(node, resolve, 2, false)}}"
                  lazy
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
              <el-row :gutter="24">
                <el-col :span="12">
                  <el-form-item label="HttpType" prop="http_type">
                    <el-select v-model="addForm.http_type" value-key="id" placeholder="请选择">
                      <el-option label="HTTP" value="HTTP" />
                      <el-option label="HTTPS" value="HTTPS" />
                    </el-select>
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="host_tag" prop="host_tag">
                    <el-select v-model="addForm.host_tag" value-key="value" placeholder="默认mk" clearable style="width: 100%">
                      <el-option v-for="item in host_tag_options" :key="item.id" :label="item.name" :value="item.value" />
                    </el-select>
                  </el-form-item>
                </el-col>
              </el-row>
              <el-row>
                <el-col :span="12">
                  <el-form-item label="状态" prop="status">
                    <el-switch
                      v-model="addForm.status"
                      active-color="#13ce66"
                    />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="更新状态" prop="name">
                    <el-select v-model="addForm.update_status" value-key="id" placeholder="请选择">
                      <el-option label="待处理" :value="0" />
                      <el-option label="待验证" :value="1" />
                      <el-option label="已处理" :value="2" />
                    </el-select>
                  </el-form-item>
                </el-col>
              </el-row>
              <el-form-item label="描述" prop="description">
                <el-input v-model="addForm.description" type="textarea" :rows="2" />
              </el-form-item>
            </el-collapse-item>
          </el-collapse>

          <!--  请求 - Request  -->
          <el-collapse value="1" @change="handleChange">
            <el-collapse-item name="1">
              <span slot="title" style="font-weight:bold;font-size:14px;color:#2C8DF4;">请求</span>
              <el-tabs v-model="requestTabsActiveName" type="card" @tab-click="handleClick">
                <!--  请求参数Body  -->
                <el-tab-pane label="Body" name="body">
                  <request-parameters v-model="addForm" />
                </el-tab-pane>
                <!--  请求头 Header -->
                <el-tab-pane label="Header" name="req_headers">
                  <request-headers v-model="addForm.req_headers" />
                </el-tab-pane>
              </el-tabs>
            </el-collapse-item>
          </el-collapse>

          <!--  期望输出 - Response  -->
          <el-collapse value="1" @change="handleChange">
            <el-collapse-item name="1">
              <span slot="title" style="font-weight:bold;font-size:14px;color:#2C8DF4;">期望输出</span>
              <response-validate v-model="addForm.validator" />
            </el-collapse-item>
          </el-collapse>
        </el-form>
        <!-- 取消、提交 -->
        <div class="demo-drawer__footer">
          <el-button :size="themeSize" @click.native="addFormVisible = false; editLoading = false">取消</el-button>
          <el-button :size="themeSize" type="primary" :loading="editLoading" @click.native="addSubmit">提交</el-button>
        </div>
      </div>
    </el-drawer>

  </div>
</template>

<script>
import {
  addApiInfo,
  bulkDeleteApiInfo,
  bulkUpdateApiInfo,
  dataSyncYapi,
  deleteApiInfo,
  getApiInfoList,
  getDuplicateApiInfoList,
  getNoCaseApiInfoList,
  getToDoApiInfoList,
  updateApiInfo,
  updateCaseTemplate
} from '@/api/apiTest/api_info'
import Clipboard from 'clipboard'
import get_base_data from '@/api/apiTest/get_base_data'
import YapiParametersDesc from '@/views/apiTest/components/YapiParametersDesc'
import RequestHeaders from '@/views/apiTest/components/RequestHeaders'
import RequestParameters from '@/views/apiTest/components/RequestParameters'
import ResponseValidate from '@/views/apiTest/components/ResponseValidate'
import { syncUpdateStatusToApiUpdateHistory } from '@/api/apiTest/api_update_history'

export default {
  name: 'ApiList',
  components: { YapiParametersDesc, RequestHeaders, RequestParameters, ResponseValidate },
  mixins: [get_base_data],
  props: {
    fetchDataMethod: {
      type: String,
      default() {
        return '' // getNoCaseApi | getToDoApi
      }
    },
    projectId: {
      type: String,
      default() {
        return ''
      }
    },
    tableName: {
      type: String,
      default() {
        return '接口列表'
      }
    }
  },
  data() {
    return {
      // 公共
      themeSize: this.$store.state.settings.themeSize,
      tableConfig: {
        isLoading: false,
        height: window.innerHeight - 275 // 下面剩余多少空白部分（即最下面距离底部有多少距离）
      },
      editLoading: false,
      addLoading: false,
      syncLoading: false,
      updateTemplateLoading: false,
      delLoading: false,
      bulkSyncLoading: false,
      bulkUpdateLoading: false,
      bulkDelLoading: false,
      requestTabsActiveName: 'body',
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

      // 接口列表
      total: 0,
      page_count: 0,
      page: 1,
      page_size: 20,
      dataList: null,
      filters: {
        name: null,
        path: null,
        project: [],
        api_group: '',
        project__isnull: null,
        api_group__isnull: null,
        update_status: []
      },
      sels: [], // 列表选中列
      api_group_options: [],

      // 编辑接口
      dialogTableVisible: false,
      editFormVisible: false, // 编辑界面是否显示
      // 编辑界面数据规则
      editFormRules: {
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
      // 编辑界面数据
      editForm: {
        name: '',
        description: '',
        project: { id: '', name: '' },
        api_group: { id: '', name: '' },
        http_type: 'HTTPS',
        host_tag: '',
        method: 'GET',
        path: '',
        // YAPI参数定义
        yapi_req_headers: '',
        yapi_req_params: '',
        yapi_req_query: '',
        yapi_req_body_form: '',
        yapi_req_body_other: '',
        yapi_res_body: '',
        // 用例模板参数
        req_headers: '',
        req_params: '',
        req_json: '',
        req_data: '',
        validator: '',
        // 状态
        status: true,
        update_status: 0,
        labels: []
      },

      // 新增接口
      addFormVisible: false, // 新增界面是否显示
      // 新增界面数据规则
      addFormRules: {
        name: [
          { required: true, message: '请输入名称', trigger: 'blur' },
          { min: 1, max: 50, message: '长度在 1 到 50 个字符', trigger: 'blur' }
        ],
        project: [
          { required: true, message: '请选择所属项目', trigger: 'blur' }
        ],
        api_group: [
          { required: true, message: '请选择所属分组', trigger: 'blur' }
        ],
        path: [
          { required: true, message: '请输入接口地址', trigger: 'blur' }
        ],
        description: [
          { required: false, message: '请输入版本号', trigger: 'blur' },
          { max: 1024, message: '不能超过1024个字符', trigger: 'blur' }
        ]
      },
      // 新增界面数据
      addForm: {
        name: '',
        description: '',
        project: { id: '', name: '' },
        api_group: { id: '', name: '' },
        http_type: 'HTTPS',
        method: 'GET',
        path: '',
        // YAPI参数定义
        yapi_req_headers: '',
        yapi_req_params: '',
        yapi_req_query: '',
        yapi_req_body_form: '',
        yapi_req_body_other: '',
        yapi_res_body: '',
        // 用例模板参数
        req_headers: '',
        req_params: '',
        req_json: '',
        req_data: '',
        validator: '',
        // 状态
        status: true,
        update_status: 0,
        labels: []
      },

      // 批量处理
      bulkEditFormVisible: false,
      bulkEditForm: {
        project: null,
        api_group: null,
        host_tag: null
      },
      bulkStatus: true,

      // 批量修改接口分组
      bulkApiGroupLoading: false,
      bulkApiGroupFormVisible: false, // 批量修改接口分组界面是否显示
      bulkApiGroupFormRules: {
        name: [
          { required: true, message: '请输入名称', trigger: 'blur' },
          { min: 1, max: 50, message: '长度在 1 到 50 个字符', trigger: 'blur' }
        ],
        description: [
          { required: false, message: '请输入描述', trigger: 'blur' },
          { max: 1024, message: '不能超过1024个字符', trigger: 'blur' }
        ]
      },
      bulkApiGroupForm: {
        api_group: ''
      }
    }
  },
  created() {
  },
  mounted() {
    this.getLabel(['优先级'])
    this.getProject()
    this.getApiGroup()
    // this.fetchData()
  },
  methods: {
    // ========== 公共 ==========
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
    // 清空所有下拉框
    filterClear() {
      this.filters.name = null
      this.filters.path = null
      this.filters.api_group = {}
      this.filters.update_status = []
    },
    // 标签页 click
    handleClick(tab, event) {
      console.log(tab, event)
    },
    // 查询接口列表
    fetchData() {
      const project_ids = []
      for (let i = 0; i < this.filters.project.length; i++) {
        project_ids.push(this.filters.project[i].id)
      }
      const update_status_ids = []
      for (let i = 0; i < this.filters.update_status.length; i++) {
        update_status_ids.push(this.filters.update_status[i].id)
      }
      const params = {
        page: this.page,
        page_size: this.page_size,
        name_icontains: this.filters.name,
        path_icontains: this.filters.path,
        project__id__in: project_ids.length > 0 ? project_ids.join(',') : null,
        update_status__in: update_status_ids.length > 0 ? update_status_ids.join(',') : null,
        api_group: this.filters.api_group.id,
        project__isnull: this.filters.project__isnull,
        api_group__isnull: this.filters.api_group__isnull
      }
      this.tableConfig.isLoading = true
      if (this.fetchDataMethod === 'getNoCaseApi') {
        getNoCaseApiInfoList(params).then(response => {
          this.dataList = response.data.list
          this.total = response.data.count
          this.tableConfig.isLoading = false
        })
      } else if (this.fetchDataMethod === 'getToDoApi') {
        getToDoApiInfoList(params).then(response => {
          this.dataList = response.data.list
          this.total = response.data.count
          this.tableConfig.isLoading = false
        })
      } else if (this.fetchDataMethod === 'getDuplicateApi') {
        getDuplicateApiInfoList(params).then(response => {
          this.dataList = response.data.list
          this.total = response.data.count
          this.tableConfig.isLoading = false
        })
      } else {
        getApiInfoList(params).then(response => {
          this.dataList = response.data.list
          this.total = response.data.count
          this.tableConfig.isLoading = false
        })
      }
    },

    // ========== 接口 ==========
    clearAddForm() {
      this.addForm = {
        name: '',
        description: '',
        project: { id: '', name: '' },
        api_group: { id: '', name: '' },
        http_type: 'HTTPS',
        method: 'GET',
        path: '',
        req_headers: '',
        req_params: '',
        req_json: '',
        req_data: '',
        validator: '',
        status: true,
        update_status: 0,
        labels: []
      }
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
    // 接口编辑级联
    handleEditCascaderChange(val) {
      // console.log(val)
      if (val.length > 2) {
        this.editForm.project = val[1]
        this.editForm.api_group = val[2]
      }
    },
    // 接口新增级联
    handleAddCascaderChange(val) {
      // console.log(val)
      if (val.length > 2) {
        this.addForm.project = val[1]
        this.addForm.api_group = val[2]
      }
    },
    // 接口批量编辑级联
    handleBulkEditCascaderChange(val) {
      // console.log(val)
      if (val.length > 2) {
        this.bulkEditForm.project = val[1].id
        this.bulkEditForm.api_group = val[2].id
      }
    },
    copyText(event) {
      const btnID = '#' + event.currentTarget.id
      // console.log(btnID)
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
    prettyPrintParameter(space = 2) {
      const obj = JSON.parse(this.editForm.parameter)
      this.editForm.parameter = JSON.stringify(obj, undefined, space)
    },
    // 显示编辑界面
    handleEdit: function(index, row) {
      this.editFormVisible = true
      this.editForm = Object.assign({}, row)
    },
    // 复制接口
    handleCopy: function(index, row) {
      this.addFormVisible = true
      this.addForm = Object.assign({}, row)
      this.addForm.name += '-copy'
      this.addForm.description += '-copy'
      this.addForm.status = true
    },
    // 显示新增界面
    handleAdd: function() {
      this.clearAddForm()
      this.addFormVisible = true
    },
    // 改变接口分组
    handleChangeApiGroup: function(index, row, group_id) {
      updateApiInfo(row.id, { api_group: group_id }).then(response => {
        const { code, msg } = response
        if (code === 2) {
          this.$message({
            message: '修改分组成功',
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
    // 改变接口状态
    handleChangeStatus: function(index, row) {
      let params, opt
      if (row.status) {
        opt = '禁用'
        params = { status: false }
      } else {
        opt = '启用'
        params = { status: true }
      }
      updateApiInfo(row.id, params).then(response => {
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
    // 拉取YAPI数据并同步
    handleSyncYAPI: function(rows) {
      this.$confirm('确认拉取选中接口YAPI数据吗？', '提示', {
        type: 'warning'
      }).then(() => {
        this.syncLoading = true
        dataSyncYapi(rows).then(response => {
          const { msg, code } = response
          this.syncLoading = false
          if (code === 2) {
            this.$message({
              message: '同步成功',
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
          this.fetchData()
        })
      })
    },
    // 更新用例模板
    handleUpdateTemplate: function(rows) {
      this.$confirm('确认更新选中接口用例模板吗？', '提示', {
        type: 'warning'
      }).then(() => {
        this.updateTemplateLoading = true
        updateCaseTemplate(rows).then(response => {
          const { msg, code } = response
          this.updateTemplateLoading = false
          if (code === 2) {
            this.$message({
              message: '模板更新成功',
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

    // 编辑
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
              description: this.editForm.description,
              project: this.editForm.project ? this.editForm.project.id : null,
              api_group: this.editForm.api_group ? this.editForm.api_group.id : null,
              host_tag: this.editForm.host_tag,
              http_type: this.editForm.http_type,
              method: this.editForm.method,
              path: this.editForm.path,
              req_headers: this.editForm.req_headers,
              req_params: this.editForm.req_params,
              req_json: this.editForm.req_json,
              req_data: this.editForm.req_data,
              validator: this.editForm.validator,
              status: this.editForm.status,
              update_status: this.editForm.update_status,
              labels: lablel_ids
            }
            updateApiInfo(this.editForm.id, params).then(_data => {
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
            }).then(() => {
              syncUpdateStatusToApiUpdateHistory({
                api_id: this.editForm.id,
                update_status: this.editForm.update_status
              })
              this.fetchData()
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
            const lablel_ids = []
            for (let j = 0; j < this.addForm.labels.length; j++) {
              lablel_ids.push(this.addForm.labels[j].id)
            }
            const params = {
              name: this.addForm.name,
              description: this.addForm.description,
              project: this.addForm.project.id,
              api_group: this.addForm.api_group.id,
              host_tag: this.addForm.host_tag,
              http_type: this.addForm.http_type,
              method: this.addForm.method,
              path: this.addForm.path,
              req_headers: this.addForm.req_headers,
              req_params: this.addForm.req_params,
              req_json: this.addForm.req_json,
              req_data: this.addForm.req_data,
              validator: this.addForm.validator,
              status: this.addForm.status,
              update_status: this.addForm.update_status,
              labels: lablel_ids
            }
            addApiInfo(params).then(_data => {
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
        deleteApiInfo(row.id).then(response => {
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
        bulkUpdateApiInfo(dataArr).then(response => {
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
      bulkUpdateApiInfo(dataArr).then(response => {
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
    // 批量删除
    bulkRemove: function() {
      const ids = this.sels.map(item => item.id)
      this.$confirm('确认删除选中记录吗？', '提示', {
        type: 'warning'
      }).then(() => {
        const params = {
          id_in: ids.join(',')
        }
        bulkDeleteApiInfo(params).then(response => {
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
    // 批量修改分组
    handleBatchChangeApiGroup() {
      this.bulkApiGroupFormVisible = true
    },
    bulkChangeApiGroup() {
      const ids = this.sels.map(item => item.id)
      // NProgress.start();
      const params = {
        api_group: this.bulkApiGroupForm.api_group.id
      }
      for (let i = 0; i < ids.length; i++) {
        updateApiInfo(ids[i], params).then(response => {
          const { code, msg } = response
          if (code === 2) {
            this.$message({
              message: '分组修改成功',
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
      this.bulkApiGroupFormVisible = false
      this.fetchData()
    },

    // 运行API
    handleRunAPI: function() {
      this.$message.warning('TODO')
    },
    // 批量运行API
    bulkRunAPI: function() {
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
