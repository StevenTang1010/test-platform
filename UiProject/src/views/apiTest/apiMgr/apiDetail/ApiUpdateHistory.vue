<template>
  <div class="main" v-loading="listLoading" >
    <el-timeline :reverse="true" style="padding-top: 10px">
      <el-timeline-item
        v-for="(item, index) in dataList"
        :key="index"
        :type="getType(item.update_status)"
        :timestamp="getTimestamp(index+1, item)"
        placement="top"
      >
        <el-table :size="themeSize" :data="JSON.parse(item.content)" style="width: 95%">
          <el-table-column prop="change" label="变更类型" show-overflow-tooltip width="100" />
          <el-table-column prop="node" label="节点" width="300" />
          <el-table-column prop="value" label="内容">
            <template slot-scope="scope">
              {{ scope.row.value }}
            </template>
          </el-table-column>
        </el-table>
      </el-timeline-item>
    </el-timeline>
  </div>
</template>

<script>
import { getApiUpdateHistoryList } from '@/api/apiTest/api_update_history'

export default {
  name: 'UpdateHistory',
  data() {
    return {
      themeSize: this.$store.state.settings.themeSize,
      listLoading: false,
      dataList: []
    }
  },
  mounted() {
    this.fetchData()
  },
  methods: {
    // 查询接口变更历史
    fetchData() {
      this.listLoading = true
      getApiUpdateHistoryList({ api__id: this.$route.params.api_id }).then(response => {
        this.dataList = response.data.list
        this.total = response.data.count
        this.listLoading = false
      })
    },
    getType(update_status) {
      if (update_status === 0) {
        return 'danger'
      } else if (update_status === 1) {
        return 'warning'
      } else {
        return 'success'
      }
    },
    getTimestamp(index, item) {
      let timestamp = index + '. ' + item.update_status_name + ' ' + item.update_time + '(api.id:' + item.api + ')'
      if (item.updater) {
        timestamp += ' ' + item.updater
      }
      return timestamp
    }
  }
}
</script>

<style scoped>

</style>
