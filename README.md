# Telegram Zip/Unzip Bot

A bot for zipping/unzipping files (with optional password), including forwarded files, and auto-cleanup after 2 hours.

## 🛠️ Deployment (Mobile-friendly)

1. Fork this repo to your GitHub account (tap **Fork** on GitHub mobile).
2. Visit [render.com](https://render.com) and sign up.
3. Create a **New Web Service** → Connect your GitHub → Select your fork.
4. Set build/start commands:
   - Build: `pip install -r requirements.txt`
   - Start: `python main.py`
5. Set the environment variable `BOT_TOKEN` with your Telegram bot token.
6. Deploy! Wait till status says **Live**.

Now you can message your bot for file zipping/unzipping in Telegram.

---

## 📝 Features

- Zip/unzip files and forwarded files
- Optional password protect archives
- Auto deletes uploaded/unzipped files after 2 hours
