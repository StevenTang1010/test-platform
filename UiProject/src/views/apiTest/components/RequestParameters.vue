<template>
  <!-- 自定义参数BODY -->
  <div class="demo-input-suffix" style="width: 80%;padding: 10px 10px 10px 0;">
    <el-radio v-model="parameterType" label="params">query</el-radio>
    <el-radio v-model="parameterType" label="json">json</el-radio>
    <el-radio v-model="parameterType" label="data">data</el-radio>
    <el-button type="primary" :size="themeSize" plain @click="formatParameter">格式化</el-button>
    <el-link type="primary" :underline="false" href="https://www.bejson.com" target="_blank" style="padding-left: 10px">JSON工具</el-link>
    <el-input
      v-show="parameterType==='params'"
      v-model="paramsKwargs"
      type="textarea"
      :autosize="{ minRows: 2}"
      placeholder="请输入参数 query string"
    />
    <el-input
      v-show="parameterType==='json'"
      v-model="jsonKwargs"
      type="textarea"
      :autosize="{ minRows: 2}"
      placeholder="请输入json参数 content-type/json"
    />
    <el-input
      v-show="parameterType==='data'"
      v-model="dataKwargs"
      type="textarea"
      :autosize="{ minRows: 2}"
      placeholder="请输入参数 form data"
    />
  </div>
</template>

<script>
export default {
  name: 'RequestParameters',
  props: {
  },
  data() {
    return {
      themeSize: this.$store.state.settings.themeSize,
      format: false,

      parameterType: 'json',
      paramsKwargs: this.$attrs.value.req_params,
      jsonKwargs: this.$attrs.value.req_json,
      dataKwargs: this.$attrs.value.req_data
    }
  },
  computed: {
    form() {
      return {
        req_params: this.paramsKwargs,
        req_json: this.jsonKwargs,
        req_data: this.dataKwargs
      }
    }
  },
  watch: {
    form() {
      this.$emit('input', {
        ...this.$attrs.value,
        ...this.form
      })
    },
    '$attrs.value.req_params': function(n) {
      this.paramsKwargs = this.$attrs.value.req_params
    },
    '$attrs.value.req_json': function(n) {
      this.jsonKwargs = this.$attrs.value.req_json
    },
    '$attrs.value.req_data': function(n) {
      this.dataKwargs = this.$attrs.value.req_data
    },
    paramsKwargs() {},
    jsonKwargs() {},
    dataKwargs() {}
  },
  methods: {
    formatParameter() {
      this.format = !this.format
      const space = this.format ? 2 : 0
      try {
        if (this.$attrs.value.req_params) {
          const paramsObj = JSON.parse(this.$attrs.value.req_params)
          this.paramsKwargs = JSON.stringify(paramsObj, undefined, space)
        }
        if (this.$attrs.value.req_json) {
          const jsonObj = JSON.parse(this.$attrs.value.req_json)
          this.jsonKwargs = JSON.stringify(jsonObj, undefined, space)
        }
        if (this.$attrs.value.req_data) {
          const dataObj = JSON.parse(this.$attrs.value.req_data)
          this.dataKwargs = JSON.stringify(dataObj, undefined, space)
        }
      } catch (e) {
        console.log('捕获到异常：', e)
        this.$message.error({
          message: e
        })
      }
    }
  }
}
</script>

<style scoped>

</style>
