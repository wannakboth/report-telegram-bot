from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

from calc import calculate_daily_totals

GROUP_ID = -1002830689602

# Track which users are collecting messages
user_active = {}

# Store collected messages per user
user_messages = {}

# /start command
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_active[user_id] = True
    user_messages[user_id] = []
    await update.message.reply_text("Started collecting messages!")

# /stop command
async def stop_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    collected = user_messages.get(user_id, [])
    user_active[user_id] = False

    if collected:
        text = "\n".join(collected)
        responseText = ""
        daily_totals = calculate_daily_totals(text)
        for date, totals in daily_totals.items():
            responseText = responseText + f"Date: {date} → ៛{totals['riel']:,} | ${totals['usd']:.2f}"
            # print(responseText)
        
        await update.message.reply_text(f"{responseText}")
        
    else:
        await update.message.reply_text("No messages collected.")

# Catch group messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if message.chat.id != GROUP_ID:
        return  # only collect from this group

    user_id = message.from_user.id
    if user_active.get(user_id):
        msg_text = f"{message.from_user.first_name}: {message.text}"
        user_messages[user_id].append(msg_text)

if __name__ == '__main__':
    app = ApplicationBuilder().token('7930828014:AAFy5Carxx20ul3387UB3IoUeoO-pBtU5lg').build()

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    app.add_handler(CommandHandler("daily", start_command))
    app.add_handler(CommandHandler("stop", stop_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Bot is listening for group messages...")
    app.run_polling()
