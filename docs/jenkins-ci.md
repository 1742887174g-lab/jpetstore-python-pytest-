# Jenkins CI 集成说明

本项目已提供 `Jenkinsfile`，用于在 Jenkins 中执行自动化测试并归档 Allure 原始结果。

## 前置条件

Jenkins Agent 需要具备：

- Windows 环境
- Python 3.11+
- Git
- 能访问 JPetStore 被测地址
- 可选：Allure Jenkins Plugin

如果要运行 `ui` / `smoke` / `regression`，还需要浏览器环境。当前项目使用 Playwright，首次运行前可在 Agent 上执行：

```powershell
python -m pip install playwright==1.49.1
python -m playwright install chromium
```

## Jenkins Pipeline 参数

`Jenkinsfile` 提供两个参数：

- `TEST_SUITE`: `api` / `smoke` / `regression` / `ui` / `all`
- `BASE_URL`: JPetStore 被测地址，默认 `http://localhost:8080/jpetstore`

## Pipeline 流程

```text
拉取代码
创建 Python 虚拟环境
安装 automation 依赖
执行 pytest
生成 Allure raw results
归档测试结果
```

执行命令核心为：

```powershell
cd automation
..\.venv\Scripts\python.exe run_tests.py --suite %TEST_SUITE% --base-url %BASE_URL% --allure-results-dir reports\ci\allure-results
```

## Allure 报告

如果 Jenkins 安装了 Allure Jenkins Plugin，流水线会调用 `allure` step 展示报告。

如果没有安装插件，流水线仍会归档：

```text
automation/reports/ci/allure-results/**
```

后续可以手动下载这些结果并生成报告：

```powershell
allure generate automation\reports\ci\allure-results -o allure-report --clean
```
