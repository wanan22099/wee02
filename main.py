from telegram import ReplyKeyboardMarkup, KeyboardButton, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

TOKEN = "YOUR_BOT_TOKEN"

async def start(update: Update, context: CallbackContext) -> None:
    # 创建四个按钮
    keyboard = [
        [
            KeyboardButton("Open Mini App", web_app=WebAppInfo(url="https://your-mini-app-url")),
            KeyboardButton("Join Group", url="https://t.me/your_group")
        ],
        [
            KeyboardButton("Join Channel", url="https://t.me/your_channel"),
            KeyboardButton("Contact Support", url="https://t.me/your_contact")
        ]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, persistent=True)
    await update.message.reply_text('Please choose an option:', reply_markup=reply_markup)

def main() -> None:
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.run_polling()

if __name__ == "__main__":
    main()
