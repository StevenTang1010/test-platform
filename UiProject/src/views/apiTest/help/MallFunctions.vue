<template>
  <div class="main">
    <div v-loading="isLoading">
      <p style="padding-left: 10px" v-html="htmlContent" />
    </div>
  </div>
</template>

<script>

import { getMallFunctionList } from '@/api/apiTest/help_functions'

export default {
  name: 'MallFunctions',
  data() {
    return {
      themeSize: this.$store.state.settings.themeSize,

      isLoading: false,
      htmlContent: ''
    }
  },
  mounted() {
    this.fetchData()
  },
  methods: {
    fetchData() {
      this.isLoading = true
      getMallFunctionList().then(response => {
        const { msg, code } = response
        this.isLoading = false
        if (code === 2) {
          this.htmlContent = response.data
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
