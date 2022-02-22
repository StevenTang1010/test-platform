<template>
  <!-- 自定义 设置变量 -->
  <div class="demo-input-suffix" style="width: 80%;padding: 10px 10px 10px 0;">
    <el-button type="primary" :size="themeSize" plain @click="formatVariable">格式化</el-button>
    <el-input
      v-model="inputValue"
      type="textarea"
      :autosize="{ minRows: 2}"
      placeholder="提取响应结果到全局变量: json格式字符串，支持JMESPath/JSONPath，示例:
       {'foo': 'body.args.foo'}"
    />
  </div>
</template>

<script>
export default {
  name: 'ResponseExtract',
  data() {
    return {
      themeSize: this.$store.state.settings.themeSize,
      format: false
    }
  },
  computed: {
    inputValue: {
      get() {
        return this.$attrs.value
      },
      set(v) {
        this.$emit('input', v)
      }
    }
  },
  methods: {
    formatVariable() {
      this.format = !this.format
      const space = this.format ? 2 : 0
      try {
        const obj = JSON.parse(this.inputValue)
        this.inputValue = JSON.stringify(obj, undefined, space)
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
