<template>
  <div class="main">
    <!--显示接口分组信息：如果指定接口分组-->
    <el-collapse value="1" @change="handleChange">
      <el-collapse-item name="2">
        <span slot="title" style="font-weight:bold;font-size:14px;color:#2C8DF4;width: 90%">
          {{ apiGroupData.name }}
          <el-button style="float:right;" type="text" class="el-icon-delete" @click="handleDeleteApiGroup" />
          <el-button style="padding-right:10px; float:right;" type="text" class="el-icon-edit" @click="handleEditApiGroup" />
        </span>
        <el-card class="box-card" shadow="never">
          <el-description>
            <el-description-item label="描述" :value="apiGroupData.description" :span="8" :span-map="{md:12}" />
          </el-description>
        </el-card>
      </el-collapse-item>
    </el-collapse>

    <!--编辑接口分组界面-->
    <el-drawer
      title="编辑接口分组"
      :with-header="true"
      :wrapper-closable="false"
      :visible.sync="editApiGroupFormVisible"
      direction="rtl"
      size="50%"
    >
      <el-container>
        <!-- 编辑接口分组 -->
        <el-main style="text-align: left;">
          <el-form ref="editApiGroupForm" :model="editApiGroupForm" label-width="120px" :rules="editApiGroupFormRules">
            <el-collapse value="1" @change="handleChange">
              <el-collapse-item name="1">
                <span slot="title" style="font-weight:bold;font-size:14px;color:#2C8DF4;">基本信息</span>
                <el-form-item label="分组名称" prop="name">
                  <el-input v-model="editApiGroupForm.name" auto-complete="off" />
                </el-form-item>
                <el-form-item label="描述" prop="description">
                  <el-input v-model="editApiGroupForm.description" type="textarea" :rows="2" />
                </el-form-item>
              </el-collapse-item>
            </el-collapse>
          </el-form>
        </el-main>
        <!-- 取消、提交 -->
        <el-footer style="text-align: center;">
          <div>
            <el-button @click.native="editApiGroupFormVisible = false; editApiGroupLoading = false">取消</el-button>
            <el-button type="primary" :loading="editApiGroupLoading" @click.native="editApiGroupSubmit">提交</el-button>
          </div>
        </el-footer>
      </el-container>
    </el-drawer>
  </div>
</template>

<script>
import { getApiGroupDetail, updateApiGroup } from '@/api/apiTest/api_group'
import ElDescription from '@/components/Description/ElDescription'
import ElDescriptionItem from '@/components/Description/ElDescriptionItem'

export default {
  name: 'ApiGroupDetail',
  components: { ElDescription, ElDescriptionItem },
  data() {
    return {
      themeSize: this.$store.state.settings.themeSize,
      apiGroupId: '',

      editApiGroupLoading: false,
      editApiGroupFormVisible: false, // 编辑接口分组界面是否显示
      apiGroupData: {},
      editApiGroupFormRules: {
        name: [
          { required: true, message: '请输入名称', trigger: 'blur' },
          { min: 1, max: 50, message: '长度在 1 到 50 个字符', trigger: 'blur' }
        ],
        description: [
          { required: false, message: '请输入描述', trigger: 'blur' },
          { max: 1024, message: '不能超过1024个字符', trigger: 'blur' }
        ]
      },
      editApiGroupForm: {
        name: '',
        description: ''
      }
    }
  },
  methods: {
    handleChange(val) {
      // console.log(val)
    },
    fetchGroupDetail() {
      this.listLoading = true
      getApiGroupDetail(this.apiGroupId).then(response => {
        this.apiGroupData = response.data
        this.listLoading = false
      })
    },
    // 编辑接口分组事件
    handleEditApiGroup() {
      this.editApiGroupForm = Object.assign({}, this.apiGroupData)
      this.editApiGroupFormVisible = true
    },
    // 删除接口分组事件
    handleDeleteApiGroup() {
      if (this.total > 0) {
        this.$notify.error({
          title: '错误',
          message: '接口分组中存在API，不能删除！！！'
        })
      } else {
        this.$notify.warning({
          title: 'TODO',
          message: '暂时不支持删除！！！'
        })
      }
    },
    // 修改接口分组
    editApiGroupSubmit() {
      this.$refs.editApiGroupForm.validate((valid) => {
        if (valid) {
          this.$confirm('确认提交吗？', '提示', {}).then(() => {
            this.editApiGroupLoading = true
            // NProgress.start();
            const params = {
              name: this.editApiGroupForm.name,
              description: this.editApiGroupForm.description
            }
            updateApiGroup(this.editApiGroupForm.id, params).then(_data => {
              const { msg, code } = _data
              this.editApiGroupLoading = false
              if (code === 2) {
                this.$message({
                  message: '修改成功',
                  center: true,
                  type: 'success'
                })
                this.$refs['editApiGroupForm'].resetFields()
                this.editApiGroupFormVisible = false
                this.fetchData()
              } else if (code === 400) { // 参数错误或数据库不允许的输入
                this.$message.error({
                  message: msg,
                  center: true
                })
              } else {
                this.$message.error({
                  message: msg,
                  center: true
                })
                this.editApiGroupFormVisible = false
                this.fetchData()
              }
            }).then(_res => {
              this.fetchGroupDetail()
            })
          })
        }
      })
    }
  }
}
</script>

<style scoped>

</style>
