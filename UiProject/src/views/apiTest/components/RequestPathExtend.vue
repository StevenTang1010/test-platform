<template>
  <!-- 请求路径扩展 -->
  <div class="main" style="width: 90%">
    <el-input
      v-model="inputValue"
      type="textarea"
      :autosize="{ minRows: 1}"
      placeholder="请求路径末尾扩展，支持常量、变量、方法拼接，示例:/$cusID-${foo()}/detail"
    />
  </div>
</template>

<script>

export default {
  name: 'RequestPathExtend',
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
  methods: {}
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
