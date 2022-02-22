<template>
  <!-- setup / teardown / setup_class / teardown_class -->
  <div class="main">
    <!-- setup -->
    <div>
      <el-divider class="blue-line" direction="vertical" />
      <span style="font-weight:bold;font-size:14px;color:#2C8DF4;">setup</span>
      <el-popover
        placement="left"
        width="600"
        trigger="click"
      >
        <img src="@/assets/setup_teardown_desc.png" style="height:100%;width:100%"/>
        <span slot="reference" type="text" style="padding-left: 5px">
          <el-button :size="themeSize" type="text" title="帮助" icon="el-icon-info"/>
        </span>

      </el-popover>
      <el-table
        ref="setupTableRef"
        :data="setUp"
        :size="themeSize"
        highlight-current-row
        style="width: 100%"
      >
        <template slot="empty">
          <span>No Data  </span>
          <el-button :size="themeSize" type="primary" class="el-icon-plus" @click="addSetupData">添加</el-button>
        </template>
        <el-table-column prop="name" label="用例" min-width="300" sortable>
          <template slot-scope="scope">
            <el-cascader
              placeholder="搜索：部门/用例集/用例名称"
              :props="{lazy: true, lazyLoad (node, resolve) {deptCaseTreeLoad(node, resolve, 2, false, {test_case: {type: 'setup'}})}}"
              style="width: 60%"
              :size="themeSize"
              filterable
              clearable
              @change="handleSetupCascader($event, scope.$index)"
            >
              <template slot-scope="{ node, data }">
                <span>{{ data.label }}</span>
              </template>
            </el-cascader>
            <el-button :size="themeSize" type="text">{{ scope.row? scope.row.name: '' }}</el-button>
          </template>
        </el-table-column>
        <el-table-column label="操作" min-width="110">
          <template slot-scope="scope">
            <el-button v-if="scope.$index===(setUp.length-1)" :size="themeSize" type="primary" class="el-icon-plus" @click="addSetupData">添加</el-button>
            <el-button v-if="scope.$index>=0" :size="themeSize" type="danger" @click="delSetupData(scope.$index)">删除</el-button>
          </template>
        </el-table-column>
        <el-table-column label="" min-width="40%" />
      </el-table>
    </div>

    <!-- setup_class -->
    <div>
      <el-divider class="blue-line" direction="vertical" />
      <span style="font-weight:bold;font-size:14px;color:#2C8DF4;">setup_class</span>
      <el-table
        ref="setupClassTableRef"
        :data="setupClass"
        :size="themeSize"
        highlight-current-row
        style="width: 100%"
      >
        <template slot="empty">
          <span>No Data  </span>
          <el-button :size="themeSize" type="primary" class="el-icon-plus" @click="addSetupClassData">添加</el-button>
        </template>
        <el-table-column prop="name" label="用例" min-width="300" sortable>
          <template slot-scope="scope">
            <el-cascader
              placeholder="搜索：部门/用例集/用例名称"
              :props="{lazy: true, lazyLoad (node, resolve) {deptCaseTreeLoad(node, resolve, 2, false, {test_case: {type: 'setup'}})}}"
              style="width: 60%"
              :size="themeSize"
              filterable
              clearable
              @change="handleSetupClassCascader($event, scope.$index)"
            >
              <template slot-scope="{ node, data }">
                <span>{{ data.label }}</span>
              </template>
            </el-cascader>
            <el-button :size="themeSize" type="text">{{ scope.row? scope.row.name: '' }}</el-button>
          </template>
        </el-table-column>
        <el-table-column label="操作" min-width="110">
          <template slot-scope="scope">
            <el-button v-if="scope.$index===(setupClass.length-1)" :size="themeSize" type="primary" class="el-icon-plus" @click="addSetupClassData">添加</el-button>
            <el-button v-if="scope.$index>=0" :size="themeSize" type="danger" @click="delSetupClassData(scope.$index)">删除</el-button>
          </template>
        </el-table-column>
        <el-table-column label="" min-width="40%" />
      </el-table>
    </div>

    <!-- teardown -->
    <div style="padding-top: 10px">
      <el-divider class="blue-line" direction="vertical" />
      <span style="font-weight:bold;font-size:14px;color:#2C8DF4;">teardown</span>
      <el-table
        ref="teardownTableRef"
        :data="tearDown"
        :size="themeSize"
        highlight-current-row
        style="width: 100%"
      >
        <template slot="empty">
          <span>No Data  </span>
          <el-button :size="themeSize" type="primary" class="el-icon-plus" @click="addTeardownData">添加</el-button>
        </template>
        <el-table-column prop="name" label="用例" min-width="300" sortable>
          <template slot-scope="scope">
            <el-cascader
              placeholder="搜索：部门/用例集/用例名称"
              :props="{lazy: true, lazyLoad (node, resolve) {deptCaseTreeLoad(node, resolve, 2, false, {test_case: {type: 'teardown'}})}}"
              style="width: 60%"
              :size="themeSize"
              filterable
              clearable
              @change="handleTeardownCascader($event, scope.$index)"
            >
              <template slot-scope="{ node, data }">
                <span>{{ data.label }}</span>
              </template>
            </el-cascader>
            <el-button :size="themeSize" type="text">{{ scope.row? scope.row.name: '' }}</el-button>
          </template>
        </el-table-column>
        <el-table-column label="操作" min-width="110">
          <template slot-scope="scope">
            <el-button v-if="scope.$index===(tearDown.length-1)" :size="themeSize" type="primary" class="el-icon-plus" @click="addSetupData">添加</el-button>
            <el-button v-if="scope.$index>=0" :size="themeSize" type="danger" @click="delTeardownData(scope.$index)">删除</el-button>
          </template>
        </el-table-column>
        <el-table-column label="" min-width="40%" />
      </el-table>
    </div>

    <!-- teardown_class -->
    <div style="padding-top: 10px">
      <el-divider class="blue-line" direction="vertical" />
      <span style="font-weight:bold;font-size:14px;color:#2C8DF4;">teardown_class</span>
      <el-table
        ref="teardownClassTableRef"
        :data="teardownClass"
        :size="themeSize"
        highlight-current-row
        style="width: 100%"
      >
        <template slot="empty">
          <span>No Data  </span>
          <el-button :size="themeSize" type="primary" class="el-icon-plus" @click="addTeardownClassData">添加</el-button>
        </template>
        <el-table-column prop="name" label="用例" min-width="300" sortable>
          <template slot-scope="scope">
            <el-cascader
              placeholder="搜索：部门/用例集/用例名称"
              :props="{lazy: true, lazyLoad (node, resolve) {deptCaseTreeLoad(node, resolve, 2, false, {test_case: {type: 'teardown'}})}}"
              style="width: 60%"
              :size="themeSize"
              filterable
              clearable
              @change="handleTeardownClassCascader($event, scope.$index)"
            >
              <template slot-scope="{ node, data }">
                <span>{{ data.label }}</span>
              </template>
            </el-cascader>
            <el-button :size="themeSize" type="text">{{ scope.row? scope.row.name: '' }}</el-button>
          </template>
        </el-table-column>
        <el-table-column label="操作" min-width="110">
          <template slot-scope="scope">
            <el-button v-if="scope.$index===(teardownClass.length-1)" :size="themeSize" type="primary" class="el-icon-plus" @click="addSetupClassData">添加</el-button>
            <el-button v-if="scope.$index>=0" :size="themeSize" type="danger" @click="delTeardownClassData(scope.$index)">删除</el-button>
          </template>
        </el-table-column>
        <el-table-column label="" min-width="40%" />
      </el-table>
    </div>
  </div>
</template>

<script>
import get_base_data from '@/api/apiTest/get_base_data'

export default {
  name: 'SetupTeardown',
  mixins: [get_base_data],
  props: {},
  data() {
    return {
      themeSize: this.$store.state.settings.themeSize,
      dataModel: [{ id: '', name: '' }], // 数据模板 -- 初始化选择列表
      setUp: this.$attrs.value.setup,
      setupClass: this.$attrs.value.setup_class,
      tearDown: this.$attrs.value.teardown,
      teardownClass: this.$attrs.value.teardown_class
    }
  },
  computed: {
    form() {
      return {
        setup: this.setUp,
        setup_class: this.setupClass,
        teardown: this.tearDown,
        teardown_class: this.teardownClass
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
    '$attrs.value.setup': function(n) {
      this.setUp = this.$attrs.value.setup
    },
    '$attrs.value.setup_class': function(n) {
      this.setupClass = this.$attrs.value.setup_class
    },
    '$attrs.value.teardown': function(n) {
      this.tearDown = this.$attrs.value.teardown
    },
    '$attrs.value.teardown_class': function(n) {
      this.teardownClass = this.$attrs.value.teardown_class
    },
    setup() {},
    setupClass() {},
    teardown() {},
    teardownClass() {}
  },
  methods: {
    // 折叠版 click
    handleChange(val) {
      // console.log(val)
    },

    // setup
    toggleSetupDataSelection(rows) {
      rows.forEach(row => {
        this.$refs.setupTableRef.toggleRowSelection(row, true)
      })
    },
    handleSetupCascader(val, idx) {
      if (val.length > 2) {
        this.setUp[idx] = val[2]
      }
    },
    addSetupData() {
      this.setUp.push({ id: '', name: '' })
      const rows = [this.setUp[this.setUp.length - 1]]
      this.toggleSetupDataSelection(rows)
    },
    delSetupData(index) {
      if (this.setUp.length !== 1) {
        this.setUp.splice(index, 1)
      } else {
        this.setUp = []
      }
    },

    // setup_class
    toggleSetupClassDataSelection(rows) {
      rows.forEach(row => {
        this.$refs.setupClassTableRef.toggleRowSelection(row, true)
      })
    },
    handleSetupClassCascader(val, idx) {
      if (val.length > 2) {
        this.setupClass[idx] = val[2]
      }
    },
    addSetupClassData() {
      this.setupClass.push({ id: '', name: '' })
      const rows = [this.setupClass[this.setupClass.length - 1]]
      this.toggleSetupClassDataSelection(rows)
    },
    delSetupClassData(index) {
      if (this.setupClass.length !== 1) {
        this.setupClass.splice(index, 1)
      } else {
        this.setupClass = []
      }
    },

    // teardown
    toggleTeardownDataSelection(rows) {
      rows.forEach(row => {
        this.$refs.teardownTableRef.toggleRowSelection(row, true)
      })
    },
    handleTeardownCascader(val, idx) {
      if (val.length > 2) {
        this.tearDown[idx] = val[2]
      }
    },
    addTeardownData() {
      this.tearDown.push({ id: '', name: '' })
      const rows = [this.tearDown[this.tearDown.length - 1]]
      this.toggleTeardownDataSelection(rows)
    },
    delTeardownData(index) {
      if (this.tearDown.length !== 1) {
        this.tearDown.splice(index, 1)
      } else {
        this.tearDown = []
      }
    },

    // teardown_class
    toggleTeardownClassDataSelection(rows) {
      rows.forEach(row => {
        this.$refs.teardownClassTableRef.toggleRowSelection(row, true)
      })
    },
    handleTeardownClassCascader(val, idx) {
      if (val.length > 2) {
        this.teardownClass[idx] = val[2]
      }
    },
    addTeardownClassData() {
      this.teardownClass.push({ id: '', name: '' })
      const rows = [this.teardownClass[this.teardownClass.length - 1]]
      this.toggleTeardownClassDataSelection(rows)
    },
    delTeardownClassData(index) {
      if (this.teardownClass.length !== 1) {
        this.teardownClass.splice(index, 1)
      } else {
        this.teardownClass = []
      }
    }
  }
}
</script>

<style scoped>

</style>
