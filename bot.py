from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, CallbackContext

TOKEN = "YOUR_BOT_TOKEN"  # 建议用 Railway 环境变量代替

async def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [
            KeyboardButton("Open Mini App", web_app=WebAppInfo(url="https://your-mini-app-url")),
            KeyboardButton("Join Group", url="https://t.me/your_group"),
        ],
        [
            KeyboardButton("Join Channel", url="https://t.me/your_channel"),
            KeyboardButton("Contact Support", url="https://t.me/your_contact"),
        ],
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, persistent=True)
    await update.message.reply_text("Choose an option:", reply_markup=reply_markup)

def main() -> None:
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()

if __name__ == "__main__":
    main()
