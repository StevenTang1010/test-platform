<template>
  <!--  统计数据展示 行  -->
  <div class="component-container">
    <div
      v-for="(item,index) in statisticList"
      :key="index"
      class="content-module"
    >
      <div class="list-label">
        <span class="label-content">{{ item.label }}</span>
      </div>
      <p class="list-count">{{ item.count }}</p>
    </div>
  </div>
</template>

<script>
export default {
  name: '',
  props: {
    statisticList: {
      type: Array,
      default() {
        return []
      }
    }
  },
  created() {
  },
  mounted() {
  },
  methods: {}
}
</script>

<style scoped>

</style>
