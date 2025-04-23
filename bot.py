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
    "👥 加入群组": {"type": "url", "data": "https://t.me/+eWZl9--S-cUwZDM0"},  # 替换为真实群组链接
    "📢 加入频道": {"type": "url", "data": "https://t.me/+eWZl9--S-cUwZDM0"},  # 替换为真实频道链接
    "📞 联系客服": {"type": "url", "data": "https://t.me/WedlthCode"},
    "🔙 返回主菜单": {"type": "command", "data": "/start"}
}

async def start(update: Update, context: CallbackContext) -> None:
    """发送主菜单"""
    try:
        keyboard = [
            [KeyboardButton("🎮 开始游戏"), KeyboardButton("👥 加入群组")],
            [KeyboardButton("📢 加入频道"), KeyboardButton("📞 联系客服")]
        ]
        reply_markup = ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True,
            one_time_keyboard=False
        )
        await update.message.reply_text(
            "欢迎使用！请选择功能：",
            reply_markup=reply_markup
        )
    except Exception as e:
        logger.error(f"主菜单错误: {e}")

async def handle_button_click(update: Update, context: CallbackContext) -> None:
    """处理所有按钮点击"""
    text = update.message.text
    if text not in BUTTONS:
        await update.message.reply_text("请使用下方菜单按钮操作")
        return

    btn = BUTTONS[text]
    
    if btn["type"] == "web_app":
        # 游戏页面：同时显示Web App按钮和返回按钮
        keyboard = [
            [KeyboardButton("🕹️ 点此打开游戏", web_app=WebAppInfo(url=btn["data"]))],
            [KeyboardButton("🔙 返回主菜单")]
        ]
        await update.message.reply_text(
            "游戏加载提示：\n\n1. 点击下方按钮进入游戏\n2. 完成后点击返回",
            reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        )

    elif btn["type"] == "url":
        # 链接跳转页面：只显示返回按钮
        await update.message.reply_text(
            f"请点击链接：{btn['data']}\n\n完成后按返回键",
            reply_markup=ReplyKeyboardMarkup([[KeyboardButton("🔙 返回主菜单")]], resize_keyboard=True),
            disable_web_page_preview=True
        )

    elif btn["type"] == "command":
        await start(update, context)  # 处理返回命令

def main() -> None:
    app = Application.builder().token(TOKEN).build()
    
    # 注册处理器
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_button_click))
    
    # 启动Bot
    logger.info("Bot启动成功")
    app.run_polling()

if __name__ == "__main__":
    main()
