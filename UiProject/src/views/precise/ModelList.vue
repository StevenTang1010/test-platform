<template>
  <div>
    <el-row style="padding-left: 1px; padding-top: 1px">
      <el-col :span="25">
        <el-form :model="modelForm">
          <el-form-item>
            <el-select v-model="systemValue" clearable placeholder="请选择系统" size="mini" @change="getPrimaryList">
              <el-option v-for="(item, index) in modelForm.system" :key="index" :label="item.system_name" :value="item.system_id" />
            </el-select>
            <el-select v-model="firstModelValue" clearable placeholder="请选择一级模块" size="mini" @change="getSecondaryList">
              <el-option v-for="(item, index) in modelForm.first" :key="index" :label="item.primary_module_name" :value="item.primary_module_id" />
            </el-select>
            <el-select v-model="secondModelValue" clearable placeholder="请选择二级模块" size="mini" @change="getThirdList">
              <el-option v-for="(item, index) in modelForm.second" :key="index" :label="item.secondary_module_name" :value="item.secondary_module_id" />
            </el-select>
            <el-select v-model="thirdModelValue" clearable placeholder="请选择三级模块" size="mini">
              <el-option v-for="(item, index) in modelForm.third" :key="index" :label="item.third_module_name" :value="item.third_module_id" />
            </el-select>
            <el-button type="primary" icon="el-icon-search" size="small" style="margin-left: 10px" circle @click.native="getSearchData" />
            <el-button type="default" icon="el-icon-refresh-left" size="small" style="margin-left: 10px" circle @click.native="filterClear" />
          </el-form-item>
        </el-form>
      </el-col>
      <el-button type="primary" icon="el-icon-plus" size="small" style="float: right; margin-right: 20px; margin-top: 2px" circle @click="addDialog" />
      <el-button type="primary" icon="el-icon-upload2" size="small" style="float: right; margin-right: 20px; margin-top: 2px" circle @click="dialogVisible = true" />
    </el-row>
    <div class="table-container" style="height: 100%">
      <el-table
        ref="table"
        v-loading="listLoading"
        :data="list.data"
        border
        row-key="func"
        element-loading-text="Loading"
      >
        <template slot="empty">
          <!--  <img class="data-pic" src="#" alt="" />-->
          <span style="font-size: 16px">先查询，不然不会有数据的</span>
        </template>
        <el-table-column align="center" label="系统" prop="system" />
        <el-table-column label="一级模块" align="center" prop="primary" :show-overflow-tooltip="true" />
        <el-table-column label="二级模块" align="center" prop="secondary" :show-overflow-tooltip="true" />
        <el-table-column label="三级模块" align="center" prop="third" :show-overflow-tooltip="true" :render-header="renderThird">
          <template slot-scope="scope">
            <router-link :to="{ name: 'thirdModel', params: {third: scope.row.third}}" style="cursor:pointer;color: #278d6c;text-decoration:underline">
              {{ scope.row.third }}
            </router-link>
          </template>
        </el-table-column>
        <el-table-column label="功能" prop="func" align="center" :show-overflow-tooltip="true" :render-header="renderFunc">
          <template slot-scope="scope">
            <router-link :to="{ name: 'function', params: {func: scope.row.func}}" style="cursor:pointer;color: #278d6c;text-decoration:underline">
              {{ scope.row.func }}
            </router-link>
          </template>
        </el-table-column>
        <el-table-column align="center" label="操作" width="200px">
          <template slot-scope="scope">
            <el-button
              type="primary"
              icon="el-icon-edit"
              circle
              @click="openRowEdit(scope.$index, scope.row)"
            />
          </template>
        </el-table-column>
      </el-table>
      <br>
    </div>
    <div>
      <el-drawer
        ref="drawer"
        title="新增模块/功能"
        size="50%"
        :visible.sync="dialogFormVisible"
        style="font-size: large;"
      >
        <el-form :model="addForm" style="margin: 20px;" label-width="80px">
          <el-form-item label="系统" prop="name">
            <el-select v-model="addSystem" autocomplete="off" clearable size="small" placeholder="请选择系统" style="padding-right: 5px" @change="getDialogPrimaryList">
              <el-option v-for="(item, index) in addForm.system" :key="index" :label="item.system_name" :value="item.system_id" />
            </el-select>
          </el-form-item>
          <el-form-item label="一级模块" prop="name">
            <el-select v-model="addFirst" autocomplete="off" clearable size="small" placeholder="请选择一级模块" style="padding-right: 5px" @change="getDialogSecondaryList">
              <el-option v-for="(item, index) in addForm.first" :key="index" :label="item.primary_module_name" :value="item.primary_module_id" />
            </el-select>
            <el-button type="primary" icon="el-icon-plus" size="small" circle />
          </el-form-item>
          <el-form-item label="二级模块" prop="name">
            <el-select v-model="addSecond" autocomplete="off" clearable size="small" placeholder="请选择二级模块" style="padding-right: 5px" @change="getDialogThirdList">
              <el-option v-for="(item, index) in addForm.second" :key="index" :label="item.secondary_module_name" :value="item.secondary_module_id" />
            </el-select>
            <el-button type="primary" icon="el-icon-plus" size="small" circle />
          </el-form-item>
          <el-form-item label="三级模块" prop="name">
            <el-select v-model="addThird" autocomplete="off" clearable size="small" placeholder="请选择三级模块" style="padding-right: 5px">
              <el-option v-for="(item, index) in addForm.third" :key="index" :label="item.third_module_name" :value="item.third_module_id" />
            </el-select>
            <el-button type="primary" icon="el-icon-plus" size="small" circle />
          </el-form-item>
          <el-form-item label="功能" prop="name">
            <el-input v-model="addFunc" autocomplete="off" placeholder="请输入功能" style="width: 70%;" />
          </el-form-item>
          <el-form-item label="关联功能">
            <el-select
              v-model="addDirectFunc"
              autocomplete="off"
              filterable
              multiple
              allow-create
              remote
              clearable
              size="small"
              placeholder="输入关键字查询"
              style="width: 70%"
              :remote-method="getDirectFuncList"
              :loading="DirectLoading"
            >
              <el-option v-for="(item, index) in addForm.directFunc" :key="index" :label="item.value" :value="item.value" />
            </el-select>
            <el-button type="primary" icon="el-icon-plus" size="small" circle style="margin-left: 5px" @click="addFunction" />
          </el-form-item>
        </el-form>
        <div class="drawer-footer" style="padding-left: 20px">
          <el-button style="width: 100px" @click="$refs.drawer.closeDrawer()">取消</el-button>
          <el-button type="primary" style="width: 100px" @click.native="addFunForm">提交</el-button>
        </div>
        <el-drawer
          title="新增功能"
          size="40%"
          :append-to-body="true"
          :visible.sync="addFuncVisible"
        />
      </el-drawer>
      <el-drawer
        ref="drawer2"
        title="编辑模块/功能"
        size="50%"
        :visible.sync="editFormVisible"
        style="font-size: large;"
      >
        <el-form :model="editForm" style="margin: 20px;" label-width="80px">
          <el-form-item label="系统" prop="name">
            <el-input v-model="editForm.system" autocomplete="off" :disabled="true" />
          </el-form-item>
          <el-form-item label="一级模块" prop="name">
            <el-input v-model="editForm.primary" autocomplete="off" :disabled="true" />
          </el-form-item>
          <el-form-item label="二级模块" prop="name">
            <el-input v-model="editForm.secondary" autocomplete="off" :disabled="true" />
          </el-form-item>
          <el-form-item label="三级模块" prop="name">
            <el-input v-model="editForm.third" autocomplete="off" :disabled="true" />
          </el-form-item>
          <el-form-item label="功能" prop="name">
            <el-input v-model="editForm.func" autocomplete="off" :disabled="true" />
          </el-form-item>
          <el-form-item label="关联功能">
            <el-select
              v-model="editDirectFunc"
              autocomplete="off"
              filterable
              multiple
              allow-create
              remote
              clearable
              size="small"
              placeholder="输入关键字查询"
              style="width: 70%"
              :remote-method="getEditDirectFuncList"
              :loading="DirectLoading"
            >
              <el-option v-for="(item, index) in editForm.editDirectFunc" :key="index" :label="item.value" :value="item.value" />
            </el-select>
          </el-form-item>
        </el-form>
        <div class="drawer-footer" style="padding-left: 20px">
          <el-button style="width: 100px" @click="$refs.drawer2.closeDrawer()">取消</el-button>
          <el-button type="primary" style="width: 100px" @click.native="editFuncForm">提交</el-button>
        </div>
        <el-drawer
          title="新增功能"
          size="40%"
          :append-to-body="true"
          :visible.sync="addFuncVisible"
        />
      </el-drawer>
    </div>
    <el-dialog
      title="批量添加"
      :visible.sync="dialogVisible"
      width="30%">
      <el-upload
        class="upload-demo"
        drag
        action="https://jsonplaceholder.typicode.com/posts/"
        :file-list="attachList">
        <i class="el-icon-upload"></i>
        <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
        <div class="el-upload__tip" slot="tip">只能上传Excel/Xmind文件，且不超过5MB</div></el-upload>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="dialogVisible = false">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<style>
  .el-drawer__body {
    overflow: auto;
  }
  .el-dialog__header{
    background:#EBEEF5;
    border-bottom: 1px solid#EBEEF5;
  }
  .el-dialog{
    text-align: left;
  }
  .el-upload, .el-upload-dragger{
    width: 100%;
  }
</style>

<script>
import * as precise from '@/api/precise'
import { Message } from 'element-ui'
import { CreateFunc, UpdateFunc } from '@/api/precise'

export default {
  name: 'ModelList',
  data() {
    return {
      DirectLoading: false,
      // 控制弹窗开关
      dialogFormVisible: false,
      // 打开编辑窗口
      editFormVisible: false,
      addFuncVisible: false,
      addfirstVisible: false,
      addsecondVisible: false,
      addthirdVisible: false,
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
      // 新增模块功能表单
      addForm: {
        system: [],
        first: [],
        second: [],
        third: [],
        func: [],
        directFunc: []
      },
      // 新增模块功能输入数据
      addSystem: '',
      addFirst: '',
      addSecond: '',
      addThird: '',
      addFunc: '',
      addDirectFunc: [],
      // 编辑模块功能输入数据
      editForm: {
        system: '',
        primary: '',
        secondary: '',
        third: '',
        func: '',
        editDirectFunc: []
      },
      editDirectFunc: [],
      // 关联功能搜索
      directFunc: [],
      // 表格内容
      list: {
        data: []
      },
      // 表格高度
      tableHeight: '',
      // table表格加载转圈
      listLoading: false,
      // 下拉框是否展示
      changeFlag: false,
      // 上传文件弹窗
      dialogVisible: false,
      // 设置文件列表属性attachList,需要绑定到<el-upload>元素上。默认值为空数组，表示文件列表为空
      attachList: []
    }
  },
  created() {
  },
  mounted() {
    if (localStorage.getItem('searchResult')) {
      this.getSearchResult()
      this.getSystemList()
    } else {
      this.getSystemList()
    }
  },
  methods: {
    // 获取全局变量，渲染返回后的内容
    getSearchResult() {
      const searchResult = JSON.parse(localStorage.getItem('searchResult'))
      console.log(searchResult)
      this.list.data = searchResult.tableData
      // this.systemValue = searchResult.system
      // this.firstModelValue = searchResult.primary
      // this.secondModelValue = searchResult.secondary
      // this.thirdModelValue = searchResult.third
    },
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
    // 获取弹窗系统列表
    getDialogSystemList() {
      precise.getSystemList().then(response => {
        this.addForm.system = response.data
      })
    },
    // 获取弹窗一级模块列表
    getDialogPrimaryList() {
      precise.getPrimaryList({ system: this.addSystem }).then(response => {
        this.addForm.first = response.data
      })
    },
    // 获取弹窗二级模块列表
    getDialogSecondaryList() {
      precise.getSecondaryList({ primary: this.addFirst }).then(response => {
        this.addForm.second = response.data
      })
    },
    // 获取弹窗三级模块列表
    getDialogThirdList() {
      precise.getThirdList({ second: this.addSecond }).then(response => {
        this.addForm.third = response.data
      })
    },
    // 新增里的搜索获取功能关联
    getDirectFuncList(querystring) {
      if (querystring !== '') {
        console.log(querystring)
        this.DirectLoading = true
        precise.MatchFunc({ query: querystring }).then(response => {
          this.DirectLoading = false
          this.addForm.directFunc = response.data
        })
      } else {
        this.addForm.directFunc = []
      }
    },
    // 编辑里的搜索获取功能关联
    getEditDirectFuncList(querystring) {
      if (querystring !== '') {
        console.log(querystring)
        this.DirectLoading = true
        precise.MatchFunc({ query: querystring }).then(response => {
          this.DirectLoading = false
          this.editForm.editDirectFunc = response.data
        })
      } else {
        this.editForm.editDirectFunc = []
      }
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
    // 新增功能提交
    addFunForm() {
      if (!this.addThird || !this.addFunc || !this.addDirectFunc) {
        Message.error({
          message: '请填写关键数据~！',
          duration: 5 * 1000
        })
      } else {
        const addData = {
          system: this.addSystem,
          first: this.addFirst,
          second: this.addSecond,
          third: this.addThird,
          func: this.addFunc,
          directFunc: this.addDirectFunc
        }
        precise.CreateFunc(addData).then(response => {
          console.log(response)
          switch (response.code) {
            case 2:
              Message.success({
                message: '新增成功',
                duration: 2 * 1000
              })
              break
            case 0:
              Message.error({
                message: '新建失败，原因么有深究',
                duration: 5 * 1000
              })
              break
          }
        })
      }
    },
    // 编辑功能提交
    editFuncForm() {
      if (!this.editForm.editDirectFunc) {
        Message.error({
          message: '请填写关键数据~！',
          duration: 5 * 1000
        })
      } else {
        const addData = {
          func: this.editForm.func,
          directFunc: this.editForm.editDirectFunc
        }
        precise.UpdateFunc(addData).then(response => {
          console.log(response)
          switch (response.code) {
            case 2:
              Message.success({
                message: '新增成功',
                duration: 2 * 1000
              })
              break
            case 0:
              Message.error({
                message: '新建失败，原因么有深究',
                duration: 5 * 1000
              })
              break
          }
        })
      }
    },
    // 搜索
    getSearchData() {
      localStorage.removeItem('searchResult')
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
          const searchResult = {
            // system: this.systemValue,
            // primary: this.firstModelValue,
            // secondary: this.secondModelValue,
            // third: this.thirdModelValue,
            tableData: response.data
          }
          localStorage.setItem('searchResult', JSON.stringify(searchResult))
        })
      }
    },
    // 打开编辑窗口
    addDialog() {
      this.dialogFormVisible = true // 打开窗口
      this.getDialogSystemList()
    },
    // 打开编辑窗口
    addFunction() {
      this.addFuncVisible = true // 打开窗口
      this.getDialogSystemList()
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
    // 打开编辑窗口
    openRowEdit(index, row) {
      this.editFormVisible = true // 打开窗口
      this.editForm = Object.assign({}, row) // 将数据传入当前dialog
      this.editForm.index = index // 传index
    }
  }
}
</script>
