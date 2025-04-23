# utils.py

import json
import os

DATA_FILE = "users.json"

def get_users():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump({}, f)
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def update_users(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def format_number(n):
    return "{:,}".format(n).replace(",", ".")
