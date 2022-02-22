<template>
  <div class="main">
    <el-container style="padding: 0">
      <!--  侧边栏容器: 用例集管理    -->
      <el-aside v-loading="baseLoading" element-loading-text="Loading" style="width:260px; padding-left: 5px">
        <div class="nav-case-side">
          <div class="case-tree">
            <!--  搜索、添加 项目 -->
            <el-input
              v-model="projectFilterText"
              :size="themeSize"
              placeholder="输入关键字进行过滤"
              clearable
            />
            <!--  部门-项目：树 -->
            <el-tree
              ref="projectTree"
              style="padding-top: 5px"
              :props="deptApiTreeProps"
              :load="deptProjectTreeLoad"
              lazy
              node-key="id"
              :default-expand-all="false"
              :expand-on-click-node="false"
              :highlight-current="true"
              :filter-node-method="filterNode"
              @node-click="handleNodeClick"
            >
              <span slot-scope="{ node, data }" class="custom-tree-node">
                <span><i v-if="data.type==='department'" class="el-icon-folder-opened" /> {{ node.label }}</span>
              </span>
            </el-tree>
          </div>
        </div>
      </el-aside>

      <el-main style="padding: 0 10px 0">
        <!-- 显示项目列表-->
        <project-list ref="projectListRef" />

        <!-- 显示项目详情-->
        <router-view />
      </el-main>
    </el-container>
  </div>
</template>

<script>
import get_base_data from '@/api/apiTest/get_base_data'
import ProjectList from '@/views/apiTest/projectMgr/ProjectList'

export default {
  name: 'CaseManager',
  components: { ProjectList },
  mixins: [get_base_data],
  data() {
    return {
      themeSize: this.$store.state.settings.themeSize,
      // 集名称筛选
      projectFilterText: '',

      showProjectList: true,
      showProjectDetail: false
    }
  },
  watch: {
    projectFilterText(val) {
      this.$refs.projectTree.filter(val)
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
    handleNodeClick: function(data) {
      if (data.type === 'allProject') {
        // 全部项目列表
        this.showProjectList = true
        this.showProjectDetail = false
        this.$refs.projectListRef.showMoreFilters = true
        this.$refs.projectListRef.filters.department = ''
        this.$refs.projectListRef.filters.department__isnull = null
        this.$refs.projectListRef.fetchData()
      } else if (data.type === 'toDoProject') {
        // 待分配项目列表
        this.showProjectList = true
        this.showProjectDetail = false
        this.$refs.projectListRef.showMoreFilters = true
        this.$refs.projectListRef.filters.department = ''
        this.$refs.projectListRef.filters.department__isnull = true
        this.$refs.projectListRef.fetchData()
      } else if (data.type === 'department') {
        // 部门项目列表
        this.showProjectList = true
        this.showProjectDetail = false
        this.$refs.projectListRef.filters.department = data.id
        this.$refs.projectListRef.filters.department__isnull = null
        this.$refs.projectListRef.fetchData()
      } else if (data.type === 'project') {
        // 项目详情
        this.showProjectList = false
        this.showProjectDetail = true
        this.$router.push({ name: '项目详情', params: { project_id: data.id }})
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
