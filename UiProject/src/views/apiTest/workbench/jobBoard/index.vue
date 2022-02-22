<template>
  <div class="main">
    TODO
  </div>
</template>

<script>

export default {
  name: 'JobBoard',
  data() {
    return {
      themeSize: this.$store.state.settings.themeSize,
      // 默认选中
      activeName: 'NoCaseApi'
    }
  },
  mounted() {
  },
  methods: {
    handleClick(tab, event) {
      console.log(tab, event)
    }
  }
}
</script>

<style scoped>

</style>
