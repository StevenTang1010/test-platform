import get_base_data from '@/api/apiTest/get_base_data'

export default {
  mixins: [get_base_data],
  data() {
    return {
      listLoading: false,
      // 获取公共数据，--供表单选择
      user_options: [], // 用户列表
      department_options: [], // 部门列表
      project_options: [], // 项目列表

      globalEnv_options: [], // 全局环境配置
      globalHeader_options: [], // 全局Header配置
      globalLabel_options: [], // 全局标签

      api_group_options: [], // 接口分组
      apiInfo_options: [], // 接口

      test_suite_options: [], // 用例集
      test_case_options: [], // 用例

      // 统计数据
      noCaseApiCountByProject: []
    }
  },
  mounted() {
    this.getProject()
    this.getTestSuite()
    this.getTestCase()
    this.getLabel()
    this.getEnv()
  },
  methods: {
  }
}
