<template>
  <div class="main">
    <!-- 显示接口列表信息 -->
    <api-list ref="apiListRef" table-name="重复接口列表TODO" fetch-data-method="getDuplicateApi" />
  </div>
</template>

<script>
import ApiList from '@/views/apiTest/apiMgr/ApiList'
export default {
  name: 'DuplicateChecking',
  components: { ApiList }
}
</script>

<style scoped>

</style>
