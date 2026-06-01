# Hermes Dashboard

> 一个零 Token 消耗的本地实时看板，监控 Hermes AI Agent 的运行状态。

![Dark Theme](https://img.shields.io/badge/Theme-Dark-AI_Generated) ![Python](https://img.shields.io/badge/Python-3.8+-blue) ![Zero Deps](https://img.shields.io/badge/Dependencies-0-green)

## ✨ 功能

- 🤖 **当前模型** — 实时显示正在使用的 LLM 模型和 Provider
- 📊 **Token 仪表盘** — 输入 / 输出 / 总计 Token，累计调用次数
- ⚡ **性能监控** — 最新延迟、缓存命中率
- 🟢🟡🔴 **三色状态灯** — 绿色在线、黄色数据延迟、红色断连
- 🔧 **工具调用流** — 最近 20 条工具调用记录
- 📡 **API 调用流** — 最近 20 次 API 调用详情
- 🎨 **毛玻璃深色主题** — AI 生成的背景图 + backdrop-filter 毛玻璃卡片
- 🖱️ **平滑视差** — 鼠标移动时背景微动

## 🎯 核心特点

| 特点 | 说明 |
|------|------|
| **零 Token 消耗** | 纯读取本地日志文件，不调用任何 API |
| **零外部依赖** | 只用 Python 标准库，无需 pip install |
| **实时刷新** | 每 2 秒自动拉取最新数据 |
| **Apple 风格设计** | 毛玻璃卡片 + 深色氛围 + 克制动效 |
| **三色健康灯** | 绿 / 黄 / 红 一眼判断看板运行状态 |

## 🚀 快速开始

### 1. 启动后端

```bash
python3 dashboard_server.py
```

启动后终端显示：`Dashboard server: http://localhost:8090`

### 2. 打开看板

浏览器访问：**http://localhost:8090**

### 3. 开机自启（可选）

```bash
nohup python3 ~/hermes-dashboard/dashboard_server.py > /dev/null 2>&1 &
```

## 📁 文件说明

```
hermes-dashboard/
├── dashboard_server.py        # 后端服务器（解析 agent.log，提供 JSON API）
├── hermes-dashboard-v3.html   # 前端看板（毛玻璃深色主题 + 三色状态灯 + 视差）
├── hermes-dashboard-bg.jpg    # AI 生成的深色氛围背景图
└── README.md                  # 本文件
```

## 🔧 工作原理

```
agent.log → Python 解析 → JSON API (:8090) → 浏览器 fetch → 看板渲染
                           ↑ 每 2 秒轮询
```

数据来源：`~/.hermes/logs/agent.log`（Hermes Agent 自动写入的结构化日志）

## 🟢🟡🔴 状态灯说明

| 颜色 | 状态 | 含义 |
|------|------|------|
| 🟢 绿色闪烁 | online | 正常，数据每 2 秒刷新 |
| 🟡 黄色慢闪 | stale | 超过 10 秒无新数据，后端可能卡顿 |
| 🔴 红色常亮 | error | 超过 30 秒无响应，后端挂了或断网 |

## 📋 系统要求

- Python 3.8+
- Hermes AI Agent（已安装并运行）
- 任何现代浏览器

## 📜 许可证

MIT License
