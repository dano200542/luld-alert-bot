import os
import time
import csv
import requests
import json
from io import StringIO
from threading import Thread
from flask import Flask

# -----------------------------
# ENV VAR (DO NOT HARD CODE WEBHOOK)
# -----------------------------
WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK")

URL = "https://www.nyse.com/api/trade-halts/current/download"
SEEN_FILE = "seen.json"

app = Flask(__name__)


# -----------------------------
# REQUIRED HEALTH CHECK ROUTE
# -----------------------------
@app.route("/")
def home():
    return "LULD bot running"


# -----------------------------
# SAFE FILE STORAGE
# -----------------------------
def load_seen():
    try:
        with open(SEEN_FILE, "r") as f:
            return set(json.load(f))
    except:
        return set()


def save_seen(seen):
    try:
        with open(SEEN_FILE, "w") as f:
            json.dump(list(seen), f)
    except:
        pass


seen = load_seen()


# -----------------------------
# DISCORD SENDER
# -----------------------------
def send_discord(msg):
    if not WEBHOOK_URL:
        print("Missing DISCORD_WEBHOOK")
        return

    try:
        requests.post(WEBHOOK_URL, json={"content": msg}, timeout=10)
    except Exception as e:
        print("Discord error:", e)


# -----------------------------
# FETCH DATA
# -----------------------------
def fetch_data():
    r = requests.get(URL, timeout=10)
    r.raise_for_status()
    return r.text


# -----------------------------
# PROCESS DATA
# -----------------------------
def process(csv_text):
    global seen

    reader = csv.DictReader(StringIO(csv_text))

    for row in reader:
        symbol = row.get("Symbol") or
