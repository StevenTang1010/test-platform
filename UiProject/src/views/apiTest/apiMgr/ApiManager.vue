<template>
  <div class="main">
    <el-container style="padding: 0">
      <!--  侧边栏容器: 分组管理    -->
      <el-aside v-loading="baseLoading" element-loading-text="Loading" style="width:210px; padding-left: 5px">
        <div class="nav-api-side">
          <div class="api-tree">
            <!--  搜索、添加 分组 -->
            <el-input
              v-model="groupFilterText"
              :size="themeSize"
              placeholder="输入关键字进行过滤"
              clearable
              prefix-icon="el-icon-search"
            />
            <!--  项目-分组-接口 列表树 -->
            <el-tree
              ref="groupTree"
              style="padding-top: 5px"
              :props="deptApiTreeProps"
              :load="deptApiTreeLoad"
              lazy
              node-key="id"
              draggable
              :default-expand-all="false"
              :expand-on-click-node="false"
              :highlight-current="true"
              :filter-node-method="filterNode"
              @node-click="handleNodeClick"
            >
              <span slot-scope="{ node, data }" class="custom-tree-node">
                <span><i v-if="data.type==='project'" class="el-icon-folder-opened" /> {{ node.label }}</span>
              </span>
            </el-tree>
          </div>
        </div>
      </el-aside>

      <el-main style="padding: 0 10px 0">
        <!-- 显示分组列表信息 -->
        <api-group-list v-show="showApiGroupList" ref="apiGroupListRef" />

        <!-- 显示接口列表信息 -->
        <api-list v-show="showApiList" ref="apiListRef" />

        <!-- 显示接口详情页 -->
        <api-detail v-show="showApiDetail" ref="apiDetailRef" :show-page-header="false" />
      </el-main>
    </el-container>
  </div>
</template>

<script>
import get_base_data from '@/api/apiTest/get_base_data'
import ApiList from '@/views/apiTest/apiMgr/ApiList'
import apiDetail from '@/views/apiTest/apiMgr/apiDetail'
import ApiGroupList from '@/views/apiTest/apiMgr/ApiGroupList'

export default {
  name: 'ApiManager',
  components: { ApiGroupList, ApiList, apiDetail },
  mixins: [get_base_data],
  data() {
    return {
      themeSize: this.$store.state.settings.themeSize,
      // 分组名称筛选
      groupFilterText: '',

      showApiGroupList: false,
      showApiList: true,
      showApiDetail: false
    }
  },
  watch: {
    groupFilterText(val) {
      this.$refs.groupTree.filter(val)
    }
  },
  mounted() {
    if (this.$route.params.api_id) {
      this.showApiGroupList = false
      this.showApiList = false
      this.showApiDetail = true
    }
  },
  methods: {
    // 折叠版 click
    handleChange(val) {
      // console.log(val)
    },
    // 分组
    filterNode(value, data) {
      if (!value) return true
      return data.label.indexOf(value) !== -1
    },
    // 点击项目/分组/接口事件
    handleNodeClick: function(data) {
      switch (data.type) {
        case 'allApi':
          // 所有接口
          this.showApiGroupList = false
          this.showApiList = true
          this.showApiDetail = false
          this.$refs.apiListRef.filters.project = []
          this.$refs.apiListRef.filters.api_group = ''
          this.$refs.apiListRef.filters.api_group__isnull = null
          this.$refs.apiListRef.fetchData()
          break
        case 'allGroup':
          // 所有分组
          this.showApiGroupList = true
          this.showApiList = false
          this.showApiDetail = false
          this.$refs.apiGroupListRef.filters.project = []
          this.$refs.apiGroupListRef.fetchData()
          break
        case 'toAllocateApi':
          // 待分配接口
          this.showApiGroupList = false
          this.showApiList = true
          this.showApiDetail = false
          this.$refs.apiListRef.filters.project = []
          this.$refs.apiListRef.filters.api_group = ''
          this.$refs.apiListRef.filters.api_group__isnull = true
          this.$refs.apiListRef.fetchData()
          break
        case 'project':
          this.showApiGroupList = false
          this.showApiList = true
          this.showApiDetail = false
          this.$refs.apiListRef.filters.project = [{ id: data.id, name: data.label }]
          this.$refs.apiListRef.filters.api_group = ''
          this.$refs.apiListRef.filters.api_group__isnull = null
          this.$refs.apiListRef.fetchData()
          break
        case 'api_group':
          this.showApiGroupList = false
          this.showApiList = true
          this.showApiDetail = false
          this.$refs.apiListRef.filters.project = []
          this.$refs.apiListRef.filters.api_group = { id: data.id, name: data.label }
          this.$refs.apiListRef.filters.api_group__isnull = null
          this.$refs.apiListRef.fetchData()
          break
        case 'api':
          this.showApiGroupList = false
          this.showApiList = false
          this.showApiDetail = true
          // this.$router.push({ name: '接口详情1', params: { api_id: data.id }})
          this.$route.params.api_id = data.id
          break
        default:
        //
      }
    }
  }
}
</script>

<style lang="scss" scoped>
  ::v-deep .nav-api-side {
    overflow: auto;
    border: 1px solid #ddd;
    width: 200px;
    margin-left: 0;
    border-radius: 4px;
    position: fixed;
    top: 100px;
    bottom: 0;
  }
  ::v-deep .api-tree {
    padding: 0;
    margin: 0;
  }
</style>
