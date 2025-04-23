import telebot
import random
import time
from config import BOT_TOKEN_MAIN
from utils import format_number, get_users, update_users

bot = telebot.TeleBot(BOT_TOKEN_MAIN)
users = get_users()
bets = {}
lock = False

@bot.message_handler(commands=['start'])
def start(msg):
    bot.reply_to(msg, "Gửi tin nhắn dạng: T 1000 hoặc X 5000 để cược!")

@bot.message_handler(func=lambda m: True)
def handle_bet(msg):
    global lock
    uid = str(msg.from_user.id)
    try:
        if lock:
            return bot.reply_to(msg, "Đã khóa cược, chờ ván tiếp theo!")

        cmd, amt = msg.text.upper().split()
        amt = int(amt)
        if cmd not in ["T", "X", "C", "L"]:
            return bot.reply_to(msg, "Sai cú pháp! Dùng T/X/C/L + số xu")

        if uid not in users:
            users[uid] = {"balance": 10000}

        if users[uid]["balance"] < amt:
            return bot.reply_to(msg, "Bạn không đủ xu!")

        users[uid]["balance"] -= amt
        bets.setdefault(cmd, []).append((uid, amt))
        update_users(users)
        bot.reply_to(msg, f"✅ Đã cược {cmd} {format_number(amt)} xu")
    except:
        bot.reply_to(msg, "Sai cú pháp. Dùng: T 1000 hoặc X 2000")

def play_round():
    global lock, bets
    while True:
        print("⏳ Đang mở cược...")
        lock = False
        bets = {}
        time.sleep(20)

        lock = True
        dice = [random.randint(1, 6) for _ in range(3)]
        total = sum(dice)
        result = []
        if total <= 10: result.append("X")
        if total >= 11: result.append("T")
        if total in [4, 6, 8]: result.append("C")
        if total in [3, 5, 7]: result.append("L")

        win_msg = f"🎲 Kết quả: {dice[0]}-{dice[1]}-{dice[2]} = {total}\n"

        for k, lst in bets.items():
            for uid, amt in lst:
                if k in result:
                    users[uid]["balance"] += amt * 2
                    win_msg += f"💰 {uid} thắng {format_number(amt)} xu\n"

        update_users(users)
        bot.send_message(msg.chat.id, win_msg)
        time.sleep(5)

import threading
threading.Thread(target=play_round, daemon=True).start()

bot.polling()
