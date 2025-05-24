from telegram.ext import Application, CommandHandler

async def start(update, context):
    await update.message.reply_text("Hello, I’m your Fear & Greed bot!")

app = Application.builder().token("YOUR_TELEGRAM_BOT_TOKEN").build()
app.add_handler(CommandHandler("start", start))

app.run_polling()
