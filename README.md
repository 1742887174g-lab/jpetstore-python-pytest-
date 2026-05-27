# JPetStore Automated Test Platform

这是一个面向 JPetStore 的自动化测试平台项目，第一版采用：

- Python + pytest 作为自动化测试框架
- Allure 作为测试报告
- Playwright 作为 Web UI 自动化驱动
- requests 作为 HTTP/API 健康检查能力
- FastAPI 作为测试平台后端雏形

## Project Layout

```text
jpetstore-test
├── automation       # pytest + allure 自动化测试工程
├── backend          # 测试平台后端，负责触发测试和记录结果
└── docs             # 项目设计文档
```

## Automation Scope

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

## Quick Start

### 运行测试平台后端

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

### 执行自动化测试

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

### 查看 Allure 报告

```powershell
cd E:\jpetstore-test
.\run_allure_report.cmd
```

## Development Setup

安装自动化测试依赖：

```powershell
cd automation
python -m pip install -r requirements.txt
python -m playwright install chromium
```

修改 `automation/config/settings.yaml` 中的 `base_url`，指向你的 JPetStore 地址。

执行测试：

```powershell
cd automation
python run_tests.py --suite smoke
```

生成并打开 Allure 报告：

```powershell
allure serve reports/allure-results
```

启动平台后端：

```powershell
cd backend
python -m pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## MVP Scope

第一阶段目标是打通完整闭环：

```text
配置被测环境 -> 执行 pytest 测试 -> 生成 Allure 结果 -> 后端记录执行结果
```
