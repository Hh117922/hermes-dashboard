# Hermes Dashboard

> 一个零 Token 消耗的本地实时看板，监控 Hermes AI Agent 的运行状态。

![Dark Theme](https://img.shields.io/badge/Theme-Dark-0f1117) ![Python](https://img.shields.io/badge/Python-3.8+-blue) ![Zero Deps](https://img.shields.io/badge/Dependencies-0-green)

## ✨ 功能

- 🤖 **当前模型** — 实时显示正在使用的 LLM 模型和 Provider
- 📊 **Token 仪表盘** — 输入/输出/总计 Token，累计调用次数
- ⚡ **性能监控** — 最新延迟、缓存命中率
- 🔧 **工具调用流** — 最近 20 条工具调用记录（名称、耗时、输出大小）
- 📡 **API 调用流** — 最近 20 次 API 调用详情

## 🎯 核心特点

| 特点 | 说明 |
|------|------|
| **零 Token 消耗** | 纯读取本地日志文件，不调用任何 API |
| **零外部依赖** | 只用 Python 标准库，无需 pip install |
| **实时刷新** | 每 2 秒自动拉取最新数据 |
| **极简部署** | 一个 Python 脚本 + 一个 HTML 文件 |

## 🚀 快速开始

### 1. 启动后端

```bash
python3 dashboard_server.py
```

启动后终端显示：`Dashboard server: http://localhost:8090`

### 2. 打开看板

在浏览器中访问：**http://localhost:8090**

或者双击打开 `hermes-dashboard.html` 文件（需配合后端服务器）。

### 3. 开机自启（可选）

```bash
# macOS 后台运行
nohup python3 ~/hermes-dashboard/dashboard_server.py > /dev/null 2>&1 &
```

## 📁 文件说明

```
hermes-dashboard/
├── dashboard_server.py    # 后端服务器（解析 agent.log，提供 JSON API）
├── hermes-dashboard.html  # 前端看板页面（深色主题，自动刷新）
└── README.md              # 本文件
```

## 🔧 工作原理

```
agent.log → Python 解析 → JSON API (:8090) → 浏览器 fetch → 看板渲染
                           ↑ 每 2 秒轮询
```

数据来源：`~/.hermes/logs/agent.log`（Hermes Agent 自动写入的结构化日志）

## 📋 系统要求

- Python 3.8+
- Hermes AI Agent（已安装并运行）
- 任何现代浏览器

## 📜 许可证

MIT License
