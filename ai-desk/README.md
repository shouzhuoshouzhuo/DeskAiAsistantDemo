<div align="center">

# 🤖 AI Desk

**一个住在你桌面上的 AI 伙伴**

`Ctrl+Space` 唤醒 · 对话 · SQL · Linux · 随时消失

[![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)](https://python.org)
[![PyQt5](https://img.shields.io/badge/PyQt5-5.15+-green?style=flat-square)](https://pypi.org/project/PyQt5/)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)
[![Stars](https://img.shields.io/github/stars/shouzhuoshouzhuo/DeskAiAsistantDemo?style=flat-square)](https://github.com/shouzhuoshouzhuo/DeskAiAsistantDemo/stargazers)

</div>

---

## ✨ 项目简介

AI Desk 是一个运行在 Windows 桌面的轻量 AI 助手。它常驻系统托盘，随叫随到，不打扰你的工作流。

不只是聊天——它还有一个会随着你们互动深度而进化的 AI 伙伴 **ido**，从陌生人到知己，主题色也会跟着悄悄变化。

---

## 🌟 功能亮点

| 功能 | 说明 |
|------|------|
| 💬 **Chat 模式** | 与 AI 伙伴 ido 自由对话，支持多轮上下文 |
| 🗄️ **SQL 模式** | 自然语言 → MySQL 语句，一键复制粘贴 |
| 🐧 **Linux 模式** | 自然语言 → Shell 命令，自动粘贴到终端 |
| 💖 **好感度系统** | 对话越多关系越深，陌生人→朋友→知己→恋人 |
| 🎨 **动态主题色** | 主题渐变色随好感度实时插值过渡（蓝→紫→粉） |
| ⌨️ **全局快捷键** | `Ctrl+Space` 随时唤出/隐藏，不影响当前窗口 |
| 📋 **Paste & Close** | SQL/Linux 结果一键复制并自动粘贴到前台应用 |
| 🧠 **记忆系统** | 记住你说过的话，下次对话自然提及 |
| 🕐 **久别问候** | 超过 24 小时未联系，ido 会主动表达想念 |

---

## 📸 预览

> *(截图放这里)*

---

## 🚀 安装步骤

### 1. 克隆项目

```bash
git clone https://github.com/shouzhuoshouzhuo/DeskAiAsistantDemo.git
cd DeskAiAsistantDemo/ai-desk
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置 API Key

复制 `.env.example` 为 `.env`，填入你的 API 信息：

```bash
cp .env.example .env
```

```env
API_KEY=your_api_key_here
MODEL=deepseek-v3.2
BASE_URL=https://your-api-endpoint/v1
```

> 支持任何兼容 OpenAI 格式的 API（DeepSeek、OpenAI、本地 Ollama 等）

### 4. 启动

```bash
python main.py
```

启动后程序静默运行在系统托盘，按 `Ctrl+Space` 唤出窗口。

---

## 📖 使用教程

### Chat 模式

直接输入任何内容与 ido 对话，支持多轮上下文。随着对话次数增加，ido 的语气和称呼会逐渐变化。

### SQL 模式

切换到 SQL 标签，用自然语言描述你的查询需求：

```
输入：查询最近 7 天的订单，按金额降序
输出：SELECT * FROM orders WHERE create_time >= NOW() - INTERVAL 7 DAY ORDER BY amount DESC;
```

点击 **Paste & Close** 自动粘贴到你的编辑器。

### Linux 模式

切换到 Linux 标签，描述你想执行的操作：

```
输入：找出占用 CPU 最高的进程
输出：ps aux --sort=-%cpu | head -10
```

点击 **Paste & Close** 自动粘贴并执行到终端。

---

## 🛠️ 技术栈

- **Python 3.10+**
- **PyQt5** — UI 框架，无边框透明窗口
- **OpenAI SDK** — 兼容多种 API 后端
- **python-dotenv** — 环境变量管理
- **keyboard / pyautogui / pyperclip** — 全局快捷键与自动粘贴

---

## 🔮 未来展望

- [ ] 支持更多 AI 模型切换（Claude、GPT-4o、本地 Ollama）
- [ ] 语音输入唤醒
- [ ] 插件系统，支持自定义 Prompt 模板
- [ ] 对话历史记录与收藏
- [ ] 多语言界面
- [ ] macOS / Linux 支持

---

## 🤝 贡献指南

欢迎任何形式的贡献！

1. Fork 本仓库
2. 创建你的分支 `git checkout -b feature/your-feature`
3. 提交改动 `git commit -m 'feat: add some feature'`
4. 推送分支 `git push origin feature/your-feature`
5. 发起 Pull Request

有 Bug 或建议？欢迎 [提交 Issue](https://github.com/shouzhuoshouzhuo/DeskAiAsistantDemo/issues)。

---

## ⭐ 支持项目

如果这个项目对你有帮助，请点一个 Star ⭐

它对我意义很大，也能让更多人发现这个项目。

[![Star History](https://img.shields.io/github/stars/shouzhuoshouzhuo/DeskAiAsistantDemo?style=social)](https://github.com/shouzhuoshouzhuo/DeskAiAsistantDemo/stargazers)

---

<div align="center">
Made with ❤️ by <a href="https://github.com/shouzhuoshouzhuo">shouzhuoshouzhuo</a>
</div>