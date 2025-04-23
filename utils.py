def format_number(n):
    return "{:,}".format(n).replace(",", ".")

def calculate_winnings(bet_type, amount):
    """Trả về số tiền thắng dựa trên loại cược"""
    if bet_type in ["T", "X", "C", "L"]:
        return amount * 2
    elif bet_type in [str(x) for x in range(4, 18)]:
        return amount * 8
    elif len(bet_type) == 3 and bet_type[0] == bet_type[1] == bet_type[2]:
        return amount * 24
    return 0