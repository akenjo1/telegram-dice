from aiogram import Bot, Dispatcher, executor, types
from config import BOT_TOKEN
from handlers import place_bet
import asyncio
from scheduler import round_loop
from utils import parse_command_args

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start(msg: types.Message):
    await msg.reply("Chào mừng đến với bot Tài Xỉu!")

@dp.message_handler()
async def handle_bet(msg: types.Message):
    bet_type, amount = parse_command_args(msg.text)
    if not bet_type or not amount:
        await msg.reply("Sai cú pháp! Ví dụ: T 1000 hoặc X 2000 hoặc L 1000")
        return
    result = place_bet(msg.from_user.id, bet_type, amount)
    await msg.reply(result)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(round_loop(bot))
    executor.start_polling(dp, skip_updates=True)