import os
import logging
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from dotenv import load_dotenv

# 初始化设置
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
    "📞 联系客服": {"type": "url", "data": "https://t.me/WedlthCode"}
}

def create_main_menu():
    """生成主菜单键盘"""
    return ReplyKeyboardMarkup(
        [
            ["🎮 开始游戏", "👥 加入群组"],
            ["📢 加入频道", "📞 联系客服"]
        ],
        resize_keyboard=True,
        persistent=True  # 保持菜单长期显示
    )

async def start(update: Update, context: CallbackContext) -> None:
    """固定菜单入口"""
    await update.message.reply_text(
        "请选择功能：",
        reply_markup=create_main_menu()
    )

async def handle_message(update: Update, context: CallbackContext) -> None:
    """处理所有消息（保持菜单显示）"""
    text = update.message.text
    
    if text in BUTTONS:
        btn = BUTTONS[text]
        
        if btn["type"] == "web_app":
            # WebApp按钮+返回主菜单
            await update.message.reply_text(
                "游戏加载中...",
                reply_markup=ReplyKeyboardMarkup(
                    [
                        [KeyboardButton("🕹️ 直接打开", web_app=WebAppInfo(url=btn["data"]))],
                        ["🔙 返回主菜单"]
                    ],
                    resize_keyboard=True
                )
            )
        elif btn["type"] == "url":
            # 链接跳转提示（保持菜单）
            await update.message.reply_text(
                f"请访问：{btn['data']}",
                reply_markup=create_main_menu(),
                disable_web_page_preview=True
            )
    else:
        # 非按钮文字消息也保持菜单
        await update.message.reply_text(
            "请使用下方菜单操作",
            reply_markup=create_main_menu()
        )

def main():
    app = Application.builder().token(TOKEN).build()
    
    # 注册处理器
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # 启动Bot
    logger.info("Bot已启动（菜单固定模式）")
    app.run_polling()

if __name__ == "__main__":
    main()
