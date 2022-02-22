<template>
  <div class="main">
    <el-radio-group v-model="activeName" :size="themeSize" style="margin-bottom: 10px;">
      <el-radio-button label="department">部门</el-radio-button>
      <el-radio-button label="user">成员</el-radio-button>
    </el-radio-group>
    <!--显示部门-->
    <template v-if="activeName==='department'">
      <dept-list />
    </template>
  </div>
</template>

<script>

import DeptList from '@/views/apiTest/projectMgr/organization/DeptList'
export default {
  name: 'Index',
  components: { DeptList },
  data() {
    return {
      themeSize: this.$store.state.settings.themeSize,
      // 默认选中
      activeName: 'department'
    }
  }
}
</script>

<style scoped>

</style>
