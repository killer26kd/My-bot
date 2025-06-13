# 📦 Telegram Video Compressor Bot

A simple Telegram bot that compresses video files (including forwarded videos) and sends back the compressed version.

---

## 💡 Features

- ✅ Compresses uploaded and forwarded video files
- ✅ Uses `ffmpeg` for efficient compression
- ✅ Deletes input/output files after 10 minutes to save space
- ✅ 24/7 cloud-hosted using Railway
- ✅ Works entirely on mobile (no Termux or Replit needed)

---

## ⚙️ How It Works

1. User sends or forwards a video to the bot
2. Bot downloads and compresses the video
3. Compressed video is sent back to the user
4. Temporary files are deleted automatically after 10 minutes

---

## 🚀 Deployment

You need:

- A [Telegram Bot Token](https://t.me/BotFather)
- A [GitHub Account](https://github.com)
- A [Railway Account](https://railway.app)

### 1. Upload files to GitHub

Required files:
- `main.py`
- `requirements.txt`

Optional:
- `README.md`

### 2. Deploy to Railway

- Go to [https://railway.app](https://railway.app)
- Click **New Project → Deploy from GitHub**
- Connect your repo
- Add `BOT_TOKEN` as a **variable**
- Railway will install dependencies and start the bot

---

## 🧪 Tech Stack

- Python
- ffmpeg
- python-telegram-bot

---

## 🤖 Created With Help From ChatGPT