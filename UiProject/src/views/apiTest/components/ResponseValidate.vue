<template>
  <!-- 期望输出 -->
  <div class="main" style="width: 90%">
    <el-button type="primary" :size="themeSize" plain @click="formatValue">格式化</el-button>
    <el-button :size="themeSize" type="text" title="帮助" icon="el-icon-info" @click="helpVisible = true" />
    <el-button id="copyBtn" type="text" :size="themeSize" title="复制" class="el-icon-document-copy" :data-clipboard-text="inputValue" @click="copyText($event)" />
    <el-input
      v-model="inputValue"
      type="textarea"
      :autosize="{ minRows: 2}"
      placeholder="返回数据校验: json格式字符串，支持JMESPath/JSONPath，示例:
       {'eq':{'body.args.foo': 100}}"
    />
  </div>
</template>

<script>
import Clipboard from 'clipboard'

export default {
  name: 'ResponseValidate',
  data() {
    return {
      themeSize: this.$store.state.settings.themeSize,
      format: false,

      // 显示帮助信息
      helpVisible: false
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
    formatValue() {
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
    },
    copyText(event) {
      const btnID = '#' + event.currentTarget.id
      // console.log(btnID)
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
    }
  }
}
</script>

<style lang="scss" scoped>
  ::v-deep .el-popover{
      height: 200px;
      overflow: auto;
    }

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
