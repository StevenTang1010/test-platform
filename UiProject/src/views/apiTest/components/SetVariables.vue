<template>
  <!-- 自定义 设置变量 -->
  <div class="demo-input-suffix" style="width: 80%;padding: 10px 10px 10px 0;">
    <el-button type="primary" :size="themeSize" plain @click="formatVariable(2)">格式化</el-button>
    <el-button type="primary" :size="themeSize" plain @click="formatVariable(0)">压缩</el-button>
    <el-link type="primary" :underline="false" href="https://www.bejson.com" target="_blank" style="padding-left: 10px">JSON工具</el-link>
    <el-input
      v-model="inputValue"
      type="textarea"
      :autosize="{ minRows: 2}"
      placeholder="设置变量: json格式字符串，示例:
       {'foo1': 1, 'foo2':'$var1', 'foo3': '${sum(1,2)}'}"
    />
  </div>
</template>

<script>
export default {
  name: 'SetVariables',
  data() {
    return {
      themeSize: this.$store.state.settings.themeSize
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
    formatVariable(space = 2) {
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
