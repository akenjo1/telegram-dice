from aiogram import Bot, Dispatcher, executor, types
from config import ADMIN_BOT_TOKEN, ADMIN_IDS
from db import get_users, update_users
from utils import format_number

bot = Bot(token=ADMIN_BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start(msg: types.Message):
    if msg.from_user.id not in ADMIN_IDS:
        return await msg.reply("Bạn không có quyền.")
    await msg.reply("Chào admin! Dùng lệnh: /cong, /tru, /reset, /xoa, /code")

@dp.message_handler(commands=["cong"])
async def cong(msg: types.Message):
    if msg.from_user.id not in ADMIN_IDS: return
    try:
        _, username, amount = msg.text.split()
        amount = int(amount)
        users = get_users()
        for uid, u in users.items():
            if u.get("username") == username or uid == username:
                u["balance"] += amount
                update_users(users)
                return await msg.reply(f"✅ Đã cộng {format_number(amount)} xu cho {username}")
        await msg.reply("Không tìm thấy user.")
    except:
        await msg.reply("Cú pháp: /cong @user 10000")

@dp.message_handler(commands=["reset"])
async def reset(msg: types.Message):
    if msg.from_user.id not in ADMIN_IDS: return
    try:
        _, uid = msg.text.split()
        users = get_users()
        if uid in users:
            users[uid]["balance"] = 10000
            update_users(users)
            await msg.reply("Đã reset tài khoản.")
        else:
            await msg.reply("Không tìm thấy user.")
    except:
        await msg.reply("Cú pháp: /reset user_id")

@dp.message_handler(commands=["xoa"])
async def xoa(msg: types.Message):
    if msg.from_user.id not in ADMIN_IDS: return
    try:
        _, uid = msg.text.split()
        users = get_users()
        if uid in users:
            del users[uid]
            update_users(users)
            await msg.reply("Đã xoá tài khoản.")
        else:
            await msg.reply("Không tìm thấy user.")
    except:
        await msg.reply("Cú pháp: /xoa user_id")