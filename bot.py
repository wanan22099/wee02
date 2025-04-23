import os
import sys
import logging
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from telegram.error import Conflict
from dotenv import load_dotenv

# 初始化配置
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# 日志配置
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# 按钮配置
BUTTONS = {
    "🎮 开始游戏": {"type": "web_app", "data": "https://wealth1254.cc/#/"},
    "👥 加入群组": {"type": "url", "data": "https://t.me/your_group"},
    "📢 加入频道": {"type": "url", "data": "https://t.me/your_channel"},
    "📞 联系客服": {"type": "url", "data": "https://t.me/WedlthCode"},
    "🔙 返回主菜单": {"type": "command"}
}

def create_keyboard(buttons):
    """通用键盘生成器（兼容新旧版本）"""
    try:
        return ReplyKeyboardMarkup(
            buttons,
            resize_keyboard=True,
            persistent=True,  # 尝试使用新特性
            one_time_keyboard=False
        )
    except TypeError:
        return ReplyKeyboardMarkup(buttons, resize_keyboard=True)

async def start(update: Update, context: CallbackContext):
    """处理 /start 命令"""
    await update.message.reply_text(
        "请选择功能：",
        reply_markup=create_keyboard([
            ["🎮 开始游戏", "👥 加入群组"],
            ["📢 加入频道", "📞 联系客服"]
        ])
    )

async def handle_message(update: Update, context: CallbackContext):
    """处理所有消息"""
    text = update.message.text
    
    if text == "🔙 返回主菜单":
        await start(update, context)
        return
        
    if text in BUTTONS:
        btn = BUTTONS[text]
        if btn["type"] == "web_app":
            await update.message.reply_text(
                "游戏加载中...",
                reply_markup=create_keyboard([
                    [KeyboardButton("🕹️ 直接打开", web_app=WebAppInfo(url=btn["data"]))],
                    ["🔙 返回主菜单"]
                ])
            )
        elif btn["type"] == "url":
            await update.message.reply_text(
                f"请访问：{btn['data']}",
                reply_markup=create_keyboard([["🔙 返回主菜单"]])
            )

def main():
    app = Application.builder().token(TOKEN).build()
    
    # 注册处理器（确保start函数已定义）
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    try:
        logger.info("Bot启动成功")
        app.run_polling()
    except Conflict:
        logger.error("检测到冲突，正在恢复...")
        os.execl(sys.executable, sys.executable, *sys.argv)

if __name__ == "__main__":
    main()
