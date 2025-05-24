import logging
import schedule
import time
import threading
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Replace this with your actual bot token
BOT_TOKEN = 'YOUR_BOT_TOKEN'

# Replace this with your Telegram user ID (you can use @userinfobot to get it)
OWNER_ID = 123456789

# Dummy prediction logic (replace with your actual F&G algorithm)
def predict_fear_greed():
    # Placeholder prediction logic
    return "Predicted Fear & Greed Index for today is: 70"

# Triggered by scheduler
def scheduled_prediction(context: ContextTypes.DEFAULT_TYPE):
    context.bot.send_message(chat_id=OWNER_ID, text=predict_fear_greed())

# /predict command handler
async def predict(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = predict_fear_greed()
    await update.message.reply_text(result)

# /settime command handler
async def settime(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        hour, minute = map(int, context.args)
        schedule.clear()
        schedule.every().day.at(f"{hour:02d}:{minute:02d}").do(lambda: scheduled_prediction(context))
        await update.message.reply_text(f"Scheduled prediction set for {hour:02d}:{minute:02d} UTC.")
    except:
        await update.message.reply_text("Usage: /settime HH MM")

# Scheduler thread
def run_schedule(app):
    while True:
        schedule.run_pending()
        time.sleep(1)

# Start bot
def main():
    logging.basicConfig(level=logging.INFO)
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("predict", predict))
    app.add_handler(CommandHandler("settime", settime))

    threading.Thread(target=run_schedule, args=(app,), daemon=True).start()
    app.run_polling()

if __name__ == "__main__":
    main()
