import os
import requests
from flask import Flask
from threading import Thread
import time

app = Flask(__name__)

WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK")

@app.route("/")
def home():
    return "OK"

def fire_alert():
    time.sleep(3)  # small delay so logs show up
    print("FIRING DISCORD ALERT")

    if not WEBHOOK_URL:
        print("NO WEBHOOK IN ENV")
        return

    try:
        r = requests.post(
            WEBHOOK_URL,
            json={"content": "🚨 RENDER BOT IS RUNNING (TEST ALERT)"},
            timeout=10
        )
        print("STATUS:", r.status_code)
        print("RESPONSE:", r.text)
    except Exception as e:
        print("ERROR:", e)

if __name__ == "__main__":
    Thread(target=fire_alert, daemon=True).start()

    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
