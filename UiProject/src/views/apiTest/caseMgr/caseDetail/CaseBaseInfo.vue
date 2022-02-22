<template>
  <div class="main">
    <el-divider class="blue-line" direction="vertical" />
    <el-button type="text" style="font-weight:bold;font-size:14px;color:#2C8DF4;" @click="showCaseInfo">
      {{ caseInfo.name }}
    </el-button>

    <el-drawer
      title="用例详情"
      :with-header="true"
      :visible.sync="showCaseInfoVisible"
      direction="rtl"
      size="30%"
    >
      <!-- 用例详情 -->
      <div class="demo-drawer__content">
        <el-description>
          <el-description-item label="名称" :value="caseInfo.name" :span-map="{md:24}" />
          <el-description-item label="描述" :value="caseInfo.description" :span-map="{md:24}" />
          <el-description-item label="状态" :span-map="{md:24}">
            <template slot="content">
              <el-tag v-if="caseInfo.status" :size="themeSize" type="success">启用</el-tag>
              <el-tag v-if="!caseInfo.status" :size="themeSize" type="danger">禁用</el-tag>
            </template>
          </el-description-item>
          <el-description-item label="标签" :span-map="{md:24}">
            <template slot="content">
              <span v-for="label in caseInfo.labels" :key="label.id" style="margin:0 2px" :title="label" type="mini">
                <el-tag :size="themeSize">{{ label.name }}
                </el-tag>
              </span>
            </template>
          </el-description-item>
          <el-description-item label="类型" :value="caseInfo.type" :span-map="{md:24}" />
          <el-description-item label="所属用例集" :value="caseInfo.test_suite.name" :span-map="{md:24}" />
          <el-description-item label="SafeName" :value="caseInfo.safe_name" :span-map="{md:24}" />
        </el-description>
      </div>

      <!-- 取消、执行用例 -->
      <div class="demo-drawer__footer">
        <el-button :size="themeSize" @click.native="showCaseInfoVisible = false">取消</el-button>
        <el-button :size="themeSize" type="primary" @click.native="runTest">执行用例</el-button>
      </div>
    </el-drawer>

    <!-- 执行测试 -->
    <run-test ref="runTestRef" />

  </div>
</template>

<script>
import { getTestCaseDetail } from '@/api/apiTest/test_case'
import ElDescription from '@/components/Description/ElDescription'
import ElDescriptionItem from '@/components/Description/ElDescriptionItem'
import RunTest from '@/views/apiTest/components/RunTest'

export default {
  name: 'CaseBaseInfo',
  components: { ElDescription, ElDescriptionItem, RunTest },
  data() {
    return {
      themeSize: this.$store.state.settings.themeSize,
      showCaseInfoVisible: false,
      caseId: '',
      caseInfo: {
        test_suite: { name: '' }
      }
    }
  },
  created() {
  },
  mounted() {
  },
  methods: {
    getCaseInfo(caseId) {
      if (typeof (this.$route.params.case_id) !== 'undefined') {
        caseId = this.$route.params.case_id
      }
      getTestCaseDetail(caseId).then(response => {
        const { msg, code } = response
        this.listLoading = false
        if (code === 2) {
          this.caseInfo = response.data
        } else {
          this.$message.error({
            message: msg,
            center: true
          })
        }
      })
    },
    showCaseInfo() {
      this.showCaseInfoVisible = true
    },
    runTest() {
      this.$refs.runTestRef.handleRunTest('test_case', [this.caseInfo])
    }
  }
}
</script>

<style scoped>
  ::v-deep .el-drawer__body {
      overflow: auto;
    }
  ::v-deep .demo-drawer__content {
    margin-bottom: 2px;
    padding: 10px 20px 20px;
    overflow: auto;
  }
  ::v-deep .demo-drawer__footer{
    width: 100%;
    position: absolute;
    bottom: 0;
    left: 0;
    border-top: 1px solid #e8e8e8;
    padding: 10px 16px;
    text-align: center;
    background-color: white;
  }
</style>
