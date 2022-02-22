<template>
  <div class="main">
    <router-view />
  </div>
</template>

<script>

export default {
  name: 'Index',
  data() {
    return {}
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
