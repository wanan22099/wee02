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

# 按钮配置（替换为你的实际链接）
BUTTONS = {
    "🎮 开始游戏": {"type": "web_app", "data": "https://wealth1254.cc/#/"},  # 内置小程序
    "👥 加入群组": {"type": "url", "data": "https://t.me/+eWZl9--S-cUwZDM0"},       # 群组
    "📢 加入频道": {"type": "url", "data": "https://t.me/+eWZl9--S-cUwZDM0"},    # 频道
    "📞 联系客服": {"type": "url", "data": "https://t.me/WedlthCode"}     # 联系人
}

async def start(update: Update, context: CallbackContext) -> None:
    """发送带固定菜单的欢迎消息"""
    try:
        # 创建两行按钮（每行两个）
        keyboard = [
            [KeyboardButton("🎮 开始游戏"), KeyboardButton("👥 加入群组")],
            [KeyboardButton("📢 加入频道"), KeyboardButton("📞 联系客服")]
        ]
        reply_markup = ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True,
            persistent=True,
            input_field_placeholder="点击下方按钮操作👇"
        )
        await update.message.reply_text(
            "欢迎使用！请选择功能：",
            reply_markup=reply_markup
        )
    except Exception as e:
        logger.error(f"启动命令错误: {e}")

async def handle_button_click(update: Update, context: CallbackContext) -> None:
    """处理按钮点击事件"""
    text = update.message.text
    if text in BUTTONS:
        btn = BUTTONS[text]
        if btn["type"] == "web_app":
            # 打开内置小程序
            await update.message.reply_text(
                "正在加载游戏...",
                reply_markup=ReplyKeyboardMarkup.from_button(
                    KeyboardButton(
                        "点此直接打开",
                        web_app=WebAppInfo(url=btn["data"])
                ))
        elif btn["type"] == "url":
            # 发送跳转链接
            await update.message.reply_text(
                f"点击链接跳转：{btn['data']}",
                disable_web_page_preview=True
            )
    else:
        await update.message.reply_text("未知命令，请点击菜单按钮。")

def main() -> None:
    # 创建Bot实例
    app = Application.builder().token(TOKEN).build()
    
    # 注册处理器
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_button_click))
    
    # 启动Bot
    logger.info("Bot已启动，使用 /start 测试")
    app.run_polling()

if __name__ == "__main__":
    main()
