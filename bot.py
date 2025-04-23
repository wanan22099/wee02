import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, CallbackContext
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: CallbackContext) -> None:
    try:
        keyboard = [
            [
                InlineKeyboardButton("🎮 Open Mini App", web_app=WebAppInfo(url="https://wealth1254.cc/#/")),
                InlineKeyboardButton("👥 Join Group", url="https://t.me/+eWZl9--S-cUwZDM0")
            ],
            [
                InlineKeyboardButton("📢 Join Channel", url="https://t.me/+eWZl9--S-cUwZDM0"),
                InlineKeyboardButton("📞 Contact Support", url="https://t.me/WedlthCode")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "🚀 Welcome! Choose an option:",
            reply_markup=reply_markup
        )
    except Exception as e:
        logger.error(f"Error in start command: {e}")
        await update.message.reply_text("❌ An error occurred. Please try again.")

def main() -> None:
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()

if __name__ == "__main__":
    main()
