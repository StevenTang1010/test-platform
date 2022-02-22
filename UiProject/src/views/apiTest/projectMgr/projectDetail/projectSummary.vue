<template>
  <div class="main">
    <!--  项目详情页  -->
    <el-card class="box-card" shadow="never">
      <div slot="header" class="clearfix"> <h1>{{ name }}</h1> </div>
      <el-description :span="24">
        <el-description-item label="版本" :value="version" :span-map="{md:12}">
          <template slot="content">
            <el-tag :size="themeSize"> {{ version }} </el-tag>
          </template>
        </el-description-item>
        <el-description-item label="状态" :span-map="{md:12}">
          <template slot="content">
            <span v-show="data.status"><el-tag :size="themeSize" type="success"> 启用 </el-tag></span>
            <span v-show="!data.status"><el-tag :size="themeSize" type="danger">禁用 </el-tag></span>
          </template>
        </el-description-item>
        <el-description-item label="所属部门" :value="department" :span-map="{md:12}" />
        <el-description-item label="创建时间" :value="create_time" :span-map="{md:12}" />
        <el-description-item label="更新时间" :value="update_time" :span-map="{md:12}" />
      </el-description>
    </el-card>
    <el-row :span="24">
      <el-col :span="4" class="inline">
        <el-card class="box-card">
          <router-link :to="{name: '成员管理'}" style="text-decoration: none;color: #000000;"><h1>{{ memberCount }}</h1></router-link>
          <div>项目组成员</div>
        </el-card>
      </el-col>
      <el-col :span="5" class="inline">
        <el-card class="box-card">
          <router-link :to="{name: '接口管理'}" style="text-decoration: none;color: #000000;"><h1>{{ apiCount }}</h1></router-link>
          <div>接口数量</div>
        </el-card>
      </el-col>
      <el-col :span="5" class="inline">
        <el-card class="box-card">
          <router-link :to="{name: '项目用例', params: { project_id: project_id }}" style="text-decoration: none;color: #000000;"><h1>{{ stepCount }}</h1></router-link>
          <div>用例步骤数量</div>
        </el-card>
      </el-col>
      <el-col :span="5" class="inline">
        <el-card class="box-card">
          <router-link :to="{name: '接口覆盖率'}" style="text-decoration: none;color: #000000;">
            <h1>{{ apiCoverage*100 }}%</h1>
          </router-link>
          <div>接口覆盖率</div>
        </el-card>
      </el-col>
      <el-col :span="5" class="inline">
        <el-card class="box-card">
          <h1>{{ parseFloat(apiPassRate*100).toFixed(0) }}%</h1>
          <div>接口通过率</div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { getProjectDetail } from '@/api/apiTest/project'
import ElDescription from '@/components/Description/ElDescription'
import ElDescriptionItem from '@/components/Description/ElDescriptionItem'

export default {
  name: 'ProjectDetail',
  components: { ElDescription, ElDescriptionItem },
  data() {
    return {
      themeSize: this.$store.state.settings.themeSize,
      project_id: this.$route.params.project_id,
      data: {},
      name: '',
      type: '',
      version: '',
      department: '',
      apiCount: 0,
      apiCoverage: 0,
      apiPassRate: 0,
      stepCount: 0,
      dynamicCount: 0,
      memberCount: 0,
      create_time: '',
      update_time: ''
    }
  },
  created() {
  },
  mounted() {
    this.getProjectInfo()
  },
  methods: {
    getProjectInfo() {
      const project_id = this.$route.params.project_id
      getProjectDetail(project_id).then(response => {
        const { msg, code } = response
        this.listLoading = false
        if (code === 2) {
          this.data = response.data
          this.name = response.data.name
          this.type = response.data.type
          this.version = response.data.version
          this.department = response.data.department ? response.data.department.name : ''
          this.apiCount = response.data.apiCount
          this.apiCoverage = response.data.apiCoverage
          this.apiPassRate = response.data.apiPassRate
          this.stepCount = response.data.stepCount
          this.dynamicCount = response.data.dynamicCount
          this.memberCount = response.data.memberCount
          this.create_time = response.data.create_time
          this.update_time = response.data.update_time
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
