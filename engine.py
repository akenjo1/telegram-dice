import random

def roll_dice():
    return [random.randint(1, 6) for _ in range(3)]

def check_result(dice):
    total = sum(dice)
    tai_xiu = "T" if total >= 11 else "X"
    chan_le = "C" if total in [4, 6, 8] else "L" if total in [3, 5, 7] else""
    triple = f"{dice[0]}{dice[1]}{dice[2]}" if dice[0] == dice[1] == dice[2] else None
    return {
        "total": total,
        "tai_xiu": tai_xiu,
        "chan_le": chan_le,
        "triple": triple,
        "dice": dice
    }