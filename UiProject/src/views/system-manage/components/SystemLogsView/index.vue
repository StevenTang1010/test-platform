<template>
  <div class="main">
    <el-container>
      <el-header style="padding-bottom: 0">
        <span> 查询最后N行(0-全部)：</span>
        <el-input-number v-model="currentTailNum" :size="themeSize" :step="100" />
        <el-button :size="themeSize" type="primary" @click="fetchData">查询</el-button>
      </el-header>
      <el-main style="padding-top: 0">
        <div v-loading="isLoading">
          <p style="padding-left: 10px;white-space: pre-wrap;" v-text="logContent" />
        </div>
      </el-main>
    </el-container>
  </div>
</template>

<script>
import { getSystemLogs } from '@/api/systemManage/system_logs'

export default {
  name: 'SystemLogsView',
  props: {
    logName: {
      type: String,
      default() {
        return 'message'
      }
    },
    tailNum: {
      type: Number,
      default() {
        return 0
      }
    }
  },
  data() {
    return {
      themeSize: this.$store.state.settings.themeSize,

      currentTailNum: this.tailNum,
      isLoading: false,
      logContent: ''
    }
  },
  mounted() {
    this.fetchData()
  },
  methods: {
    fetchData() {
      this.isLoading = true
      getSystemLogs(this.logName, { tail_num: this.currentTailNum }).then(response => {
        const { msg, code } = response
        this.isLoading = false
        if (code === 2) {
          this.logContent = response.data
        } else {
          this.$message.error({
            message: msg,
            center: true
          })
        }
      })
    }
  }
}
</script>

<style scoped>

</style>
