import os
import time
import requests
from flask import Flask
from threading import Thread

# -----------------------------
# DISCORD WEBHOOK
# -----------------------------
WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK")

app = Flask(__name__)

# -----------------------------
# HEALTH CHECK (RENDER)
# -----------------------------
@app.route("/")
def home():
    return "Bot is alive"

# -----------------------------
# DISCORD MESSAGE
# -----------------------------
def send_discord(msg):
    if not WEBHOOK_URL:
        print("❌ DISCORD_WEBHOOK missing in environment")
        return

    try:
        requests.post(WEBHOOK_URL, json={"content": msg}, timeout=10)
        print("✅ Sent to Discord")
    except Exception as e:
        print("❌ Discord error:", e)

# -----------------------------
# TEST LOOP (NO DATA, JUST PROOF)
# -----------------------------
def bot_loop():
    time.sleep(5)

    send_discord("🧪 BOT IS ONLINE - Render deployment successful")

    while True:
        print("🟢 Bot still running...")
        time.sleep(60)

# -----------------------------
# START APP
# -----------------------------
if __name__ == "__main__":
    Thread(target=bot_loop, daemon=True).start()

    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
