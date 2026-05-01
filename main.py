import os
import time
import requests
from flask import Flask
from threading import Thread

app = Flask(__name__)

WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK")

@app.route("/")
def home():
    return "alive"

def send_discord(msg):
    print("SEND ATTEMPT")
    print("WEBHOOK:", WEBHOOK_URL)

    if not WEBHOOK_URL:
        print("NO WEBHOOK FOUND")
        return

    r = requests.post(WEBHOOK_URL, json={"content": msg})
    print("STATUS:", r.status_code)
    print("RESPONSE:", r.text)

def bot_loop():
    print("LOOP STARTED")

    time.sleep(5)

    send_discord("🧪 FINAL TEST: bot is running")

    while True:
        print("TICK")
        time.sleep(30)

if __name__ == "__main__":
    Thread(target=bot_loop, daemon=True).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
