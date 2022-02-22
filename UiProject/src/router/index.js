import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

/* Layout */
import Layout from '@/layout'
// import fa from 'element-ui/src/locale/lang/fa'

/**
 * Note: sub-menu only appear when route children.length >= 1
 * Detail see: https://panjiachen.github.io/vue-element-admin-site/guide/essentials/router-and-nav.html
 *
 * hidden: true                   if set true, item will not show in the sidebar(default is false)
 * alwaysShow: true               if set true, will always show the root menu
 *                                if not set alwaysShow, when item has more than one children route,
 *                                it will becomes nested mode, otherwise not show the root menu
 * redirect: noRedirect           if set noRedirect will no redirect in the breadcrumb
 * name:'router-name'             the name is used by <keep-alive> (must set!!!)
 * meta : {
    roles: ['admin','editor']    control the page roles (you can set multiple roles)
    title: 'title'               the name show in sidebar and breadcrumb (recommend set)
    icon: 'svg-name'/'el-icon-x' the icon show in the sidebar
    breadcrumb: false            if set false, the item will hidden in breadcrumb(default is true)
    activeMenu: '/example/list'  if set path, the sidebar will highlight the path you set
  }
 */

/**
 * constantRoutes
 * a base page that does not have permission requirements
 * all roles can be accessed
 */
export const constantRoutes = [
  {
    path: '/login',
    component: () => import('@/views/login/index'),
    hidden: true
  },

  {
    path: '/404',
    component: () => import('@/views/404'),
    hidden: true
  },
  {
    path: '/',
    component: Layout,
    redirect: '/dashboard',
    hidden: true,
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        hidden: true,
        component: () => import('@/views/dashboard'),
        meta: { title: 'Dashboard', icon: 'dashboard' }
      }
    ]
  },
  // 仪表盘
  {
    path: '/api/dashboard',
    component: Layout,
    // redirect: '/',
    name: 'Dashboard',
    meta: { title: 'Dashboard', icon: '' }
  },
  // 工单分析
  {
    path: '/api/order',
    component: Layout,
    redirect: '/api/order/list',
    name: 'Orders',
    meta: { title: '工单分析', icon: 'form' },
    children: [
      {
        path: 'list',
        name: 'order',
        component: () => import('@/views/orders/OrderList'),
        meta: { title: '工单列表', icon: 'table' }
      },
      {
        path: 'statistic',
        name: 'Statistics',
        component: () => import('@/views/orders/Statistics'),
        meta: { title: '数据统计', icon: 'blue-bar' }
      },
      {
        path: 'analysis',
        name: 'Analysis',
        component: () => import('@/views/orders/Analysis'),
        meta: { title: '趋势分析', icon: 'blue-line' }
      }
    ]
  },
  // 禅道BUG分析
  {
    path: '/api/zt_bug',
    component: Layout,
    redirect: '/api/zt_dashboard',
    name: 'Zt_Bug',
    meta: { title: 'BUG分析', icon: 'form' },
    hidden: false,
    children: [
      {
        path: 'build',
        name: 'zt_bug',
        component: () => import('@/views/zt/BuildTrend'),
        meta: { title: '版本数据', icon: 'table' }
      },
      {
        path: 'member',
        name: 'zt_bug',
        component: () => import('@/views/zt/BuildTrend'),
        meta: { title: '人员数据', icon: 'blue-bar' }
      },
      {
        path: 'member',
        name: 'zt_bug',
        component: () => import('@/views/zt/BuildTrend'),
        meta: { title: '趋势分析', icon: 'blue-bar' }
      }
    ]
  },
  // 精准测试相关
  {
    path: '/api/precise',
    component: Layout,
    redirect: '/api/precise/model',
    name: 'Precise',
    meta: { title: '精准检索', icon: 'eye' },
    hidden: true,
    children: [
      {
        path: 'model',
        name: 'model',
        component: () => import('@/views/precise/ModelList'),
        hidden: true,
        meta: { title: '模块检索', icon: 'tree', keepAlive: true }
      },
      {
        path: 'code',
        name: 'codeDiff',
        component: () => import('@/views/precise/CaseHover'),
        hidden: true,
        meta: { title: '用例覆盖', icon: 'tree' }
      },
      {
        path: 'model_detail',
        name: 'thirdModel',
        component: () => import('@/views/precise/ModelDetail'),
        hidden: true,
        meta: { title: '关联模块', icon: 'link' }
      },
      {
        path: 'func_detail',
        name: 'function',
        component: () => import('@/views/precise/FuncDetail'),
        hidden: true,
        meta: { title: '关联功能', icon: 'eye-open' }
      },
      {
        path: 'case_detail',
        name: 'case',
        component: () => import('@/views/precise/CaseDetail'),
        hidden: true,
        meta: { title: '关联用例', icon: 'eye-open' }
      }
    ]
  },
  // 接口测试
  {
    path: '/api/apiTest',
    redirect: '/api/apiTest/workbench',
    component: Layout,
    name: '接口测试',
    meta: { title: '接口测试', icon: 'el-icon-cpu' },
    children: [
      {
        path: 'workbench',
        component: () => import('@/views/apiTest/workbench'),
        name: '工作台',
        meta: { title: '工作台', icon: 'el-icon-s-platform' }
      },
      {
        path: 'global',
        component: () => import('@/views/apiTest/globalMgr'),
        name: '全局配置',
        meta: { title: '全局配置', icon: 'el-icon-setting' }
      },
      {
        path: 'projectMgr',
        name: '项目管理',
        component: () => import('@/views/apiTest/projectMgr'),
        meta: { title: '项目管理', icon: 'tree' }
      },
      {
        path: 'projectMgr/project_id=:project_id',
        component: () => import('@/views/apiTest/projectMgr/projectDetail'),
        hidden: true,
        name: '项目详情',
        meta: { title: '项目详情', icon: 'table' }
      },
      {
        path: 'apiMgr',
        name: '接口管理',
        component: () => import('@/views/apiTest/apiMgr'),
        meta: { title: '接口管理', icon: 'el-icon-s-ticket' },
        children: [
          {
            path: 'api_id=:api_id',
            component: () => import('@/views/apiTest/apiMgr/apiDetail'),
            hidden: true,
            name: '接口详情1',
            meta: { title: '接口详情1' }
          }
        ]
      },
      {
        path: 'apiMgr/api_id=:api_id',
        component: () => import('@/views/apiTest/apiMgr/apiDetail'),
        hidden: true,
        name: '接口详情',
        meta: { title: '接口详情', icon: 'table', keepAlive: true }
      },
      {
        path: 'caseMgr',
        component: () => import('@/views/apiTest/caseMgr'),
        name: '用例管理',
        meta: { title: '用例管理', icon: 'el-icon-suitcase', keepAlive: true }
      },
      {
        path: 'caseMgr/case_id=:case_id',
        component: () => import('@/views/apiTest/caseMgr/caseDetail'),
        hidden: true,
        name: '用例详情',
        meta: { title: '用例详情', icon: 'table', keepAlive: true }
      },
      {
        path: 'testReport',
        name: '历史报告',
        component: () => import('@/views/apiTest/reportMgr'),
        meta: { title: '历史报告', icon: 'el-icon-notebook-1' },
        children: [
          {
            hidden: true,
            path: 'pytest_html/report_id=:report_id',
            component: () => import('@/views/apiTest/reportMgr/reportDetail/PytestHtmlReport'),
            name: 'PytestHtml',
            meta: { title: 'PytestHtml' }
          },
          {
            hidden: true,
            path: 'allure_html/report_id=:report_id',
            component: () => import('@/views/apiTest/reportMgr/reportDetail/AllureHtmlReport'),
            name: 'AllureHtml',
            meta: { title: 'AllureHtml' }
          },
          {
            hidden: true,
            path: 'test_logs/report_id=:report_id',
            component: () => import('@/views/apiTest/reportMgr/reportDetail/TestLogs'),
            name: 'TestLogs',
            meta: { title: 'TestLogs' }
          }
        ]
      },
      {
        path: 'dataMgr',
        name: '导入导出',
        component: () => import('@/views/apiTest/dataMgr/index'),
        meta: { title: '数据管理', icon: 'el-icon-upload' }
      },
      {
        path: 'taskMgr',
        name: '任务管理',
        component: () => import('@/views/apiTest/taskMgr/index'),
        meta: { title: '任务管理', icon: 'el-icon-s-promotion' }
      },
      {
        path: '/api/apiTest/statisticalAnalysis',
        component: () => import('@/views/apiTest/statisticalAnalysis'),
        name: '统计分析',
        meta: { title: '统计分析', icon: 'el-icon-s-data' },
        children: [
          {
            path: 'summary',
            component: () => import('@/views/apiTest/statisticalAnalysis/summary/index'),
            name: '概览',
            meta: { title: '概览' }
          },
          {
            path: 'api',
            component: () => import('@/views/apiTest/statisticalAnalysis/apiAnalysis/index'),
            name: '接口分析',
            meta: { title: '接口分析' }
          },
          {
            path: 'case',
            component: () => import('@/views/apiTest/statisticalAnalysis/caseAnalysis/index'),
            name: '用例分析',
            meta: { title: '用例分析' }
          },
          {
            path: 'result',
            component: () => import('@/views/apiTest/statisticalAnalysis/resultAnalysis/index'),
            name: '结果分析',
            meta: { title: '结果分析' }
          },
          {
            path: 'work',
            component: () => import('@/views/apiTest/statisticalAnalysis/workAnalysis/index'),
            name: '进度分析',
            meta: { title: '进度分析' }
          }
        ]
      },
      {
        path: '/api/apiTest/help',
        name: '帮助文档',
        component: () => import('@/views/apiTest/help'),
        meta: { title: '帮助', icon: 'tree' },
        children: [
          {
            path: 'validate_rules',
            component: () => import('@/views/apiTest/help/BuiltinComparators'),
            name: '数据校验器',
            meta: { title: '数据校验器' }
          },
          {
            path: 'builtin_functions',
            component: () => import('@/views/apiTest/help/BuiltinFunctions'),
            name: '内建函数',
            meta: { title: '内建函数' }
          },
          {
            path: 'customized_functions',
            component: () => import('@/views/apiTest/help/CustomizedFunctions'),
            name: '接口封装',
            meta: { title: '接口封装' }
          }
        ]
      }
    ]
  },
  // 数据工厂
  {
    path: '/api/dataServer',
    component: Layout,
    redirect: '/apiTest',
    name: '数据工厂',
    meta: { title: '数据工厂', icon: 'el-icon-s-help' },
    hidden: true,
    children: [
      {
        path: 'dataManage',
        name: '数据管理',
        component: () => import('@/views/apiTest/dataMgr/index'),
        meta: { title: '数据管理', icon: 'table' }
      },
      {
        path: 'setting',
        name: '使用配置',
        component: () => import('@/views/apiTest/globalMgr/const'),
        meta: { title: '使用配置', icon: 'table' }
      }
    ]
  },

  // 系统管理
  {
    path: '/api/systemManage',
    component: Layout,
    name: '系统管理',
    meta: { title: '系统管理', icon: 'el-icon-setting' },
    children: [
      {
        path: 'organization',
        component: () => import('@/views/system-manage/organization'),
        name: '团队组织',
        meta: { title: '团队组织', icon: 'peoples' },
        // hidden: true,
        children: [
          {
            path: 'department',
            component: () => import('@/views/system-manage/organization/department'),
            name: '部门管理',
            meta: { title: '部门管理', icon: 'tree-table' }
          },
          {
            path: 'user',
            component: () => import('@/views/system-manage/organization/user'),
            name: '用户管理',
            meta: { title: '用户管理', icon: 'el-icon-user' }
          },
          {
            path: 'permission',
            component: () => import('@/views/system-manage/config-center/Permission'),
            name: '权限管理',
            meta: { title: '权限管理', icon: 'el-icon-lock' }
          }
        ]
      },
      {
        path: 'configCenter',
        component: () => import('@/views/system-manage/config-center'),
        name: '配置中心',
        meta: { title: '配置中心', icon: 'el-icon-setting' },
        hidden: true,
        children: [
          {
            path: 'permission',
            component: () => import('@/views/system-manage/config-center/Permission'),
            name: '权限管理',
            meta: { title: '权限管理', icon: 'el-icon-lock' }
          },
          {
            path: 'theme',
            component: () => import('@/views/system-manage/config-center/Theme'),
            name: '主题配置',
            meta: { title: '主题配置', icon: 'el-icon-s-open' }
          }
        ]
      },
      {
        path: 'systemLogs',
        component: () => import('@/views/system-manage/system-logs'),
        name: '系统日志',
        meta: { title: '系统日志', icon: 'el-icon-notebook-2' },
        children: [
          {
            path: 'message',
            component: () => import('@/views/system-manage/system-logs/Message'),
            name: 'message',
            meta: { title: 'message', icon: 'el-icon-notebook-2' }
          },
          {
            path: 'logs/api_test',
            component: () => import('@/views/system-manage/system-logs/ApiTest'),
            name: 'api_test',
            meta: { title: 'api_test', icon: 'el-icon-notebook-2' }
          },
          {
            path: 'logs/error',
            component: () => import('@/views/system-manage/system-logs/Error'),
            name: 'error',
            meta: { title: 'error', icon: 'el-icon-notebook-2' }
          }
        ]
      }
    ]
  },
  // 404 page must be placed at the end !!!
  { path: '*', redirect: '/404', hidden: true }
]

const createRouter = () => new Router({
  // mode: 'history', // require service support
  scrollBehavior: () => ({ y: 0 }),
  routes: constantRoutes
})

const router = createRouter()

// Detail see: https://github.com/vuejs/vue-router/issues/1234#issuecomment-357941465
export function resetRouter() {
  const newRouter = createRouter()
  router.matcher = newRouter.matcher // reset router
}

export default router
