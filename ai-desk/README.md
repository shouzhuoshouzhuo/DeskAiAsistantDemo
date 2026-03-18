# 🚀 AI-Desk

> A lightweight desktop AI assistant with SQL & Linux command generation.

## ✨ Features

* 🧠 Chat with AI (general purpose)
* 💾 Natural language → SQL
* 🖥 Natural language → Linux commands
* ⚡ Global shortcut to open (Ctrl + Space)
* 🎯 Minimal & clean UI (PyQt)

## ✨ Preview

(放截图)

## 🚀 Getting Started

```bash
pip install -r requirements.txt
python main.py
```

## 🧠 Example

### SQL Mode

Input:

> Get orders from last 7 days

Output:

```sql
SELECT * FROM orders WHERE create_time >= NOW() - INTERVAL 7 DAY;
```

### Linux Mode

Input:

> Show processes using most CPU

Output:

```bash
top -o %CPU
```

## 🔧 Tech Stack

* Python
* PyQt5
* AI API (Claude / OpenAI)

## 📌 Roadmap

* [ ] Multi-model support (Claude + GPT)
* [ ] Plugin system
* [ ] Context-aware mode detection
* [ ] History & favorites

## ⭐ Star this repo if you like it!
