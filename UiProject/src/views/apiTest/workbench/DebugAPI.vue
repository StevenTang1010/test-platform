<template>
  <div class="main" style="padding:20px;">
    <el-form ref="form" :model="form" :rules="formRules">
      <!--  基础请求    -->
      <el-row :span="24">
        <el-col :span="16">
          <el-form-item prop="addr">
            <el-input v-model.trim="form.addr" placeholder="地址" auto-complete="true" clearable>
              <el-select slot="prepend" v-model="form.request4" placeholder="请求方式" style="width:100px" @change="checkRequest">
                <el-option v-for="(item,index) in request" :key="index+''" :label="item.label" :value="item.value" />
              </el-select>
            </el-input>
          </el-form-item>
        </el-col>
        <el-col :span="4">
          <el-form-item prop="globalEnv">
            <el-select v-model="form.globalEnv" value-key="id" placeholder="请选择环境配置" style="width:200px" clearable>
              <el-option v-for="item in globalEnvs" :key="item.id" :label="'环境配置:'+item.name" :value="item" />
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="2">
          <el-form-item>
            <el-button type="primary" :loading="loadingSend" style="width: 90%;" @click="fastTest">发送</el-button>
          </el-form-item>
        </el-col>
        <el-col :span="2">
          <el-form-item>
            <el-button type="primary" :loading="loadingSave" style="width: 90%;" @click="saveTest">保存</el-button>
          </el-form-item>
        </el-col>
      </el-row>
      <!--   请求头部、请求参数   -->
      <el-row :span="24">
        <el-tabs>
          <!-- 请求头部 -->
          <el-tab-pane>
            <span slot="label" style="font-weight:bold;font-size:14px;color:#2C8DF4;">请求头部</span>
            <el-table ref="multipleHeadTable" size="mini" :data="form.head" highlight-current-row style="width: 100%" @selection-change="selsChangeHead">
              <el-table-column type="selection" min-width="5%" label="头部" />
              <el-table-column prop="name" label="名称" min-width="40%" sortable>
                <template slot-scope="scope">
                  <el-select v-model="scope.row.value" size="mini" value-key="id" filterable placeholder="全局Headers">
                    <el-option v-for="item in globalHeaders" :key="item.id" :label="item.name" :value="item.value" />
                  </el-select>
                </template>
              </el-table-column>
              <el-table-column label="操作" min-width="10%">
                <template slot-scope="scope">
                  <el-popover placement="bottom" trigger="click" :content="scope.row.value">
                    <el-button slot="reference" size="mini" type="primary">查看</el-button>
                  </el-popover>
                </template>
              </el-table-column>
              <el-table-column label="" min-width="40%">
                <template slot-scope="scope">
                  <el-button v-if="scope.$index===(form.head.length-1)" size="mini" type="primary" class="el-icon-plus" @click="addHead">添加</el-button>
                  <el-button v-if="scope.$index>=1" size="mini" type="danger" @click="delHead(scope.$index)">删除</el-button>
                </template>
              </el-table-column>
            </el-table>
            <template>
              <div class="demo-input-suffix" style="width: 50%;padding: 10px 10px 10px 0;">
                <span style="font-size:14px;color:#2C8DF4;">自定义</span>
                <el-button type="text" size="mini" icon="el-icon-info" @click="dialogTableVisible=true" />
                <el-dialog title="Header示例" :visible.sync="dialogTableVisible">
                  <el-table :data="header">
                    <el-table-column property="label" label="Header" width="150" />
                    <el-table-column property="value" label="示例" width="200" />
                  </el-table>
                </el-dialog>
                <el-button type="primary" size="mini" plain @click="prettyPrintCustomHeader(2)">格式化</el-button>
                <el-button type="primary" size="mini" plain @click="prettyPrintCustomHeader(0)">压缩</el-button>
                <el-link type="primary" :underline="false" href="https://www.bejson.com" target="_blank" style="padding-left: 10px">JSON工具</el-link>
                <el-input
                  v-model="form.customHeader"
                  type="textarea"
                  :autosize="{ minRows: 2}"
                  placeholder="自定义Header: json格式字符串"
                />
              </div>
            </template>
          </el-tab-pane>
          <!-- 请求参数 -->
          <el-tab-pane>
            <span slot="label" style="font-weight:bold;font-size:14px;color:#2C8DF4;">请求参数</span>
            <template>
              <el-radio v-model="form.parameterType" label="params">query</el-radio>
              <el-radio v-model="form.parameterType" label="json">json</el-radio>
              <el-radio v-model="form.parameterType" label="data">data</el-radio>
              <el-button type="primary" size="mini" plain @click="prettyPrintParameter(2)">格式化</el-button>
              <el-button type="primary" size="mini" plain @click="prettyPrintParameter(0)">压缩</el-button>
              <el-link type="primary" :underline="false" href="https://www.bejson.com" target="_blank" style="padding-left: 10px">JSON工具</el-link>
            </template>
            <template>
              <div class="demo-input-suffix" style="width: 50%;padding: 10px 10px 10px 0;">
                <el-input
                  v-model="form.parameter"
                  type="textarea"
                  :autosize="{ minRows: 2}"
                  placeholder="请求参数: json格式字符串"
                />
              </div>
            </template>
          </el-tab-pane>
        </el-tabs>
      </el-row>
      <!--   响应结果   -->
      <el-row :span="24" style="padding-top: 30px">
        <el-tabs>
          <el-tab-pane>
            <span slot="label" style="font-weight:bold;font-size:14px;color:#2C8DF4;">响应结果</span>
            <el-card class="box-card" style="width: 80%">
              <div slot="header" class="clearfix">
                <span style="font-size: 15px">
                  <el-tag :size="themeSize">{{ form.request4 }} &nbsp; {{ form.statusCode }} </el-tag>
                  {{ form.requestURL }}
                </span>
              </div>
              <div v-show="!format" :class="resultShow? 'parameter-a': 'parameter-b'">
                <span style="font-size:14px;color:#2C8DF4;">Body</span>
                <el-input
                  v-model="form.resultData"
                  style="font-size:12px;"
                  type="textarea"
                  :autosize="{ minRows: 2, maxRows: 20 }"
                  placeholder="响应Body"
                />
              </div>
              <div :class="resultShow? 'parameter-b': 'parameter-a'" style="padding-top: 10px">
                <span style="font-size:14px;color:#2C8DF4;">Header</span>
                <el-input
                  v-model="form.resultHead"
                  style="font-size:12px;"
                  type="textarea"
                  :autosize="{ minRows: 2, maxRows: 10 }"
                  placeholder="响应Header"
                />
              </div>
            </el-card>
          </el-tab-pane>
        </el-tabs>
      </el-row>
    </el-form>
  </div>
</template>

<script>
import $ from 'jquery'
import { getGlobalEnvList } from '@/api/apiTest/global_env'
import { getGlobalHeaderList } from '@/api/apiTest/global_header'

export default {
  data() {
    const checkJson = (rule, value, callback) => {
      try {
        JSON.parse(value)
      } catch (e) {
        console.log('json格式错误')
        callback(new Error('JSON格式错误！'))
      }
      callback()
    }
    return {
      request: [{ value: 'get', label: 'GET' },
        { value: 'post', label: 'POST' },
        { value: 'put', label: 'PUT' },
        { value: 'delete', label: 'DELETE' }],
      Http: [{ value: 'http', label: 'HTTP' },
        { value: 'https', label: 'HTTPS' }],
      listLoading: false,
      loadingSend: false,
      loadingSave: false,
      dialogTableVisible: false,
      header: [{ value: 'Accept', label: 'Accept' },
        { value: 'Accept-Charset', label: 'Accept-Charset' },
        { value: 'Accept-Encoding', label: 'Accept-Encoding' },
        { value: 'Accept-Language', label: 'Accept-Language' },
        { value: 'Accept-Ranges', label: 'Accept-Ranges' },
        { value: 'Authorization', label: 'Authorization' },
        { value: 'Cache-Control', label: 'Cache-Control' },
        { value: 'Connection', label: 'Connection' },
        { value: 'Cookie', label: 'Cookie' },
        { value: 'Content-Length', label: 'Content-Length' },
        { value: 'Content-Type', label: 'Content-Type' },
        { value: 'Content-MD5', label: 'Content-MD5' },
        { value: 'Date', label: 'Date' },
        { value: 'Expect', label: 'Expect' },
        { value: 'From', label: 'From' },
        { value: 'Host', label: 'Host' },
        { value: 'If-Match', label: 'If-Match' },
        { value: 'If-Modified-Since', label: 'If-Modified-Since' },
        { value: 'If-None-Match', label: 'If-None-Match' },
        { value: 'If-Range', label: 'If-Range' },
        { value: 'If-Unmodified-Since', label: 'If-Unmodified-Since' },
        { value: 'Max-Forwards', label: 'Max-Forwards' },
        { value: 'Origin', label: 'Origin' },
        { value: 'Pragma', label: 'Pragma' },
        { value: 'Proxy-Authorization', label: 'Proxy-Authorization' },
        { value: 'Range', label: 'Range' },
        { value: 'Referer', label: 'Referer' },
        { value: 'TE', label: 'TE' },
        { value: 'Upgrade', label: 'Upgrade' },
        { value: 'User-Agent', label: 'User-Agent' },
        { value: 'Via', label: 'Via' },
        { value: 'Warning', label: 'Warning' }],
      header4: '',
      request3: true,
      result: true,

      globalEnvs: [], // 获取到的全局环境配置
      globalHeaders: [], // 获取到的全局Header配置
      form: {
        request4: 'GET',
        Http4: 'HTTP',
        addr: '',
        head: [{ name: '', value: '' }],
        globalEnv: '',
        customHeader: '{}',
        parameter: '{}',
        parameterType: 'json',
        requestURL: '',
        statusCode: '',
        resultData: '',
        resultHead: ''
      },
      formRules: {
        addr: [
          { required: true, message: '请输入地址', trigger: 'blur' }
        ],
        globalEnv: [
          { required: false, message: '请选择环境配置', trigger: 'blur' }
        ],
        customHeader: [
          { required: true, validator: checkJson, message: '请输入正确的json格式且不能为空', trigger: 'blur' }
        ]
      },
      headers: '',
      parameters: '',
      resultShow: true,
      format: false
    }
  },
  watch: {
  },
  mounted() {
    this.toggleHeadSelection(this.form.head)
    this.getEnv()
    this.getHeader()
  },
  methods: {
    checkRequest() {
      const request = this.form.request4
      this.request3 = !(request === 'GET' || request === 'DELETE')
    },
    prettyPrintCustomHeader(space = 2) {
      const obj = JSON.parse(this.form.customHeader)
      this.form.customHeader = JSON.stringify(obj, undefined, space)
    },
    prettyPrintParameter(space = 2) {
      const obj = JSON.parse(this.form.parameter)
      this.form.parameter = JSON.stringify(obj, undefined, space)
    },
    prettyPrintResultData() {
      if (this.format === false) {
        this.form.resultData = JSON.stringify(this.form.resultData, undefined, 2)
        this.format = !this.format
      }
    },
    // 获取HOST列表
    getEnv() {
      this.listLoading = true
      getGlobalEnvList({}).then(response => {
        const { msg, code } = response
        this.listLoading = false
        if (code === 2) {
          this.globalEnvs = response.data.list
        } else {
          this.$message.error({
            message: msg,
            center: true
          })
        }
      })
    },
    getHeader() {
      this.listLoading = true
      getGlobalHeaderList({}).then(response => {
        const { msg, code } = response
        this.listLoading = false
        if (code === 2) {
          this.globalHeaders = response.data.list
        } else {
          this.$message.error({
            message: msg,
            center: true
          })
        }
      })
    },
    toggleHeadSelection(rows) {
      rows.forEach(row => {
        this.$refs.multipleHeadTable.toggleRowSelection(row, true)
      })
    },
    addHead() {
      const headers = { name: '', value: '' }
      this.form.head.push(headers)
      const rows = [this.form.head[this.form.head.length - 1]]
      this.toggleHeadSelection(rows)
    },
    delHead(index) {
      if (this.form.head.length !== 1) {
        this.form.head.splice(index, 1)
      }
    },
    selsChangeHead: function(sels) {
      this.headers = sels
    },
    extend(des, src, override) {
      if (src instanceof Array) {
        for (let i = 0, len = src.length; i < len; i++) { this.extend(des, src[i], override) }
      }
      for (const i in src) {
        if (override || !(i in des)) {
          des[i] = src[i]
        }
      }
      return des
    },
    fastTest: function() {
      // 清空响应结果旧数据
      this.form.statusCode = ''
      this.form.resultHead = ''
      this.form.resultData = ''
      this.form.requestURL = ''

      this.$refs.form.validate((valid) => {
        if (valid) {
          this.loadingSend = true
          let _parameter = {}
          let _headers = {}
          const self = this
          self.form.statusCode = ''
          self.form.resultData = ''
          self.form.resultHead = ''
          for (let i = 0; i < this.form.head.length; i++) {
            const v = this.form.head[i]['value']
            if (v) {
              _headers = Object.assign(_headers, JSON.parse(v))
            }
          }
          _headers = Object.assign(_headers, JSON.parse(this.form.customHeader))
          const _url = this.form.globalEnv.host_mk + this.form.addr
          // const _parameterType = this.form.parameterType
          _parameter = Object.assign(_parameter, JSON.parse(this.form.parameter))
          this.form.requestURL = _url

          // console.log('请求头：' + JSON.stringify(_headers))
          // console.log('请求地址：' + this.form.request4 + ' ' + _url)
          // console.log('请求参数：' + _parameterType + ', ' + JSON.stringify(_parameter))
          $.ajax(_url, {
            type: this.form.request4,
            url: _url,
            async: true, // 默认设置为true，所有请求均为异步请求。如果需要发送同步请求，请将此选项设置为false。
            // 注意，同步请求将锁住浏览器，用户其他操作必须等待请求完成才可以执行。
            data: _parameter,
            headers: _headers,
            timeout: 5000,
            dataType: 'json',
            success: function(data, status, jqXHR) {
              // console.log(data)
              self.loadingSend = false
              self.form.statusCode = jqXHR.status
              self.form.resultData = JSON.stringify(data, undefined, 2)
              self.form.resultHead = jqXHR.getAllResponseHeaders()
            },
            error: function(jqXHR, error, errorThrown) {
              self.loadingSend = false
              self.form.statusCode = jqXHR.status
              self.form.resultData = jqXHR.responseJSON
              self.form.resultHead = jqXHR.getAllResponseHeaders()
            }
          })
          // console.log('请求响应：' + this.form.resultData)
        }
      })
    },
    saveTest: function() {
      this.$message({
        message: '功能待开发...',
        type: 'warning'
      })
    },
    showBody() {
      this.resultShow = true
    },
    showHeader() {
      this.resultShow = false
    },
    handleChange(val) {
    },
    onSubmit() {
      console.log('submit!')
    }
  }
}
</script>

<style scoped>
  .el-header, .el-footer {
    background-color: #B3C0D1;
    color: #333;
    text-align: center;
    line-height: 60px;
  }

  .el-aside {
    background-color: #D3DCE6;
    color: #333;
    text-align: center;
    line-height: 200px;
  }

  .el-main {
    background-color: #E9EEF3;
    color: #333;
    text-align: center;
    line-height: 160px;
  }

  body > .el-container {
    margin-bottom: 40px;
  }

  .el-container:nth-child(5) .el-aside,
  .el-container:nth-child(6) .el-aside {
    line-height: 260px;
  }

  .el-container:nth-child(7) .el-aside {
    line-height: 320px;
  }
</style>
