import logging
import os
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Telegram bot token
TOKEN = "7628995512:AAHOoEEbPSfW-wEosiEY8iT8BGr7Jk7yKHs"

# Cashfree credentials
CLIENT_ID = "1036175253b19b5aa60f9e0fd725716301"
SECRET_KEY = "cfsk_ma_prod_b4a79cff91b12dd41c80032fac4d9144_20a9a054"

# Your group ID
GROUP_ID = -1002774845217

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("₹99 for 30 Days", callback_data="plan_99")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Welcome! Choose a plan to continue:", reply_markup=reply_markup)

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "plan_99":
        user_id = query.from_user.id
        user_name = query.from_user.first_name

        response = requests.post(
            "https://api.cashfree.com/pg/links",
            headers={
                "x-api-version": "2022-09-01",
                "x-client-id": CLIENT_ID,
                "x-client-secret": SECRET_KEY,
                "Content-Type": "application/json"
            },
            json={
                "customer_details": {
                    "customer_id": str(user_id),
                    "customer_name": user_name,
                    "customer_email": f"{user_id}@bot.com"
                },
                "order_id": f"order_{user_id}",
                "order_amount": 99,
                "order_currency": "INR",
                "order_note": "Premium Telegram Access",
                "link_notify": {"send_sms": False, "send_email": False},
                "link_expiry_time": 3600
            }
        )
        link = response.json().get("payment_link")
        if link:
            await query.message.reply_text(f"Pay here: {link}")
        else:
            await query.message.reply_text("Something went wrong, try again later.")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_callback))
    print("Bot started...")
    app.run_polling()
