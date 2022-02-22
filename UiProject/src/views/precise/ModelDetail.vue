<template>
  <div>
    <div>
      <br>
      <el-button type="primary" size="small" icon="el-icon-back" style="margin-left: 20px" circle @click="$router.back()"></el-button>
      <p style="float: right; margin-right: 10px; font-family: 'Microsoft YaHei UI'; color: #567d56">
        {{ this.datalist.third_name }}: {{ this.datalist.total }}</p>
    </div>
    <div class="table-container" style="height: 100%">
      <el-table
        ref="table"
        v-loading="listLoading"
        :data="datalist.detail"
        border
        element-loading-text="Loading"
        :max-height="tableHeight"
      >
        <template slot="empty">
          <!--  <img class="data-pic" src="#" alt="" />-->
          <span style="font-size: 16px">先查询，不然不会有数据的</span>
        </template>
        <el-table-column label="关联三级模块" align="center" prop="third_module_name" :show-overflow-tooltip="true">
        </el-table-column>
        <el-table-column label="归属二级模块" align="center" prop="second_name" :show-overflow-tooltip="true">
        </el-table-column>
        <el-table-column label="最后操作人" align="center" prop="updated_by" :show-overflow-tooltip="true">
        </el-table-column>
        <el-table-column align="center" label="操作" width="200px">
          <template slot-scope="scope">
            <el-button
              type="primary"
              icon="el-icon-edit"
              circle
              @click="openDialog(scope.$index, scope.row)">
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      <br>
    </div>
  </div>
</template>

<script>
import { GetDetail } from '@/api/precise'
import { Message } from 'element-ui'

export default {
  data() {
    return {
      // 表格内容
      datalist: {
        detail: []
      },
      // 表格高度
      tableHeight: window.innerHeight,
      // table表格加载转圈
      listLoading: false
    }
  },
  created() {
  },
  mounted() {
    this.getDetail()
  },
  methods: {
    // 获取查询列表
    getDetail() {
      const params = {
        third: this.$route.params.third
      }
      console.log(params)
      GetDetail(params).then(response => {
        if (response.data.detail.length === 0) {
          Message.warning(
            {
              message: '未查询到数据',
              duration: 2 * 1000
            }
          )
        } else {
          this.datalist = response.data
        }
      })
    },
    openDialog() {}
  }
}
</script>
