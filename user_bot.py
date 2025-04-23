# user_bot_termux.py

import telebot
from config import BOT_TOKEN_USER
from utils import get_users, format_number

bot = telebot.TeleBot(BOT_TOKEN_USER)

@bot.message_handler(commands=["start", "profile"])
def profile(msg):
    users = get_users()
    uid = str(msg.from_user.id)
    if uid not in users:
        return bot.reply_to(msg, "Bạn chưa từng chơi.")
    
    balance = format_number(users[uid]["balance"])
    text = f"👤 ID: {uid}\n💰 Xu: {balance}"
    bot.reply_to(msg, text)

bot.polling()
