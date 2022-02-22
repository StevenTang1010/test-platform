<template>
  <div class="main">
    <el-radio-group v-model="activeName" :size="themeSize" style="margin-bottom: 10px;">
      <el-radio-button label="yapi">YAPI</el-radio-button>
      <el-radio-button label="swagger">SWAGGER</el-radio-button>
    </el-radio-group>
    <!--显示接口数据同步页面：YAPI-->
    <template v-if="activeName==='yapi'">
      <yapi-data-sync />
    </template>
    <!--显示接口数据同步页面：SWAGGER-->
    <template v-if="activeName==='swagger'">
      <span>TODO</span>
    </template>
  </div>
</template>

<script>
import YapiDataSync from '@/views/apiTest/apiMgr/apiDataSync/YapiDataSync'

export default {
  name: 'ApiDataSync',
  components: { YapiDataSync },
  data() {
    return {
      themeSize: this.$store.state.settings.themeSize,
      // 默认选中
      activeName: 'yapi'
    }
  },
  mounted() {
  },
  methods: {
  }
}
</script>

<style scoped>

</style>
