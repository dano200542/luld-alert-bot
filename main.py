import os
import time
import csv
import requests
import json
from io import StringIO
from threading import Thread
from flask import Flask

# -----------------------------
# Discord webhook (FROM RENDER ENV)
# -----------------------------
WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK")

URL = "https://www.nyse.com/api/trade-halts/current/download"
SEEN_FILE = "seen.json"

app = Flask(__name__)


# -----------------------------
# Health check route (REQUIRED FOR RENDER)
# -----------------------------
@app.route("/")
def home():
    return "LULD bot running"


# -----------------------------
# Load / Save seen alerts
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
    except Exception as e:
        print("Save error:", e)


seen = load_seen()


# -----------------------------
# Discord sender
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
# Fetch NYSE data
# -----------------------------
def fetch_data():
    r = requests.get(URL, timeout=10)
    r.raise_for_status()
    return r.text


# -----------------------------
# Process data
# -----------------------------
def process(csv_text):
    global seen

    reader = csv.DictReader(StringIO(csv_text))

    for row in reader:
        symbol = row.get("Symbol") or row.get("symbol")
        reason = (row.get("Reason") or row.get("reason") or "").upper()

        if not symbol:
            continue

        if "LULD" not in reason:
            continue

        key = f"{symbol}-{reason
