<template>
  <!--  YAPI参数展示（请求参数+返回数据）  -->
  <div class="main">
    <!--  标签页  -->
    <el-tabs v-model="activeName" @tab-click="clickTab">
      <el-tab-pane
        v-for="(item,index) in getYapiParamsList()"
        :key="index"
        :label="item.label"
        :name="item.name"
        lazy
      >
        <json-viewer :value="item.value ? JSON.parse(item.value):String(item.value)" :expand-depth="2" copyable sort />
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import JsonViewer from 'vue-json-viewer'

export default {
  name: '',
  components: { JsonViewer },
  props: {
    apiInfo: {
      type: Object,
      default() {
        return {
          yapi_req_headers: '',
          yapi_req_params: '',
          yapi_req_query: '',
          yapi_req_body_form: '',
          yapi_req_body_other: ''
        }
      }
    }
  },
  data() {
    return {
      activeName: '' // 默认选中
    }
  },
  created() {
  },
  mounted() {
  },
  methods: {
    // 控制每次点击标签，都重新请求子组件的接口
    clickTab(tab, event) {
      console.log(tab, event)
    },
    getYapiParamsList() {
      return [
        {
          name: 'yapi_req_headers',
          label: 'Headers',
          value: this.apiInfo.yapi_req_headers
        },
        {
          name: 'yapi_req_params',
          label: 'Params',
          value: this.apiInfo.yapi_req_params
        },
        {
          name: 'yapi_req_query',
          label: 'Query',
          value: this.apiInfo.yapi_req_query
        },
        {
          name: 'yapi_req_body_form',
          label: 'BodyForm',
          value: this.apiInfo.yapi_req_body_form
        },
        {
          name: 'yapi_req_body_other',
          label: 'BodyOther',
          value: this.apiInfo.yapi_req_body_other
        },
        {
          name: 'yapi_res_body',
          label: '响应数据',
          value: this.apiInfo.yapi_res_body
        }
      ]
    }
  }
}
</script>

<style scoped>

</style>
