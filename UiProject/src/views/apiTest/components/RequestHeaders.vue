<template>
  <!-- 自定义请求headers -->
  <div class="demo-input-suffix" style="width: 80%;padding: 10px 10px 10px 0;">
    <el-button type="primary" :size="themeSize" plain @click="formatHeader">格式化</el-button>
    <el-link type="primary" :underline="false" href="https://www.bejson.com" target="_blank" style="padding-left: 10px">JSON工具</el-link>
    <el-input
      v-model="inputValue"
      type="textarea"
      :autosize="{ minRows: 2}"
      placeholder="请求头: json格式字符串"
    />
  </div>
</template>

<script>
export default {
  name: 'RequestHeaders',
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
    formatHeader() {
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
