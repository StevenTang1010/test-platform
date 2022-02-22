<template>
  <div class="main">
    <!--接口更新统计信息-->
    <el-divider class="blue-line" direction="vertical" />
    <span slot="title" style="font-weight:bold;font-size:14px;color:#2C8DF4;">接口更新统计</span>

    <el-description v-if="apiCountData.apiCount >0" style="padding-top: 10px">
      <el-col :span="14">
        <el-row :span="24">
          <el-description-item :label="'待处理('+apiCountData.toUpdateApiCount+'/'+apiCountData.apiCount+')'" :span-map="{md:16}">
            <template slot="content">
              <el-progress
                :text-inside="true"
                :stroke-width="26"
                status="exception"
                :percentage="Math.round(apiCountData.toUpdateApiCount/apiCountData.apiCount*100)"
              />
            </template>
          </el-description-item>
        </el-row>
        <el-row :span="24">
          <el-description-item :label="'待验证('+apiCountData.toVerifyApiCount+'/'+apiCountData.apiCount+')'" :span-map="{md:16}">
            <template slot="content">
              <el-progress
                :text-inside="true"
                :stroke-width="26"
                status="warning"
                :percentage="Math.round(apiCountData.toVerifyApiCount/apiCountData.apiCount*100)"
              />
            </template>
          </el-description-item>
        </el-row>
        <el-row :span="24">
          <el-description-item :label="'已处理('+apiCountData.updatedApiCount+'/'+apiCountData.apiCount+')'" :span-map="{md:16}">
            <template slot="content">
              <el-progress
                :text-inside="true"
                :stroke-width="26"
                status="success"
                :percentage="Math.round(apiCountData.updatedApiCount/apiCountData.apiCount*100)"
              />
            </template>
          </el-description-item>
        </el-row>
      </el-col>
      <el-col :span="10">
        <el-steps :active="stepActive">
          <el-step title="待处理" description="API有更新，需要同步处理用例" />
          <el-step title="待验证" description="用例已更新，待执行验证" />
          <el-step title="已处理" description="API对应的用例全部PASS" />
        </el-steps>
      </el-col>
    </el-description>

    <!-- 显示接口列表信息 -->
    <api-list ref="apiListRef" table-name="接口更新列表" fetch-data-method="getToDoApi" style="padding-top: 10px" />
  </div>

</template>

<script>
import ElDescriptionItem from '@/components/Description/ElDescriptionItem'
import ApiList from '@/views/apiTest/apiMgr/ApiList'
import ElDescription from '@/components/Description/ElDescription'
import { getApiCount } from '@/api/apiTest/api_info'

export default {
  name: 'Update',
  components: { ElDescription, ElDescriptionItem, ApiList },
  data() {
    return {
      listLoading: false,
      stepActive: 1,
      apiCountData: {
        apiCount: 0,
        toUpdateApiCount: 0,
        toVerifyApiCount: 0,
        updatedApiCount: 0
      }
    }
  },
  mounted() {
    this.$refs.apiListRef.fetchData()
    this.getApiUpdateStatusCountData()
  },
  methods: {
    // 获取接口更新状态统计信息
    getApiUpdateStatusCountData() {
      const project_id = this.$route.params.project_id ? this.$route.params.project_id : ''
      getApiCount({ project: project_id, group_by_field: 'update_status' }).then(response => {
        const { msg, code } = response
        this.listLoading = false
        if (code === 2) {
          const countData = response.data
          for (let i = 0; i < countData.length; i++) {
            const data = countData[i]
            const update_status = data['update_status']
            const count = data['count']
            this.apiCountData['apiCount'] += count
            if (update_status === 0) {
              this.apiCountData['toUpdateApiCount'] = count
            } else if (update_status === 1) {
              this.apiCountData['toVerifyApiCount'] = count
            } else if (update_status === 2) {
              this.apiCountData['updatedApiCount'] = count
            } else {
              // 无效的update_status
            }
          }
          // 更新处理进度状态
          if (this.apiCountData.toUpdateApiCount > 0) {
            this.stepActive = 1
          } else if (this.apiCountData.toVerifyApiCount > 0) {
            this.stepActive = 2
          } else {
            this.stepActive = 3
          }
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
