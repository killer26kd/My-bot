import os
import logging
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import subprocess
import uuid

TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

# Create "temp" folder if it doesn't exist
os.makedirs("temp", exist_ok=True)

async def compress_video(input_path, output_path):
    cmd = [
        "ffmpeg",
        "-i", input_path,
        "-vcodec", "libx264",
        "-crf", "28",
        output_path
    ]
    try:
        subprocess.run(cmd, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

async def delete_file_later(file_path, delay=600):
    await asyncio.sleep(delay)
    try:
        os.remove(file_path)
    except:
        pass

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    video = update.message.video or update.message.document
    if not video:
        await update.message.reply_text("❌ Please send a valid video file.")
        return

    file_id = video.file_id
    file = await context.bot.get_file(file_id)

    unique_id = str(uuid.uuid4())
    input_path = f"temp/{unique_id}_input.mp4"
    output_path = f"temp/{unique_id}_compressed.mp4"

    await update.message.reply_text("📥 Downloading...")
    await file.download_to_drive(input_path)

    await update.message.reply_text("⚙️ Compressing video...")
    success = await compress_video(input_path, output_path)

    if success:
        await update.message.reply_video(video=open(output_path, "rb"), caption="✅ Compressed Video")
        await update.message.reply_text("🗑 This file will be deleted in 10 minutes.")
        asyncio.create_task(delete_file_later(input_path))
        asyncio.create_task(delete_file_later(output_path))
    else:
        await update.message.reply_text("❌ Failed to compress the video.")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.VIDEO | filters.Document.VIDEO, handle_video))

print("Bot is running...")
app.run_polling()
