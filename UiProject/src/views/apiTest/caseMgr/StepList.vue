<template>
  <div class="main">
    <el-divider class="blue-line" direction="vertical" />
    <span style="font-weight:bold;font-size:14px;color:#2C8DF4;">{{ tableName }}</span>

    <!--顶部工具条-->
    <el-col v-show="showTopTools" :span="24" class="toolbar">
      <el-form ref="filters" :inline="true" :v-model="filters" :size="themeSize" @submit.native.prevent>
        <el-form-item v-if="showMoreFilters" style="width: 150px">
          <el-select v-model="filters.id" placeholder="用例步骤ID" value-key="id" multiple filterable allow-create clearable @keyup.enter.native="fetchData">
            <span slot="empty" class="el-select-dropdown__empty">请输入用例步骤ID</span>
            <el-option v-for="item in []" :key="item.value" :label="item.label" :value="item.value.replace(/[^\d]/g,'')" />
          </el-select>
        </el-form-item>
        <el-form-item style="width: 150px">
          <el-input v-model="filters.name" placeholder="用例步骤名称" clearable @keyup.enter.native="fetchData" />
        </el-form-item>
        <el-form-item style="width: 150px">
          <el-input v-model="filters.description" placeholder="用例步骤描述" clearable @keyup.enter.native="fetchData" />
        </el-form-item>
        <el-form-item style="width: 150px">
          <el-select v-model="filters.result" value-key="id" multiple placeholder="测试结果" clearable>
            <el-option label="passed" value="passed" />
            <el-option label="failed" value="failed" />
            <el-option label="skipped" value="skipped" />
            <el-option label="error" value="error" />
            <el-option label="未执行" value="null" />
          </el-select>
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
          <el-button type="primary" @click="handleAdd">新增步骤</el-button>
        </el-form-item>
        <el-form-item v-if="allowUpdateStepId">
          <el-button type="primary" @click="openDragSort">修改顺序</el-button>
        </el-form-item>
        <el-form-item v-if="allowUpdateStepId&&saveSortBtnShow">
          <el-button type="primary" @click="bulkUpdateStepId">保存顺序</el-button>
        </el-form-item>
        <el-form-item>
          <el-button type="default" @click.native="filterClear">重置</el-button>
        </el-form-item>
      </el-form>
    </el-col>

    <!--列表-->
    <el-table
      ref="sortTable"
      v-loading="tableConfig.isLoading"
      class="stepTable"
      :data="dataList"
      element-loading-text="Loading"
      border
      fit
      highlight-current-row
      :size="themeSize"
      :height="tableConfig.height"
      style="width: 100%"
      row-key="id"
      :default-sort="{prop: 'sid', order: 'ascending'}"
      @cell-mouse-enter="cellMouseEnter"
      @cell-mouse-leave="cellMouseLeave"
      @selection-change="selsChange"
    >
      <el-table-column fixed type="selection" />
      <el-table-column prop="sid" label="步骤" sortable width="70" />
      <el-table-column prop="name" label="名称" sortable show-overflow-tooltip width="200">
        <template slot-scope="scope">
          <img v-show="scope.row.status" src="@/assets/icon-yes.svg" alt="">
          <img v-show="!scope.row.status" src="@/assets/icon-no.svg" alt="">
          {{ scope.row.name }}
        </template>
      </el-table-column>
      <el-table-column prop="description" label="描述" sortable show-overflow-tooltip width="200" />
      <el-table-column prop="apiInfo" label="接口路径" show-overflow-tooltip width="350">
        <template slot-scope="scope">
          <el-popover
            placement="right"
            width="600"
            trigger="click"
          >
            <el-card class="box-card" shadow="never">
              <div slot="header" class="clearfix">
                接口信息：{{ scope.row.apiInfo.name }}
                <el-button style="float: right; padding: 3px 0" type="text">
                  <router-link
                    :to="{ name: '接口详情', params: {api_id: scope.row.apiInfo.id}}"
                    style="cursor:pointer;color: #0000ff"
                    target="_blank"
                  >
                    详情
                  </router-link>
                </el-button>
              </div>
              <el-description>
                <el-description-item label="状态" :span-map="{md:12}">
                  <template slot="content">
                    <el-tag v-if="scope.row.apiInfo.status" :size="themeSize" type="success">启用</el-tag>
                    <el-tag v-if="!scope.row.apiInfo.status" :size="themeSize" type="danger">禁用</el-tag>
                  </template>
                </el-description-item>
                <el-description-item label="更新状态" :span-map="{md:12}">
                  <template slot="content">
                    <el-tag v-if="scope.row.apiInfo.update_status===0" :size="themeSize" type="danger">待处理</el-tag>
                    <el-tag v-if="scope.row.apiInfo.update_status===1" :size="themeSize" type="warning">待验证</el-tag>
                    <el-tag v-if="scope.row.apiInfo.update_status===2" :size="themeSize" type="success">已处理</el-tag>
                  </template>
                </el-description-item>
                <el-description-item label="项目" :value="scope.row.apiInfo.project? scope.row.apiInfo.project.name:''" :span-map="{md:12}" />
                <el-description-item label="分组" :value="scope.row.apiInfo.api_group? scope.row.apiInfo.api_group.name:''" :span-map="{md:12}" />
                <el-description-item label="接口路径" :span-map="{md:24}">
                  <template slot="content">
                    <el-tag v-if="scope.row.apiInfo.method==='POST'" :size="themeSize">{{ scope.row.apiInfo.method }}</el-tag>
                    <el-tag v-if="scope.row.apiInfo.method==='GET'" :size="themeSize" type="success">{{ scope.row.apiInfo.method }}</el-tag>
                    <el-tag v-if="scope.row.apiInfo.method==='PUT'" :size="themeSize" type="warning">{{ scope.row.apiInfo.method }}</el-tag>
                    <el-tag v-if="scope.row.apiInfo.method==='CALL'" :size="themeSize" type="warning">{{ scope.row.apiInfo.method }}</el-tag>
                    <el-tag v-if="scope.row.apiInfo.method==='DELETE'" :size="themeSize" type="danger">{{ scope.row.apiInfo.method }}</el-tag>
                    {{ scope.row.apiInfo.path }}
                    <el-button id="copyBtn" :size="themeSize" type="text" class="el-icon-document-copy" :data-clipboard-text="scope.row.apiInfo.path" @click="copyText($event)" />
                  </template>
                </el-description-item>
                <el-description-item label="接口描述" :value="scope.row.apiInfo.description" :span-map="{md:24}" />
                <el-description-item label="更新时间" :value="scope.row.apiInfo.update_time" :span-map="{md:12}" />
              </el-description>
            </el-card>
            <span slot="reference" type="text">
              <el-tag v-if="scope.row.apiInfo.method==='POST'" :size="themeSize">{{ scope.row.apiInfo.method }}</el-tag>
              <el-tag v-if="scope.row.apiInfo.method==='GET'" :size="themeSize" type="success">{{ scope.row.apiInfo.method }}</el-tag>
              <el-tag v-if="scope.row.apiInfo.method==='PUT'" :size="themeSize" type="warning">{{ scope.row.apiInfo.method }}</el-tag>
              <el-tag v-if="scope.row.apiInfo.method==='CALL'" :size="themeSize" type="warning">{{ scope.row.apiInfo.method }}</el-tag>
              <el-tag v-if="scope.row.apiInfo.method==='DELETE'" :size="themeSize" type="danger">{{ scope.row.apiInfo.method }}</el-tag>
              {{ scope.row.apiInfo.path }}
            </span>
          </el-popover>
        </template>
      </el-table-column>
      <el-table-column prop="update_statusName" label="更新" sortable width="80">
        <template slot-scope="scope">
          <el-tag v-if="scope.row.apiInfo.update_status===0" :size="themeSize" type="danger">待处理</el-tag>
          <el-tag v-if="scope.row.apiInfo.update_status===1" :size="themeSize" type="warning">待验证</el-tag>
          <el-tag v-if="scope.row.apiInfo.update_status===2" :size="themeSize" type="success">已处理</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="status" label="结果" sortable width="80">
        <template slot-scope="scope">
          <el-tag v-if="scope.row.result==='passed'" :size="themeSize" type="success">passed</el-tag>
          <el-tag v-if="scope.row.result==='failed'" :size="themeSize" type="danger">failed</el-tag>
          <el-tag v-if="scope.row.result==='skipped'" :size="themeSize" type="warning">skipped</el-tag>
          <el-tag v-if="scope.row.result==='error'" :size="themeSize" type="danger">error</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="labels" label="标签" show-overflow-tooltip width="200">
        <template slot-scope="scope">
          <el-tag v-for="item in scope.row.labels" :key="item.id" :size="themeSize">{{ item.name }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="depends" label="依赖" show-overflow-tooltip width="80">
        <template slot-scope="scope">
          <el-popover
            placement="right"
            width="660"
            trigger="click"
          >
            <el-row>
              {{ scope.row.name }}：{{ scope.row.description }}
            </el-row>
            <el-table :data="scope.row.depends" style="width: 100%" :size="themeSize">
              <el-table-column label="类型" prop="type" sortable show-overflow-tooltip min-width="100">
                <template slot-scope="scope2">
                  <el-tag type="primary" :size="themeSize">{{ scope.row.sid > scope2.row.sid? '依赖':'被依赖' }}</el-tag>
                </template>
              </el-table-column>
              <el-table-column label="SID" prop="sid" sortable show-overflow-tooltip min-width="80" />
              <el-table-column label="名称" prop="name" sortable show-overflow-tooltip min-width="200" />
              <el-table-column label="描述" prop="description" sortable show-overflow-tooltip min-width="200" />
            </el-table>
            <el-button slot="reference" :size="themeSize" type="text">{{ scope.row.depends.length>0? '详情': '' }}</el-button>
          </el-popover>
        </template>
      </el-table-column>
      <el-table-column prop="host_tag" label="host_tag" show-overflow-tooltip width="80">
        <template slot-scope="scope">
          <el-tag :size="themeSize">{{ scope.row.apiInfo.host_tag }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="req_headers" label="req_headers" show-overflow-tooltip width="100" />
      <el-table-column prop="req_params" label="req_params" show-overflow-tooltip width="200" />
      <el-table-column prop="req_json" label="req_json" show-overflow-tooltip width="200" />
      <el-table-column prop="req_data" label="req_data" show-overflow-tooltip width="200" />
      <el-table-column prop="validator" label="期望输出" show-overflow-tooltip width="200" />
      <el-table-column prop="extractor" label="响应提取" show-overflow-tooltip width="200" />
      <el-table-column prop="test_case.id" label="CaseID" sortable width="100" />
      <el-table-column prop="id" label="StepID" sortable width="100" />
      <el-table-column prop="test_case.name" label="CaseName" sortable show-overflow-tooltip width="200" />
      <el-table-column fixed="right" label="操作" width="180">
        <template slot-scope="scope">
          <!-- v-show="currentRow === scope.row" -->
          <el-row>
            <el-button type="info" icon="el-icon-edit" circle :size="themeSize" title="编辑步骤" @click="handleEdit(scope.$index, scope.row)" />
            <el-button type="info" icon="el-icon-document-copy" circle :size="themeSize" title="复制步骤" @click="handleCopy(scope.$index, scope.row)" />
            <el-button :loading="scope.row.runLoading" type="primary" icon="el-icon-caret-right" circle :size="themeSize" title="运行步骤" @click="runTest(scope.row)" />
            <el-popover style="margin-left: 10px" trigger="hover">
              <div style="text-align: center">
                <el-button type="warning" icon="el-icon-s-flag" circle :size="themeSize" :title="scope.row.status===false?'启用':'禁用'" @click="handleChangeStatus(scope.$index, scope.row)" />
                <el-button type="danger" icon="el-icon-delete" circle :size="themeSize" :loading="delLoading" title="删除步骤" @click="handleDel(scope.$index, scope.row)" />
              </div>
              <el-button slot="reference" icon="el-icon-more" title="更多" circle :size="themeSize" />
            </el-popover>
          </el-row>
        </template>
      </el-table-column>
    </el-table>

    <!--底部工具条-->
    <el-row v-show="showBottomTools" class="toolbar">
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
        <el-form-item label="所属用例" prop="test_case">
          <el-cascader
            placeholder="搜索：部门/用例集/用例名称"
            :props="{lazy: true, lazyLoad (node, resolve) {deptCaseTreeLoad(node, resolve, 2, false)}}"
            style="width: 100%"
            filterable
            clearable
            @change="handleBulkEditFormCascaderCase"
          >
            <template slot-scope="{ node, data }">
              <span>{{ data.label }}</span>
            </template>
          </el-cascader>
          <el-button :size="themeSize" type="text">{{ bulkEditForm.test_case? bulkEditForm.test_case.name: '' }}</el-button>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button :size="themeSize" @click.native="bulkEditFormVisible = false">取消</el-button>
        <el-button :size="themeSize" type="primary" @click.native="bulkEdit()">确定</el-button>
      </div>
    </el-dialog>

    <!--编辑用例步骤界面-->
    <el-drawer
      title="编辑用例步骤"
      :with-header="true"
      :wrapper-closable="false"
      :visible.sync="editFormVisible"
      :append-to-body="true"
      direction="rtl"
      size="50%"
    >
      <!-- 用例步骤详情 -->
      <div class="demo-drawer__content">
        <el-form ref="editForm" :model="editForm" label-width="120px" :size="themeSize" :rules="editFormRules">
          <!--  基本信息  -->
          <el-collapse value="1" @change="handleChange">
            <el-collapse-item name="1">
              <span slot="title" style="font-weight:bold;font-size:14px;color:#2C8DF4;">基本信息</span>
              <el-form ref="editForm" :model="editForm" label-width="100px" :size="themeSize" :rules="editFormRules">
                <el-form-item label="步骤名称" prop="name">
                  <el-input v-model="editForm.name" auto-complete="off" />
                </el-form-item>
                <el-form-item label="标签">
                  <el-select v-model="editForm.labels" value-key="id" placeholder="标签" multiple clearable style="width: 100%">
                    <el-option-group v-for="group in globalLabel_options" :key="group.label" :label="group.label">
                      <el-option v-for="item in group.options" :key="item.id" :label="item.name" :value="item" />
                    </el-option-group>
                  </el-select>
                </el-form-item>
                <el-form-item label="描述" prop="description">
                  <el-input v-model="editForm.description" type="textarea" :rows="2" />
                </el-form-item>
                <el-form-item label="所属接口" prop="apiInfo">
                  <el-cascader
                    v-model="editForm.apiInfo"
                    placeholder="搜索：接口名/地址"
                    :props="{lazy: true, lazyLoad (node, resolve) {deptApiTreeLoad(node, resolve, 3, false)}}"
                    style="width: 100%"
                    filterable
                    clearable
                    @change="handleEditFormCascaderApi"
                  >
                    <template slot-scope="{ node, data }">
                      <span v-if="!node.isLeaf">{{ data.label }}</span>
                      <el-tooltip v-if="node.isLeaf" placement="right" effect="light">
                        <div slot="content">
                          <el-tag v-if="data.value.method==='POST'" :size="themeSize">{{ data.value.method }}</el-tag>
                          <el-tag v-if="data.value.method==='GET'" :size="themeSize" type="success">{{ data.value.method }}</el-tag>
                          <el-tag v-if="data.value.method==='PUT'" :size="themeSize" type="warning">{{ data.value.method }}</el-tag>
                          <el-tag v-if="data.value.method==='CALL'" :size="themeSize" type="warning">{{ data.value.method }}</el-tag>
                          <el-tag v-if="data.value.method==='DELETE'" :size="themeSize" type="danger">{{ data.value.method }}</el-tag>
                          {{ data.value.path }}<br>{{ data.value.description }}
                        </div>
                        <el-button type="text">{{ data.label }}</el-button>
                      </el-tooltip>
                    </template>
                  </el-cascader>
                  <el-button :size="themeSize" type="primary" @click="applyApiInfoToEditCase(editForm.apiInfo)">复用接口数据</el-button>
                  <el-tooltip v-if="editForm.apiInfo" placement="right" effect="light">
                    <div slot="content">
                      <span>接口：{{ editForm.apiInfo.name }}</span><br>
                      <span>描述：{{ editForm.apiInfo.description }}</span><br>
                      <span>地址：</span>
                      <el-tag v-if="editForm.apiInfo.method==='POST'" :size="themeSize">{{ editForm.apiInfo.method }}</el-tag>
                      <el-tag v-if="editForm.apiInfo.method==='GET'" :size="themeSize" type="success">{{ editForm.apiInfo.method }}</el-tag>
                      <el-tag v-if="editForm.apiInfo.method==='PUT'" :size="themeSize" type="warning">{{ editForm.apiInfo.method }}</el-tag>
                      <el-tag v-if="editForm.apiInfo.method==='CALL'" :size="themeSize" type="warning">{{ editForm.apiInfo.method }}</el-tag>
                      <el-tag v-if="editForm.apiInfo.method==='DELETE'" :size="themeSize" type="danger">{{ editForm.apiInfo.method }}</el-tag>
                      {{ editForm.apiInfo.path }}
                    </div>

                    <el-button type="text">
                      <router-link
                        :to="{ name: '接口详情', params: {api_id: editForm.apiInfo.id}}"
                        style="cursor:pointer;color: #0000ff"
                        target="_blank"
                      >
                        {{ editForm.apiInfo.name }}
                      </router-link>
                    </el-button>
                  </el-tooltip>
                </el-form-item>
                <el-form-item label="所属用例" prop="test_case">
                  <el-cascader
                    placeholder="搜索：部门/用例集/用例名称"
                    :props="{lazy: true, lazyLoad (node, resolve) {deptCaseTreeLoad(node, resolve, 2, false)}}"
                    style="width: 60%"
                    filterable
                    clearable
                    @change="handleEditFormCascaderCase"
                  >
                    <template slot-scope="{ node, data }">
                      <span>{{ data.label }}</span>
                    </template>
                  </el-cascader>
                  <el-button :size="themeSize" type="text">{{ editForm.test_case.name }}</el-button>
                </el-form-item>
                <el-form-item label="依赖步骤">
                  <el-select v-model="editForm.depends" value-key="id" placeholder="依赖步骤（仅可以依赖当前用例中的步骤）" multiple clearable style="width: 100%">
                    <el-option v-for="item in dataList" :key="item.id" :label="item.name" :value="item" :disabled="item.sid>=editForm.sid" />
                  </el-select>
                </el-form-item>
              </el-form>
            </el-collapse-item>
          </el-collapse>

          <!--  setup/teardown hooks  -->
          <el-collapse value="1" @change="handleChange">
            <el-collapse-item name="2">
              <span slot="title" style="font-weight:bold;font-size:14px;color:#2C8DF4;">Setup/Teardown Hooks</span>
              <setup-teardown-hooks v-model="editForm" />
            </el-collapse-item>
          </el-collapse>

          <!--  请求 - Request  -->
          <el-collapse value="1" @change="handleChange">
            <el-collapse-item name="1">
              <span slot="title" style="font-weight:bold;font-size:14px;color:#2C8DF4;">请求</span>
              <el-tabs v-model="requestTabsActiveName" @tab-click="handleClick">
                <!--  请求参数Body  -->
                <el-tab-pane label="Body" name="body">
                  <request-parameters v-model="editForm" />
                </el-tab-pane>
                <!--  请求头 Header -->
                <el-tab-pane label="Header" name="req_header">
                  <request-headers v-model="editForm.req_headers" />
                </el-tab-pane>
                <!--  请求路径扩展 -->
                <el-tab-pane label="PathExtend" name="req_path_extend">
                  <request-path-extend v-model="editForm.req_path_extend" />
                </el-tab-pane>
              </el-tabs>
            </el-collapse-item>
          </el-collapse>

          <!--  期望输出 - Response  -->
          <el-collapse value="1" @change="handleChange">
            <el-collapse-item name="1">
              <span slot="title" style="font-weight:bold;font-size:14px;color:#2C8DF4;">期望输出</span>
              <response-validate v-model="editForm.validator" />
            </el-collapse-item>
          </el-collapse>

          <!--  保存响应结果为全局变量 -->
          <el-collapse value="1" @change="handleChange">
            <el-collapse-item name="1">
              <span slot="title" style="font-weight:bold;font-size:14px;color:#2C8DF4;">保存结果</span>
              <response-extract v-model="editForm.extractor" />
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

    <!--新增用例步骤界面-->
    <el-drawer
      :title="addCaseTitle"
      :with-header="true"
      :wrapper-closable="false"
      :visible.sync="addFormVisible"
      :append-to-body="true"
      direction="rtl"
      size="50%"
      :before-close="closeAddForm"
    >
      <!-- 用例步骤详情 -->
      <div class="demo-drawer__content">
        <el-form ref="addForm" :model="addForm" label-width="100px" :size="themeSize" :rules="addFormRules">
          <!--  基本信息  -->
          <el-collapse value="1" @change="handleChange">
            <el-collapse-item name="1">
              <span slot="title" style="font-weight:bold;font-size:14px;color:#2C8DF4;">基本信息</span>
              <el-form-item label="name" prop="name">
                <el-input v-model="addForm.name" auto-complete="off" placeholder="步骤名" />
              </el-form-item>
              <el-form-item label="标签">
                <el-select v-model="addForm.labels" value-key="id" placeholder="标签" multiple clearable style="width: 100%">
                  <el-option-group v-for="group in globalLabel_options" :key="group.label" :label="group.label">
                    <el-option v-for="item in group.options" :key="item.id" :label="item.name" :value="item" />
                  </el-option-group>
                </el-select>
              </el-form-item>
              <el-form-item label="步骤描述" prop="description">
                <el-input v-model="addForm.description" type="textarea" :rows="2" />
              </el-form-item>
              <el-form-item label="所属接口" prop="apiInfo">
                <el-cascader
                  v-show="cascaderVisible"
                  placeholder="搜索：接口名/地址"
                  :props="{lazy: true, lazyLoad (node, resolve) {deptApiTreeLoad(node, resolve, 3, false)}}"
                  style="width: 100%"
                  filterable
                  clearable
                  :filter-method="apiDataFilter"
                  @change="handleAddFormCascaderApi"
                >
                  <template slot-scope="{ node, data }">
                    <span v-if="!node.isLeaf">{{ data.label }}</span>
                    <el-tooltip v-if="node.isLeaf" placement="right" effect="light">
                      <div slot="content">
                        <el-tag v-if="data.value.method==='POST'" :size="themeSize">{{ data.value.method }}</el-tag>
                        <el-tag v-if="data.value.method==='GET'" :size="themeSize" type="success">{{ data.value.method }}</el-tag>
                        <el-tag v-if="data.value.method==='PUT'" :size="themeSize" type="warning">{{ data.value.method }}</el-tag>
                        <el-tag v-if="data.value.method==='CALL'" :size="themeSize" type="warning">{{ data.value.method }}</el-tag>
                        <el-tag v-if="data.value.method==='DELETE'" :size="themeSize" type="danger">{{ data.value.method }}</el-tag>
                        {{ data.value.path }}<br>{{ data.value.description }}
                      </div>
                      <el-button type="text">{{ data.label }}</el-button>
                    </el-tooltip>
                  </template>
                </el-cascader>
                <el-button :size="themeSize" type="primary" @click="applyApiInfoToAddCase(addForm.apiInfo)">复用接口数据</el-button>
                <el-tooltip v-if="addForm.apiInfo" placement="right" effect="light">
                  <div slot="content">
                    <span>接口：{{ addForm.apiInfo.name }}</span><br>
                    <span>描述：{{ addForm.apiInfo.description }}</span><br>
                    <span>地址：</span>
                    <el-tag v-if="addForm.apiInfo.method==='POST'" :size="themeSize">{{ addForm.apiInfo.method }}</el-tag>
                    <el-tag v-if="addForm.apiInfo.method==='GET'" :size="themeSize" type="success">{{ addForm.apiInfo.method }}</el-tag>
                    <el-tag v-if="addForm.apiInfo.method==='PUT'" :size="themeSize" type="warning">{{ addForm.apiInfo.method }}</el-tag>
                    <el-tag v-if="addForm.apiInfo.method==='CALL'" :size="themeSize" type="warning">{{ addForm.apiInfo.method }}</el-tag>
                    <el-tag v-if="addForm.apiInfo.method==='DELETE'" :size="themeSize" type="danger">{{ addForm.apiInfo.method }}</el-tag>
                    {{ addForm.apiInfo.path }}
                  </div>
                  <el-button type="text">
                    <router-link
                      :to="{ name: '接口详情', params: {api_id: addForm.apiInfo.id}}"
                      style="cursor:pointer;color: #0000ff"
                      target="_blank"
                    >
                      {{ addForm.apiInfo.name }}
                    </router-link>
                  </el-button>
                </el-tooltip>
              </el-form-item>
              <el-form-item label="所属用例" prop="test_case">
                <el-cascader
                  v-show="cascaderVisible"
                  placeholder="搜索：部门/用例集/用例名称"
                  :props="{lazy: true, lazyLoad (node, resolve) {deptCaseTreeLoad(node, resolve, 2, false)}}"
                  style="width: 60%"
                  filterable
                  clearable
                  @change="handleAddFormCascaderCase"
                >
                  <template slot-scope="{ node, data }">
                    <span>{{ data.label }}</span>
                  </template>
                </el-cascader>
                <el-button :size="themeSize" type="text">{{ addForm.test_case.name }}</el-button>
              </el-form-item>
              <el-form-item label="依赖步骤">
                <el-select v-model="addForm.depends" value-key="id" placeholder="依赖步骤（仅可以依赖当前用例中的步骤）" multiple clearable style="width: 100%">
                  <el-option v-for="item in dataList" :key="item.id" :label="item.name" :value="item" :disabled="item.sid>=addForm.sid" />
                </el-select>
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

          <!--  setup/teardown hooks  -->
          <el-collapse value="1" @change="handleChange">
            <el-collapse-item name="2">
              <span slot="title" style="font-weight:bold;font-size:14px;color:#2C8DF4;">Setup/Teardown Hooks</span>
              <setup-teardown-hooks v-model="addForm" />
            </el-collapse-item>
          </el-collapse>

          <!--  请求 - Request  -->
          <el-collapse value="1" @change="handleChange">
            <el-collapse-item name="1">
              <span slot="title" style="font-weight:bold;font-size:14px;color:#2C8DF4;">请求</span>
              <el-tabs v-model="requestTabsActiveName" @tab-click="handleClick">
                <!--  请求参数Body  -->
                <el-tab-pane label="Body" name="body">
                  <request-parameters v-model="addForm" />
                </el-tab-pane>
                <!--  请求头 Header -->
                <el-tab-pane label="Header" name="req_headers">
                  <request-headers v-model="addForm.req_headers" />
                </el-tab-pane>
                <!--  请求路径扩展 -->
                <el-tab-pane label="PathExtend" name="req_path_extend">
                  <request-path-extend v-model="addForm.req_path_extend" />
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

          <!--  保存响应结果为全局变量 -->
          <el-collapse value="1" @change="handleChange">
            <el-collapse-item name="1">
              <span slot="title" style="font-weight:bold;font-size:14px;color:#2C8DF4;">结果提取</span>
              <response-extract v-model="addForm.extractor" />
            </el-collapse-item>
          </el-collapse>
        </el-form>
        <!-- 取消、提交 -->
        <div class="demo-drawer__footer">
          <el-button :size="themeSize" @click.native="addFormVisible = false; cascaderVisible = false; addLoading = false">取消</el-button>
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
  addTestStep, bulkDeleteTestStep,
  bulkUpdateTestStep,
  deleteTestStep,
  getTestStepList,
  updateTestStep
} from '@/api/apiTest/test_step'

import Sortable from 'sortablejs'
import Clipboard from 'clipboard'
import ElDescription from '@/components/Description/ElDescription'
import ElDescriptionItem from '@/components/Description/ElDescriptionItem'
import get_base_data from '@/api/apiTest/get_base_data'
import SetupTeardownHooks from '@/views/apiTest/components/SetupTeardownHooks'
import RequestHeaders from '@/views/apiTest/components/RequestHeaders'
import RequestParameters from '@/views/apiTest/components/RequestParameters'
import RequestPathExtend from '@/views/apiTest/components/RequestPathExtend'
import ResponseValidate from '@/views/apiTest/components/ResponseValidate'
import ResponseExtract from '@/views/apiTest/components/ResponseExtract'
import RunTest from '@/views/apiTest/components/RunTest'

export default {
  name: 'CaseList',
  components: { ElDescription, ElDescriptionItem, SetupTeardownHooks,
    RequestHeaders, RequestParameters, RequestPathExtend, ResponseValidate, ResponseExtract, RunTest
  },
  mixins: [get_base_data],
  props: {
    showTopTools: {
      type: Boolean,
      default() {
        return true
      }
    },
    showBottomTools: {
      type: Boolean,
      default() {
        return true
      }
    },
    tableName: {
      type: String,
      default() {
        return '步骤列表'
      }
    }
  },
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

      hooksTabsActiveName: 'setup_hooks',
      requestTabsActiveName: 'body',

      // 用例步骤
      total: 0,
      page: 1,
      page_size: 20,
      dataList: [],
      newDataList: [],
      filters: {
        id: [],
        description: '',
        project: [],
        department: [],
        result: [],
        apiInfo: [],
        test_case: []
      },
      sels: [], // 用例步骤列表选中列
      currentRow: '', // 用例步骤列表当前行
      showMoreFilters: false,

      // 编辑用例步骤
      editFormVisible: false, // 编辑界面是否显示
      // 编辑界面数据规则
      editFormRules: {
        name: [
          { required: true, message: '请输入名称', trigger: 'blur' },
          { min: 1, max: 50, message: '长度在 1 到 500 个字符', trigger: 'blur' }
        ],
        test_case: [
          { required: true, message: '请选择所属用例', trigger: 'blur' }
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
        test_case: '',
        apiInfo: {
          update_status: ''
        },
        skipif: '',
        setup_hooks: [],
        teardown_hooks: [],
        req_headers: '',
        req_params: '',
        req_json: '',
        req_data: '',
        validator: '',
        extractor: '',
        status: true,
        updater: ''
      },

      // 新增用例步骤
      addCaseTitle: '新增用例步骤',
      projectApiTreeData: [], // 选择接口 Tree
      addFormVisible: false, // 新增界面是否显示
      // 新增界面数据规则
      addFormRules: {
        name: [
          { required: true, message: '请输入名称', trigger: 'blur' },
          { min: 1, max: 50, message: '长度在 1 到 500 个字符', trigger: 'blur' }
        ],
        apiInfo: [
          { required: true, message: '请选择所属接口', trigger: 'blur' }
        ],
        test_case: [
          { required: true, message: '请选择所属用例', trigger: 'blur' }
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
        labels: [],
        test_case: '',
        apiInfo: {
          update_status: ''
        },
        creator: '',
        skipif: '',
        setup_hooks: [],
        teardown_hooks: [],
        req_headers: '',
        req_params: '',
        req_json: '',
        req_data: '',
        validator: '',
        extractor: '',
        status: true
      },
      // 新增、编辑界面 接口级联面板 数据
      cascaderVisible: false, // 接口级联面板是否显示

      // 批量处理
      bulkEditFormVisible: false,
      bulkEditForm: {
        test_case: null
      },
      bulkStatus: true,

      // 更新步骤
      mySortable: null,
      allowUpdateStepId: false,
      saveSortBtnShow: false
    }
  },
  created() {
  },
  mounted() {
    if (typeof (this.$route.params.api_id) !== 'undefined') {
      this.filters.apiInfo = [this.$route.params.api_id]
      this.fetchData()
    }
    // if (typeof (this.$route.params.case_id) !== 'undefined') {
    //   this.filters.test_case = [{ id: this.$route.params.case_id }]
    //   this.fetchData()
    // }
  },
  methods: {
    // ========== 公共 ==========
    // 折叠版 click
    handleChange(val) {
      // console.log(val)
    },
    // 标签页 click
    handleClick(tab, event) {
      // console.log(tab, event)
    },
    // 顶部工具条 重置（清空所有下拉框）
    filterClear() {
      this.filters.id = []
      this.filters.name = ''
      this.filters.description = ''
      this.filters.result = []
      this.filters.department = []
    },
    // 接口级联查询器
    apiDataFilter(node, keyword) {
      console.log(node)
      return (node.text.includes(keyword) || node.value.path.includes(keyword))
    },
    handleEditFormCascaderApi(val) {
      // console.log(val)
      if (val.length > 3) {
        this.editForm.apiInfo = val[3]
      }
    },
    handleEditFormCascaderCase(val) {
      // console.log(val)
      if (val.length > 2) {
        this.editForm.test_case = val[2]
      }
    },
    handleAddFormCascaderApi(val) {
      // console.log(val)
      if (val.length > 3) {
        this.addForm.apiInfo = val[3]
      }
    },
    handleAddFormCascaderCase(val) {
      if (val.length > 2) {
        this.addForm.test_case = val[2]
      }
    },
    handleBulkEditFormCascaderCase(val) {
      // console.log(val)
      if (val.length > 2) {
        this.bulkEditForm.test_case = val[2].id
      }
    },
    // 数组对象排序 - 比较方法 int
    compare(prop) {
      return function(obj1, obj2) {
        let val1 = obj1[prop]
        let val2 = obj2[prop]
        if (!isNaN(Number(val1)) && !isNaN(Number(val2))) {
          val1 = Number(val1)
          val2 = Number(val2)
        }
        if (val1 < val2) {
          return -1
        } else if (val1 > val2) {
          return 1
        } else {
          return 0
        }
      }
    },

    // ========== 用例步骤 ==========
    // 查询 filters data
    fetchFiltersData() {
      this.getDepartment()
      this.getTestSuite()
    },
    // 查询用例步骤列表
    fetchData() {
      this.saveSortBtnShow = false
      this.newDataList = null
      const test_case_ids = []
      for (let i = 0; i < this.filters.test_case.length; i++) {
        test_case_ids.push(this.filters.test_case[i].id)
      }
      const department_ids = []
      for (let i = 0; i < this.filters.department.length; i++) {
        department_ids.push(this.filters.department[i].id)
      }
      const params = {
        page: this.page,
        page_size: this.page_size,
        id_in: this.filters.id.join(','),
        name: this.filters.name,
        description: this.filters.description,
        result__in: this.filters.result.join(','),
        test_case__in: test_case_ids.join(','),
        apiInfo__in: this.filters.apiInfo.join(','),
        department__in: department_ids.length > 0 ? department_ids.join(',') : null
      }
      this.tableConfig.isLoading = true
      getTestStepList(params).then(response => {
        this.dataList = response.data.list
        this.dataList.sort(this.compare('sid'))
        this.total = response.data.count
        this.tableConfig.isLoading = false
      }).then(() => {
        this.isAllowUpdateStepId()
        this.rowDrop(this.saveSortBtnShow)
        this.$refs.sortTable.clearSort()
        this.$refs.sortTable.sort('sid', 'ascending')
      })
    },
    // 选中用例步骤列表行
    selsChange: function(sels) {
      this.sels = sels
    },
    cellMouseEnter(row) {
      this.currentRow = row
    },
    cellMouseLeave(row) {
      this.currentRow = ''
    },
    // 用例步骤编辑新增相关
    copyText(event) {
      const btnID = '#' + event.currentTarget.id
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
    // 显示编辑用例步骤界面
    handleEdit: function(index, row) {
      this.getLabel(['优先级'])
      this.editFormVisible = true
      this.editForm = Object.assign({}, row)
    },
    // 复制用例步骤
    handleCopy: function(index, row) {
      this.getLabel(['优先级'])
      this.addCaseTitle = '复制用例步骤'
      this.addFormVisible = true
      this.addForm = Object.assign({}, row)
      this.addForm.name += '-copy'
      this.addForm.description += '-copy'
      this.addForm.result = ''
      this.addForm.status = true
    },
    applyApiInfoToEditCase: function(apiInfo) {
      console.log(apiInfo.req_json)
      this.editForm.name = apiInfo.name
      this.editForm.description = apiInfo.description
      this.editForm.labels = apiInfo.labels
      this.editForm.req_headers = apiInfo.req_headers
      this.editForm.req_params = apiInfo.req_params
      this.editForm.req_json = apiInfo.req_json
      this.editForm.req_data = apiInfo.req_data
      this.editForm.validator = apiInfo.validator
    },
    applyApiInfoToAddCase: function(apiInfo) {
      this.addForm.name = apiInfo.name
      this.addForm.description = apiInfo.description
      this.addForm.labels = apiInfo.labels
      this.addForm.req_headers = apiInfo.req_headers
      this.addForm.req_params = apiInfo.req_params
      this.addForm.req_json = apiInfo.req_json
      this.addForm.req_data = apiInfo.req_data
      this.addForm.validator = apiInfo.validator
    },
    // 清空新增页面数据
    addFormClear() {
      this.addForm = {
        name: '',
        description: '',
        label: '',
        test_case: '',
        apiInfo: {
          update_status: ''
        },
        creator: '',
        req_headers: '',
        req_params: '',
        req_json: '',
        req_data: '',
        response: '',
        status: true
      }
    },
    // 显示新增用例步骤界面
    handleAdd: function() {
      this.addFormClear()
      this.getLabel(['优先级'])
      this.addCaseTitle = '新增用例步骤'
      this.cascaderVisible = true
      this.addFormVisible = true
    },
    closeAddForm: function() {
      this.cascaderVisible = false
      this.addFormVisible = false
    },
    // 改变用例步骤状态
    handleChangeStatus: function(index, row) {
      let params, opt
      if (row.status) {
        opt = '禁用'
        params = { status: false }
      } else {
        opt = '启用'
        params = { status: true }
      }
      updateTestStep(row.id, params).then(response => {
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
    // 编辑用例步骤
    editSubmit: function() {
      this.$refs.editForm.validate((valid) => {
        if (valid) {
          this.$confirm('确认提交吗？', '提示', {}).then(() => {
            // NProgress.start();
            const lablel_ids = []
            if (typeof (this.editForm.labels) !== 'undefined') {
              for (let i = 0; i < this.editForm.labels.length; i++) {
                lablel_ids.push(this.editForm.labels[i].id)
              }
            }
            const depend_step_ids = []
            if (typeof (this.editForm.depends) !== 'undefined') {
              for (let j = 0; j < this.editForm.depends.length; j++) {
                depend_step_ids.push(this.editForm.depends[j].id)
              }
            }
            const params = {
              name: this.editForm.name,
              description: this.editForm.description,
              test_case: this.editForm.test_case.id,
              apiInfo: this.editForm.apiInfo.id,
              skipif: this.editForm.skipif,
              setup_hooks: this.editForm.setup_hooks,
              teardown_hooks: this.editForm.teardown_hooks,
              req_headers: this.editForm.req_headers,
              req_params: this.editForm.req_params,
              req_json: this.editForm.req_json,
              req_data: this.editForm.req_data,
              req_path_extend: this.editForm.req_path_extend,
              validator: this.editForm.validator,
              extractor: this.editForm.extractor,
              status: this.editForm.status,
              labels: lablel_ids,
              depends: depend_step_ids
            }
            this.editLoading = true
            updateTestStep(this.editForm.id, params).then(_data => {
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
    // 新增用例步骤
    addSubmit: function() {
      this.$refs.addForm.validate((valid) => {
        if (valid) {
          this.$confirm('确认提交吗？', '提示', {}).then(() => {
            // NProgress.start();
            const lablel_ids = []
            if (typeof (this.addForm.labels) !== 'undefined') {
              for (let j = 0; j < this.addForm.labels.length; j++) {
                lablel_ids.push(this.addForm.labels[j].id)
              }
            }
            const depend_step_ids = []
            if (typeof (this.addForm.depends) !== 'undefined') {
              for (let j = 0; j < this.addForm.depends.length; j++) {
                depend_step_ids.push(this.addForm.depends[j].id)
              }
            }
            Object.assign(this.addForm, {
              name: this.addForm.name,
              apiInfo: this.addForm.apiInfo.id,
              test_case: this.addForm.test_case.id,
              labels: lablel_ids,
              depends: depend_step_ids,
              sid: this.dataList.length + 1
              // creator: this.addForm.creator.id
            })
            this.addLoading = true
            addTestStep(this.addForm).then(_data => {
              const { msg, code } = _data
              this.addLoading = false
              if (code === 2) {
                this.$message({
                  message: '添加成功',
                  center: true,
                  type: 'success'
                })
                this.$refs['addForm'].resetFields()
                this.cascaderVisible = false
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
                this.cascaderVisible = false
                this.addFormVisible = false
              }
            }).then(() => { this.fetchData() })
          })
        }
      })
    },
    // 删除用例步骤
    handleDel: function(index, row) {
      this.$confirm('确认删除该记录吗?', '提示', {
        type: 'warning'
      }).then(() => {
        // NProgress.start();
        deleteTestStep(row.id).then(response => {
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

    // 批量处理 - 编辑（局部更新）
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
        bulkUpdateTestStep(dataArr).then(response => {
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
    // 批量修改步骤状态
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
      bulkUpdateTestStep(dataArr).then(response => {
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
    // 批量删除用例步骤
    bulkRemove: function() {
      const ids = this.sels.map(item => item.id)
      this.$confirm('确认删除选中记录吗？', '提示', {
        type: 'warning'
      }).then(() => {
        const params = {
          id_in: ids.join(',')
        }
        bulkDeleteTestStep(params).then(response => {
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

    // 运行用例步骤
    runTest(row) {
      this.$refs.runTestRef.handleRunTest('test_step', [row])
      this.$set(row, 'runLoading', false)
    },
    // 批量运行用例步骤
    bulkRunTest() {
      this.$refs.runTestRef.handleRunTest('test_step', this.sels)
      this.bulkRunLoading = false
    },

    // 排序
    indexMethod(index) {
      return index + 1
    },
    isAllowUpdateStepId: function() {
      this.allowUpdateStepId = (
        this.filters.id.length === 0 &&
        this.filters.description === '' &&
        this.filters.result.length === 0
      )
    },
    openDragSort() {
      this.saveSortBtnShow = !this.saveSortBtnShow
      this.$nextTick(() => {
        this.rowDrop(this.saveSortBtnShow)
      })
    },
    rowDrop(enabled = true) {
      if (!this.mySortable) {
        const tbody = document.querySelector('.stepTable .el-table__body-wrapper tbody')
        const _this = this
        this.mySortable = Sortable.create(tbody, {
          sort: true,
          //  指定父元素下可被拖拽的子元素
          draggable: '.stepTable .el-table__row',
          onEnd({ newIndex, oldIndex }) {
            const currRow = _this.dataList.splice(oldIndex, 1)[0]
            _this.dataList.splice(newIndex, 0, currRow)
          }
        })
      }
      this.mySortable.options.sort = enabled
    },
    bulkUpdateStepId: function() {
      if (this.filters.id.length > 0 ||
          this.filters.description !== '' ||
          this.filters.project.length > 0 ||
          this.filters.result.length > 0) {
        this.$message.warning({
          message: '当前用例步骤被筛选，禁止更新执行顺序！',
          center: true
        })
      } else if (this.filters.test_case.length === 0) {
        this.$message.warning({
          message: '当前为全部用例步骤，未指定用例，禁止更新执行顺序！',
          center: true
        })
      } else {
        this.$confirm('确认更新当前用例步骤执行顺序吗？', '提示', {
          type: 'warning'
        }).then(() => {
          this.editLoading = true
          // NProgress.start();
          const start_sid = (this.page - 1) * this.page_size + 1
          const dataArr = []
          for (let i = 0; i < this.dataList.length; i++) {
            const item = this.dataList[i]
            dataArr.push({
              id: item.id,
              sid: start_sid + i
            })
          }
          bulkUpdateTestStep(dataArr).then(response => {
            const { code, msg } = response
            this.editLoading = false
            if (code === 2) {
              this.$message({
                message: '修改步骤顺序成功',
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
            this.mySortable.options.sort = false
            this.fetchData()
          })
        })
      }
    },
    toggleExpanded() {
      this.expanded = !this.expanded
    },
    dependsAnalysis(row) {
      const depends = row.depends
      const dst = {
        depends: [],
        depend_by: []
      }
      if (depends) {
        for (const i in depends) {
          const d = depends[i]
          const depend_sid = d['sid']
          if (depend_sid > row.sid) {
            // 依赖项
            dst['depends'].push(d)
          } else {
            dst['depend_by'].push(d)
          }
        }
      }
      console.log(dst)
      return dst
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
