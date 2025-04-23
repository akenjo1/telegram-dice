import asyncio
from shared import *
from engine import roll_dice, sum_dice, is_tai, is_xiu, is_chan, is_le, is_jackpot, get_jackpot_type
from db import get_users, update_users, get_jackpot, save_jackpot
from utils import format_number

async def round_loop(bot):
    global lock_bet, current_bets, round_id, jackpot_amount
    
    while True:
        round_id += 1
        lock_bet = False
        current_bets.clear()

        await bot.send_message(chat_id="@your_channel_or_group", text=f"Ván #{round_id} bắt đầu! Đặt cược ngay!")
        await asyncio.sleep(20)

        lock_bet = True
        dice = roll_dice()
        total = sum_dice(dice)

        result_text = f"Kết quả: {'-'.join(map(str, dice))} = {total}"
        outcome = []
        if is_tai(total): outcome.append("TÀI")
        if is_xiu(total): outcome.append("XỈU")
        if is_chan(total): outcome.append("CHẴN")
        if is_le(total): outcome.append("LẺ")

        users = get_users()
        jackpot = get_jackpot()

        winners = []
        total_pot = 0
        for bet in current_bets:
            uid = str(bet["user_id"])
            btype = bet["type"]
            amt = bet["amount"]
            total_pot += amt
            if btype in outcome:
                win_amt = amt * 2
                users[uid]["balance"] += win_amt
                winners.append((uid, win_amt))
                users[uid]["win_streak"] += 1
            else:
                users[uid]["win_streak"] = 0

        # Check Jackpot
        if is_jackpot(dice):
            jackpot_type = get_jackpot_type(dice)
            reward_text = f"HŨ NỔ {jackpot_type}!"
            await bot.send_message(chat_id="@your_channel_or_group", text=reward_text)
            if jackpot["amount"] > 0:
                for uid, win_amt in winners:
                    ratio = win_amt / sum(w for _, w in winners)
                    reward = int(jackpot["amount"] * ratio)
                    users[uid]["balance"] += reward
                jackpot["amount"] = 0
        else:
            # Add excess to jackpot
            side_counts = {"TÀI": 0, "XỈU": 0}
            for b in current_bets:
                if b["type"] in side_counts:
                    side_counts[b["type"]] += b["amount"]
            if abs(side_counts["TÀI"] - side_counts["XỈU"]) > 0:
                jackpot["amount"] += abs(side_counts["TÀI"] - side_counts["XỈU"])

        update_users(users)
        save_jackpot(jackpot)

        await bot.send_message(chat_id="@your_channel_or_group", text=f"{result_text} => {'/'.join(outcome)}\nJackpot: {format_number(jackpot['amount'])}")
        await asyncio.sleep(2)