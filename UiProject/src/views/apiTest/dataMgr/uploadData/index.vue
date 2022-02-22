<template>
  <div class="main">
    <el-card class="box-card" :size="themeSize">
      <div slot="header" class="clearfix">
        <span>数据导入</span>
      </div>
      <el-form :size="themeSize" :model="uploadForm" :rules="uploadFormRules">
        <el-form-item label="数据类型:" prop="data_type">
          <el-select v-model="uploadForm.data_type" value-key="id" placeholder="数据类型">
            <el-option label="用例类型" :value="0" />
            <el-option label="接口类型" :value="1" />
          </el-select>
        </el-form-item>
        <el-form-item label="数据同步:" prop="load_type">
          <el-select v-model="uploadForm.load_type" value-key="id" placeholder="数据同步方式">
            <el-option label="智能合并" :value="0" />
            <el-option label="完全覆盖" :value="1" />
          </el-select>
        </el-form-item>
        <el-form-item label="所属部门:" prop="department">
          <el-select v-model="uploadForm.department" placeholder="所属部门" clearable>
            <el-option v-for="item in department_options" :key="item.id" :label="item.name" :value="item.id" />
          </el-select>
        </el-form-item>
      </el-form>
      <el-upload
        class="upload-demo"
        drag
        :action="action"
        :data="uploadForm"
        multiple
      >
        <i class="el-icon-upload" />
        <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
        <div slot="tip" class="el-upload__tip">只能上传 xmind / excel 文件</div>
      </el-upload>
    </el-card>
  </div>
</template>

<script>
import get_base_data from '@/api/apiTest/get_base_data'
export default {
  name: 'UploadDataIndex',
  mixins: [get_base_data],
  data() {
    return {
      themeSize: this.$store.state.settings.themeSize,
      action: process.env.VUE_APP_BASE_API + '/api_test/file/upload',
      uploadFormRules: {
        data_type: [
          { required: true, message: '请选择数据类型', trigger: 'blur' }
        ],
        load_type: [
          { required: true, message: '请选择数据同步方式', trigger: 'blur' }
        ],
        department: [
          { required: true, message: '请选择所属部门', trigger: 'blur' }
        ]
      },
      uploadForm: {
        data_type: 0,
        load_type: 0,
        department: null
      }
    }
  },
  mounted() {
    this.getDepartment()
  }
}
</script>

<style scoped>
  .box-card {
    width: 410px;
  }
</style>
