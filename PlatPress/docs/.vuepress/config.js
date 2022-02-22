module.exports = {
  base: '/',
  port: 8865,
  theme: '',
  plugins: [
    '@vuepress/back-to-top', //此处是添加返回顶部的插件
    '@vuepress/medium-zoom'
  ],
  title: 'qalab.docs',
  head: [
    // 设置 favicon.ico
    ['link', {rel: 'icon', href: '/assets/img/logo.png'}],
  ],
  themeConfig: {
    logo: '/assets/img/logo.png',
    // 右上角搜索框后面的菜单导航
    nav: [
      {text: '首页', link: '/'},
      {text: '工单分析', link: '/order/'},
      {text: '精准测试', link: '/precise/'},
      {
        text: '接口测试', link: '/api_test/',
        items: [
          {text: '指南', link: '/api_test/guide/'},
          {text: '进阶篇', link: '/api_test/advanced/'},
          {text: '解决方案', link: '/api_test/solutions/'},
          {text: '注意事项', link: '/api_test/attentions/'},
          {text: '开发手册', link: '/api_test/develop/'}
        ]
      },
      {text: 'GitLab', link: 'https://git.dustess.com/apitest/test-platform.git'}
    ],

    //左侧菜单
    sidebar: [
      {
        title: '接口测试',
        path: '/api_test/',
        collapsable: true, // 可选的, 默认值是 true,
        sidebarDepth: 2, // 可选的, 默认值是 1
        children: [
          {
            title: '指南',
            path: '/api_test/guide/',
            collapsable: true,
            children: [
              {title: '快速上手', path: '/api_test/guide/quick_start/', collapsable: true, sidebarDepth: 2},
              {title: '第一个测试', path: '/api_test/guide/first_test/', collapsable: true, sidebarDepth: 2},
            ]
          },
          {
            title: '进阶篇',
            path: '/api_test/advanced/',
            collapsable: true,
            children: [
              {title: '权限管理', path: '/api_test/advanced/permission/', collapsable: true, sidebarDepth: 2},
              {title: '全局配置', path: '/api_test/advanced/global_config/', collapsable: true, sidebarDepth: 2},
              {title: '项目管理', path: '/api_test/advanced/project_manager/', collapsable: true, sidebarDepth: 2},
              {
                title: '接口管理',
                path: '/api_test/advanced/api_manager/',
                collapsable: true,
                children: [
                  {title: '接口操作', path: '/api_test/advanced/api_manager/api_opt/', collapsable: true, sidebarDepth: 2},
                  {title: '接口详情', path: '/api_test/advanced/api_manager/api_detail/', collapsable: true, sidebarDepth: 2},
                  {title: '统计分析', path: '/api_test/advanced/api_manager/api_sa/', collapsable: true, sidebarDepth: 2},
                  {title: 'YAPI同步', path: '/api_test/advanced/api_manager/yapi_sync/', collapsable: true, sidebarDepth: 2},
                  {title: '查重工具', path: '/api_test/advanced/api_manager/api_duplicate/', collapsable: true, sidebarDepth: 2},
                ]
              },
              {
                title: '用例管理',
                path: '/api_test/advanced/case_manager/',
                collapsable: true,
                sidebarDepth: 2,
                children: [
                  {title: '用例操作', path: '/api_test/advanced/case_manager/case_opt/', collapsable: true, sidebarDepth: 2},
                  {title: '用例设计', path: '/api_test/advanced/case_manager/case_design/', collapsable: true, sidebarDepth: 2},
                ]
              },
              {title: '测试执行', path: '/api_test/advanced/run_test/', collapsable: true, sidebarDepth: 2},
              {title: '测试结果', path: '/api_test/advanced/test_result/', collapsable: true, sidebarDepth: 2},
              {title: '附1：数据校验方法', path: '/api_test/advanced/validate_rules/', collapsable: true, sidebarDepth: 2},
              {title: '附2：内建方法', path: '/api_test/advanced/builtin_functions/', collapsable: true, sidebarDepth: 2},
            ]
          },
          {
            title: '解决方案',
            path: '/api_test/solutions/',
            collapsable: true,
            children: [
              {title: '环境监控、冒烟、巡检', path: '/api_test/solutions/env_monitor/', collapsable: true, sidebarDepth: 3}
            ]
          },
          {
            title: '注意事项',
            path: '/api_test/attentions/',
            collapsable: true,
            children: [
              {title: '需要处理的事', path: '/api_test/attentions/reclaim/', collapsable: true, sidebarDepth: 2},
              {title: '用例设计规范', path: '/api_test/attentions/case_design_standard/', collapsable: true, sidebarDepth: 2},
            ]
          },
          {
            title: '开发手册',
            path: '/api_test/develop/',
            collapsable: true,
            children: [
              {title: '背景', path: '/api_test/develop/background/', collapsable: true, sidebarDepth: 2},
              {title: '技术栈与设计', path: '/api_test/develop/tech_design/', collapsable: true, sidebarDepth: 2},
              {
                title: '后端接口实现',
                path: '/api_test/develop/backend/',
                collapsable: true, sidebarDepth: 2,
                children: [
                  {title: '表设计', path: '/api_test/develop/backend/models/', collapsable: true, sidebarDepth: 2},
                  {title: '过滤器', path: '/api_test/develop/backend/filters/', collapsable: true, sidebarDepth: 2},
                  {title: '序列化', path: '/api_test/develop/backend/serializers/', collapsable: true, sidebarDepth: 2},
                  {title: '接口响应', path: '/api_test/develop/backend/response/', collapsable: true, sidebarDepth: 2},
                  {title: 'DRF封装', path: '/api_test/develop/backend/drf/', collapsable: true, sidebarDepth: 2},
                  {title: 'DRF自定义', path: '/api_test/develop/backend/drf_custom/', collapsable: true, sidebarDepth: 2},
                  {title: '批量处理', path: '/api_test/develop/backend/drf_bulk/', collapsable: true, sidebarDepth: 2},
                  {title: '路由注册', path: '/api_test/develop/backend/urls/', collapsable: true, sidebarDepth: 2},
                  {title: '测试', path: '/api_test/develop/backend/test/', collapsable: true, sidebarDepth: 2},
                ]
              },
              {title: '执行引擎', path: '/api_test/develop/execution_engine/', collapsable: true, sidebarDepth: 2},
              {title: '自定义内建方法', path: '/api_test/develop/new_builtin_functions/', collapsable: true, sidebarDepth: 2},
              {title: '自定义校验方法', path: '/api_test/develop/new_validate_rules/', collapsable: true, sidebarDepth: 2},
              {title: '任务管理', path: '/api_test/develop/task_manager/', collapsable: true, sidebarDepth: 2},
              {title: 'YAPI同步', path: '/api_test/develop/yapi_sync/', collapsable: true, sidebarDepth: 2},
              {title: '导入导出', path: '/api_test/develop/import_export/', collapsable: true, sidebarDepth: 2},
            ]
          },
          {
            title: '常见问题',
            path: '/api_test/qa/',
            collapsable: true,
            sidebarDepth: 2
          }
        ]
      }
    ]
  }
}
