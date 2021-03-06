# 用例设计规范

## 目标
- **测试环境交付检验**
  - 目前测试环境交付测试团队后仍存在大量阻塞问题
  - 需要提供方法对开发交付的测试环境进行快速检验
  - 测试环境检验测试仅校验核心接口正向用例连通性，服务内部逻辑是否正确不做检查
- **实现线上业务功能巡检**
  - 每日构建、维护，全量执行。（多次）
- **冒烟测试**
  - 核心接口正向用例通过、场景测试通过

## 设计原则
- 所有测试操作的数据尽量自己构造，避免因空环境无数据导致测试无法通过 
- 各组独自完成自己部门相关的数据构造设计 
- 如需数据尽量先获取或构造

## 构建方案
### 1. 分级保障
基于现有接口测试平台、接口测试用例，通过用例分级设计、分级运行、分级校验的方式，实现快速验证测试环境接口连通性。
测试用例设计分级：
- setup/teardown：该类型测试用例不会单独执行，仅在被前后置调用时执行
- 单接口测试
  - P0：核心接口正向用例
  - P1：核心接口异常用例
  - P2：非核心接口用例
- 场景测试

::: warning 注意
1. 场景测试和P0级别的单接口测试用例需确保通过，P1和P2级用例为可选执行。
2. 优先设计P0用例，P0中又可以优先考虑接口覆盖率，推动覆盖率达到100%，再考虑用例设计覆盖全面性
:::


### 2 测试分级运行
- 测试执行维度
  - 用例集
  - 用例
  - 测试步骤
- 测试用例执行维度
  - 单接口测试
  - 场景测试
- 单接口测试用例执行维度
  - 优先级P0
  - 优先级P1
  - 优先级P2

### 3 响应分级校验
- 响应状态码
- 响应json-schema
- 响应值内容

### 4. 有变更接口选择性执行
对于存在更新且未对用例进行维护的接口，进行选择性执行：
- 场景测试：遇到有更新待处理的接口请求步骤，停止测试，标记用例失败
- 非场景测试：遇到有更新待处理的接口请求步骤，继续测试，如步骤失败，continue(标记步骤失败并继续后续步骤执行)

### 5. 测试构建类型
<font color=#E6A23C>**接口测试->工作台->快速测试/业务巡检/冒烟测试/环境验证**</font>
测试平台支持自定义校验规则。
#### 5.1 测试环境可用性验证
通过执行并验证核心接口连通性，确保测试环境基本可用。即：
- 单接口测试用例
- 优先级P0
- 仅校验响应状态码200。（或可加上response.data.code）

#### 5.2 冒烟测试
- 单接口测试用例
- 优先级P0、P1
- 全部校验：响应状态码、响应值内容
#### 5.3 业务巡检 - 每日构建
- 全部用例：单接口测试用例、场景用例
- 全部校验：响应状态码、响应值内容
#### 5.4 其他（快速测试）
灵活筛选用例执行，指定校验方式。
