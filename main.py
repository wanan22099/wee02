import logging
import os
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from telegram.inline.inline_keyboard_button import InlineKeyboardButton
from telegram.inline.inline_keyboard_markup import InlineKeyboardMarkup

# 配置日志记录
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    """
    处理 /start 命令，显示包含四个菜单按钮的消息
    """
    keyboard = [
        [
            InlineKeyboardButton("Telegram 内置小程序", url="https://t.me/addstickers/ExampleStickers"),
            InlineKeyboardButton("Telegram 群组", url="https://t.me/ExampleGroup")
        ],
        [
            InlineKeyboardButton("Telegram 频道", url="https://t.me/ExampleChannel"),
            InlineKeyboardButton("Telegram 联系人", url="https://t.me/ExampleContact")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('请选择一个选项:', reply_markup=reply_markup)


def main() -> None:
    """
    主函数，启动 Bot 并设置 Webhook
    """
    # 从环境变量获取 Bot 令牌
    bot_token = os.getenv('BOT_TOKEN')
    if not bot_token:
        raise ValueError("BOT_TOKEN 环境变量未设置")

    bot = Bot(token=bot_token)
    updater = Updater(bot=bot)

    # 获取调度器以注册处理程序
    dispatcher = updater.dispatcher

    # 注册命令处理程序
    dispatcher.add_handler(CommandHandler("start", start))

    # 启动 Bot
    port = int(os.environ.get('PORT', 8443))
    railway_app_url = os.getenv('RAILWAY_APP_URL')
    if not railway_app_url:
        raise ValueError("RAILWAY_APP_URL 环境变量未设置")

    updater.start_webhook(
        listen="0.0.0.0",
        port=port,
        url_path=bot_token,
        webhook_url=f'{railway_app_url}/{bot_token}'
    )

    # 运行 Bot，直到你使用 Ctrl - C 或进程收到 SIGINT、SIGTERM 或 SIGABRT 信号
    updater.idle()


if __name__ == '__main__':
    main()
    
