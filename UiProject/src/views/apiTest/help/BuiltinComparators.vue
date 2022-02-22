<template>
  <div class="main" style="padding-top: 10px">
    <el-container>
      <el-divider class="blue-line" direction="vertical" />
      <span style="font-weight:bold;font-size:14px;color:#2C8DF4;">格式</span>
      <el-main>
        <span style="font-size: 14px">
          {"校验方法": {"检查项": "期望值"}}
        </span>
      </el-main>
    </el-container>

    <el-container style="width: 100%">
      <el-divider class="blue-line" direction="vertical" />
      <span style="font-weight:bold;font-size:14px;color:#2C8DF4;">校验器</span>
      <el-main>
        <el-table v-loading="isLoading" :data="dataList" :size="themeSize" style="width: 100%">
          <el-table-column prop="id" label="ID" width="70" />
          <el-table-column prop="method" label="方法" width="200" />
          <el-table-column prop="keys" label="支持的关键字" width="400">
            <template slot-scope="scope">
              {{ scope.row.keys.join(' | ') }}
            </template>
          </el-table-column>
          <el-table-column prop="desc" label="描述" width="400" />
        </el-table>
      </el-main>
    </el-container>
  </div>
</template>

<script>
import { getComparatorList } from '@/api/apiTest/help_comparators'

export default {
  name: 'ValidationRules',
  data() {
    return {
      themeSize: this.$store.state.settings.themeSize,

      isLoading: false,
      dataList: []
    }
  },
  mounted() {
    this.fetchData()
  },
  methods: {
    fetchData() {
      this.isLoading = false
      getComparatorList().then(response => {
        const { msg, code } = response
        this.isLoading = false
        if (code === 2) {
          this.dataList = response.data.list
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
