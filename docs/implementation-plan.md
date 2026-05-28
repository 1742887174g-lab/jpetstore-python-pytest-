# JPetStore 自动化测试平台实现流程

## 1. 自动化框架层

技术栈：

- Python 3.11+
- pytest
- allure-pytest
- Playwright
- requests
- PyYAML

核心能力：

- 支持通过 YAML 配置 JPetStore 环境地址
- 支持 `smoke` / `ui` / `api` / `regression` 分组执行
- 支持 Page Object Model 封装页面操作
- 支持失败截图并附加到 Allure 报告
- 支持接口请求/响应内容附加到 Allure 报告
- 支持测试数据与测试代码分离
- 支持通过 `--env` 和 `--base-url` 切换测试环境
- 支持命令行一键执行并输出报告目录

已覆盖业务：

- 登录成功
- 登录失败
- 退出登录
- 商品搜索
- 商品详情
- 添加商品到购物车
- 修改购物车数量
- 删除购物车商品
- 用户注册
- 提交订单

常用命令：

```powershell
cd E:\jpetstore-test
.\run_api_tests.cmd
.\run_ui_tests.cmd
.\run_smoke_tests.cmd
.\run_regression_tests.cmd
.\run_allure_report.cmd
```

## 2. 测试平台后端

技术栈：

- FastAPI
- SQLite
- subprocess 调用 pytest

核心能力：

- 创建测试执行任务
- 触发 pytest 执行
- 保存执行状态、耗时、退出码、报告路径
- 保存 stdout / stderr，便于排查失败原因
- 查询历史执行记录
- 查询单次执行详情

已实现接口：

```text
GET  /health
POST /test-runs
GET  /test-runs
GET  /test-runs/{id}
```

`POST /test-runs` 请求示例：

```json
{
  "suite": "smoke",
  "environment": "local",
  "base_url": "http://localhost:8080/jpetstore"
}
```

SQLite 数据库位置：

```text
backend/data/test_platform.db
```

当前 `test_runs` 表记录：

- 执行套件
- 执行状态
- pytest 退出码
- 实际执行命令
- 环境名
- 被测地址
- 开始时间
- 结束时间
- 执行耗时
- Allure 结果目录
- stdout
- stderr

## 3. 测试平台前端

技术栈：

- Vue 3
- Element Plus
- ECharts
- Axios
- Vite

已实现页面：

- 首页仪表盘
- 测试执行
- 执行历史
- 执行详情

核心能力：

- 调用 `GET /test-runs` 展示执行历史
- 调用 `GET /test-runs/{id}` 展示执行详情
- 调用 `POST /test-runs` 触发测试执行
- 展示总执行次数、通过次数、失败次数和通过率
- 用 ECharts 展示 suite 执行分布
- 展示 stdout / stderr，便于定位失败原因

前端启动：

```powershell
cd E:\jpetstore-test
.\run_frontend.cmd
```

访问地址：

```text
http://127.0.0.1:5173
```

## 4. 简历亮点

可描述为：

基于 JPetStore 电商系统搭建自动化测试平台，使用 Python + pytest + Playwright 实现 UI 自动化测试，集成 Allure 生成可视化测试报告，并通过 FastAPI + SQLite 封装测试任务执行与历史记录能力，使用 Vue 3 + Element Plus 实现测试执行、历史查询、详情查看和质量数据可视化页面。
