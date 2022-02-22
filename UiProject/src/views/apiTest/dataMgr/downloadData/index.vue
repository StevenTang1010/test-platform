<template>
  <div class="main">
    <el-card class="box-card" :size="themeSize" style="height: 445px">
      <div slot="header" class="clearfix">
        <span>数据导出</span>
      </div>
      <el-form :size="themeSize" :model="downloadForm" :rules="downloadFormRules">
        <el-form-item label="数据导出方式:" prop="dump_type">
          <el-select v-model="downloadForm.dump_type" value-key="id" placeholder="数据导出方式">
            <el-option label="Excel" :value="0" />
            <el-option label="Xmind" :value="1" />
          </el-select>
        </el-form-item>
        <div style="text-align: center">
          <el-button type="info" plain @click="handleDownload">导出</el-button>
        </div>
      </el-form>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'DownloadDataIndex',
  data() {
    return {
      themeSize: this.$store.state.settings.themeSize,
      downloadFormRules: {
        dump_type: [
          { required: true, message: '请选择数据导出方式', trigger: 'blur' }
        ]
      },
      downloadForm: {
        dump_type: ''
      }
    }
  },
  methods: {
    handleDownload() {
      this.$message({
        type: 'warning',
        message: 'TODO'
      })
    }
  }
}
</script>

<style scoped>
  .box-card {
    width: 410px;
  }
</style>
