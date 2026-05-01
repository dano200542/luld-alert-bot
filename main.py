import os
import time
import csv
import requests
import json
from io import StringIO
from threading import Thread
from flask import Flask

# -----------------------------
# ENV VAR (SET IN RENDER)
# -----------------------------
WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK")

URL = "https://www.nyse.com/api/trade-halts/current/download"
SEEN_FILE = "seen.json"

app = Flask(__name__)

# -----------------------------
# HEALTH CHECK (REQUIRED FOR RENDER)
# -----------------------------
@app.route("/")
def home():
    return "LULD bot running"

# -----------------------------
# LOAD / SAVE SEEN ALERTS
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
        symbol = row.get("Symbol") or row.get("symbol")
        reason = (row.get("Reason") or row.get("reason") or "").upper()

        if not symbol:
            continue

        if "LULD" not in reason:
            continue

        key = f"{symbol}-{reason}"

        if key in seen:
            continue

        seen.add(key)
        save_seen(seen)

        send_discord(
            "🚨 NYSE LULD HALT\n"
            f"Symbol: {symbol}\n"
            f"Reason: {reason}"
        )

# -----------------------------
# BOT LOOP
# -----------------------------
def bot_loop():
    print("LULD bot running...")
    time.sleep(3)

    while True:
        try:
            csv_text = fetch_data()
            process(csv_text)
        except Exception as e:
            print("Error:", e)

        time.sleep(10)

# -----------------------------
# START EVERYTHING (RENDER SAFE)
# -----------------------------
if __name__ == "__main__":
    Thread(target=bot_loop, daemon=True).start()

    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
