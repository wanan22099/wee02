import os
import logging
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, CallbackContext
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# 配置日志
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: CallbackContext) -> None:
    try:
        keyboard = [
            [
                KeyboardButton("🎮 Open Mini App", web_app=WebAppInfo(url="https://your-mini-app-url")),
                KeyboardButton("👥 Join Group", url="https://t.me/your_group")
            ],
            [
                KeyboardButton("📢 Join Channel", url="https://t.me/your_channel"),
                KeyboardButton("📞 Contact Support", url="https://t.me/your_contact")
            ]
        ]
        reply_markup = ReplyKeyboardMarkup(
            keyboard, 
            resize_keyboard=True,
            persistent=True,
            input_field_placeholder="Select an option below👇"
        )
        await update.message.reply_text(
            "🚀 Welcome! Choose an option:",
            reply_markup=reply_markup
        )
    except Exception as e:
        logger.error(f"Error in start command: {e}")
        await update.message.reply_text("❌ An error occurred. Please try again.")

async def error_handler(update: Update, context: CallbackContext) -> None:
    logger.error(f"Update {update} caused error {context.error}")

def main() -> None:
    if not TOKEN:
        raise ValueError("BOT_TOKEN environment variable not set!")

    app = Application.builder().token(TOKEN).build()
    
    # 注册处理器
    app.add_handler(CommandHandler("start", start))
    
    # 错误处理
    app.add_error_handler(error_handler)
    
    # 启动Bot
    logger.info("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.critical(f"Bot crashed: {e}")
