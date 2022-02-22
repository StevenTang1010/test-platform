<template>
  <div class="main">
    <el-card shadow="hover" style="background:#f6f6f8">
      <div slot="header" class="clearfix">
        <el-divider class="blue-line" direction="vertical" />
        <span style="font-weight:bold;font-size:14px;color:#2C8DF4;">测试用例</span>
        <el-button type="success" :size="themeSize" style="float: right" :loading="runLoading" @click="runTest">执行</el-button>
      </div>
      <!--查询条件-->
      <el-form ref="filters" :inline="true" :v-model="filters" :size="themeSize" @submit.native.prevent>
        <el-form-item style="width: 150px">
          <el-select v-model="filters.id" placeholder="用例ID" value-key="id" multiple filterable allow-create clearable @keyup.enter.native="fetchData">
            <span slot="empty" class="el-select-dropdown__empty">请输入用例ID</span>
            <el-option v-for="item in []" :key="item.value" :label="item.label" :value="item.value.replace(/[^\d]/g,'')" />
          </el-select>
        </el-form-item>
        <el-form-item style="width: 150px">
          <el-input v-model="filters.name" placeholder="用例名称" clearable @keyup.enter.native="fetchData" />
        </el-form-item>
        <el-form-item>
          <el-select v-model="filters.test_suite" value-key="id" multiple placeholder="所属用例集" filterable clearable>
            <el-option v-for="item in test_suite_options" :key="item.id" :label="item.name" :value="item" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-select v-model="filters.department" value-key="id" multiple placeholder="所属部门" filterable clearable>
            <el-option v-for="item in department_options" :key="item.id" :label="item.name" :value="item" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-select v-model="filters.type" value-key="id" multiple placeholder="用例类型" filterable clearable>
            <el-option v-for="(item, index) in test_case_type_options" :key="index" :label="item" :value="item" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-select v-model="filters.labels" value-key="id" placeholder="标签" clearable style="width: 100%">
            <el-option-group v-for="group in globalLabel_options" :key="group.label" :label="group.label">
              <el-option v-for="item in group.options" :key="item.id" :label="item.name" :value="item" />
            </el-option-group>
          </el-select>
        </el-form-item>
        <el-form-item style="width: 150px">
          <el-select v-model="filters.result" value-key="id" multiple placeholder="测试结果" clearable>
            <el-option label="passed" value="passed" />
            <el-option label="failed" value="failed" />
            <el-option label="skipped" value="skipped" />
            <el-option label="error" value="error" />
            <el-option label="未执行" value="null" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="fetchData">查询</el-button>
        </el-form-item>
        <el-form-item>
          <el-button type="default" @click.native="filterClear">重置</el-button>
        </el-form-item>
      </el-form>
      <span style="font-size: 14px;"> 查询到 {{ dataList.length }} 条用例</span>
    </el-card>

    <!-- 执行测试-->
    <run-test ref="runTestRef" />
  </div>
</template>

<script>
import get_base_data from '@/api/apiTest/get_base_data'
import RunTest from '@/views/apiTest/components/RunTest'
import { getTestCaseList } from '@/api/apiTest/test_case'

export default {
  name: 'RunTestCase',
  components: { RunTest },
  mixins: [get_base_data],
  data() {
    return {
      themeSize: this.$store.state.settings.themeSize,
      test_case_type_options: [
        '单接口测试',
        '场景测试',
        '性能测试',
        'setup',
        'teardown'
      ],
      filters: {
        id: null,
        name: null,
        test_suite: null,
        department: null,
        type: null,
        labels: null
      },
      isLoading: false,
      total: 0,
      dataList: [],

      runLoading: false
    }
  },
  mounted() {
    this.getTestSuite()
    this.getDepartment()
    this.getLabel()
  },
  methods: {
    filterClear() {},
    // 查询 用例列表
    fetchData() {
      const test_suite_ids = []
      for (let i = 0; i < this.filters.test_suite.length; i++) {
        test_suite_ids.push(this.filters.test_suite[i].id)
      }
      const department_ids = []
      for (let i = 0; i < this.filters.department.length; i++) {
        department_ids.push(this.filters.department[i].id)
      }
      const params = {
        page: 1,
        page_size: 10000,
        id_in: this.filters.id.length > 0 ? this.filters.id.join(',') : null,
        name: this.filters.name ? this.filters.name : null,
        result__in: this.filters.result.length > 0 ? this.filters.result.join(',') : null,
        test_suite__in: test_suite_ids.length > 0 ? test_suite_ids.join(',') : null,
        department__in: department_ids.length > 0 ? department_ids.join(',') : null,
        type__in: this.filters.type.length > 0 ? this.filters.type.join(',') : null,
        label__contains: this.filters.labels ? this.filters.labels.id : null
      }
      this.isLoading = true
      return getTestCaseList(params).then(response => {
        this.dataList = response.data.list
        this.total = response.data.count
        this.isLoading = false
      })
    },
    // 运行测试
    runTest() {
      this.fetchData().then(() => {
        this.$refs.runTestRef.handleRunTest('test_case', this.dataList)
        this.runLoading = false
      })
    }
  }
}
</script>

<style scoped>

</style>
