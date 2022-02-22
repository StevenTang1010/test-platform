<template>
  <div class="main">
    <el-container style="padding: 0">
      <el-main style="padding: 0 10px 0">
        <el-form ref="form" :model="form" :size="themeSize" label-width="200px">
          <el-form-item prop="debug" label="调试模式：">
            <el-switch v-model="form.debug" />
          </el-form-item>
          <el-form-item prop="file_log_level" label="日志等级（文件）：">
            <el-select v-model="form.file_log_level" value-key="id" placeholder="日志等级（文件）">
              <el-option v-for="(item, index) in log_level_options" :key="index" :label="item" :value="item" />
            </el-select>
          </el-form-item>
          <el-form-item prop="console_log_level" label="日志等级（控制台）：">
            <el-select v-model="form.console_log_level" value-key="id" placeholder="日志等级（控制台）">
              <el-option v-for="(item, index) in log_level_options" :key="index" :label="item" :value="item" />
            </el-select>
          </el-form-item>
          <el-form-item prop="testcase_max_rotation" label="构建最大保留数：">
            <el-input-number v-model="form.testcase_max_rotation" controls-position="right" :min="1" :max="100" />
          </el-form-item>
        </el-form>
      </el-main>
      <el-footer>
        <el-button :size="themeSize" @click.native="updateLoading = false">取消</el-button>
        <el-button :size="themeSize" type="primary" :loading="updateLoading" @click.native="total===0? addSubmit():editSubmit()">保存</el-button>
      </el-footer>
    </el-container>
  </div>
</template>

<script>
import { getAppSettingList, getAppSettingDataDefault, addAppSetting, updateAppSetting } from '@/api/apiTest/app_setting'

export default {
  name: 'AppSetting',
  data() {
    return {
      themeSize: this.$store.state.settings.themeSize,
      isLoading: false,
      updateLoading: false,

      page: 1,
      page_size: 20,
      total: 0,

      form: {
        debug: false,
        testcase_max_rotation: 50
      },

      log_level_options: [
        'DEBUG',
        'INFO',
        'WARNING',
        'ERROR',
        'CRITICAL'
      ]
    }
  },
  mounted() {
    this.fetchData()
  },
  methods: {
    // 获取ENV列表
    fetchData() {
      this.isLoading = true
      const params = {
        page: this.page,
        page_size: this.page_size
      }
      getAppSettingList(params).then(response => {
        const { msg, code } = response
        this.isLoading = false
        if (code === 2) {
          this.total = response.data.count
          if (response.data.count > 0) {
            this.form = response.data.list[0].data
          } else {
            this.addSubmit()
          }
        } else {
          this.$message.error({
            message: msg,
            center: true
          })
        }
      })
    },
    fetchDefaultAppSetting() {
      getAppSettingDataDefault({}).then(response => {
        const { msg, code } = response
        if (code === 2) {
          this.form = response.data
        } else {
          this.$message.error({
            message: msg,
            center: true
          })
        }
      })
    },
    addSubmit() {
      console.log('add')
      this.updateLoading = true
      const addData = {
        id: 1,
        data: this.form
      }
      addAppSetting(addData).then(response => {
        const { msg, code } = response
        this.updateLoading = false
        if (code === 2) {
          this.$message({
            message: '添加成功',
            center: true,
            type: 'success'
          })
        } else if (code === 3) {
          this.$message.error({
            message: msg,
            center: true
          })
        } else {
          this.$message.error({
            message: msg,
            center: true
          })
        }
      }).then(() => { this.fetchData() })
    },
    editSubmit() {
      console.log('update')
      this.updateLoading = true
      const editData = {
        data: this.form
      }
      updateAppSetting(1, editData).then(response => {
        const { msg, code } = response
        this.updateLoading = false
        if (code === 2) {
          this.$message({
            message: '修改成功',
            center: true,
            type: 'success'
          })
        } else if (code === 3) {
          this.$message.error({
            message: msg,
            center: true
          })
        } else {
          this.$message.error({
            message: msg,
            center: true
          })
        }
      }).then(() => { this.fetchData() })
    }
  }
}
</script>

<style lang="scss" scoped>
  ::v-deep .el-footer{
    width: 100%;
    bottom: 0;
    left: 0;
    border-top: 1px solid #e8e8e8;
    padding: 10px;
    text-align: center;
    background-color: white;
  }
</style>
