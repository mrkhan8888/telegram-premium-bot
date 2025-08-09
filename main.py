from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext
import os

# ====== CONFIG ======
BOT_TOKEN = os.getenv("BOT_TOKEN")  # Render में Environment Variable में डालना
ADMIN_ID = 5073222820  # सिर्फ तेरा Telegram ID
# ====================

# डिफॉल्ट मैसेज और बटन
current_message = "Default message from bot"
current_button_text = "Click Me"
current_button_url = "https://example.com"


# चेक करे कि यूजर एडमिन है या नहीं
def is_admin(update: Update):
    return update.effective_user.id == ADMIN_ID


# मैसेज बदलने का कमांड
def set_message(update: Update, context: CallbackContext):
    if not is_admin(update):
        update.message.reply_text("⛔ आपके पास अनुमति नहीं है!")
        return
    global current_message
    if context.args:
        current_message = " ".join(context.args)
        update.message.reply_text(f"✅ नया मैसेज सेट हुआ:\n{current_message}")
    else:
        update.message.reply_text("❗ नया मैसेज लिखें, जैसे:\n`/setmsg Hello World`", parse_mode="Markdown")


# मैसेज देखने का कमांड
def get_message(update: Update, context: CallbackContext):
    update.message.reply_text(f"📢 Current message:\n{current_message}")


# बटन बदलने का कमांड
def set_button(update: Update, context: CallbackContext):
    if not is_admin(update):
        update.message.reply_text("⛔ आपके पास अनुमति नहीं है!")
        return
    global current_button_text, current_button_url
    if len(context.args) >= 2:
        current_button_text = context.args[0]
        current_button_url = context.args[1]
        update.message.reply_text(f"✅ बटन अपडेट हुआ:\nText: {current_button_text}\nURL: {current_button_url}")
    else:
        update.message.reply_text("❗ सही फॉर्मेट:\n`/setbtn Text URL`", parse_mode="Markdown")


# पोस्ट भेजने का कमांड
def send_post(update: Update, context: CallbackContext):
    keyboard = [[InlineKeyboardButton(current_button_text, url=current_button_url)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(current_message, reply_markup=reply_markup)


# बॉट स्टार्ट
def start(update: Update, context: CallbackContext):
    update.message.reply_text("🤖 Bot is running...")


if __name__ == "__main__":
    updater = Updater(BOT_TOKEN)
    dp = updater.dispatcher

    # कमांड हैंडलर
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("setmsg", set_message))
    dp.add_handler(CommandHandler("getmsg", get_message))
    dp.add_handler(CommandHandler("setbtn", set_button))
    dp.add_handler(CommandHandler("sendpost", send_post))

    updater.start_polling()
    updater.idle()
