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
    bot_token = os.getenv('BOT_TOKEN')
    if not bot_token:
        raise ValueError("BOT_TOKEN 环境变量未设置")

    updater = Updater(token=bot_token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))

    # 使用轮询模式
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
