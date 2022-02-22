<template>
  <el-col
    :span="span"
    :xs="spanMap.xs"
    :sm="spanMap.sm"
    :md="spanMap.md"
    :lg="spanMap.lg"
    :xl="spanMap.xl"
    class="descriptions-item"
  >
    <div class="descriptions-item-content">
      <div class="descriptions-item-label">{{ label }}：</div>
      <div class="descriptions-item-value">
        <slot v-if="$slots.content" name="content" />
        <div v-else class="default-value" :title="value">{{ value }}</div>
      </div>
    </div>
  </el-col>
</template>

<script>
export default {
  name: 'ElDescriptionItem',
  props: {
    spanMap: {
      type: Object,
      required: false,
      default: () => { return { } }
    },
    span: {
      type: Number,
      required: false,
      default: 6
    },
    label: {
      required: true
    },
    value: {
      required: false,
      default() {
        return ''
      }
    }
  }

}
</script>

<style scoped lang="scss">
  .descriptions-item {
    padding-bottom: 10px;
    padding-right: 20px;
    span {
      display: inline-block;
    }
    .descriptions-item-content {
      display: flex;
      justify-content: flex-start;
      align-items: center;
      color: rgba(0,0,0,.65);
      font-size: 14px;
      -webkit-font-smoothing: antialiased;
      text-rendering: optimizeLegibility;
      font-family: Helvetica Neue, Helvetica, PingFang SC, Hiragino Sans GB, Microsoft YaHei, Arial, sans-serif;
      line-height: 1.0;
      width: 100%;
      .descriptions-item-label{
        flex-grow: 0;
        flex-shrink: 0;
        color: rgba(0,0,0,.85);
        font-weight: 400;
        font-size: 14px;
        line-height: 1.0;
        text-align: left;
        //text-align-last: justify;
        min-width: 40px;
      }
      .descriptions-item-value{
        flex-grow: 1;
        overflow: hidden;
        .default-value{
          overflow: hidden;
          text-overflow: ellipsis;
          white-space: nowrap;
        }
      }
    }
  }
</style>
