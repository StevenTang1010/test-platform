<template>
  <div>
    <el-row style="margin-left: 1px">
      <el-col :span="25">
        <el-form :model="modelForm">
          <el-form-item>
            <el-select v-model="systemValue" clearable placeholder="请选择系统" size="mini" @visible-change="handleChangeFlag" @change="getPrimaryList">
              <el-option v-for="(item, index) in modelForm.system" :key="index" :label="item.system_name" :value="item.system_id"></el-option>
            </el-select>
            <el-select v-model="firstModelValue" clearable placeholder="请选择一级模块" size="mini" @visible-change="handleChangeFlag" @change="getSecondaryList">
              <el-option v-for="(item, index) in modelForm.first" :key="index" :label="item.primary_module_name" :value="item.primary_module_id"></el-option>
            </el-select>
            <el-select v-model="secondModelValue" clearable placeholder="请选择二级模块" size="mini" @visible-change="handleChangeFlag" @change="getThirdList">
              <el-option v-for="(item, index) in modelForm.second" :key="index" :label="item.secondary_module_name" :value="item.secondary_module_id"></el-option>
            </el-select>
            <el-select v-model="thirdModelValue" clearable placeholder="请选择三级模块" size="mini" @visible-change="handleChangeFlag">
              <el-option v-for="(item, index) in modelForm.third" :key="index" :label="item.third_module_name" :value="item.third_module_id"></el-option>
            </el-select>
            <el-button type="primary" icon="el-icon-search" size="small" style="margin-left: 10px" circle @click.native="getSearchData"></el-button>
            <el-button type="default" icon="el-icon-refresh-left" size="small" style="margin-left: 10px" circle @click.native="filterClear"></el-button>
          </el-form-item>
        </el-form>
      </el-col>
      <el-button type="primary" icon="el-icon-plus" size="small" style="float: right; margin-right: 20px; margin-top: 2px"></el-button>
    </el-row>
    <div class="table-container" style="height: 100%">
      <el-table
        ref="table"
        v-loading="listLoading"
        :data="list.data"
        border
        element-loading-text="Loading"
        :max-height="tableHeight"
      >
        <template slot="empty">
          <!--  <img class="data-pic" src="#" alt="" />-->
          <span style="font-size: 16px">先查询，不然不会有数据的</span>
        </template>
        <el-table-column align="center" label="系统" prop="system">
        </el-table-column>
        <el-table-column label="一级模块" align="center" prop="primary" :show-overflow-tooltip="true">
        </el-table-column>
        <el-table-column label="二级模块" align="center" prop="secondary" :show-overflow-tooltip="true">
        </el-table-column>
        <el-table-column label="三级模块" align="center" prop="third" :show-overflow-tooltip="true" :render-header="renderThird">
          <template slot-scope="scope">
            <router-link :to="{ name: 'model', params: {id: scope.row.id}}" style="cursor:pointer;color: #0000ff;text-decoration:underline">
              {{ scope.row.third }}
            </router-link>
          </template>
        </el-table-column>
        <el-table-column label="功能" prop="func" align="center" :show-overflow-tooltip="true" :render-header="renderFunc">
        </el-table-column>
        <el-table-column align="center" label="操作" width="200px">
          <template slot-scope="scope">
            <el-button
              type="primary"
              icon="el-icon-edit"
              circle
              @click="openDialog(scope.$index, scope.row)">
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      <br>
    </div>
<!--    <div>-->
<!--      <el-dialog title="编辑工单详情" :visible.sync="dialogFormVisible">-->
<!--        <div slot="footer" class="dialog-footer">-->
<!--          <el-button @click.native="dialogFormVisible = false">取消</el-button>-->
<!--          <el-button type="primary" @click.native="updateForm">更新</el-button>-->
<!--        </div>-->
<!--      </el-dialog>-->
<!--    </div>-->
  </div>
</template>

<script>
import * as precise from '@/api/precise'
import { Message } from 'element-ui'

export default {
  data() {
    return {
      // 模块联级筛选
      modelForm: {
        system: [
        ],
        first: [],
        second: [],
        third: []
      },
      systemValue: '',
      firstModelValue: '',
      secondModelValue: '',
      thirdModelValue: '',

      // 表格内容
      list: {
        data: []
      },
      // 表格高度
      tableHeight: '',
      // table表格加载转圈
      listLoading: false,
      // 下拉框是否展示
      changeFlag: false
    }
  },
  created() {
  },
  mounted() {
    this.getSystemList()
  },
  methods: {
    // 自定义三级模块表头hover
    renderThird(h) {
      return h('span', {}, [
        h('span', {}, '三级模块'),
        h('el-popover', { props: { placement: 'top-start', trigger: 'hover', content: '点击进入关联三级模块详情列表' }}, [
          h('i', { slot: 'reference', class: 'el-icon-question' }, '')
        ])
      ])
    },
    // 自定义功能表头hover
    renderFunc(h) {
      return h('span', {}, [
        h('span', {}, '功能'),
        h('el-popover', { props: { placement: 'top-start', trigger: 'hover', content: '点击进入关联功能详情列表' }}, [
          h('i', { slot: 'reference', class: 'el-icon-question' }, '')
        ])
      ])
    },
    // 获取系统列表
    getSystemList() {
      precise.getSystemList().then(response => {
        this.modelForm.system = response.data
      })
    },
    // 获取一级模块列表
    getPrimaryList() {
      precise.getPrimaryList({ system: this.systemValue }).then(response => {
        this.modelForm.first = response.data
      })
    },
    // 获取二级模块列表
    getSecondaryList() {
      precise.getSecondaryList({ primary: this.firstModelValue }).then(response => {
        this.modelForm.second = response.data
      })
    },
    // 获取三级模块列表
    getThirdList() {
      precise.getThirdList({ second: this.secondModelValue }).then(response => {
        this.modelForm.third = response.data
      })
    },
    // 清空所有下拉框
    filterClear() {
      this.systemValue = ''
      this.firstModelValue = ''
      this.secondModelValue = ''
      this.thirdModelValue = ''
      this.modelForm.first = []
      this.modelForm.second = []
      this.modelForm.third = []
      this.list.data = []
    },
    // 下拉框是否展示
    handleChangeFlag(type) {
      console.log(type)
      this.changeFlag = type
    },
    // 搜索
    getSearchData() {
      if (!this.systemValue || !this.firstModelValue || !this.secondModelValue) {
        Message.error({
          message: '系统、一二级模块均为必填项',
          duration: 2 * 1000
        })
      } else {
        const params = {
          system: this.systemValue,
          primary: this.firstModelValue,
          secondary: this.secondModelValue
        }
        if (this.thirdModelValue) {
          params.third = this.thirdModelValue
        }
        precise.ModelSearch(params).then(response => {
          this.list.data = response.data
        // console.log(this.list.data)  //for debug
        })
      }
    }
  }
}
</script>
