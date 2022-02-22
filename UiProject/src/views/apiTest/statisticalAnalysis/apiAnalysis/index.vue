<template>
  <div class="main">
    <tabs-menu :tab-pane-list="tabPaneList" />
    <!--分组-->
    <div style="padding-left: 10px">
      <el-radio-group v-model="groupByField" :size="themeSize" @change="fetchData">
        <el-radio-button label="project__department__name">按部门</el-radio-button>
        <el-radio-button label="project__name">按项目</el-radio-button>
      </el-radio-group>
    </div>

    <el-container>
      <el-aside style="width:520px; padding-left: 5px">
        <no-case-api ref="noCaseApiRef" :group-by-field="groupByField" />
      </el-aside>
      <el-aside style="width:520px; padding-left: 5px">
        <to-do-api ref="toDoApiRef" :group-by-field="groupByField" />
      </el-aside>
    </el-container>
  </div>
</template>

<script>
import TabsMenu from '@/views/apiTest/components/TabsMenu'
import NoCaseApi from '@/views/apiTest/statisticalAnalysis/apiAnalysis/NoCaseApi'
import ToDoApi from '@/views/apiTest/statisticalAnalysis/apiAnalysis/ToDoApi'

export default {
  name: 'Index',
  components: { TabsMenu, NoCaseApi, ToDoApi },
  data() {
    return {
      themeSize: this.$store.state.settings.themeSize,
      tabPaneList: [
        {
          name: 'ApiAnalysis',
          label: '接口分析',
          components: []
        }
      ],
      groupByField: 'project__name'
    }
  },
  methods: {
    fetchData() {
      this.$refs.noCaseApiRef.noCaseApiCountData = []
      this.$refs.noCaseApiRef.fetchData()

      this.$refs.toDoApiRef.toDoApiCountData = []
      this.$refs.toDoApiRef.fetchData()
    }
  }
}
</script>

<style scoped>

</style>
