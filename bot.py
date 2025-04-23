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

# 按钮配置（统一管理，避免硬编码）
BUTTONS = {
    "🎮 开始游戏": {"type": "web_app", "data": "https://wealth1254.cc/#/"},
    "👥 加入群组": {"type": "url", "data": "https://t.me/your_group"},
    "📢 加入频道": {"type": "url", "data": "https://t.me/your_channel"},
    "📞 联系客服": {"type": "url", "data": "https://t.me/WedlthCode"},
    "🔙 返回主菜单": {"type": "menu", "data": None}  # ✅ 新增返回按钮
}

def create_main_menu():
    """生成主菜单键盘（强制显示，禁用单次键盘）"""
    return ReplyKeyboardMarkup(
        [
            ["🎮 开始游戏", "👥 加入群组"],
            ["📢 加入频道", "📞 联系客服"]
        ],
        resize_keyboard=True,
        persistent=True,  # ✅ 保持菜单在回复时重复显示
        one_time_keyboard=False  # ✅ 明确禁用“单次键盘”（默认 False，但显式声明更清晰）
    )

def create_webapp_keyboard():
    """生成 WebApp 专用键盘（包含返回主菜单按钮）"""
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton("🕹️ 直接打开", web_app=WebAppInfo(url=BUTTONS["🎮 开始游戏"]["data"]))],
            [KeyboardButton(BUTTONS["🔙 返回主菜单"]["data"])]  # ✅ 使用统一的按钮文本
        ],
        resize_keyboard=True,
        persistent=True,
        one_time_keyboard=False
    )

async def start(update: Update, context: CallbackContext) -> None:
    """固定菜单入口（首次显示主菜单）"""
    await update.message.reply_text(
        "请选择功能：",
        reply_markup=create_main_menu()
    )

async def handle_message(update: Update, context: CallbackContext) -> None:
    """处理所有消息（确保每次回复都携带菜单）"""
    text = update.message.text
    
    if text in BUTTONS:
        btn = BUTTONS[text]
        
        if btn["type"] == "web_app":
            # WebApp 流程：显示 WebApp 按钮 + 返回菜单（保持菜单状态）
            await update.message.reply_text(
                "游戏加载中...",
                reply_markup=create_webapp_keyboard()  # ✅ 专用键盘，含返回按钮
            )
        elif btn["type"] == "url":
            # 链接跳转提示（回复后强制显示主菜单）
            await update.message.reply_text(
                f"请访问：{btn['data']}",
                reply_markup=create_main_menu()  # ✅ 每次回复都重新生成主菜单
            )
        elif btn["type"] == "menu" and text == "🔙 返回主菜单":
            # 返回主菜单逻辑（显式处理返回按钮）
            await update.message.reply_text(
                "已返回主菜单",
                reply_markup=create_main_menu()
            )
    else:
        # 非按钮消息：提示并显示主菜单（防止菜单消失）
        await update.message.reply_text(
            "请使用下方菜单操作",
            reply_markup=create_main_menu()  # ✅ 强制显示菜单
        )

def main():
    app = Application.builder().token(TOKEN).build()
    
    # 注册处理器（确保所有消息类型都触发菜单更新）
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    logger.info("Bot已启动（强化版固定菜单模式）")
    app.run_polling()

if __name__ == "__main__":
    main()
