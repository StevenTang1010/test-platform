<template>
  <div class="main">
    <div>
      <el-divider class="blue-line" direction="vertical" />
      <span style="font-weight:bold;font-size:14px;color:#2C8DF4;">请求参数</span>
      <el-tabs v-model="activeName">
        <!--  请求参数Body  -->
        <el-tab-pane label="Body" name="body">
          <request-parameters v-model="apiInfo" />
        </el-tab-pane>
        <!--  请求头 Header -->
        <el-tab-pane label="Header" name="req_headers">
          <request-headers v-model="apiInfo.req_headers" />
        </el-tab-pane>
      </el-tabs>
    </div>
    <div>
      <el-divider class="blue-line" direction="vertical" />
      <span style="font-weight:bold;font-size:14px;color:#2C8DF4;">期望输出</span>
      <response-validate v-model="apiInfo.validator" />
    </div>
  </div>
</template>

<script>
import RequestHeaders from '@/views/apiTest/components/RequestHeaders'
import RequestParameters from '@/views/apiTest/components/RequestParameters'
import ResponseValidate from '@/views/apiTest/components/ResponseValidate'

export default {
  name: 'ApiTestTemplate',
  components: { RequestHeaders, RequestParameters, ResponseValidate },
  data() {
    return {
      activeName: 'body'
    }
  },
  computed: {
    apiInfo: {
      get() {
        return this.$attrs.value
      },
      set(v) {
        this.$emit('input', v)
      }
    }
  }
}
</script>

<style scoped>

</style>
