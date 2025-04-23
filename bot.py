import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, CallbackContext
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
WEB_APP_URL = "https://wealth1254.cc/#/"  # ← 必须替换为真实 URL

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: CallbackContext) -> None:
    try:
        keyboard = [
            [
                InlineKeyboardButton("🎮 Open Mini App", web_app=WebAppInfo(url=WEB_APP_URL)),
                InlineKeyboardButton("👥 Join Group", url="https://t.me/+eWZl9--S-cUwZDM0")
            ],
            [
                InlineKeyboardButton("📢 Join Channel", url="https://t.me/+eWZl9--S-cUwZDM0"),
                InlineKeyboardButton("📞 Contact Support", url="https://t.me/WedlthCode")
            ]
        ]
        await update.message.reply_text(
            "🚀 Welcome! Choose an option:",
            reply_markup=InlineKeyboardMarkup(keyboard)
    except Exception as e:
        logging.error(f"Error: {e}")
        await update.message.reply_text("❌ Failed to load options. Please try later.")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()

if __name__ == "__main__":
    main()
