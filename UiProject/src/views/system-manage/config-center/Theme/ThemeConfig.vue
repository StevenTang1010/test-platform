<template>
  <div class="main">
    <el-container>
      <el-main>
        <el-form ref="form" :model="form" label-width="80px">
          <el-form-item label="主题大小">
            <el-radio v-model="form.themeSize" label="medium">medium</el-radio>
            <el-radio v-model="form.themeSize" label="small">small</el-radio>
            <el-radio v-model="form.themeSize" label="mini">mini</el-radio>
          </el-form-item>
          <el-form-item label="主题换肤">
            <el-color-picker
              v-model="form.themeColor"
              :size="form.themeSize"
              :predefine="predefineColors"
              @change="handleChange"
            />
          </el-form-item>
        </el-form>
      </el-main>
      <el-footer>
        <el-button :size="form.themeSize" type="primary" @click="onSubmit">保存</el-button>
        <el-button :size="form.themeSize">取消</el-button>
      </el-footer>
    </el-container>
  </div>
</template>

<script>
export default {
  name: 'Theme',
  data() {
    return {
      form: {
        themeSize: this.$store.state.settings.themeSize,
        themeColor: this.$store.state.settings.themeColor
      },
      predefineColors: [
        '#409EFF',
        '#67C23A',
        '#E6A23C',
        '#F56C6C',
        '#909399'
      ]
    }
  },
  methods: {
    handleChange(val) {
      // console.log(val)
    },
    onSubmit() {
      console.log('submit!')
      this.$store.commit('settings/CHANGE_SETTING', {
        themeSize: this.form.themeSize,
        themeColor: this.form.themeColor
      })
      this.$store.state.settings.themeSize = this.form.themeSize
      this.$store.state.settings.themeColor = this.form.themeColor
      this.$message({
        message: '主题修改成功---TODO',
        center: true,
        type: 'success'
      })
    }
  }
}
</script>

<style scoped>

</style>
