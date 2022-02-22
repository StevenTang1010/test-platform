<template>
  <div class="main">
    <tabs-menu :tab-pane-list="tabPaneList" />
    <el-container>
      <router-view />
    </el-container>
  </div>

</template>

<script>
import TabsMenu from '@/views/apiTest/components/TabsMenu'

export default {
  name: 'Index',
  components: { TabsMenu },
  data() {
    return {
      themeSize: this.$store.state.settings.themeSize,
      tabPaneList: [
        {
          name: this.$route.path,
          label: this.$route.name,
          components: []
        }
      ]
    }
  },
  methods: {}
}
</script>

<style scoped>

</style>
