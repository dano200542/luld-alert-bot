import os
import time
import requests
from flask import Flask
from threading import Thread

app = Flask(__name__)

WEBHOOK_URL = "https://discord.com/api/webhooks/1463521320582250498/Oi0KYpKQzUVYLnRIKGSToqnrkfEd1A-BIPnDz5bmW7gsi5T46CrTzO7u2Eu1AuK1IoLA"

@app.route("/")
def home():
    return "OK - LIVE"

def fire_alert():
    time.sleep(3)

    print("TRYING DISCORD")

    try:
        r = requests.post(
            WEBHOOK_URL,
            json={"content": "🚨 BOT IS LIVE - TEST MESSAGE"},
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
