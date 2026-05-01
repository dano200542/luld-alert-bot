import os
import time
import csv
import requests
from io import StringIO
from threading import Thread
from flask import Flask

app = Flask(__name__)

WEBHOOK_URL = os.environ.get("https://discord.com/api/webhooks/1463521320582250498/Oi0KYpKQzUVYLnRIKGSToqnrkfEd1A-BIPnDz5bmW7gsi5T46CrTzO7u2Eu1AuK1IoL")
URL = "https://www.nyse.com/api/trade-halts/current/download"

seen = set()

def send_discord(msg):
    if not WEBHOOK_URL:
        print("Missing DISCORD_WEBHOOK")
        return

    try:
        requests.post(WEBHOOK_URL, json={"content": msg}, timeout=10)
    except Exception as e:
        print("Discord error:", e)

def fetch_data():
    r = requests.get(URL, timeout=5)
    r.raise_for_status()
    return r.text

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

        send_discord(
            f"🚨 NYSE LULD HALT\nSymbol: {symbol}\nReason: {reason}"
        )

def worker():
    print("LULD bot running...")
    while True:
        try:
            csv_text = fetch_data()
            process(csv_text)
        except Exception as e:
            print("Error:", e)
        time.sleep(30)

@app.route("/")
def home():
    return "Bot is running"

if __name__ == "__main__":
    Thread(target=worker).start()
    app.run(host="0.0.0.0", port=10000)
