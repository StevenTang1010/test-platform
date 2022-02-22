<template>
  <!-- setup/teardown hooks -->
  <div class="main">
    <!-- setup_hooks -->
    <div>
      <el-divider class="blue-line" direction="vertical" />
      <span style="font-weight:bold;font-size:14px;color:#2C8DF4;">setup_hooks</span>
      <el-table
        ref="setupTableRef"
        :data="setupHooks"
        :size="themeSize"
        highlight-current-row
        style="width: 100%"
      >
        <template slot="empty">
          <span>No Data  </span>
          <el-button :size="themeSize" type="primary" class="el-icon-plus" @click="addSetupData">添加</el-button>
        </template>
        <el-table-column prop="var_name" label="VarName" min-width="150" sortable>
          <template slot-scope="scope">
            <el-input v-model="scope.row.var_name" :size="themeSize" />
          </template>
        </el-table-column>
        <el-table-column prop="hook_content" label="HookContent" min-width="220" sortable>
          <template slot-scope="scope">
            <el-input v-model="scope.row.hook_content" type="textarea" :autosize="{ minRows: 1}" :size="themeSize" />
          </template>
        </el-table-column>
        <el-table-column label="操作" min-width="60">
          <template slot-scope="scope">
            <el-button v-if="scope.$index===(setupHooks.length-1)" :size="themeSize" type="primary" icon="el-icon-plus" circle @click="addSetupData" />
            <el-button v-if="scope.$index>=0" :size="themeSize" type="danger" icon="el-icon-delete" circle @click="delSetupData(scope.$index)" />
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- teardown_hooks -->
    <div style="padding-top: 10px">
      <el-divider class="blue-line" direction="vertical" />
      <span style="font-weight:bold;font-size:14px;color:#2C8DF4;">teardown_hooks</span>
      <el-table
        ref="teardownTableRef"
        :data="teardownHooks"
        :size="themeSize"
        highlight-current-row
        style="width: 100%"
      >
        <template slot="empty">
          <span>No Data  </span>
          <el-button :size="themeSize" type="primary" class="el-icon-plus" @click="addTeardownData">添加</el-button>
        </template>
        <el-table-column prop="var_name" label="VarName" min-width="150" sortable>
          <template slot-scope="scope">
            <el-input v-model="scope.row.var_name" :size="themeSize" />
          </template>
        </el-table-column>
        <el-table-column prop="hook_content" label="HookContent" min-width="220" sortable>
          <template slot-scope="scope">
            <el-input v-model="scope.row.hook_content" type="textarea" :autosize="{ minRows: 1}" :size="themeSize" />
          </template>
        </el-table-column>
        <el-table-column label="操作" min-width="60">
          <template slot-scope="scope">
            <el-button v-if="scope.$index===(teardownHooks.length-1)" :size="themeSize" type="primary" icon="el-icon-plus" circle @click="addTeardownData" />
            <el-button v-if="scope.$index>=0" :size="themeSize" type="danger" icon="el-icon-delete" circle @click="delTeardownData(scope.$index)" />
          </template>
        </el-table-column>
      </el-table>
    </div>

  </div>
</template>

<script>
export default {
  name: 'SetupTeardownHooks',
  props: {},
  data() {
    return {
      themeSize: this.$store.state.settings.themeSize,

      setupHooks: this.$attrs.value.setup_hooks,
      teardownHooks: this.$attrs.value.teardown_hooks
    }
  },
  computed: {
    form() {
      return {
        setup_hooks: this.setupHooks,
        teardown_hooks: this.teardownHooks
      }
    }
  },
  watch: {
    form() {
      this.$emit('input', {
        ...this.$attrs.value,
        ...this.form
      })
    },
    '$attrs.value.setup_hooks': function(n) {
      this.setupHooks = this.$attrs.value.setup_hooks
    },
    '$attrs.value.teardown_hooks': function(n) {
      this.teardownHooks = this.$attrs.value.teardown_hooks
    },
    setupHooks() {},
    teardownHooks() {}
  },
  methods: {
    // setup_hooks
    toggleSetupDataSelection(rows) {
      rows.forEach(row => {
        this.$refs.setupTableRef.toggleRowSelection(row, true)
      })
    },
    addSetupData() {
      this.setupHooks.push({ var_name: '', hook_content: '' })
      const rows = [this.setupHooks[this.setupHooks.length - 1]]
      this.toggleSetupDataSelection(rows)
    },
    delSetupData(index) {
      if (this.setupHooks.length !== 1) {
        this.setupHooks.splice(index, 1)
      } else {
        this.setupHooks = []
      }
    },

    // teardown_hooks
    toggleTeardownDataSelection(rows) {
      rows.forEach(row => {
        this.$refs.teardownTableRef.toggleRowSelection(row, true)
      })
    },
    addTeardownData() {
      this.teardownHooks.push({ var_name: '', hook_content: '' })
      const rows = [this.teardownHooks[this.teardownHooks.length - 1]]
      this.toggleTeardownDataSelection(rows)
    },
    delTeardownData(index) {
      if (this.teardownHooks.length !== 1) {
        this.teardownHooks.splice(index, 1)
      } else {
        this.teardownHooks = []
      }
    }
  }
}
</script>

<style scoped>

</style>
