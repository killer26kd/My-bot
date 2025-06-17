import os
import zipfile
import pyminizip
import asyncio
import glob
import time
from pathlib import Path
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (ApplicationBuilder, CommandHandler,
                          MessageHandler, filters,
                          CallbackQueryHandler, ContextTypes)

TOKEN = os.environ.get("BOT_TOKEN")
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)
CLEANUP_AFTER = 2 * 60 * 60  # 2 hours in seconds

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📦 Send or forward a file to zip/unzip (password supported).")

async def cleanup_loop():
    while True:
        now = time.time()
        for filepath in glob.glob(str(UPLOAD_DIR / "*")):
            if os.path.getmtime(filepath) + CLEANUP_AFTER < now:
                try:
                    os.remove(filepath)
                except:
                    pass
        await asyncio.sleep(60 * 10)  # check every 10 minutes

async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    file_obj = msg.document or msg.audio or msg.video or msg.voice

    if not file_obj:
        await msg.reply_text("❌ Unsupported file type.")
        return

    fname = file_obj.file_name or "file"
    fpath = UPLOAD_DIR / fname
    await file_obj.get_file().download_to_drive(str(fpath))
    context.user_data["file_path"] = str(fpath)

    if fname.lower().endswith(".zip"):
        buttons = [
            [InlineKeyboardButton("🔓 Unzip (no password)", callback_data='unzip_nopass')],
            [InlineKeyboardButton("🔐 Unzip (with password)", callback_data='unzip_pass')]
        ]
    else:
        buttons = [
            [InlineKeyboardButton("📦 Zip (no password)", callback_data='zip_nopass')],
            [InlineKeyboardButton("🔐 Zip (with password)", callback_data='zip_pass')]
        ]
    await msg.reply_text("Choose an option:", reply_markup=InlineKeyboardMarkup(buttons))

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    context.user_data["action"] = q.data
    if "pass" in q.data:
        await q.edit_message_text("🔑 Send the password now.")
    else:
        await perform(update, context, None)

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    action = context.user_data.get("action")
    if action and "pass" in action:
        await perform(update, context, update.message.text.strip())

async def perform(update: Update, context: ContextTypes.DEFAULT_TYPE, password):
    ufile = context.user_data.get("file_path")
    action = context.user_data.get("action")
    msg = update.callback_query or update.message

    if not ufile or not action:
        await msg.reply_text("⚠️ No file or action found.")
        return

    if action.startswith("zip"):
        output = ufile + ".zip"
        if password:
            pyminizip.compress(ufile, None, output, password, 5)
        else:
            with zipfile.ZipFile(output, 'w') as zf:
                zf.write(ufile, arcname=os.path.basename(ufile))
        await msg.reply_document(open(output, "rb"))
    else:
        dest = UPLOAD_DIR / "unzipped"
        dest.mkdir(exist_ok=True)
        try:
            with zipfile.ZipFile(ufile) as zf:
                if password:
                    zf.extractall(dest, pwd=password.encode('utf-8'))
                else:
                    zf.extractall(dest)
            for file in dest.iterdir():
                await msg.reply_document(open(file, "rb"))
        except Exception as e:
            await msg.reply_text(f"❌ Error: {e}")

    context.user_data.clear()

# Bot application setup
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.Document.ALL | filters.Audio.ALL | filters.Video.ALL | filters.Voice.ALL, handle_file))
app.add_handler(CallbackQueryHandler(button_handler))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), text_handler))
# Start cleanup background task once built
app.post_init(lambda app: asyncio.create_task(cleanup_loop()))

if __name__ == "__main__":
    app.run_polling()
