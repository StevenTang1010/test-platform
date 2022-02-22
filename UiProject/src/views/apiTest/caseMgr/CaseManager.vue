<template>
  <div class="main">
    <el-container style="padding: 0">
      <!--  侧边栏容器: 用例集管理    -->
      <el-aside v-loading="baseLoading" element-loading-text="Loading" style="width:260px; padding-left: 5px">
        <div class="nav-case-side">
          <div class="case-tree">
            <!--  搜索、添加 用例集 -->
            <el-input
              v-model="suiteFilterText"
              :size="themeSize"
              placeholder="输入关键字进行过滤"
              clearable
            />
            <!--  部门-用例集-用例：树 -->
            <el-tree
              ref="suiteTree"
              style="padding-top: 5px"
              node-key="id"
              :props="deptCaseTreeProps"
              :load="deptCaseTreeLoad"
              lazy
              :default-expand-all="false"
              :expand-on-click-node="false"
              :highlight-current="true"
              :filter-node-method="filterNode"
              @node-click="handleNodeClick"
            >
              <span slot-scope="{ node, data }" class="custom-tree-node">
                <span><i v-if="data.type==='department'||data.type==='suite'" class="el-icon-folder-opened" /> {{ node.label }}</span>
              </span>
            </el-tree>
          </div>
        </div>
      </el-aside>

      <el-main style="padding: 0 10px 0">
        <!-- 显示用例列表-->
        <case-list v-if="showCaseList" ref="caseListRef" />

        <!-- 显示用例步骤列表-->
        <step-list v-if="showStepList" ref="stepListRef" />

        <!-- 显示用例集列表-->
        <suite-list v-if="showSuiteList" ref="suiteListRef" />

        <!-- 显示用例集信息+用例列表-->
        <suite-detail v-if="showSuiteDetail" ref="suiteDetailRef" />

        <!-- 显示用例详情+步骤 -->
        <case-detail v-if="showCaseDetail" ref="caseDetailRef" />
      </el-main>
    </el-container>
  </div>
</template>

<script>
import get_base_data from '@/api/apiTest/get_base_data'
import CaseList from '@/views/apiTest/caseMgr/CaseList'
import StepList from '@/views/apiTest/caseMgr/StepList'
import SuiteList from '@/views/apiTest/caseMgr/SuiteList'
import suiteDetail from '@/views/apiTest/caseMgr/suiteDetail'
import caseDetail from '@/views/apiTest/caseMgr/caseDetail'

export default {
  name: 'CaseManager',
  components: { CaseList, caseDetail, StepList, SuiteList, suiteDetail },
  mixins: [get_base_data],
  data() {
    return {
      themeSize: this.$store.state.settings.themeSize,
      // 用例集名称筛选
      suiteFilterText: '',
      // 树目录显示用例集数据
      suiteTreeData: [],

      showStepList: false,
      showCaseList: true,
      showSuiteList: false,
      showSuiteDetail: false,
      showCaseDetail: false
    }
  },
  watch: {
    suiteFilterText(val) {
      this.$refs.suiteTree.filter(val)
    }
  },
  mounted() {
  },
  methods: {
    // 折叠版 click
    handleChange(val) {
      // console.log(val)
    },
    // 用例集
    filterNode(value, data) {
      if (!value) return true
      return data.label.indexOf(value) !== -1
    },
    // 点击用例集事件
    handleNodeClick: function(data, node) {
      // console.log(node)
      switch (data.type) {
        case 'allCase':
          // 全部用例
          this.showCaseList = true
          this.showStepList = false
          this.showSuiteList = false
          this.showSuiteDetail = false
          this.showCaseDetail = false
          this.$nextTick(() => {
            this.$refs.caseListRef.showMoreFilters = true
            this.$refs.caseListRef.fetchFiltersData()
            this.$refs.caseListRef.fetchData()
          })
          break
        case 'allStep':
          // 全部用例步骤
          this.showCaseList = false
          this.showStepList = true
          this.showSuiteList = false
          this.showSuiteDetail = false
          this.showCaseDetail = false
          this.$nextTick(() => {
            this.$refs.stepListRef.showMoreFilters = true
            this.$refs.stepListRef.allowUpdateStepId = false
            this.$refs.stepListRef.fetchFiltersData()
            this.$refs.stepListRef.fetchData()
          })
          break
        case 'allSuite':
          // 全部用例集
          this.showCaseList = false
          this.showStepList = false
          this.showSuiteList = true
          this.showSuiteDetail = false
          this.showCaseDetail = false
          this.$nextTick(() => {
            this.$refs.suiteListRef.showMoreFilters = true
            this.$refs.suiteListRef.filters.department = []
            this.$refs.suiteListRef.filters.department__isnull = null
            this.$refs.suiteListRef.fetchData()
          })
          break
        case 'toDoSuite':
          // 待分配用例集
          this.showCaseList = false
          this.showStepList = false
          this.showSuiteList = true
          this.showSuiteDetail = false
          this.showCaseDetail = false
          this.$nextTick(() => {
            this.$refs.suiteListRef.filters.department = []
            this.$refs.suiteListRef.filters.department__isnull = true
            this.$refs.suiteListRef.fetchData()
          })
          break
        case 'department':
          // 部门用例集
          this.showCaseList = false
          this.showStepList = false
          this.showSuiteList = true
          this.showSuiteDetail = false
          this.showCaseDetail = false
          this.$nextTick(() => {
            this.$refs.suiteListRef.showMoreFilters = false
            this.$refs.suiteListRef.filters.department = [{ id: data.id, name: data.label }]
            this.$refs.suiteListRef.filters.department__isnull = null
            this.$refs.suiteListRef.fetchData()
          })
          break
        case 'suite':
          // 用例集详情+用例列表
          this.showCaseList = false
          this.showStepList = false
          this.showSuiteList = false
          this.showSuiteDetail = true
          this.showCaseDetail = false
          this.$nextTick(() => {
            this.$refs.suiteDetailRef.fetchData(data.id)
          })
          break
        case 'case':
          // 用例-步骤列表
          this.showCaseList = false
          this.showStepList = false
          this.showSuiteList = false
          this.showSuiteDetail = false
          this.showCaseDetail = true
          this.$nextTick(() => {
            this.$refs.caseDetailRef.getCaseStepInfo(data.id)
          })
          break
        default:
          //
      }
    }
  }
}
</script>

<style lang="scss" scoped>
  ::v-deep .nav-case-side {
    overflow: auto;
    border: 1px solid #ddd;
    width: 250px;
    margin-left: 0;
    border-radius: 4px;
    position: fixed;
    top: 100px;
    bottom: 0;
  }
  ::v-deep .case-tree {
    padding: 0;
    margin: 0;
  }
</style>
