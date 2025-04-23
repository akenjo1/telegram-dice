from aiogram import Bot, Dispatcher, executor, types
from config import USER_BOT_TOKEN
from db import get_users
from utils import format_number
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

bot = Bot(token=USER_BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start(msg: types.Message):
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton("Xem Profile", callback_data="profile"),
        InlineKeyboardButton("Top Tuần", callback_data="top_week"),
        InlineKeyboardButton("Nạp Tiền", url="https://t.me/admin_bot")
    )
    kb.add(InlineKeyboardButton("Hướng Dẫn", callback_data="help"))
    kb.add(InlineKeyboardButton("Vào Bot Chơi", url="https://t.me/your_main_bot"))

    await msg.answer("Chào bạn! Chọn một trong các mục sau:", reply_markup=kb)

@dp.callback_query_handler(lambda c: True)
async def callback_handler(query: types.CallbackQuery):
    uid = str(query.from_user.id)
    users = get_users()

    if query.data == "profile":
        if uid in users:
            u = users[uid]
            msg = (
                f"**Thông tin cá nhân**\n"
                f"Số dư: {format_number(u['balance'])} xu\n"
                f"Thắng liên tiếp: {u['win_streak']}\n"
                f"Số lần cược: {u['bet_count']}"
            )
            await query.message.edit_text(msg, parse_mode="Markdown")
        else:
            await query.message.edit_text("Bạn chưa từng chơi.")
    
    elif query.data == "top_week":
        # Cần thêm hàm lấy top tuần
        await query.message.edit_text("Tính năng đang cập nhật...")

    elif query.data == "help":
        msg = (
            "Hướng dẫn đặt cược:\n"
            "`T 1000` = Tài 1000 xu\n"
            "`X 2000` = Xỉu 2000 xu\n"
            "`C 1000` = Chẵn\n"
            "`L 1000` = Lẻ\n"
            "`4 1000` = Tổng 4\n"
            "`333 1000` = Bộ ba 3\n"
        )
        await query.message.edit_text(msg, parse_mode="Markdown")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)