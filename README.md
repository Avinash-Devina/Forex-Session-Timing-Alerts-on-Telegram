

# 📈 Forex Market Open Alerts (IST → Telegram)

A lightweight Python automation that sends **Telegram notifications** when major **Forex markets open**, based on **Indian Standard Time (IST)**.

Runs **100% serverless** using **GitHub Actions** — no VPS, no cloud setup, no cost.

---

## 🚀 Features

- 🔔 Telegram alerts for market **OPEN times**
- ⏰ IST-based scheduling
- 🤖 Runs automatically via GitHub Actions
- 🆓 Completely free (uses GitHub’s runner)
- 🛠 Simple & customizable

---

## 🌍 Forex Market Sessions (IST)

| Market | Open | Close |
|------|------|------|
| Sydney | 01:30 AM | 10:30 AM |
| Tokyo | 05:30 AM | 02:30 PM |
| London | 01:30 PM | 10:30 PM |
| New York | 06:30 PM | 03:30 AM (next day) |

> ⚠️ Note: London & New York session times may change during Daylight Saving Time (DST).

---

## 🧰 Tech Stack

- Python 3.11
- GitHub Actions (cron scheduler)
- Telegram Bot API

---

## 📦 Setup Guide

### 1️⃣ Create Telegram Bot
- Open Telegram → search **@BotFather**
- Run `/newbot`
- Save your **BOT TOKEN**

Get your chat ID using **@userinfobot**

---

### 2️⃣ Clone Repository
```bash
git clone https://github.com/your-username/forex-telegram-alerts.git
cd forex-telegram-alerts