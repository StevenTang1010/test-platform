<template>
  <div class="main">
    <el-divider class="blue-line" direction="vertical" />
    <span slot="title" style="font-weight:bold;font-size:14px;color:#2C8DF4;">YAPI变更事件列表</span>

    <!--顶部工具条-->
    <el-col :span="24" class="toolbar" style="padding-bottom: 0;padding-top: 10px;">
      <el-form :inline="true" :model="filters" :size="themeSize" @submit.native.prevent>
        <el-form-item>
          <el-input v-model="filters.yapi_id" placeholder="YAPI ID" clearable @keyup.enter.native="fetchData" />
        </el-form-item>
        <el-form-item>
          <el-input v-model="filters.event" placeholder="事件" clearable @keyup.enter.native="fetchData" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="fetchData">查询</el-button>
        </el-form-item>
        <el-form-item>
          <el-button type="warning" :loading="syncLoading" @click="handleYapiDataSync(['all'])">数据同步</el-button>
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
      style="width: 100%"
      :height="tableConfig.height"
      :default-sort="{prop: 'id', order: 'descending'}"
      @selection-change="selsChange"
    >
      <el-table-column fixed type="selection" />
      <el-table-column prop="id" label="ID" sortable show-overflow-tooltip width="100" />
      <el-table-column prop="yapi_id" label="YAPI ID" sortable show-overflow-tooltip width="100" />
      <el-table-column prop="event" label="事件" sortable show-overflow-tooltip width="300" />
      <el-table-column prop="content" label="详情" sortable show-overflow-tooltip width="500" />
      <el-table-column fixed="right" label="操作" width="200">
        <template slot-scope="scope">
          <el-row>
            <el-button type="info" icon="el-icon-refresh" circle :size="themeSize" title="同步数据" @click="handleYapiDataSync([scope.row])" />
            <el-button type="danger" icon="el-icon-delete" circle :size="themeSize" title="删除" @click="handleDel(scope.row)" />
          </el-row>
        </template>
      </el-table-column>
    </el-table>

    <!--底部工具条-->
    <el-col :span="24" class="toolbar" style="padding:5px;">
      <el-button type="primary" :disabled="sels.length===0" :size="themeSize" @click="batchDataSync">批量同步</el-button>
      <el-button type="danger" :disabled="sels.length===0" :size="themeSize" @click="batchRemove">批量删除</el-button>
      <span style="font-size: 14px"> 选中{{ sels.length }}条</span>
      <el-pagination
        background
        style="float:right;"
        :current-page.sync="page"
        layout="total, sizes, prev, pager, next, jumper"
        :page-size="page_size"
        :page-sizes="[20, 50, 100]"
        :total="total"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </el-col>

  </div>
</template>

<script>
import { getYapiEventList, dataSyncYapiEvent, deleteYapiEvent } from '@/api/apiTest/yapi_event'

export default {
  name: 'YapiEventList',
  data() {
    return {
      // 公共
      themeSize: this.$store.state.settings.themeSize,
      tableConfig: {
        isLoading: false,
        height: window.innerHeight - 275 // 下面剩余多少空白部分（即最下面距离底部有多少距离）
      },
      syncLoading: false,

      // 事件列表
      total: 0,
      page_count: 0,
      page: 1,
      page_size: 20,
      dataList: [],
      filters: {
        yapi_id: '',
        event: ''
      },
      sels: [] // 列表选中列
    }
  },
  created() {
  },
  mounted() {
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
      this.filters.yapi_id = ''
      this.filters.event = ''
    },
    // 标签页 click
    handleClick(tab, event) {
      console.log(tab, event)
    },
    // 查询事件列表
    fetchData() {
      const params = {
        page: this.page,
        page_size: this.page_size,
        yapi_id: this.filters.yapi_id,
        event: this.filters.event
      }
      this.tableConfig.isLoading = true
      getYapiEventList(params).then(response => {
        this.dataList = response.data.list
        this.total = response.data.count
        this.tableConfig.isLoading = false
      })
    },
    // 选中行
    selsChange: function(sels) {
      this.sels = sels
    },
    // 同步
    handleYapiDataSync: function(rows) {
      this.$confirm('确认提交吗？', '提示', {}).then(() => {
        this.syncLoading = true
        dataSyncYapiEvent(rows).then(response => {
          const { code, data } = response
          this.syncLoading = false
          if (code === 2) {
            if (data.msg.indexOf('失败') !== -1) {
              this.$notify.error({
                title: data.msg,
                message: JSON.stringify(data.data),
                duration: 5000
              })
            } else {
              this.$message.success({
                message: data.msg,
                center: true
              })
            }
          } else {
            this.$message.error({
              message: data.msg,
              center: true
            })
          }
        })
      }).then(() => { this.fetchData() })
    },
    // 删除
    handleDel: function(row) {
      this.$confirm('确认删除该记录吗?', '提示', { type: 'warning' }).then(() => {
        // NProgress.start();
        deleteYapiEvent(row.id).then(response => {
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
      }).then(() => { this.fetchData() })
    },
    // 批量同步
    batchDataSync: function() {
      this.$message.warning('TODO')
    },
    // 批量删除
    batchRemove: function() {
      this.$message.warning('TODO')
    }
  }
}
</script>

<style scoped>

</style>
