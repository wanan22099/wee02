import os
import logging
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# 配置日志
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# 按钮配置
BUTTONS = {
    "🎮 开始游戏": {"type": "web_app", "data": "https://wealth1254.cc/#/"},
    "👥 加入群组": {"type": "url", "data": "https://+eWZl9--S-cUwZDM0"},
    "📢 加入频道": {"type": "url", "data": "https://+eWZl9--S-cUwZDM0"},
    "📞 联系客服": {"type": "url", "data": "https://t.me/WedlthCode"},
    "🔙 返回主菜单": {"type": "command", "data": "/start"}  # 新增返回按钮
}

async def start(update: Update, context: CallbackContext) -> None:
    try:
        keyboard = [
            [KeyboardButton("🎮 开始游戏"), KeyboardButton("👥 加入群组")],
            [KeyboardButton("📢 加入频道"), KeyboardButton("📞 联系客服")]
        ]
        reply_markup = ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True,
            one_time_keyboard=False,
            selective=False
        )
        await update.message.reply_text(
            "欢迎使用！请选择功能：",
            reply_markup=reply_markup
        )
    except Exception as e:
        logger.error(f"错误：{e}")

async def handle_button_click(update: Update, context: CallbackContext) -> None:
    text = update.message.text
    if text in BUTTONS:
        btn = BUTTONS[text]
        if btn["type"] == "web_app":
            # 创建带返回按钮的键盘
            return_keyboard = ReplyKeyboardMarkup(
                [[KeyboardButton("🔙 返回主菜单")]],
                resize_keyboard=True
            )
            
            # 先发送返回按钮
            await update.message.reply_text(
                "您正在游戏中...",
                reply_markup=return_keyboard
            )
            
            # 再发送Web App按钮
            await update.message.reply_text(
                "点此直接打开游戏：",
                reply_markup=ReplyKeyboardMarkup.from_button(
                    KeyboardButton(
                        "打开游戏",
                        web_app=WebAppInfo(url=btn["data"])
                    )
                )
        elif btn["type"] == "url":
            # 发送带返回按钮的链接消息
            return_keyboard = ReplyKeyboardMarkup(
                [[KeyboardButton("🔙 返回主菜单")]],
                resize_keyboard=True
            )
            await update.message.reply_text(
                f"点击链接跳转：{btn['data']}",
                reply_markup=return_keyboard,
                disable_web_page_preview=True
            )
        elif btn["type"] == "command":
            # 处理返回主菜单命令
            await start(update, context)
    else:
        await update.message.reply_text("未知命令，请点击菜单按钮。")

def main() -> None:
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_button_click))
    logger.info("Bot已启动，使用 /start 测试")
    app.run_polling()

if __name__ == "__main__":
    main()
