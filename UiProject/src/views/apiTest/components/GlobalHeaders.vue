<template>
  <!-- 全局header选择+自定义header -->
  <el-collapse value="2" @change="handleChange">
    <el-collapse-item name="1">
      <span slot="title" style="font-weight:bold;font-size:14px;color:#2C8DF4;">请求头</span>
      <el-table ref="multipleHeadTable" :size="themeSize" :data="headerModel" highlight-current-row style="width: 100%" @selection-change="selsChangeHead">
        <el-table-column type="selection" min-width="5%" label="头部" />
        <el-table-column prop="name" label="名称" min-width="50%" sortable>
          <template slot-scope="scope">
            <el-select v-model="scope.row.value" :size="themeSize" value-key="id" filterable placeholder="全局Headers">
              <el-option v-for="item in globalHeader_options" :key="item.id" :label="item.name" :value="item.value" />
            </el-select>
          </template>
        </el-table-column>
        <el-table-column label="操作" min-width="15%">
          <template slot-scope="scope">
            <el-popover placement="bottom" trigger="click" :content="scope.row.value">
              <el-button slot="reference" :size="themeSize" type="primary">查看</el-button>
            </el-popover>
          </template>
        </el-table-column>
        <el-table-column label="" min-width="40%">
          <template slot-scope="scope">
            <el-button v-if="scope.$index===(headerModel.length-1)" :size="themeSize" type="primary" class="el-icon-plus" @click="addHead">添加</el-button>
            <el-button v-if="scope.$index>=1" :size="themeSize" type="danger" @click="delHead(scope.$index)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      <template>
        <div class="demo-input-suffix" style="width: 100%;padding: 10px 10px 10px 0;">
          <span style="font-size:14px;color:#2C8DF4;">自定义</span>
          <el-button type="primary" :size="themeSize" plain @click="prettyPrintCustomHeader(2)">格式化</el-button>
          <el-button type="primary" :size="themeSize" plain @click="prettyPrintCustomHeader(0)">压缩</el-button>
          <el-link type="primary" :underline="false" href="https://www.bejson.com" target="_blank" style="padding-left: 10px">JSON工具</el-link>
          <el-input
            v-model="customHeader"
            type="textarea"
            :autosize="{ minRows: 2}"
            placeholder="自定义Header: json格式字符串  -- TODO"
          />
        </div>
      </template>
    </el-collapse-item>
  </el-collapse>
</template>

<script>
import get_base_data from '@/api/apiTest/get_base_data'

export default {
  name: 'GlobalHeaders',
  mixins: [get_base_data],
  props: {
    headers: {
      type: String,
      default() {
        return ''
      }
    }
  },
  data() {
    return {
      themeSize: this.$store.state.settings.themeSize,
      headerModel: [{ name: '', value: '' }], // header模板 -- 初始化herder选择列表
      customHeader: '{}'
    }
  },
  mounted() {
    this.getHeader()
  },
  methods: {
    // 折叠版 click
    handleChange(val) {
      // console.log(val)
    },
    toggleHeadSelection(rows) {
      rows.forEach(row => {
        this.$refs.multipleHeadTable.toggleRowSelection(row, true)
      })
    },
    addHead() {
      const headers = { name: '', value: '' }
      this.headerModel.push(headers)
      const rows = [this.headerModel[this.headerModel.length - 1]]
      this.toggleHeadSelection(rows)
    },
    delHead(index) {
      if (this.headerModel.length !== 1) {
        this.headerModel.splice(index, 1)
      }
    },
    selsChangeHead: function(sels) {
      this.headers = sels
    },
    // JSON格式化header
    prettyPrintCustomHeader(space = 2) {
      try {
        const obj = JSON.parse(this.customHeader)
        this.customHeader = JSON.stringify(obj, undefined, space)
      } catch (e) {
        console.log('捕获到异常：', e)
        this.$message.error({
          message: e
        })
      }
    },
    // 头部信息格式化
    parseHeader() {
      let _headers = {}
      for (let i = 0; i < this.headerModel.length; i++) {
        const v = this.headerModel[i]['value']
        if (v) {
          _headers = Object.assign(_headers, JSON.parse(v))
        }
      }
      _headers = Object.assign(_headers, JSON.parse(this.customHeader))
      this.headers = JSON.stringify(_headers)
    }
  }
}
</script>

<style scoped>

</style>
