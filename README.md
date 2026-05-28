# JPetStore 自动化测试平台

这是一个面向 JPetStore 的自动化测试平台项目，当前使用：

- Python + pytest 作为自动化测试框架
- Playwright 作为 Web UI 自动化驱动
- requests 作为接口测试能力
- Allure 作为测试报告
- FastAPI 作为测试平台后端
- SQLite 保存测试执行历史
- Vue 3 + Element Plus 作为测试平台前端

## 项目结构

```text
jpetstore-test
├── automation       # pytest + allure 自动化测试工程
├── backend          # 测试平台后端，负责触发测试和记录结果
├── frontend         # Vue 3 测试平台前端
├── docs             # 项目设计文档
└── run_*.cmd        # 一键运行脚本
```

## 自动化覆盖范围

当前自动化框架已覆盖：

- API 健康检查
- Catalog 首页访问
- 商品搜索
- 商品详情
- 登录成功 / 登录失败 / 退出登录
- 用户注册
- 购物车添加、修改数量、删除商品
- 默认用户提交订单

测试分组：

- `api`: 接口/HTTP 层检查
- `ui`: Web UI 自动化用例
- `smoke`: 核心冒烟测试
- `regression`: 回归测试，包含注册、下单等有业务副作用的流程
- `all`: 全量测试

## 运行测试平台后端

```powershell
cd E:\jpetstore-test
.\run_backend.cmd
```

启动成功后访问：

```text
http://127.0.0.1:8000/docs
```

在 Swagger 中调用 `POST /test-runs`，body 示例：

```json
{
  "suite": "smoke"
}
```

也可以指定环境或临时覆盖被测地址：

```json
{
  "suite": "smoke",
  "environment": "local",
  "base_url": "http://localhost:8080/jpetstore"
}
```

测试执行结束后，后端会把执行记录保存到 SQLite：

```text
backend/data/test_platform.db
```

查询执行历史：

```text
GET http://127.0.0.1:8000/test-runs
```

查询单次执行详情：

```text
GET http://127.0.0.1:8000/test-runs/{id}
```

## 运行测试平台前端

先启动后端：

```powershell
cd E:\jpetstore-test
.\run_backend.cmd
```

再打开一个新的 PowerShell 启动前端：

```powershell
cd E:\jpetstore-test
.\run_frontend.cmd
```

前端地址：

```text
http://127.0.0.1:5173
```

当前页面包括：

- 仪表盘：展示执行次数、通过率、Suite 分布和最近执行
- 执行测试：选择 suite 并触发测试
- 执行历史：查看历史记录
- 执行详情：查看命令、stdout、stderr 和 Allure 结果目录

## 执行自动化测试

API 测试：

```powershell
cd E:\jpetstore-test
.\run_api_tests.cmd
```

UI 测试：

```powershell
cd E:\jpetstore-test
.\run_ui_tests.cmd
```

冒烟测试：

```powershell
cd E:\jpetstore-test
.\run_smoke_tests.cmd
```

回归测试：

```powershell
cd E:\jpetstore-test
.\run_regression_tests.cmd
```

查看 Allure 报告：

```powershell
cd E:\jpetstore-test
.\run_allure_report.cmd
```

## Jenkins CI

项目已提供 Jenkins Pipeline：

```text
Jenkinsfile
```

Jenkins 可通过参数选择执行：

- `api`
- `smoke`
- `ui`
- `regression`
- `all`

详细说明见：

```text
docs/jenkins-ci.md
```

## 开发环境

安装自动化测试依赖：

```powershell
cd E:\jpetstore-test
.\.venv\Scripts\python.exe -m pip install -r automation\requirements.txt
```

安装后端依赖：

```powershell
cd E:\jpetstore-test
.\.venv\Scripts\python.exe -m pip install -r backend\requirements.txt
```

安装前端依赖：

```powershell
cd E:\jpetstore-test\frontend
npm install
```

修改 JPetStore 地址：

```text
automation/config/settings.yaml
```

或执行时临时覆盖：

```powershell
cd E:\jpetstore-test\automation
..\.venv\Scripts\python.exe run_tests.py --suite smoke --base-url http://localhost:8080/jpetstore
```
