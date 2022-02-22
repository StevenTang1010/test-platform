<template>
  <div style="padding:30px;">
    <el-alert :closable="false" title="Custom" type="success">
      <router-view />
    </el-alert>
  </div>
</template>

<script>
export default {
  name: 'Custom'
}
</script>

<style scoped>

</style>
