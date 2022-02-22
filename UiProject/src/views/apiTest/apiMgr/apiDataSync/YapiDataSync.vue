<template>
  <div class="main">
    <!-- 显示YapiEvent列表信息 -->
    <yapi-event-list ref="yapiEventListRef" style="padding-top: 10px" />
  </div>

</template>

<script>
import YapiEventList from '@/views/apiTest/apiMgr/YapiEventList'

export default {
  name: 'Update',
  components: { YapiEventList },
  props: {
    projectData: {
      type: Object,
      default() {
        return { apiCoverage: 0 }
      }
    },
    stepActive: {
      type: Number,
      default() {
        return 1
      }
    },
    tableName: {
      type: String,
      default() {
        return '接口更新列表'
      }
    }
  },
  data() {
    return {
      listLoading: false,
      noCaseApiList: []
    }
  },
  mounted() {
    this.$refs.yapiEventListRef.fetchData()
  },
  methods: {
    handleChange(val) {
      // console.log(val)
    }
  }
}
</script>

<style scoped>

</style>
