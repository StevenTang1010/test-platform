<template>
  <div class="main">
    <el-card shadow="hover" style="background:#f6f6f8">
      <div slot="header" class="clearfix">
        <el-divider class="blue-line" direction="vertical" />
        <span style="font-weight:bold;font-size:14px;color:#2C8DF4;">测试用例集</span>
        <el-button type="success" :size="themeSize" style="float: right" :loading="runLoading" @click="runTest">执行</el-button>
      </div>
      <!--查询条件-->
      <el-col :span="24" class="toolbar" style="padding-bottom: 0;padding-top: 10px">
        <el-form ref="filters" :inline="true" :v-model="filters" :size="themeSize" @submit.native.prevent>
          <el-form-item style="width: 150px">
            <el-select v-model="filters.id" placeholder="用例集ID" value-key="id" multiple filterable allow-create clearable @keyup.enter.native="fetchData">
              <span slot="empty" class="el-select-dropdown__empty">请输入用例集ID</span>
              <el-option v-for="item in []" :key="item.value" :label="item.label" :value="item.value.replace(/[^\d]/g,'')" />
            </el-select>
          </el-form-item>
          <el-form-item style="width: 150px">
            <el-input v-model="filters.name" placeholder="用例集名称" clearable @keyup.enter.native="fetchData" />
          </el-form-item>
          <el-form-item>
            <el-select v-model="filters.department" value-key="id" multiple placeholder="所属部门" filterable clearable>
              <el-option v-for="item in department_options" :key="item.id" :label="item.name" :value="item" />
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="fetchData">查询</el-button>
          </el-form-item>
          <el-form-item>
            <el-button type="default" @click.native="filterClear">重置</el-button>
          </el-form-item>
        </el-form>
      </el-col>
      <span style="font-size: 14px;"> 查询到 {{ dataList.length }} 条用例集</span>
    </el-card>

    <!-- 执行测试-->
    <run-test ref="runTestRef" />
  </div>
</template>

<script>
import get_base_data from '@/api/apiTest/get_base_data'
import { getTestSuiteList } from '@/api/apiTest/test_suite'
import RunTest from '@/views/apiTest/components/RunTest'

export default {
  name: 'RunTestSuite',
  components: { RunTest },
  mixins: [get_base_data],
  data() {
    return {
      themeSize: this.$store.state.settings.themeSize,
      filters: {
        id: null,
        name: null,
        department: null
      },
      isLoading: false,
      total: 0,
      dataList: [],

      runLoading: false
    }
  },
  mounted() {
    this.getDepartment()
    this.getLabel()
  },
  methods: {
    filterClear() {},
    // 查询 用例集列表
    fetchData() {
      const department_ids = []
      for (let i = 0; i < this.filters.department.length; i++) {
        department_ids.push(this.filters.department[i].id)
      }
      const params = {
        page: 1,
        page_size: 10000,
        id_in: this.filters.id.join(','),
        name: this.filters.name,
        department__in: department_ids.join(',')
      }
      this.isLoading = true
      return getTestSuiteList(params).then((res) => {
        const { msg, code } = res
        this.isLoading = false
        if (code === 2) {
          this.dataList = res.data.list
          this.total = res.data.count
        } else {
          this.$message.error({
            message: msg,
            center: true
          })
        }
      })
    },
    // 运行测试
    runTest() {
      this.fetchData().then(() => {
        this.$refs.runTestRef.handleRunTest('test_suite', this.dataList)
        this.runLoading = false
      })
    }
  }
}
</script>

<style scoped>

</style>
