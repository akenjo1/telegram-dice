from config import ADMIN_IDS
from utils import format_number
from db import get_users, update_users
from shared import *

def ensure_user(user_id):
    users = get_users()
    if str(user_id) not in users:
        users[str(user_id)] = {
            "balance": 10000,
            "history": [],
            "win_streak": 0,
            "bet_count": 0,
        }
        update_users(users)

def place_bet(user_id, bet_type, amount):
    ensure_user(user_id)
    if lock_bet:
        return "Cược đã bị khóa!"
    
    users = get_users()
    user = users[str(user_id)]
    
    if user["balance"] < amount:
        return "Bạn không đủ xu để đặt cược!"
    
    user["balance"] -= amount
    update_users(users)
    
    current_bets.append({
        "user_id": user_id,
        "type": bet_type.upper(),
        "amount": amount
    })
    return f"✅ Bạn đã cược {format_number(amount)} vào {bet_type.upper()}"