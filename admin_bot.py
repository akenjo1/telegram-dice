# admin_bot_termux.py

import telebot
from config import BOT_TOKEN_ADMIN, ADMIN_ID
from utils import get_users, update_users, format_number

bot = telebot.TeleBot(BOT_TOKEN_ADMIN)
users = get_users()

@bot.message_handler(commands=["start"])
def start(msg):
    if msg.from_user.id != ADMIN_ID:
        return
    bot.send_message(msg.chat.id, "Bot Admin sẵn sàng. Lệnh: /add, /sub, /reset")

@bot.message_handler(commands=["add"])
def add(msg):
    if msg.from_user.id != ADMIN_ID: return
    try:
        _, uid, amt = msg.text.split()
        amt = int(amt)
        users[uid] = users.get(uid, {"balance": 10000})
        users[uid]["balance"] += amt
        update_users(users)
        bot.reply_to(msg, f"✅ Đã cộng {format_number(amt)} xu cho {uid}")
    except:
        bot.reply_to(msg, "Sai cú pháp. Dùng: /add 123456789 10000")

@bot.message_handler(commands=["sub"])
def sub(msg):
    if msg.from_user.id != ADMIN_ID: return
    try:
        _, uid, amt = msg.text.split()
        amt = int(amt)
        users[uid]["balance"] = max(users[uid]["balance"] - amt, 0)
        update_users(users)
        bot.reply_to(msg, f"❌ Đã trừ {format_number(amt)} xu của {uid}")
    except:
        bot.reply_to(msg, "Sai cú pháp. Dùng: /sub 123456789 5000")

bot.polling()
